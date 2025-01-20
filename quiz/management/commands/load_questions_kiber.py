import json
from pathlib import Path
from django.core.management.base import BaseCommand

from core.settings import BASE_DIR
from quiz.models import Question, Option


class Command(BaseCommand):
    """
    shell ga python manage.py load_questions <slug_name> shu ko'rinishda ishlatish kerak
    """

    help = "Load questions and options from the questions_kiber.json file"

    def handle(self, *args, **kwargs):
        try:
            # JSON faylning yo'lini aniqlash
            file_path = Path(BASE_DIR) / "data" / "questions_kiber.json"
            with file_path.open(encoding='utf-8') as file:
                questions_data = json.load(file)

                # Savollarni va variantlarni bazaga yuklash
                for question_data in questions_data:
                    # Savolni yaratish
                    question = Question.objects.create(question_text=question_data["question_text"])

                    # Variantlarni yaratish
                    for option_data in question_data["options"]:
                        Option.objects.create(
                            question=question,
                            option_text=option_data["option_text"],
                            is_correct=option_data["is_correct"]
                        )

                self.stdout.write(self.style.SUCCESS("Questions and options loaded successfully!"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("questions_mta.json file not found."))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Error decoding JSON. Please check the questions_mta.json file."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
