from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from uuid import UUID
from models import *
from sqlalchemy import create_engine, text, Column, ForeignKey, String
from sqlalchemy.orm import declarative_base
from datetime import datetime, time, date
import uvicorn
import pymysql
import threading
from chatbot import *
from servermodel import *
import json, base64
from dictionary import *
from t2s import *
import random

app = FastAPI()
conn = pymysql.connect(host='jaminidb2.mysql.database.azure.com', user='sktflyaiambition4', password='rmaWhrdl8!', db='jamini', charset='utf8', ssl={"fake_flag_to_enable_tls":True})

db = conn.cursor()
                                                                                                                                                                                                                            

model = KoGPT2Chat.load_from_checkpoint("model_chp/model_-0228.ckpt")
load_model_lock = threading.Lock()

class ModelLoaderThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global model
        with load_model_lock:
            model = KoGPT2Chat.load_from_checkpoint("model_chp/model_-0228.ckpt")

model_loader_thread = ModelLoaderThread()
model_loader_thread.start()

@app.get("/")
async def root():
    sql = f'SELECT * FROM USER;'
    db.execute(sql)

    result = db.fetchall()
    return {"msg": "main",
            "sql": result}


################################# 일반 질문 (찐_완성!) ##########################################
## 일반 질문 type(normal1 인지 nomarl2 인지) 으로 입력받아서 return
## + 질문한 내용 chatting 테이블에 저장함
@app.get("/question/{type}")
async def fetch_normalQ(type:str):
    if type=='hello':
        sql0 = f"DELETE FROM CHATTING WHERE day = curdate();"
        db.execute(sql0)
        conn.commit()
    elif type=='goodbye':
        sqlgoodbye = f"SELECT sentence from QUESTION WHERE type = '{type}' LIMIT 1;"
        db.execute(sqlgoodbye)
        temp = db.fetchone()
        goodbye = str(temp)
        send_goodbye = base64.b64encode(texttospeech(goodbye[2:-3])).decode('utf-8')

    sql1  = f"select sentence from QUESTION WHERE type = '{type}' order by rand() LIMIT 1;"
    #result = db.execute(sql1).fetchone()
    db.execute(sql1)
    result = db.fetchone()
    result2 = str(result)
    sql2 = f'INSERT INTO CHATTING VALUES(1,curdate(),curtime(),"bot","{result2[2:-3]}");'
    db.execute(sql2)
    # return result
    # return {"sentence":str(result)}
    conn.commit()
    send_tts = base64.b64encode(texttospeech(result2[2:-3])).decode('utf-8')
    sendtts = send_goodbye if type=='goodbye' else send_tts
    return {"sentence": result2[2:-3],
            "send_tts": sendtts}
#############################################################################################


####################### 키워드 번호로 해당 키워드 질문 받아오기 (찐_완성!) ############################
@app.get("/question2/keyword")
async def fetch_keywordQ():
    # sql = f"select * from QUESTION where keyword ='keyword';"
    # sql1 = f"select sentence from QUESTION WHERE type = '{type}' order by rand()  LIMIT 1;"
    sql0 = f"SELECT keyword_index FROM KEYWORD WHERE day = curdate() ORDER BY rand() LIMIT 1;"
    db.execute(sql0)
    tmp = db.fetchone()
    tmp = tmp[0]
    print(tmp)
    print(type(tmp))
    tmp = tmp.strip("][").split(",")
    templist = []
    randomlist = []
    for x in tmp:
        templist.append(int(x))
    randomlist = random.sample(templist,2)
    sql1 = f"SELECT sentence FROM QUESTION WHERE keyword = {randomlist[0]} ORDER BY RAND() LIMIT 1;"
    db.execute(sql1)
    result1 = db.fetchone()
    result1 = str(result1)
    sql2 = f"SELECT sentence FROM QUESTION WHERE keyword = {randomlist[1]} ORDER BY RAND() LIMIT 1;"
    db.execute(sql2)
    result2 = db.fetchone()
    result2 = str(result2)
    sql3 = f'INSERT INTO CHATTING VALUES(1,curdate(),curtime(),"bot","{result1[2:-3]}");'
    sql4 = f'INSERT INTO CHATTING VALUES(1, curdate(), curtime() + INTERVAL 1 SECOND, "bot","{result2[2:-3]}");'
    db.execute(sql3)
    db.execute(sql4)
    conn.commit()
    # return result
    send_tts1 = base64.b64encode(texttospeech(result1[2:-3])).decode('utf-8')
    send_tts2=base64.b64encode(texttospeech(result2[2:-3])).decode('utf-8')
    return {"sentence1":result1[2:-3],
            "sentence2":result2[2:-3],
            "send_tts1":send_tts1,
            "send_tts2":send_tts2}

#################################################################################################### 

#################################################################################################### 
@app.post("/tts")
async def changetts(tts: str):
    temp = tts
    sendjava = base64.b64encode(texttospeech(temp)).decode('utf-8')
    return {"sentence": sendjava}

