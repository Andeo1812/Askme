import django.contrib.auth.models
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.utils import timezone


class TagManager(models.Manager):
    def top_tags(self, count=9):
        return self.annotate(count=Count('tag_related')).order_by('-count')[:count]


class AnswerManager(models.Manager):
    def hot(self):
        res = self.annotate(likes=Sum('answer_like__mark_l')).order_by('-likes').exclude(likes=None)
        if res.count() < 3:
            res = self.annotate(likes=Sum('answer_like__mark_l')).order_by('-likes')
        return res

    def answer_by_question(self, id):
        return self.annotate(likes=Sum('answer_like__mark_l')).order_by('-likes').filter(question_id=id)


class QuestionManager(models.Manager):
    def count_answers(self):
        return self.annotate(answers=Count('answer_related', distinct=True))

    def count_likes(self):
        res = self.count_answers().annotate(likes=Sum('question_like__mark_l')).order_by('-likes').exclude(likes=None)
        if res.count() < 3:
            res = self.count_answers().annotate(likes=Sum('question_like__mark_l')).order_by('-likes')
        return res

    def get_by_id(self, id):
        return self.count_likes().get(id=id)

    def by_tag(self, tag):
        return self.count_answers().filter(tags__name=tag)

    def new(self):
        return self.count_likes().order_by('-pub_date')

    def hot(self):
        return self.count_likes()



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
    views = models.IntegerField(default=0)

    title = models.CharField(max_length=255)

    text = models.TextField()

    pub_date = models.DateTimeField(default=timezone.now)

    rating = models.IntegerField(verbose_name="question_rating", default=0)

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    tags = models.ManyToManyField(Tag, related_name='tag_related')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ['-pub_date']


class Answer(models.Model):
    views = models.IntegerField(default=0)

    text = models.TextField()

    pub_date = models.DateTimeField(auto_now_add=True)

    correct = models.BooleanField(default=False)

    profile = models.ForeignKey(Profile, related_name='profile_related', on_delete=models.CASCADE)

    question = models.ForeignKey(Question, related_name='answer_related', on_delete=models.CASCADE)

    tags = models.ManyToManyField(Tag, related_name='tag_related_a')

    objects = AnswerManager()

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        ordering = ['-pub_date']


class LikeQuestion(models.Model):
    LIKE = '1'
    DISLIKE = '-1'

    MARK_L = [
        (LIKE, 'Like'),
        (DISLIKE, 'UnLike'),
    ]
    MARK_D = [
        (LIKE, 'DisLike'),
        (DISLIKE, 'UnDislike')
    ]

    mark_l = models.IntegerField(choices=MARK_L, blank=True, null=True)

    mark_d = models.IntegerField(choices=MARK_D, blank=True, null=True)

    question = models.ForeignKey(Question, related_name="question_like", on_delete=models.CASCADE)

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    pub_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'app_like_question'
        verbose_name = 'Like_question'
        verbose_name_plural = 'Likes_questions'


class LikeAnswer(models.Model):
    LIKE = '1'
    DISLIKE = '-1'

    MARK_L = [
        (LIKE, 'Like'),
        (DISLIKE, 'UnLike'),
    ]
    MARK_D = [
        (LIKE, 'DisLike'),
        (DISLIKE, 'UnDislike')
    ]

    mark_l = models.IntegerField(choices=MARK_L, blank=True, null=True)

    mark_d = models.IntegerField(choices=MARK_D, blank=True, null=True)

    answer = models.ForeignKey(Answer, related_name="answer_like", on_delete=models.CASCADE)

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    pub_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'app_like_answer'
        verbose_name = 'Like_answer'
        verbose_name_plural = 'Likes_answers'
