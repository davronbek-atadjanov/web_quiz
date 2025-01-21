from django.contrib import admin
from .models import Option, Question, Subject

admin.site.register(Subject)
admin.site.register(Question)
admin.site.register(Option)
