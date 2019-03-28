import os
import sys

from django.http import HttpResponse
from django.shortcuts import render
from golearning import decision
from golearning.dao.babydao import addbaby


def subuser(request):
    context = {}
    context['user'] = 'user1'
    return render(request, 'subuser.html', context)


def getuserinfo(request):
    uname = request.POST.get('uname', '')
    sex = int(request.POST.get('sex', 1))
    age = int(request.POST.get('age', 1))
    fly = int(request.POST.get('fly', 1))

    social = int(request.POST.get('social', 1))
    read = int(request.POST.get('read', 1))
    language = int(request.POST.get('language', 1))
    high = int(request.POST.get('high', 1))
    weight = int(request.POST.get('weight', 1))
    sleep = int(request.POST.get('sleep', 1))
    chinese = int(request.POST.get('chinese', 1))
    math = int(request.POST.get('mathematics', 1))
    english = int(request.POST.get('english', 1))

    user_base = [sex, age, fly]
    user_able = [social, read, language]
    user_body = [high, weight, sleep]
    user_class = [chinese, math, english]
    user_info = [user_able, user_body, user_class]
    new_user = [user_base, user_info]

    print(user_base, user_info)

    chara_style = decision.getCharacter(user_base, user_info)
    # print(chara_style)
    temper_style = decision.getTemperament(user_base, user_info)
    # print(temper_style)
    agelevel = decision.getAgeLevel(user_base, user_info)
    # print(agelevel)

    books = []
    if len(chara_style) > 3 and chara_style[3]:
        # print('1-------------')
        # for b in chara_style[3]: books += '<a href='+str(b[1])+'>'+str(b[0])+'</a>,'
        for b in chara_style[3]:  books.append(b)
    if len(temper_style) > 3 and temper_style[3]:
        for t in temper_style[3]:  books.append(t)
    if len(agelevel) > 1 and agelevel[1]:
        # print('2------------')
        # for a in agelevel[1]: books += '<a href='+str(a[1])+'>'+str(a[0])+'</a>'
        for a in agelevel[1]: books.append(a)

    # books = {'123':['《123》', 'https://123.com'], '456':['<456>', 'http://456.com']}
    # assert False

    chart = ''
    if len(chara_style) > 2 and chara_style[2]:
        for c in chara_style[2]: chart += str(c) + ','
    if len(temper_style) > 2 and temper_style[2]:
        for t in temper_style[2]: chart += str(t)+','
    if len(agelevel) > 0 and agelevel[0]:
        for e in agelevel[0]: chart += str(e) + ','

    # print(books, chart)
    if (len(chara_style) > 0):
        context = {'message': '用户: ' + uname, 'nuser': '年龄：' + str(chara_style[0]) + '阶段', 'character': '标签：' + chart,
                   'booklist': books}
    else:
        context = {'message': '用户: ' + uname, 'nuser': '年龄：' + str(chara_style[0]) + '阶段'}

    # 添加新数据入库
    print(addbaby(uname, new_user))

    return render(request, 'subuser.html', context)
