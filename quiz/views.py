# views.py
from django.shortcuts import render, redirect
from .models import Question, Option
from django.http import HttpResponse, JsonResponse


def question_list(request):
    # 25 ta random savol olish
    questions = Question.objects.all().order_by('?')[:15]
    context = {
        'questions': questions
    }
    return render(request, 'questions/question_list.html', context)


def submit_answers(request):
    if request.method == 'POST':
        correct_answers = 0
        total_questions = 0

        questions = Question.objects.all()

        for question in questions:
            user_answer = request.POST.get(f'question_{question.id}')
            if user_answer:
                total_questions += 1
                selected_option_id = int(user_answer)

                correct_option = question.options.filter(is_correct=True).first()
                if correct_option and correct_option.id == selected_option_id:
                    correct_answers += 1

        if total_questions != 0:
            score = (correct_answers / 15) * 100
        else:
            score = 0

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
