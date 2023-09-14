from django.shortcuts import get_object_or_404, render
from .models import Question, Choice
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def index(request):
    latest_question=Question.objects.all().order_by('-pub_date')[:5]
    context={'latest_question':latest_question}
    return render(request,'polls/index.html',context)

def detail (request, question_id):
    question=get_object_or_404(Question,pk=question_id)
    return render(request,'polls/detail.html',{'question':question})

def results (request, question_id):
    question=get_object_or_404(Question,pk=question_id)
    return render(request,'polls/results.html',{'question':question})
    

def vote (request, question_id):
   question=get_object_or_404(Question,pk=question_id)
   try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
   except (KeyError, Choice.DoesNotExist):
        return render(request,'polls/detail.html',{'question':question,'error_message':"you didn't select a choice"})
   else:
        selected_choice.votes+=1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))
