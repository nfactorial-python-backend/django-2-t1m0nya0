from django.shortcuts import render, reverse, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from .models import NewsModel, CommentModel
from .forms import NewsForm
from django.views import View


def news(request):
    all_news = NewsModel.objects.order_by('-created_at').all()
    context = {"all_news": all_news}
    return render(request, "news/news.html", context)


def detail(request, news_id):
    if request.method == "POST":
        comment_content = request.POST["comment"]
        comment = CommentModel(news_id=news_id, comment_content=comment_content)
        comment.save()
        return redirect(reverse('news:detail', args=(news_id,)))
    news_db = get_object_or_404(NewsModel, pk=news_id)
    comments = CommentModel.objects.filter(news=news_db).order_by("-created_at").all()
    context = {"news_db": news_db, "comments": comments}
    return render(request, "news/detail.html", context)


class UpdateNews(View):
    template_name = "news/change.html"

    def get(self, request, news_id):
        news_db = get_object_or_404(NewsModel, pk=news_id)
        form = NewsForm(instance=news_db)
        return render(request, self.template_name, {"news_db": news_db, "form": form})

    def post(self, request, news_id):
        news_db = get_object_or_404(NewsModel, pk=news_id)
        form = NewsForm(request.POST, instance=news_db)
        if form.is_valid():
            form.save()
            return redirect(reverse("news:detail", args=(news_id,)))
        return render(request, self.template_name, {"news_db": news_db, "form": form})


def post_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            news_save = form.save()
            news_save.save()
            return HttpResponseRedirect(reverse("news:detail", args=[news_save.id, ]))
    else:
        form = NewsForm(request.POST)
    return render(request, "news/post.html", {"form": form})
