from django.core.checks import Tags
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Avg

from app.models import *
import random
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        ratio = options.get('ratio')
        users = []
        profiles = []
        tags = []
        questions = []
        answers = []
        questions_likes = []
        answer_likes = []

        # Users and Profiles
        for i in range(ratio):
            random_image_number = random.randint(1, 6)
            if random_image_number != 4:
                image_path = f'avatar{random_image_number}.jpg'
            else:
                image_path = None
            user = User(username=f'user{i}', email=fake.email(), password='12345678')
            users.append(user)
            profiles.append(Profile(user=user, name=fake.name(),
                                    avatar=image_path))
        User.objects.bulk_create(users)
        Profile.objects.bulk_create(profiles)
        print('User and Profile data created')

        # Tags
        for i in range(ratio):
            name = fake.word()
            if not any(tag.name == name for tag in tags):
                tags.append(Tag(name=name))
        Tag.objects.bulk_create(tags)
        print('Tags data created')

        # Questions
        for i in range(ratio * 10):
            question = Question(title=fake.word(), content=fake.text(max_nb_chars=100),
                                user=random.choice(users))
            questions.append(question)
        Question.objects.bulk_create(questions)

        created_questions = Question.objects.all()
        for question in created_questions:
            tags_set = random.sample(tags, 3)
            question.tags.set(tags_set)
        print('Question data created')

        # Answers
        for i in range(ratio * 100):
            answers.append(Answer(user=random.choice(users), question=random.choice(created_questions),
                                  content=fake.text(max_nb_chars=100)))
        Answer.objects.bulk_create(answers)
        print('Answer data created')

        # Likes
        users = list(User.objects.all())
        questions = list(Question.objects.all())
        answers = list(Answer.objects.all())

        for i in range(ratio):
            user = users[i]
            question = questions[i]
            like = QuestionLike(user=user, question=question)
            questions_likes.append(like)

        for i in range(ratio):
            user = users[i]
            for j in range(2):
                answer = answers[j]
                like = AnswerLike(user=user, answer=answer)
                answer_likes.append(like)
        QuestionLike.objects.bulk_create(questions_likes)
        AnswerLike.objects.bulk_create(answer_likes)
        print('QuestionLike and AnswerLike data created')

        # updating rating
        profiles = Profile.objects.all()
        for profile in profiles:
            rating = Question.objects.filter(user=profile.user).count() + Answer.objects.filter(
                user=profile.user).count()
            profile.rating = rating
        Profile.objects.bulk_update(profiles, ['rating'])
        print('Profile rating updated')

        questions = Question.objects.all()
        for question in questions:
            question.rating = QuestionLike.objects.filter(question=question).count()
        Question.objects.bulk_update(questions, ['rating'])
        print('Question rating updated')

        answers = Answer.objects.all()
        for answer in answers:
            answer.rating = AnswerLike.objects.filter(answer=answer).count()
        Answer.objects.bulk_update(answers, ['rating'])
        print('Answer rating updated')

        print('all data created')
