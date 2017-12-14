# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from question.models import *
# Create your views here.

@login_required
def index(request):
    if request.user.is_authenticated() or True:
        uid = request.user.id
        a = UserAnswer.objects.filter(user_id=uid)
        return render(request, 'index.html', {'answers':a})
    else:
        return  HttpResponseRedirect('/micro/')


@login_required
def match(request):
    if request.method == "GET" :
        a = Questions.objects.order_by('?')[:3]
        return render(request, 'answer.html', {'answers':a})
    else:
        uid=request.user.id
    
        a1 = request.POST.get("a1", "")
        a2 = request.POST.get("a2", "")
        a3 = request.POST.get("a3", "")

        na = MatchRequest(user_id = request.user.id, question_id=a1id, answer=a1)
        
        return HttpResponseRedirect('/match/')



