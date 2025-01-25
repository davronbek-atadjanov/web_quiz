from django.contrib import admin
from .models import Option, Question, Subject



class OptionInline(admin.TabularInline):
    model = Option
    extra = 1
class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]


admin.site.register(Subject)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)
