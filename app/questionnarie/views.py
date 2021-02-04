from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Question, Questionnaire, Answer, MultiChoiceAnswer

def index(request):
    latest_questionnaire_list = Questionnaire.objects.order_by('-pub_date')[:5]
    template = loader.get_template('test/index.html')
    context = {
        'latest_questionnaire_list': latest_questionnaire_list
    }
    return HttpResponse(template.render(context,request))

def detail (request):
    latest_question_list = Question.objects.all()
    template = loader.get_template('test/detail.html')
    context = {
        'latest_question_list': latest_question_list
    }
    return HttpResponse(template.render(context, request))

def results (request):
    questionnaire_instance = Answer.objects.get(taker=request.user)
    answer_instance = MultiChoiceAnswer.objects.all()

    if request.method == 'POST':
       questionnaire_instance.C1_score=+ answer_instance.values_list('C1',flat=True)[selected answer]