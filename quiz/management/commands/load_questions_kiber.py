import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.shortcuts import  get_object_or_404
from core.settings import BASE_DIR
from quiz.models import Question, Option
from quiz.models import Subject

class Command(BaseCommand):
    help = "Load questions and options from the questions.json file and link to subject via slug"

    def add_arguments(self, parser):
        parser.add_argument('slug', type=str, help="The slug of the subject to link questions to")

    def handle(self, *args, **kwargs):
        slug = kwargs['slug']  # slugni buyruqdan olish
        print(slug)
        try:
            # Fanni slug orqali topish
            subject = get_object_or_404(Subject, slug=slug)

            # JSON faylning yo'lini aniqlash
            file_path = Path(BASE_DIR) / "data" / "questions_kiber.json"
            with file_path.open(encoding='utf-8') as file:
                questions_data = json.load(file)

                # Savollarni va variantlarni bazaga yuklash
                for question_data in questions_data:
                    # Savolni yaratish va subjectni bog'lash
                    question = Question.objects.create(subject=subject, question_text=question_data["question_text"])

                    # Variantlarni yaratish
                    for option_data in question_data["options"]:
                        Option.objects.create(
                            question=question,
                            option_text=option_data["option_text"],
                            is_correct=option_data["is_correct"]
                        )

                self.stdout.write(
                    self.style.SUCCESS(f"Questions and options loaded successfully for subject: {subject.name}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
