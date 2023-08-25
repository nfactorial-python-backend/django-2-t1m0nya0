from django.shortcuts import render, reverse, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import NewsModel, CommentModel
from django.contrib.auth import login
from .forms import NewsForm, SignUpForm
from django.utils.decorators import method_decorator
from django.views import View


def news(request):
    all_news = NewsModel.objects.order_by('-created_at').all()
    context = {"all_news": all_news}
    return render(request, "news/news.html", context)


def detail(request, news_id):
    if request.method == "POST":
        comment_content = request.POST["comment"]
        comment = CommentModel(news_id=news_id, comment_content=comment_content, user=request.user)
        comment.save()
        return redirect(reverse('news:detail', args=(news_id,)))
    news_db = get_object_or_404(NewsModel, pk=news_id)
    comments = CommentModel.objects.filter(news=news_db).order_by("-created_at").all()
    context = {"news_db": news_db, "comments": comments}
    return render(request, "news/detail.html", context)


class UpdateNews(View):
    template_name = "news/change.html"

    @method_decorator(login_required(login_url="/login/"))
    def get(self, request, news_id):
        news_db = get_object_or_404(NewsModel, pk=news_id)
        form = NewsForm(instance=news_db)
        return render(request, self.template_name, {"news_db": news_db, "form": form})

    @method_decorator(permission_required("news.change_newsmodel", login_url="/login/"))
    def post(self, request, news_id):
        news_db = get_object_or_404(NewsModel, pk=news_id)
        form = NewsForm(request.POST, instance=news_db)
        if form.is_valid():
            update = form.save()
            update.save()
            return redirect(reverse("news:detail", args=(news_id,)))
        return render(request, self.template_name, {"news_db": news_db, "form": form})


@login_required
def post_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            news_save = form.save(commit=False)
            news_save.user = request.user
            news_save.save()
            return HttpResponseRedirect(reverse("news:detail", args=[news_save.id, ]))
    else:
        form = NewsForm(request.POST)
    return render(request, "news/post.html", {"form": form})


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/news')
    else:
        form = SignUpForm()

    return render(request, 'registration/sign_up.html', {"form": form})


@permission_required('news.delete_newsmodel')
def delete_news(request, news_id):
    news_db = get_object_or_404(NewsModel, pk=news_id)
    if request.user == news_db.user:
        news_db.delete()
    return redirect('news:news')


@permission_required('news.delete_commentmodel')
def delete_comment(request, comment_id):
    comment = get_object_or_404(CommentModel, pk=comment_id)
    news_id = comment.news.id
    if request.user == comment.user:
        comment.delete()
    return redirect('news:detail', news_id=news_id)
