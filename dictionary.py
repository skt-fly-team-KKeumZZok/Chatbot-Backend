import pandas as pd
from pykospacing import Spacing
from hanspell import spell_checker
from konlpy.tag import Okt

def dictionary(sent):
  curr_score=100 # 시작 100점
  for i in sent:
    new_sent = i.replace(" ", '') # 띄어쓰기가 없는 문장 임의로 만들기
    
    spacing = Spacing()
    kospacing_sent = spacing(new_sent) 


    spelled_sent = spell_checker.check(new_sent)

    hanspell_sent = spelled_sent.checked
    

    okt = Okt() 
    text = hanspell_sent
    temp =[]
    temp =okt.morphs(text, stem=True)

    new_list = []
    for w in temp:
        if w not in new_list:
            new_list.append(w)

  
    emotiondic_csv = pd.read_excel('data/emotiondic-revise 1.xlsx')
    emotiondic_csv

    
    for word in new_list: # sentence = ['난','우울해'] 하나씩 가져오기기
        for cate,score in zip(emotiondic_csv['cate'],emotiondic_csv['score']):
            if word ==cate:
                score=int(score) #정수형 바꿔주기
                curr_score-=score # curr_score = curr_score - score
                print(curr_score)
                
  if curr_score <40:
      result=0
  elif curr_score>=40 and curr_score<65:
      result=1
  elif curr_score>=65 and curr_score<90:
      result=2
  elif curr_score>=90 and curr_score<105:
      result=3
  elif curr_score>=105:
      result=4
  print(result)
  return (result)