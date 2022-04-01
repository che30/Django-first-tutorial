from django.shortcuts import  get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question
from django.urls import reverse
from .forms import  QuestionForm
def index(request):
  latest_question_list = Question.objects.order_by('-pub_date')[:5]
  context = {'latest_question_list': latest_question_list}
  return render(request, 'polls/index.html', context)
def results(request, question_id):
  response = "You're looking at the results of question %s."
  return HttpResponse(response % question_id)
def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
  else:
    selected_choice.votes += 1
    selected_choice.save()
  return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
def detail(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'polls/detail.html', {'question': question})
def add_question(request):
  submitted = False
  if request.method == 'POST':
    form = QuestionForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/polls/add_question?submitted=True')
  else:
    form = QuestionForm
    if 'submitted' in request.GET:
      submitted = True
  return render(request, 'polls/add_question.html',{'form':form, 'submitted': submitted})
# Create your views here.
