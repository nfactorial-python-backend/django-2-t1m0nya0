from django.db import models


class NewsModel(models.Model):
    title = models.CharField(max_length=150)
    news_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def has_comments(self):
        return self.commentmodel_set.exists()


class CommentModel(models.Model):
    news = models.ForeignKey(NewsModel, on_delete=models.CASCADE)
    comment_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
