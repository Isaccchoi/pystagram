from django.db import models
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=40)
    parent = models.ForeignKey('self', null=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False)
    category = models.ForeignKey(Category, null=True, blank=True)
    title = models.CharField(max_length=50, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to='%Y/%m/%d/', null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    # Tag모델 자체가 밑에서 선언되어 NameError 발생
    # 모델이름을 직접 입력하는데 아닌 모델의 Name Space를 넣어 충돌 방지
    # NameSpace로 넘어갈 경우 모델을 만들며 바로 관계를 맺지 않음
    # 모든 모델을 다 생성 한후 그 이후에 관계를 맺어 충돌을 방지합니다.
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    likes = GenericRelation('Like2')

    class Meta:
        ordering = ['-created_at', '-id']

    def __str__(self):
#        return '{}'.format(self.pk)
        return str(self.pk)

    def get_absolute_url(self):
        return reverse_lazy('photos:view', kwargs={'pk': self.pk})

#    def delete(self, *args, **kwargs):
#        super(Post, self).delete(*args, **kwargs)
#        self.image.delete(save=False)
# QuerySet으로 들어갈 경우[ex) filter ]에는 작동이 안됨 , 때문에 signal이 안전함

    class Meta:
        ordering = ['-updated_at']
        permissions = (("delete_post_perm", "Delete Post"),)

        permissions = (
        ("can_delete_post","delete post"),
        )


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    likes = GenericRelation('Like2')


    class Meta:
        ordering = ['-created_at']

class Tag(models.Model):
    name = models.CharField(max_length= 40)

    def __str__(self):
        return self.name

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    created_at = models.DateTimeField(auto_now_add=True)

class Like2(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
