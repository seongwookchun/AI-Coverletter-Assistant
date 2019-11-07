import hgtk

# 자음 vectorization

d_CHO_sori = {
    'ㄱ':[0,2,0],
    'ㄲ':[0,2,1],
    'ㄴ':[3,1,0],
    'ㄷ':[0,1,0],
    'ㄸ':[0,1,1],
    'ㄹ':[4,1,0],
    'ㅁ':[3,0,0],
    'ㅂ':[0,0,0],
    'ㅃ':[0,0,1],
    'ㅅ':[2,1,0],
    'ㅆ':[2,1,1],
    'ㅇ':[3,3,0],
    'ㅈ':[1,2,0],
    'ㅉ':[1,2,1],
    'ㅊ':[1,2,2],
    'ㅋ':[0,3,2],
    'ㅌ':[0,1,2],
    'ㅍ':[0,0,2],
    'ㅎ':[3,0,0],
}

d_JOONG_sori = {
'ㅏ':[3, 0, 0],
'ㅐ':[2, 0, 0],
'ㅑ':[3, 0, 1],
'ㅒ':[2, 0, 1],
'ㅓ':[2, 1, 0],
'ㅔ':[1, 0, 0],
'ㅕ':[2, 1, 1],
'ㅖ':[1, 0, 1],
'ㅗ':[1, 2, 0],
'ㅘ':[3, 0, 2],
'ㅙ':[1, 1, 1],
'ㅚ':[1, 1, 0],
'ㅛ':[1, 2, 1],
'ㅜ':[0, 3, 0],
'ㅝ':[2, 1, 2],
'ㅞ':[1, 0, 2],
'ㅟ':[0, 1, 0],
'ㅠ':[0, 3, 1],
'ㅡ':[0, 2, 0],
'ㅢ':[0, 0, 1],
'ㅣ':[0, 0, 0]
}


d_JONG_sori = {
 'ㄱ':[0,2,0],
 'ㄲ':[0,2,1],
 'ㄳ':[0,2,0],
 'ㄴ':[3,1,0],
 'ㄵ':[3,1,0],
 'ㄶ':[3,1,0],
 'ㄷ':[0,1,0],
 'ㄸ':[0,1,1],
 'ㄹ':[4,1,0],
 'ㄺ':[4,1,0],
 'ㄻ':[4,1,0],
 'ㄼ':[4,1,0],
 'ㄽ':[4,1,0],
 'ㄾ':[4,1,0],
 'ㄿ':[4,1,0],
 'ㅀ':[4,1,0],
 'ㅁ':[3,0,0],
 'ㅂ':[0,0,0],
 'ㅃ':[0,0,1],
 'ㅄ':[0,0,0],
 'ㅅ':[2,1,0],
 'ㅆ':[2,1,1],
 'ㅇ':[3,3,0],
 'ㅈ':[1,2,0],
 'ㅉ':[1,2,1],
 'ㅊ':[1,2,2],
 'ㅋ':[0,3,2],
 'ㅌ':[0,1,2],
 'ㅍ':[0,0,2],
 'ㅎ':[3,0,0]
}


d_oft_JONG_sori = {
 'ㄱ':[0,2,0],
#  'ㄲ':[0,2,1],
#  'ㄳ':[0,2,0],
 'ㄴ':[3,1,0],
#  'ㄵ':[3,1,0],
#  'ㄶ':[3,1,0],
 'ㄷ':[0,1,0],
#  'ㄸ':[0,1,1],
 'ㄹ':[4,1,0],
#  'ㄺ':[4,1,0],
#  'ㄻ':[4,1,0],
#  'ㄼ':[4,1,0],
#  'ㄽ':[4,1,0],
#  'ㄾ':[4,1,0],
#  'ㄿ':[4,1,0],
#  'ㅀ':[4,1,0],
 'ㅁ':[3,0,0],
 'ㅂ':[0,0,0],
#  'ㅃ':[0,0,1],
#  'ㅄ':[0,0,0],
 'ㅅ':[2,1,0],
 'ㅆ':[2,1,1],
 'ㅇ':[3,3,0],
#  'ㅈ':[1,2,0],
#  'ㅉ':[1,2,1],
#  'ㅊ':[1,2,2],
#  'ㅋ':[0,3,2],
#  'ㅌ':[0,1,2],
#  'ㅍ':[0,0,2],
#  'ㅎ':[3,0,0]
}



import numpy as np

def dis_sori(sori01, sori02):    # sori01 : input의 음소(초,중,종성), sori02 : 비교하려는 음소(초, 중, 종성)
#     print('in dis_sori func sori01{} sori02{}'.format(sori01, sori02))
    if sori01 in hgtk.checker.CHO:
