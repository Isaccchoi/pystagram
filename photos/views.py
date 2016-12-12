import os
import logging

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.http import HttpResponsePermanentRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import PermissionDenied
from django.core import serializers
from django.conf import settings
from django.db import transaction
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from rest_framework import serializers as drf_serializers
from rest_framework import viewsets

from .models import Post
from .models import Tag
from .models import Comment
from .models import Like
from .forms import PostForm
from .forms import CommentForm
from pystagram.sample_exceptions import HelloWorldError


logger = logging.getLogger('django')
formatter = logging.Formatter('%(asctime)s- %(name)s - %(levelname)s - %(message)s')

import base64


def get_base64_image(data):
    if data is None or ';base64,' not in data:
        return None

    _format, _content = data.split(';base64,')
    return base64.b64decode(_content)


@login_required
def create_post(request):
    if request.method == 'GET':
        form = PostForm()
    elif request.method == 'POST':
        filtered = request.POST.get('filtered_image')
        if filtered:
            filtered_image = get_base64_image(filtered)
            filename = request.FILES['image'].name.split(os.sep)[-1]
            _filedata = {
                'image': SimpleUploadedFile(
                    filename, filtered_image
                )
            }
        else:
            _filedata = request.FILES

        form = PostForm(request.POST, _filedata)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            tag_text = form.cleaned_data.get('tagtext', '')
            tags = tag_text.split(',')
            for _tag in tags:
                _tag = _tag.strip()
                tag, _ = Tag.objects.get_or_create(name=_tag, defaults={'name': _tag})
                post.tags.add(tag)

            return redirect('photos:view', pk=post.pk)

    ctx = {
        'form': form,
    }
    return render(request, 'edit_post.html', ctx)


#class PostCreateView(CreateView):
#    model = Post
#    form_class = PostForm
#    template_name = 'edit_post.html'


#create_post = PostCreateView.as_view()



def list_posts(request):
#    logger.warning("경고 경고")
#    raise HelloWorldError("뭔가 문제가 있다")
    page = request.GET.get('page', 1)
    per_page = 2

    posts = Post.objects\
                    .all()\
    #                .order_by('-created_at', '-pk')
    # Model에 Meta클래스에 ordering항목으로 대체할 수 있음

    pg = Paginator(posts, per_page)
    try:
        contents = pg.page(page)
    except PageNotAnInteger:
        contents = pg.page(1)
    except EmptyPage:
        contents = []

    # unique값이 없기 때문에 같은 시간에 값이 입력이 될 수 있음
    # 똑같은 값의 데이터가 있을때의 2번째의 인자인 pk값으로 차순위 정렬이 됨
    if request.is_ajax():
        data = serializers.serialize('json', contents)
        return HttpResponse(data)

    ctx = {
        'posts': contents,
        }

    return render(request, 'list.html', ctx)

#class PostListView(ListView):
#    model = Post
#    context_object_name = 'posts'
#    template_name = 'list.html'
#    paginate_by = 2
    # queryset = Post.objects.all().order_by('-created_at')

#    def get_queryset(self):
#        return Post.objects.order_by('-created_at')

#list_posts = PostListView.as_view()

@login_required
#@cache_page(60 * 5)
def view_post(request, pk):
    key = 'post_object_{}'.format(pk)
    post =cache.get(key)
    if not post:
        post = Post.objects.get(pk=pk)
        cache.set(key, post, 300)
        print('get data form db')
    else:
        print('get cached data')
    #post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    if request.method == "GET":
        form = CommentForm()
    elif request.method == "POST":
        if not request.user.is_authenticated():
            return redirect(settings.LOGIN_URL)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect(post)# Post모델의 'get_absolute_url()'메서드를 호출해서 가능


    ctx = {
        'post':post,
        'comment_form': form
    }
    return render(request, 'view.html', ctx)

@login_required
def delete_post(request, pk):
#    if request.method != "POST" and not request.user.id == Post.objects.get(pk=pk).user.pk:
#        return redirect(settings.LOGIN_URL)
    #print()
    #print(Post.objects.get(pk=pk).user.id)
    #if not request.user.is_authenticated:
        #return redirect(settings.LOGIN_URL)
#    print("owner",post_owner)
#    print("request_user",request.user)
    if request.method =="GET":
        return render(request, "bad_request.html")
    else:
        if not request.user == Post.objects.get(id=pk).user:
        #or not request.user.id == Post.objects.get(pk=pk).user.id:
            raise PermissionDenied
        else:
            post = get_object_or_404(Post, pk=pk)
            post.delete()

            #return HttpResponsePermanentRedirect('photos:list')
            #return render(request, 'list.html', status=302)
            return redirect('photos:list')
    #else:
        #return render(request, 'notgoodget.html')


def delete_comment(request, pk):
    if request.method != "POST":
        return HttpResponseBadRequest()
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()

    return redirect(comment.post)


def temp(request):
    return redirect('photos:list')

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method != "POST":
        raise Exception('bad request')

    qs = post.like_set.filter(user=request.user)
    if qs.exists():
        like = qs.get()
        like.delete()
    else:
        like = Like()
        like.post = post
        like.user = request.user
        like.save()

    return redirect(post)


class PostSerializer(drf_serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('image', 'content', )
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
