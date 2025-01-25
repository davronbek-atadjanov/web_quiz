from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class Subject(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Question(models.Model):
    subject = models.ForeignKey(Subject, related_name='questions', on_delete=models.CASCADE)
    question_text = RichTextField()

    def __str__(self):
        return self.question_text

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    option_text = RichTextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text