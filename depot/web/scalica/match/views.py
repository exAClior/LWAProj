# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from question.models import *
# Create your views here.

@login_required
def match(request):
    if request.user.is_authenticated() or True:
        uid = request.user.id
        //rpc call to get the match list
        a = Match
        return render(request, 'match.html', {'users':a})
    else:
        return  HttpResponseRedirect('/micro/')