@app.get("/htp/{type}")
async def hello_tts(type: str):
    if type=='hello':
        sentence = "안녕, 나랑 그림 그려볼래? 재미있을 거야!"
    elif type=='ready':
        sentence = "먼저, 종이 세 장이랑 연필, 지우개를 준비해줘!"
    elif type=='house':
        sentence = "종이를 가로로 놓고 집을 그려보자!  다 그리면 카메라 버튼을 눌러줘!"
    elif type=='tree':
        sentence = "새로운 종이를 세로로 놓고 나무를 그려보자!  다 그리면 그림을 찍어줘!"
    elif type=='person':
        sentence = "새로운 종이를 세로로 놓고 사람을 그려보자!  다 그리면 그림을 찍어줘!"

    sendjava = base64.b64encode(texttospeech(sentence)).decode('utf-8')
    return {"sentence": sendjava}


############################# 날짜별로 가져오기 성공! (찐_완성!) #####################
@app.get("/report/chat/{day}") 
async def fetch_report(day:str):
    #################
    db=conn.cursor()
    ######################
    sql1 = f"SELECT * FROM TALK_REPORT WHERE day= '{day}';"
    db.execute(sql1)
    ###
    result1= db.fetchone()
    ### 
    print(result1[2])
    print(type(result1[2]))
    # list(map(result1[2].split(",")))
    keywords_list_str = result1[2].split(",")

    return {
            "userid":result1[0],
            "day":result1[1],
            "keyword":keywords_list_str,
            "emotion":result1[3],
            "text":result1[4]
            }

@app.get("/report/draw/{day}")
async def fetch_report(day:str):
    #####################
    db=conn.cursor()
    ##########################3
    sql = f"SELECT * FROM DRAW_REPORT WHERE day = '{day}';"
    db.execute(sql)
    result = db.fetchone()
    print(type(result))
    print(result[0])
    return {
            "userid":result[0],
            "day":result[1],
            "house_img":result[2],
            "tree_img":result[3],
            "person_img":result[4],
            "result":result[5],
            "house_text":result[6],
            "tree_text":result[7],
            "person_text":result[8],
            "f_type1":result[9],
            "f_type2":result[10],
            "f_type3":result[11]
            }

#########################################################################################

########################## USER_TESTDAY에 테스트한 날짜 저장 & CHATTING TABLE에 채팅 내용 저장 #####################
@app.post("/report/chat")
async def register_chat(tmp:Sendtext):
    #채팅 내용을 db에 저장
    try:
        #sql = f"INSERT INTO USER_TESTDAY (userid,day) VALUES ({tmp.userid},curdate());"
        #db.excute(sql)
        #conn.commit()
        print("???????????????????????")
    except:
        print("?!")
    sql = f"INSERT INTO CHATTING (userid , day , time , type , chat) VALUES ({tmp.userid},curdate(),curtime(),'user','{tmp.text}');"
    db.execute(sql)
    conn.commit()

    return {"msg": "CHATTING table에 저장"}



########################### USER_TESTDAY에 테스트한 날짜 저장 & CHATTING TABLE에 채팅 내용 저장 & 모델에 input값으로 문장 넣음 (!!찐_완성!!) ##################################
@app.post("/report/chat/model")
async def register_report(tmp: Sendtext):
    #채팅 내용을 db에 저장  
    try:  
       ## sql = f"INSERT INTO USER_TESTDAY (userid, day) VALUES ({tmp.userid}, curdate());"
        # sql = f"INSERT INTO USER_TESTDAY (userid, day) VALUES (1, curdate());"
        ##db.execute(sql)
        ##conn.commit()
        print("!!!")
    except:
        print("??")
    sql = f"INSERT INTO CHATTING (userid, day, time, type, chat) VALUES ({tmp.userid},curdate(),curtime(), 'user','{tmp.text}');"
    db.execute(sql)
    conn.commit()
    strtmp = model.chat(text=tmp.text)
    sql = f"INSERT INTO CHATTING (userid, day, time, type, chat) VALUES ({tmp.userid},curdate(),curtime()+ INTERVAL 1 SECOND, 'bot','{strtmp}');"
    db.execute(sql)
    conn.commit()
    # conn.close()
    # db.close()
    print(str(strtmp))
    send_tts=base64.b64encode(texttospeech(strtmp)).decode('utf-8')
    return {"msg": "CHATTING table에 저장",
            "bot": strtmp,
            "send_tts":send_tts}

################################################################################################################################
###################################감정분석 모델#################################################################################
################################################################################################################################
@app.get('/analysis')
async def analysis_emotion():
    ##########################
    sql_temp="delete from talk_report where userid=1;"
    db.execute(sql_temp)
    conn.commit()
    #########################
    sql1 = f"SELECT * FROM CHATTING WHERE type='user' AND day = curdate();" 
    db.execute(sql1)
    result = db.fetchall()
    user_chat=[]
    for chat in result:
        
        user_chat.append(chat[4])
    analysis=modeling(user_chat)
    analysis2=dictionary(user_chat)
    print(analysis)
    print(analysis2)
    sql2 = f"INSERT INTO talk_report (userid, day, keyword, emotion,text) VALUES (1,curdate(),'{analysis}','{analysis2}','textText');"
    db.execute(sql2)
    conn.commit()
   # conn.close()
    return analysis

@app.get('/chat/{day}')
async def openchat(day: str):
    sqluser = f"SELECT chat FROM CHATTING WHERE type='user' AND day ='{day}' ORDER BY time;"
    db.execute(sqluser)
    userchats = db.fetchall()
    sqlbot = f"SELECT chat FROM CHATTING WHERE type='bot' AND day ='{day}' ORDER BY time;"
    db.execute(sqlbot)
    botchats = db.fetchall()
    users = [chat for chat in userchats]
    bots = [chat for chat in bots]