#         d_sori = d_CHO_sori
        d_sori = d_JONG_sori
    elif sori01 in hgtk.checker.JOONG:
        d_sori = d_JOONG_sori
    else:
        d_sori = d_JONG_sori
    vec01 = np.array(d_sori[sori01])
    vec02 = np.array(d_sori[sori02])
    
    res = sqrt_einsum_T(vec01, vec02)
#     print(vec01, vec02, res)
    return res

def sqrt_einsum_T(v1, v2):
    a, b = v1, v2
    a_b = a - b
    return np.sqrt(np.einsum("i,i", a_b, a_b))
# sqrt_einsum_T('ㅎ', 'ㅇ')
# dis_sori('ㅎ', 'ㅇ')
# dis_sori('ㅏ', 'ㅘ')
# dis_sori('ㄶ', 'ㄵ')


import time
time_i = time.time()

class Rhyme():
    def __init__(self):    # 멤버 변수
        self.l_res_letters = list()    # 모든 글자의 음소교환 결과만 저장한다.
        self.l_res_info = list()    # 모든 글자의 거리정보를 저장한다.
        self.res = list()
    def __str__(self):
        return 'Rhyme class'
    def str_outer(self, d_eumso01, d_eumso02, nb_eumso=12):
        l_res = list()
        d_res = dict()
        l_eumso01 = list(d_eumso01.keys())
        l_eumso02 = list(d_eumso02.keys())
        # try:
            # nb_eumso = 7    # 디버깅용 하드코딩
        l_eumso01 = l_eumso01[:nb_eumso]
        l_eumso02 = l_eumso02[:nb_eumso]
        # except:
        #     pass
        for eumso01 in l_eumso01:
            for eumso02 in l_eumso02:
                res_word = eumso01+eumso02
                # print(res_word)
#                 l_res.append(res_word)
                distance_word = (d_eumso01[eumso01] + d_eumso01[eumso01])/2
                d_res[res_word] = distance_word
        l_res = sorted(d_res.items(), key=lambda kv: kv[1])
        return l_res
    def l_change_CHOJOONG(self, inp_string, nb_eumso=10):    
        # 음소교환 대상은 입력 단어내 모든 글자로 한다.
#         self.l_res_letters = list()    # 모든 글자의 음소교환 결과만 저장한다.
#         self.l_res_info = list()    # 모든 글자의 거리정보를 저장한다.
        for nth_letter in range(len(inp_string)):
            str_last = inp_string[nth_letter]
            dec_last = hgtk.text.decompose(str_last)#.replace('ᴥ', '')
            # print(dec_last)

            # CHO JOONG JONG 선언
            inp_CHO = dec_last[0]
            inp_JOONG = dec_last[1]


            # CHO 변환
            d_res = dict()
            i = 0
            for CHO in hgtk.checker.CHO:
                res_CHO = CHO
                for JOONG in hgtk.checker.JOONG:

                    res_JOONG =JOONG

                    dis_CHO = dis_sori(inp_CHO, res_CHO)
                    dis_JOONG = dis_sori(inp_JOONG, res_JOONG)
                    # "초성 + 중성 + 종성"인 경우
                    if len(dec_last) == 4:
                        inp_JONG = dec_last[2]

        #                 for JONG in hgtk.checker.JONG[1:]:
                        for JONG in d_oft_JONG_sori.keys():
                            res_JONG = JONG
                            res_letter = hgtk.letter.compose(res_CHO, res_JOONG, res_JONG)

                            dis_JONG = dis_sori(inp_JONG, res_JONG)
                            distance = (dis_CHO + dis_JOONG + dis_JONG)/3
                            # print('초중종:{},{},{} / letter:{} distance:{:.3f}'.\
                                #   format(res_CHO, res_JOONG, res_JONG, res_letter, distance))
                            
                            d_res[res_letter] = distance

                    # "초성 + 중성"인 경우
                    elif len(dec_last) == 3:
                        res_letter = hgtk.letter.compose(res_CHO, res_JOONG)

                        distance = (dis_CHO + dis_JOONG)/2
                        # print('CHO:{}, JOONG:{} / letter:{} distance:{:.3f}'.format(res_CHO, res_JOONG, res_letter, distance))
                        d_res[res_letter] = distance
                i+=1

            d_res = dict(sorted(d_res.items(), key=lambda kv: kv[1]))
            self.l_res_info.append(d_res)
            self.l_res_letters.append(list(d_res.keys()))
#         self.res = self.str_outer(self.l_res_letters[0], self.l_res_letters[1], nb_eumso=5)
        self.res = self.str_outer(self.l_res_info[0], self.l_res_info[1], nb_eumso=nb_eumso)
        
    
    
    

# rhyme = Rhyme()
# d_baleum2vec = rhyme.l_change_CHOJOONG('멀캠')
# # d_baleum2vec = l_change_CHOJOONG('구루')
# time_e = time.time()
# print(time_e-time_i)

# display(rhyme.l_res_info)