from __future__ import unicode_literals

from _cffi_backend import typeof

from django.shortcuts import render
from golearning.dao import analysisdao
from golearning import decision
import golearning.match_user as ps
import decimal


def character(request):
    chara_age = request.POST.get('cage', 0)
    chara_ns = request.POST.getlist('NS', [])
    chara_ha = request.POST.getlist('HA', [])
    chara_rd = request.POST.getlist('RD', [])
    chara_ps = request.POST.getlist('PS', [])
    chara_sd = request.POST.getlist('SD', [])
    chara_co = request.POST.getlist('CO', [])
    chara_st = request.POST.getlist('ST', [])
    chara_em = request.POST.get('emotion', '')

    chara_list = {'NS': chara_ns, 'HA': chara_ha, 'RD': chara_rd, 'PS': chara_ps, 'SD': chara_sd, 'CO': chara_co, 'ST': chara_st}
    character_mix = []
    t_books = []
    chara_max, chara_min = '', ''
    for key, c in chara_list.items():
        score = 0
        if len(c):
            for v in c:
                score += int(v)
            if len(character_mix):
                # print(score, max(character_mix), min(character_mix))
                if score > max(character_mix):
                    chara_max = key
                elif score < min(character_mix):
                    chara_min = key
            else:
                chara_max = key
                chara_min = key
        character_mix.append(score)

    #获取年龄段
    if not chara_age:
        chara_age = 0
    pu=ps.new_user([1, int(float(chara_age)), 1], [[], [], []])
    new_user_level=pu.new_user_level


    # 获取年龄轴
    child_age = decimal.Decimal(chara_age)

    getmaxbooks = decision.getBooklist(new_user_level, decision.getKeywords(chara_max))
    for b in getmaxbooks: t_books.append(b)
    getminbooks = decision.getBooklist(new_user_level, decision.getKeywords(chara_min))
    for b in getminbooks: t_books.append(b)
    getembooks = decision.getBooklist(new_user_level, decision.getKeywords(chara_em))
    for b in getembooks: t_books.append(b)
    getcbooks=decision.getBooklist(new_user_level, decision.getKeywords(child_age))
    for b in getcbooks: t_books.append(b)

    # print(child_age, child_age.__class__, decision.getKeywords(child_age), getcbooks)
    print(new_user_level,decision.getKeywords(chara_em), getembooks)
    # print(new_user_level, decision.getKeywords(chara_max), decision.getKeywords(chara_min))

    # 列有去重
    tt_books=[]
    for book in t_books:
        if book not in tt_books:
            tt_books.append(book)

    print(analysisdao.save_character(character_mix))
    context = {'scores': character_mix, 'max': chara_max, 'min': chara_min, 'booklist': tt_books}

    return render(request, 'child_analysis.html', context)
