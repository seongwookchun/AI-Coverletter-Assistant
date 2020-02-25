import os
import pandas as pd
import re
from glob import glob

re_cd = re.compile('^cd\s.+')
flag_exit = False    # int형 입력시 이중 while문 탈출용 flag
while True:
    print('탐색 경로:', os.path.curdir)
    print('csv 파일을 선택하세요. 또는 cd 명령어를 사용하세요.')
    l_csv_files = glob('*.csv')
    for lcnt, f in enumerate(l_csv_files):
        print(lcnt, f)
    str_input = input('>>> ')
    while True:
        if re_cd.findall(str_input):
            try:
                os.path.chdir(str_input[3:].strip())
                break
            except:
                print('Command is wrong. :', str_input)
                break
        try:
            if int(str_input) < len(l_csv_files):
                int_fileno = int(str_input)
                print('선택된 번호:', int_fileno)
                flag_exit = True    # string입력 while문 탈출을 위한 flag On
                break
        except:
            print('Command is wrong. :', str_input)
            break
    if flag_exit == True:
        break

filename = l_csv_files[int_fileno]
df_data = pd.read_csv(filename)
print(df_data.head(3))
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
print('*'*100)
print('''작업을 시작하려는 데이터프레임의 인덱스 번호를 입력하세요.\n
    ! 를 입력하면 작업이 안된 인덱스를 선택할 수 있습니다.''')
print('-'*100)
print('상위 3개 작업 미처리(np.nan)')
print(df_data[df_data['human_label'].isna() == True].iloc[:3])

flag_exit = False    # 이중 루프를 벗어나기위한 flag 초기화
while True:
    str_input = input('>>> ')
    if str_input == '!':
        for lcnt, (crawl_idx, row) in enumerate(df_data.iterrows()):
            if row.isna()['human_label'] == True:
                int_idx_start = lcnt    # 최상단의 np.nan를 찾음
                flag_exit = True
                break
        if flag_exit == True:
            break
    else:
        try:
            int_idx_start = int(str_input.strip())
            break
        except:
            print('잘못된 입력 형식입니다.')
print('작업 시작 인덱스 :', int_idx_start)
# for lcnt, (_, row) in enumerate(df_data.iterrows()):#['qus']):
#     if lcnt < int_idx_start:
#         continue
 
str_help_0 = '라벨을 입력하세요. / # : 종료 \n(예 : 1,3, 5 >>> [1,3,5])'
str_help_1 = 'Enter : 다음 row / b : 이전 row / 정수 입력 : 해당 인덱스로 이동 / # : 작업 종료'
def f_key_thread(str_help, mode):
    # 다음 행으로 넘어가기 위한 키입력 처리
    global lcnt, str_input
    while True:#str_input != '':
        print(str_help)
        str_input = input('>>>')
        str_input = str_input.strip()
        if str_input == '':
            break
        elif str_input == '#':
            break
        if mode == 'input':
            if re_labels.match(str_input):
                break
            # else: 잘못된 입력
        elif mode == 'function':
            if re_int.match(str_input) != None:
                print('입력된 인덱스 {}(으)로 이동합니다.'.format(int(str_input)))
                lcnt = int(str_input) -1
                break
            elif str_input == 'b':
                lcnt = (lcnt -1) -1
                break
        else:
            print('잘못된 입력입니다.')
    # return lcnt



lcnt = int_idx_start -1    # -1의 처리 이유는 while문 시작시에 += 1을 하기 때문.
re_int = re.compile('\d+')
re_labels = re.compile('(\d+\s*,\s*)*(\d+\s*)')
# print(re_labels.match('1,2, 3'))    # ok
# print(re_labels.match('3 '))    # ok
while True:
    lcnt += 1
    row = df_data.iloc[lcnt]
    print('*'*40, 'qus', '*'*40)
    print('lcnt:', lcnt)
    crawl_idx = row['index']
    print('crawl_idx:', crawl_idx)
    qus = row['qus']
    print(qus)
    print('human_label:', row['human_label'])
    print('-'*100)
    print(str_help_labels)
    # print()
    # inp = input('>>>')
    # if inp == '#':
    #     break
    # elif inp == '':    # 다음 row로 넘어감
    #     continue
    f_key_thread(str_help_0, 'input')

    l_labels = str_input.split(',')
    print('l_labels:', l_labels)
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

    # 해당 row입력 마다 임시파일로 저장
    df_data.to_csv('tmp_humanlabeling.csv', index=False)
    print('saved as tmp_humanlabeling.csv')

    # lcnt 업데이트 및 키입력 대기
    f_key_thread(str_help_1, 'function')

    if str_input == '#':
            break
    
    clear_output()