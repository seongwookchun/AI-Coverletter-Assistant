import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import signal
import sys
from datetime import datetime,timedelta

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
    print('jobkorea qus&ans data crawling stop and save about data completed until now', '*'*100)
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



def date_split(x):
    y,m,d = x.split(',')
    return int(y),int(m),int(d)



def url_func(selector):
    for j in selector:
        news_url = 'http://news.jtbc.joins.com/' + j.attrs['href']
        # print(news_url)
        yield news_url

def jtbc_news(date_start,date_end,path):
    # date_start : ½ÃÀÛ ³¯Â¥. ÃÖ½Å ³¯Â¥ºÎÅÍ ½ÃÀÛ
    # date_end : ³¡³ª´Â ³¯Â¥. °¡Àå ³ªÁß ³¯Â¥
    # scode: ´º½º ±â»ç Ä«Å×°í¸® ex) ³¯¾¾,°æÁ¦ µî
    global path2
    path2 = path

    url = 'http://news.jtbc.joins.com/section/list.aspx'
    url_lists = []
    y_s,m_s,d_s = date_split(date_start)
    y_e,m_e,d_e = date_split(date_end)   
    date_start = datetime(y_s,m_s,d_s)
    date_end = datetime(y_e,m_e,d_e) 
    date_diff = (date_start - date_end).days

    section_url={}
    

    for i in range(date_diff,-1,-1):
        for code in range(0,10,10):
            datestr = (date_start-timedelta(i)).strftime('%Y%m%d')
            params = {'pdate':datestr,'scode':code}
            res = requests.get(url,params= params)
            soup = BeautifulSoup(res.text,'html.parser')
            selector = soup.select('ul#section_list dt.title_cr a')
            

            next_page= soup.select('div#CPContent_pager a.next')
            
            url_lists += [i for i in url_func(selector)]

            while len(next_page) >0:
                next_url = 'http://news.jtbc.joins.com/' + next_page[0].attrs['href']
                res = requests.get(next_url)
                soup = BeautifulSoup(res.text,'html.parser')
                selector = soup.select('ul#section_list dt.title_cr a')
                
                url_lists+= [i for i in url_func(selector)]
                
                next_page = soup.select('div#CPContent_pager a.next')
                
            section_url[code] = url_lists
            

    return title_text_split(section_url)


def jtbc_signal_handler(signal,frame):
    
    df = pd.DataFrame(code_list,columns=['section'])
    df['title'] = title_list     
    df['content'] = content_list
    df.to_csv(path2)
    print('jtbc_news_crawling stop and save about data completed until now ', '*'*100)
    sys.exit(0)


def title_text_split(section_url):
    signal.signal(signal.SIGINT, jtbc_signal_handler)

    section_mapping = {0:'¼Óº¸',
                       10:'Á¤Ä¡',
                       20:'°æÁ¦',
                       30:'»çÈ¸',
                       40:'±¹Á¦',
                       50:'¹®È­',
                       60:'¿¬¿¹',
                       70:'½ºÆ÷Ã÷',
                       80:'³¯¾¾'
    }

    global title_list
    title_list = []
    global content_list
    content_list =[]
    global code_list
    code_list = []
    for code,urls in section_url.items():
        for url in urls:
            res = requests.get(url)
            soup = BeautifulSoup(res.content,'html.parser')

            title = soup.select_one('div.title h3').text
            content = soup.select_one('div.article_content').text

            title_list.append(title)
            content_list.append(content)
            code_list.append(section_mapping[code])      
            
    df = pd.DataFrame(code_list,columns=['section'])
    df['title'] = title_list
    df['content'] = content_list
    df.to_csv(path2)

    return df
