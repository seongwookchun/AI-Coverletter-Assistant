import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import signal
import sys

answer_list = []
question_list = []

def jobkorea_crawling(start_page,end_page,url,path,qus_tag='dl.qnaLists span.tx',ans_tag='dl.qnaLists dd div.tx'): 
    # 1 page ´ç 20°ÇÀÇ ÀÚ¼Ò¼­°¡ Á¸Àç 
    # url = jobkorea url ÀÔ·Â
    # start_page = ½ÃÀÛ ÆäÀÌÁö
    # end_page = Á¾·á ÆäÀÌÁö
    
    url_lists = []

    for i in range(start_page,end_page):
        url = url
        params={'Page':i}

        res = requests.get(url,params=params)
        soup = BeautifulSoup(res.content,'html.parser')
        a= soup.find_all('p','tit')
        
        for j in a:
            url_lists.append('http://www.jobkorea.co.kr'+j.find('a').attrs['href'])

    return qus_ans(url_lists,qus_tag,ans_tag,path)



def signal_handler(signal,frame):
    #Áß°£¿¡ ÁßÁö¸í·ÉÀ» ³»¸± ½Ã, ÀÛ¾÷ÁßÀÌ´ø µ¥ÀÌÅÍ¸¦ ÀúÀå
    df = pd.DataFrame(question_list,columns=['qus'])
    df['ans'] = answer_list     
    df.to_csv(path)
    print('Last operation before end of the program', '*'*100)
    sys.exit(0)


def qus_ans(url_lists,qus_tag,ans_tag,path):
    # Å©·Ñ¸µÇÑ µ¥ÀÌÅÍ¸¦ Áú¹®°ú ´äº¯À¸·Î ³ª´²¼­ csv·Î ÀúÀå
    pat = re.compile('<span[\sa-zA-Z0-9="]*>[°¡-ÆR\sa-zA-Z0-9<>\/,]+<\/span>')
    parser = 'html.parser'
    signal.signal(signal.SIGINT, signal_handler)

    for idx,i in enumerate(url_lists):
        res=  requests.get(i)
        soup = BeautifulSoup(res.text,parser)
        a= soup.select(qus_tag)
        b = soup.select(ans_tag)
        

        for j in b:
            j = BeautifulSoup(pat.sub('',str(j)))
            answer_list.append(j.text)
            
        for j in a:
            question_list.append(j.text)
 
    df = pd.DataFrame(question_list,columns=['qus'])
    df['ans'] = answer_list     
    df.to_csv(path)

    return  df

