from django.db import models
from django.contrib.auth.models import User


class NewsModel(models.Model):
    title = models.CharField(max_length=150)
    news_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def has_comments(self):
        return self.commentmodel_set.exists()


class CommentModel(models.Model):
    news = models.ForeignKey(NewsModel, on_delete=models.CASCADE)
    comment_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
