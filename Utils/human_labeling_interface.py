import pandas as pd
filename = input('csv 파일 경로를 입력하세요.\n>>>')
df_data = pd.read_csv(filename)
# df_data = pd.read_csv('tmp_humanlabeling.csv')


str_help_labels = '''<자신에 관한 내용>	
0	성장과정
1	성격 장단점, 생활신조 / 윤리의식(환경, 직업윤리)
2	직무역량(강점만 어필하는 느낌) / 강약점(직무상의 강약점, 학과, 자격증, 수강과목 따라서 이런일에 역량을 발휘할 수 있습니다.)
3	지원동기 및 입사후 포부 / 입사를 위한 준비과정 / 회사 이해도(어떤 사업을 하고 있는지, 혁신(입사 후 제안 서비스))
4	사회경험(인턴, 동아리, 공모전, 봉사활동, 아르바이트 및 학창시절) / 도전, 성취 경험 / 
5	경력사항(일을 했던 경력)
<자신 외적에 관한 내용>	
6	사회이슈(사회의 특정 사건에 대해서 어떤 견해를 가지고 있는지)
<자신과 타인에 관한 내용>	
7	조직적응력, 사회성(대인관계) > 팀워크 / 소통(이견있을 때 어떻게 해결? / 리더십)
8	문제해결력(의사결정-상사가 지시한 일/ 시한이 급한 일 어떤 일에 우선순위를 둘 것인가, 시나리오 문제), 정보능력(잘 안나올 것같음)'''


from datetime import datetime
from datetime import timedelta
now = datetime.utcnow() + timedelta(seconds=60*60*9)
str_now = now.strftime("%Y/%m/%d/ %H:%M:%S")
str_now

from IPython.display import clear_output
import ast

hm_worker = input('작업자의 성함을 입력하세요. (예: DjPark, MikePK, Kbrow)\n>>>')
hm_date = now.strftime("%Y/%m/%d/ %H:%M:%S")
int_idx_start = input('작업을 시작하려는 데이터프레임의 인덱스 번호를 입력하세요.\n>>>')
if int_idx_start == '!':
    for lcnt, (crawl_idx, row) in enumerate(df_data.iterrows()):
        if row['human_labeling'].isna() == True:
            int_idx_start = lcnt

int_idx_start = int(int_idx_start)
for lcnt, (crawl_idx, row) in enumerate(df_data.iterrows()):#['qus']):
    if lcnt < int_idx_start:
        continue
    print('**** qus ****')
    print('lcnt:', lcnt)
    print('crawl_idx:', crawl_idx)
    qus = row['qus']
    print(qus)
    print('human_label:', row['human_label'])
    print('-'*100)
    print(str_help_labels)
    inp = input('\n라벨을 입력하세요. (예 : 1,3, 5 >>> [1,3,5])\n>>>')
    if inp == '#':
        break
    if inp == '':    # 다음 row로 넘어감
        continue
    l_labels = inp.split(',')
    l_labels = sorted(list(map(int, l_labels)))
    print('converted in to list<int> :', l_labels)
    df_data.loc[crawl_idx, 'human_label'] = str(l_labels)
    df_data.loc[crawl_idx, 'hm_worker'] = hm_worker

    # 해당 row의 내용 기록한 시각 입력
    now = datetime.utcnow() + timedelta(seconds=60*60*9)
    hm_date = now.strftime("%Y/%m/%d/ %H:%M:%S")
    df_data.loc[crawl_idx, 'hm_date'] = hm_date
    # print('row:')
    # print(df_data.loc[crawl_idx])

    # 임시파일로 저장
    df_data.to_csv('tmp_humanlabeling.csv', index=False)
    
    # 다음 행으로 넘어가기 위한 키입력 처리    
    while inp != '':
        inp = input('Enter to next\n>>>')
        if inp == '#':
            break
    if inp == '#':
            break
    
    clear_output()