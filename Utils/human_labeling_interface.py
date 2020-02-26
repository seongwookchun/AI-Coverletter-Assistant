# -*- coding: utf-8 -*-

# - 프로그램 흐름 -
# 작업자 입력
# 파일 선택
# 라벨 입력, 이동 및 종료
# 라벨 입력 확인


import os
import pandas as pd
import re
from glob import glob
# row 기록 시간 입력용 모듈 import
from datetime import datetime
from datetime import timedelta

# 작업자 입력
hm_worker = input('작업자의 성함을 입력하세요. (예: DjPark, MikePK, Kbrow)\n>>>')

# 파일 선택
str_tmp_filename = 'tmp.csv'    # 임시 저장용 csv 파일 이름 초기화
re_cd = re.compile('cd\s(.+)')
re_int = re.compile('\d+')
print('*'*100)
os.chdir('../Rsc')    # Rsc 폴더로 작업경로를 초기화 한다.
print('csv file list')
l_csv_files = glob('*.csv')
for lcnt, f in enumerate(l_csv_files):
	print('(' + str(lcnt) + ')', f)
while True:
	print('csv 파일의 번호를 입력 또는 cd/ ls 명령어를 입력하세요.')
	print('csv 파일을 목록을 갱신하려면 csv를 입력하세요.')
	str_input = input('>>> ').strip()
	# 경로 변경
	if re_cd.match(str_input):
		re_res = re_cd.match(str_input)
		print('re_res.string:', re_res.string)
		# str_path = str_input[re_res.start(): re_res.end()]
		# print('str_path:', str_path)
		os.chdir(re_res.string)
		print('path :', os.getcwd())
	# ls 명령어
	elif str_input == 'ls':
		for lcnt, f in enumerate(glob('*')):
			print(f)
	# csv 목록 출력
	elif str_input == 'csv':
		l_csv_files = glob('*.csv')
		for lcnt, f in enumerate(l_csv_files):
			print('(' + str(lcnt) + ')', f)
	# csv 번호 선택
	elif re_int.match(str_input):
		print('selcted number :', str_input)
		print('selcted file name :', l_csv_files[int(str_input)])
		df_data = pd.read_csv(l_csv_files[int(str_input)])
		print('head of selected dataframe :')
		print(df_data.head(3))
		break    # 파일 선택 프로그램 종료
	# 입력이 명령어에 해당하지 않는 경우
	else:
		print('no match')
	input('Enter')


# 키입력
# console 화면 지우기
# # import call method from subprocess module 
# from subprocess import call 
  
# # import sleep to show output for some time period 
# from time import sleep 
  
# # define clear function 
# def clear(): 
#     # check and make call for specific operating system 
#     _ = call('clear' if os.name =='posix' else 'cls') 


str_help = '''이동 (b: 이전/ n: 다음/ m <int>: 인덱스 이동)
라벨 입력 및 확인 (1, 2,3 or 1 2  3 <라벨>: 데이터 프레임에 갱신)
기타 (f: 자소서 9종 클래스 목록 도움말 플래그 On-Off / r: 콘솔화면 지우기)'''
with open('jasoseo_class_help.txt', 'r', encoding='utf-8') as f:
	str_jasoseo_class_help = f.read()

re_chidx = re.compile('m\s(\d+)\s*')
re_label = re.compile('(\d+\s*[,\s])*(\d\s*)')
re_label_split = re.compile('(,\s*)|\s{2,}')
# fl_help_labels = False    # 자소서 9종 분류 도움말 표시 선택용 flag를 False로 초기화
len_df_data = len(df_data)
# 키입력 처리 함수 구현
def f_key_proc(vstr_input):
	global str_input
	global int_cur, l_inp_label, fl_help_labels, df_data
	# print('len_df_data :', len_df_data)
	if vstr_input == 'h':
		print('*'*100)
		print(str_help)
	elif vstr_input == 'b':
		int_cur += -1 -1
	elif vstr_input == 'n':
		pass
	elif re_label.match(vstr_input):
		l_inp_label = re_label_split.sub(' ', 
									re_label.match(vstr_input).string).split()
		l_inp_label = sorted(l_inp_label)
		print('l_inp_label:', l_inp_label)
		print('Enter : 저장 후 다음으로 이동 / 그외 : 취소')
		str_input = input('>>> ')
		if str_input == '':
			now = datetime.utcnow() + timedelta(seconds=60*60*9)
			str_now = now.strftime("%Y/%m/%d/ %H:%M:%S")
			df_data.loc[int_cur, 'human_label'] = str(l_inp_label)    # 아래 에러를 피하기 위해, str() 처리함.
			# ValueError: Must have equal len keys and value when setting with an iterable
			df_data.loc[int_cur, 'hm_worker'] = hm_worker
			df_data.loc[int_cur, 'hm_date'] = str_now
			df_data.to_csv(str_tmp_filename, index=False)
			print('df_data has been saved as', str_tmp_filename)
		else:
			int_cur -= 1    # row를 이동하지 않기 위해 -=1 처리함

	elif re_chidx.match(vstr_input):
		int_cur = int(re_chidx.match(vstr_input).group(1)) -1
		print('인덱스 이동 ->', int_cur +1)
	# console 화면 지우기
	elif vstr_input == 'r':
		# print('', end='\r')
		# sys.stdout.write("\033[K")
		# sys.stdout.flush()
		# clear()
		int_cur -= 1    # row를 이동하지 않기 위해 -=1 처리함
	elif vstr_input == 'f':
		fl_help_labels = bool((fl_help_labels+1)%2)
		print('flag for jasoseo_class_help')
		print('flag state:', 'On' if fl_help_labels == True else 'Off')
		int_cur -= 1    # row를 이동하지 않기 위해 -=1 처리함
	# 내용 데이터프레임에 반영 및 tmp 파일 저장
	elif vstr_input == '':    # 다음 row로 이동
		pass
	else:
		print('잘못된 입력입니다.')
		int_cur -= 1    # row를 이동하지 않기 위해 -=1 처리함


# 메인 함수
print('*'*100)
print(str_help)
l_inp_label = list()    # global variable 초기화
fl_help_labels = False
int_cur = -1
while True:
	print('*'*100)
	int_cur += 1
	int_cur %= len_df_data
	print('int_cur:', int_cur)
	if fl_help_labels == True:
		print(str_jasoseo_class_help)
		print('-'*100)
	print('qus:')
	print(df_data.loc[int_cur, 'qus'])
	print('human_label:',df_data.loc[int_cur, 'human_label'])

	str_input = input('>>> ').strip()
	f_key_proc(str_input)