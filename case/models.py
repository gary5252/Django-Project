from django.db import models
from django.db.models.deletion import SET_NULL, CASCADE
from user.models import Profile, Respondent
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    createdon = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    createdon = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Amount(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    createdon = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Mode(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    createdon = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Period(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    createdon = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Case(models.Model):
    # CASCADE: 一旦所屬 Profile 遭到刪除，此整筆資料會同時刪除
    owner = models.ForeignKey(Profile, on_delete=CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    contact = models.CharField(max_length=100)
    skill = models.TextField(null=True, blank=True)
    createdon = models.DateTimeField(auto_now_add=True)
    view = models.IntegerField(default=0)

    category = models.ForeignKey(Category, null=True, on_delete=SET_NULL)
    amount = models.ForeignKey(Amount, null=True, on_delete=SET_NULL)
    period = models.ForeignKey(Period, null=True, on_delete=SET_NULL)
    respondent = models.ManyToManyField(Respondent)
    state = models.ForeignKey(State, null=True, on_delete=SET_NULL)
    mode = models.ManyToManyField(Mode)

    # 倒排序 越新發布的資料排越上面
    class Meta:
        ordering = ['-createdon']

    def __str__(self):
        return self.title
