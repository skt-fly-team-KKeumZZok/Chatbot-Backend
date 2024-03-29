from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from uuid import UUID
from models import *
from sqlalchemy import create_engine, text, Column, ForeignKey, String
from sqlalchemy.orm import declarative_base
from datetime import datetime, time, date
from chatbot import *
import uvicorn
import pymysql
##############################################################
#, encoding="utf-8"
app = FastAPI()
conn = pymysql.connect(host='jaminidb2.mysql.database.azure.com', user='sktflyaiambition4', password='rmaWhrdl8!', db='jamini', charset='utf8', ssl={"fake_flag_to_enable_tls":True})
db = conn.cursor()

# app.database = database
# connection = database.connect()
# db = app.database

model = KoGPT2Chat.load_from_checkpoint("model_chp/model_-0217_2.ckpt")


@app.get("/")
async def root():
    sql = f'SELECT * FROM USER;'
    result= db.execute(sql).fetchall()
    return {"msg": "오지마오지마오지마",
            "sql": result}


################################# 일반 질문 (찐_완성!) ##########################################
## 일반 질문 type(normal1 인지 nomarl2 인지) 으로 입력받아서 return
## + 질문한 내용 chatting 테이블에 저장함
@app.get("/question/{type}")
async def fetch_normalQ(type:str):
    sql1  = f"select sentence from QUESTION WHERE type = '{type}' order by rand()  LIMIT 1;"
    result = db.execute(sql1).fetchone()
    result2 = str(result)
    sql2 = f'INSERT INTO CHATTING VALUES(1,curdate(),curtime(),"bot","{result2[2:-3]}");'
    db.execute(sql2)
    return result

#############################################################################################


####################### 키워드 번호로 해당 키워드 질문 받아오기 (찐_완성!) ############################
@app.get("/question/keyword/{keyword}")
async def fetch_keywordQ(keyword:int):
    # sql = "select * from QUESTION where keyword ='keyword';"
    # sql1  = f"select sentence from QUESTION WHERE type = '{type}' order by rand()  LIMIT 1;"

    sql = f"SELECT sentence FROM QUESTION WHERE keyword = '{keyword}' ORDER BY RAND() LIMIT 1;"
    result = db.execute(sql).fetchone()
    result2 = str(result)
    sql2 = f'INSERT INTO CHATTING VALUES(1,curdate(),curtime(),"bot","{result2[2:-3]}");'
    db.execute(sql2)
    return result

#################################################################################################### 


############################# 날짜별로 가져오기 성공! (찐_완성!) #####################
@app.get("/report/chat/{day}") 
async def fetch_report(day:str):
    sql1 = f"SELECT * FROM TALK_REPORT WHERE day= '{day}';"
    result1 = db.execute(sql1).fetchone()

    return result1  

@app.get("/report/draw/{day}")
async def fetch_report(day:str):
    sql = f"SELECT * FROM DRAW_REPORT WHERE day = '{day}';"
    result = db.execute(sql).fetchone()


    return result

#########################################################################################


########################### USER_TESTDAY에 테스트한 날짜 저장 & CHATTING TABLE에 채팅 내용 저장 (!!찐_완성!!) ##################################
@app.post("/report/chat")
async def register_report(tmp: Sendtext):
    #채팅 내용을 db에 저장  
    try:  
        # sql = f"INSERT INTO USER_TESTDAY (userid, day) VALUES ({tmp.userid}, curdate());"
        sql = f"INSERT INTO USER_TESTDAY (userid, day) VALUES (1, curdate());"
        conn.commit()
        conn.execute(sql)
        conn.close()
    except:
        print("??")
    strtmp = model.chat(tmp.text)
    sql = f"INSERT INTO CHATTING (userid, day, time, type, chat) VALUES ({tmp.userid},curdate(),curtime(), 'user','{tmp.text}');"
    conn.commit()
    conn.execute(sql)
    conn.close()
    # db.close()
    return {"msg": "CHATTING table에 저장",
            "bot": strtmp}

################################################################################################################################

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)