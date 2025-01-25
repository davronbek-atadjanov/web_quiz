from random import sample
from django.views.generic import ListView
from .models import Subject

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Option
from django.http import HttpResponse, JsonResponse

def subject_list(request):
        subjects = Subject.objects.all()

        context = {
            "subjects": subjects
        }
        return render(request, 'questions/subject_list.html', context)

def question_list(request, slug):
    if slug == "mta":
        quiz_count = 15
    else:
        quiz_count = 25
    subject = get_object_or_404(Subject, slug=slug)
    question_ids = list(Question.objects.filter(subject=subject).values_list('id', flat=True))
    random_ids = sample(question_ids, min(len(question_ids), quiz_count))
    questions = Question.objects.filter(id__in=random_ids)
    print(type(questions))
    context = {
        'questions': questions,
        'selected_subject': slug,
        'subject_name': subject.name,
    }
    return render(request, 'questions/question_list.html', context)

def submit_answers(request, slug):
    if slug == "mta":
        quiz_count = 15
    else:
        quiz_count = 25

    if request.method == 'POST':
        correct_answers = 0
        incorrect_answers_details = []
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
            if correct_dict.get(question_id) == selected_option_id:
                correct_answers += 1
            else:
                question = Question.objects.get(id=question_id)
                correct_option = Option.objects.get(question_id=question_id, is_correct=True)
                selected_option = Option.objects.get(id=selected_option_id)
                incorrect_answers_details.append({
                    'question': question.question_text,
                    'selected_option': selected_option.option_text,
                    'correct_option': correct_option.option_text
                })

        score = round((correct_answers / quiz_count) * 100, 2)

        request.session['correct_answers'] = correct_answers
        request.session['score'] = score
        request.session['incorrect_answers_details'] = incorrect_answers_details

        return redirect('result-view', slug=slug)

    return JsonResponse({"error": "Faqat POST so'rovi qabul qilinadi!"}, status=405)
def result_view(request, slug):
    if slug == "mta":
        quiz_count = 15
    else:
        quiz_count = 25

    all_questions = []
    question_ids = list(Question.objects.filter(subject__slug=slug).values_list('id', flat=True))
    user_answers = request.session.get('user_answers', {})
    correct_options = Option.objects.filter(
        Q(question_id__in=question_ids) & Q(is_correct=True)
    ).values('question_id', 'id')

    correct_dict = {opt['question_id']: opt['id'] for opt in correct_options}

    for question_id in question_ids:
        question = Question.objects.get(id=question_id)
        correct_option = Option.objects.get(question_id=question_id, is_correct=True).option_text
        selected_option_id = user_answers.get(question_id)
        selected_option = Option.objects.get(id=selected_option_id).option_text if selected_option_id else None
        all_questions.append({
            'text': question.question_text,
            'selected_option': selected_option,
            'correct_option': correct_option,
            'correct': correct_dict.get(question_id) == selected_option_id
        })

    context = {
        'total_questions': quiz_count,
        'correct_answers': request.session.get('correct_answers', 0),
        'incorrect_answers': quiz_count - request.session.get('correct_answers', 0),
        'score': request.session.get('score', 0),
        'all_questions': all_questions,
        'slug': slug,
    }
    return render(request, 'questions/result.html', context)
