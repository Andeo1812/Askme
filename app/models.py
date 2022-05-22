import django.contrib.auth.models
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.utils import timezone


class TagManager(models.Manager):
    def top_tags(self, count=9):
        return self.annotate(count=Count('tag_related')).order_by('-count')[:count]


class AnswerManager(models.Manager):
    def count_likes(self):
        return self.annotate(Count("likes"))

    def hot(self):
        return self.order_by('-likes')

    def answer_by_question(self, id):
        return self.filter(question__id=id)


class QuestionManager(models.Manager):
    def get_by_id(self, id):
        return self.get(id=id)

    def count_likes(self, id):
        return self.get(id=id).get_likes()

    def by_tag(self, tag):
        return self.filter(tags__name=tag)

    def new(self):
        return self.order_by('-pub_date')

    def hot(self):
        return self.order_by('-likes')



class ProfileManager(models.Manager):
    def get_top_users(self, count=5):
        return self.annotate(answers=Count('profile_related')).order_by('-answers')[:count]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="", default='static/img/1.png')

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class Tag(models.Model):
    name = models.CharField(max_length=32)
    objects = TagManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = 'Tags'


class Question(models.Model):
    title = models.CharField(max_length=256)

    views = models.IntegerField(default=0)

    likes = models.IntegerField(default=0)

    dislikes = models.IntegerField(default=0)

    text = models.TextField()

    pub_date = models.DateTimeField(default=timezone.now)

    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    tags = models.ManyToManyField(Tag, related_name='tag_related')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def get_likes(self):
        return '%d' % (self.likes)

    def answers(self):
        return '%d' % (Answer.objects.filter(question_id=self.id)).count()

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ['-pub_date']


class Answer(models.Model):
    views = models.IntegerField(default=0)

    likes = models.IntegerField(default=0)

    dislikes = models.IntegerField(default=0)

    text = models.TextField()

    pub_date = models.DateTimeField(auto_now_add=True)

    correct = models.BooleanField(default=False)

    author = models.ForeignKey(Profile, related_name='profile_related', on_delete=models.CASCADE)

    tags = models.ManyToManyField(Tag, related_name='tag_related_a')

    question = models.ForeignKey(Question, related_name='answer_related', on_delete=models.CASCADE)

    objects = AnswerManager()

    def __str__(self):
        return '%s' % (self.author.user.username)

    def get_likes(self):
        return self.likes

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        ordering = ['-pub_date']
