from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        QuestionLike.objects.all().delete()
        AnswerLike.objects.all().delete()
        Answer.objects.all().delete()
        Question.objects.all().delete()
        Tag.objects.all().delete()
        Profile.objects.all().delete()
        users = User.objects.all()
        users.filter(is_superuser=False).delete()
        print("Deleted all data")
