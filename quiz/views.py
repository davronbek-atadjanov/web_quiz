from random import sample

from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Question, Option
from django.http import HttpResponse, JsonResponse


def question_list(request):
    question_ids = list(Question.objects.values_list('id', flat=True))
    random_ids = sample(question_ids, min(len(question_ids), 15))
    questions = Question.objects.filter(id__in=random_ids)

    context = {
        'questions': questions
    }
    return render(request, 'questions/question_list.html', context)

def submit_answers(request):
    if request.method == 'POST':
        correct_answers = 0
        total_questions = 0

        user_answers = {
            int(key.split('_')[1]): int(value)
            for key, value in request.POST.items() if key.startswith('question_')
        }
        question_ids = user_answers.keys()

        correct_options = Option.objects.filter(
            Q(question_id__in=question_ids) & Q(is_correct=True)
        ).values('question_id', 'id')

        correct_dict = {opt['question_id']: opt['id'] for opt in correct_options}

        for question_id, selected_option_id in user_answers.items():
            total_questions += 1
            if correct_dict.get(question_id) == selected_option_id:
                correct_answers += 1

        score = (correct_answers / 15) * 100 if total_questions != 0 else 0

        request.session['total_questions'] = total_questions
        request.session['correct_answers'] = correct_answers
        request.session['score'] = score

        return redirect('result-view')

    return JsonResponse({"error": "Faqat POST so'rovi qabul qilinadi!"}, status=405)

def result_view(request):
    total_questions = request.session.get('total_questions')
    correct_answers = request.session.get('correct_answers')
    score = request.session.get('score')

    incorrect_answers = 15 - correct_answers
    context = {
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'score': score
    }
    return render(request, 'questions/result.html', context)
