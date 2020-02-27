#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import signal
import sys
from datetime import datetime,timedelta
from multiprocessing.pool import ThreadPool
from time import time
import concurrent.futures
import numpy as np

import os.path



answer_list = []
question_list = []

def jobkorea_crawling(start_page,end_page,url,path,qus_tag='dl.qnaLists span.tx',ans_tag='dl.qnaLists dd div.tx'): 
    # 1 page 당 20건의 자소서가 존재 
    # url = jobkorea url 입력
    # start_page = 시작 페이지
    # end_page = 종료 페이지
    
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
    #중간에 중지명령을 내릴 시, 작업중이던 데이터를 저장
    df = pd.DataFrame(question_list,columns=['qus'])
    df['ans'] = answer_list     
    df.to_csv(path)
    print('jobkorea qus&ans data crawling stop and save about data completed until now', '*'*100)
    sys.exit(0)


def qus_ans(url_lists,qus_tag,ans_tag,path):
    # 크롤링한 데이터를 질문과 답변으로 나눠서 csv로 저장
    pat = re.compile('<span[\sa-zA-Z0-9="]*>[가-R\sa-zA-Z0-9<>\/,]+<\/span>')
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





def date_split(x):
    y,m,d = x.split(',')
    return int(y),int(m),int(d)


def url_func(selector):
    for j in selector:
        news_url = 'http://news.jtbc.joins.com/' + j.attrs['href']
        
        yield news_url


def multi_thread(date_diff,date_start,url,code):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        return [executor.submit(thread_func,date_start,i,url,code) for i in range(date_diff,-1,-1)]
    



def thread_func(date_start,i,url,code):
    
    url_lists = []
    pgi_dict ={}
    date_dict= {}
    
    datestr = (date_start-timedelta(i)).strftime('%Y%m%d')
    params = {'pdate':datestr,'scode':code}
    res = requests.get(url,params= params)
    soup = BeautifulSoup(res.text,'html.parser')
    selector = soup.select('ul#section_list dt.title_cr a')   
    next_page= soup.select('div#CPContent_pager a.next')
    url_lists += [i for i in url_func(selector)]
    
    # pgi(page number) 추가 2020.02.27
    pgi = soup.select_one('div#CPContent_pager span.num.selected')
    
    if pgi is None:
        pgi=1
        pgi_dict[pgi]=url_lists

    else:
        pgi_dict[int(pgi.text)] = url_lists


    while len(next_page) >0:
        
        next_url = 'http://news.jtbc.joins.com/' + next_page[0].attrs['href']
        res = requests.get(next_url)
        soup = BeautifulSoup(res.text,'html.parser')
        selector = soup.select('ul#section_list dt.title_cr a')      
        url_lists= [i for i in url_func(selector)]      
        next_page = soup.select('div#CPContent_pager a.next')
        
        # page number 추가 2020.02.27
        pgi = soup.select_one('div#CPContent_pager span.num.selected')
        pgi_dict[int(pgi.text)] = url_lists

    # 날짜 데이터 추가 2020.02.27
    date_dict[datestr] = pgi_dict
    return date_dict


def jtbc_news(date_start,date_end,path):
    """
    crawling jtbc news data by category news from politics to weather 

    # date_start : 시작 날짜. 최신 날짜부터 시작  //입력 예) '2020,02,25'  
    # date_end : 끝나는 날짜. 가장 나중 날짜 //입력 예) '2020,02,24'  
    # path : 파일을 생성할 위치와 csv 파일명  
    # scode: 뉴스 기사 카테고리 ex) 날씨,경제 등  

    """
    section_scode = list(np.arange(10,90,10))
    global path2
    path2 = path
    time_i = time()
    url = 'http://news.jtbc.joins.com/section/list.aspx'
    
    y_s,m_s,d_s = date_split(date_start)
    y_e,m_e,d_e = date_split(date_end)   
    date_start = datetime(y_s,m_s,d_s)
    date_end = datetime(y_e,m_e,d_e) 
    date_diff = (date_start - date_end).days

    section_url={}
    

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = [executor.submit(multi_thread,date_diff,date_start,url,code) for code in section_scode]
       
    
        for code,i in zip(section_scode,future):
            result1 = []

            for j in i.result():
                result = j.result()

                result1.append(result)
    
            section_url[code]= result1

    print(round(time() - time_i,2),'초')
    # print(section_url)

    """ section_url 형식 :
     {10: [{'20200224': {1: ['http://news.jtbc.joins.com//html/520/NB11936520.html', 
     {scode : [{날짜 : {page number : [url ] } } } } ]
     """

    return title_text_split(section_url)




#긴급정지 저장 function 잠시 수정.
# def jtbc_signal_handler(signal,frame):
    
#     df = pd.DataFrame(code_list,columns=['section'])
#     df['title'] = title_list     
#     df['content'] = content_list
#     df.to_csv(path2)
#     print('jtbc_news_crawling stop and save about data completed until now ', '*'*100)
#     sys.exit(0)

# 5층 Thread function
def title_txt_multi_thread1(code,date_list):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        return [executor.submit(title_txt_multi_thread2,code,i) for i in date_list]

def title_txt_multi_thread2(code,date_dict):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        return [executor.submit(title_txt_multi_thread3,code,date,p_dict) for date,p_dict in date_dict.items()]

def title_txt_multi_thread3(code,date,p_dict):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        return [executor.submit(title_txt_multi_thread4,code,date,page,urls) for page,urls in p_dict.items()]


def title_txt_multi_thread4(code,date,page,urls):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        return [executor.submit(title_content_thread,code,url,date,page) for url in urls]

# 개별 뉴스 url에서 title,content 추출하는 Thread function
def title_content_thread(code,url,date,page):
   
    section_mapping = {0:'속보',
                       10:'정치',
                       20:'경제',
                       30:'사회',
                       40:'국제',
                       50:'문화',
                       60:'연예',
                       70:'스포츠',
                       80:'날씨' }
    
    res = requests.get(url)
    soup = BeautifulSoup(res.content,'html.parser')

    title = soup.select_one('div.title h3').text
    content = soup.select_one('div.article_content').text

    return title,content,section_mapping[code],date,page
      
    
def title_text_split(section_url):
    time_i = time()
   
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = [executor.submit(title_txt_multi_thread1,code,urls) for code,urls in section_url.items()]

    # Thread 리턴
    for i in future:
        for j in i.result():
            for k in j.result():
                for y in k.result():
                    for z in y.result():
            
                        title,content,code,date,page = z.result()
                        
                        # 기존 데이터가 존재하면 데이터 추가 없다면 생성
                        if os.path.exists(path2):
                            df = pd.read_csv(path2)
                            df = df.append({'section':code,'title':title,'content':content,'date':date,'page_num':page},ignore_index=True)
                            df.to_csv(path2,index=False)
                        
                        else:
                            df= pd.DataFrame(columns=['section','title','content','date','page_num'])
                            df= df.append({'section':code,'title':title,'content':content,'date':date,'page_num':page},ignore_index=True)
                            df.to_csv(path2,index=False)
                
                    

        
    print(round(time() - time_i,2),'초')
    
    return df
        
