from django.shortcuts import render
import hgtk
from .NLPengine import gen_rhyme
import time

# Create your views here.
def home(request):
    return render(request, 'main/index.html')

def func01(request, dj_param01):
    print(dj_param01*5)
    var_01 = list(range(int(dj_param01)))
    # var_01 = [1, 2, 3, 4, 5]
    return render(request, 'main/index.html', {'k_var_01':var_01})

def func02(request, djvar_02):
    print(request)
    vwvar_20 = hgtk.text.decompose(djvar_02)
    print('func02')
    return render(request, 'main/index.html', 
            {'k_vwvar_20':vwvar_20,})

def func_rhyme(request, djvar_03):
    time_i = time.time()
    
    rhyme = gen_rhyme.Rhyme()
    print(djvar_03)
    rhyme.l_change_CHOJOONG(djvar_03, nb_eumso=8)

    time_e = time.time()
    print('func_rhyme elpased time:', time_e-time_i)
    
    vwvar_rhyme_01 = rhyme.res[:]
    # print(rhyme.l_res_info)
    # print(gen_rhyme.d_oft_JONG_sori)
    return render(request, 'main/index.html', 
            {'k_vwvar_rhyme_01':vwvar_rhyme_01,})

def func03(request):
    text_area_content = request.args.get('text_name')

    return render(request, 'main/index.html', 
            {'k_vwvar_func03':text_area_content,})