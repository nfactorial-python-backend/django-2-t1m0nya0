from django.test import TestCase
from .models import NewsModel,CommentModel
from django.urls import reverse


class NewsModelTest(TestCase):
    def test_has_comments_true(self):
        news = NewsModel.objects.create(title="Test 1",news_content="Test which return True")
        comment = CommentModel.objects.create(news=news,comment_content="True")
        comment.save()

        response = self.client.get(reverse("news:detail",args=(news.id, )))
        self.assertEqual(200,response.status_code)
        self.assertTrue(news.has_comments())

    def test_has_comments_false(self):
        news = NewsModel.objects.create(title="Test 1",news_content="Test which return True")

        response = self.client.get(reverse("news:detail",args=(news.id, )))
        self.assertEqual(200,response.status_code)
        self.assertFalse(news.has_comments())


class NewsViewTest(TestCase):
    def test_get_news_list_is_order(self):
        for count in range(1,5):
            news = NewsModel(title=f"news {count}",news_content=f"Is my {count} content")
            news.save()
        response = self.client.get(reverse("news:news"))
        self.assertEqual(200,response.status_code)
        self.assertQuerySetEqual(NewsModel.objects.order_by("-created_at").all(),response.context["all_news"])

    def test_check_detail_news(self):
        news = NewsModel.objects.create(title="Check Detail",news_content="do U check me?")
        response = self.client.get(reverse("news:detail",args=(news.id,)))
        self.assertEqual(200,response.status_code)
        self.assertEqual("Check Detail",response.context["news_db"].title)
        self.assertEqual("do U check me?",response.context["news_db"].news_content)

    def test_comment_exists_and_ordered(self):
        news = NewsModel.objects.create(title="This is news for comment exists",news_content="Yes it's ok")
        comment1 = CommentModel.objects.create(news=news,comment_content="This is 1 comment, but is should place 2 th")
        comment2 = CommentModel.objects.create(news=news,comment_content="This is 2 comment, but is should place 1 th")
        response = self.client.get(reverse("news:detail",args=(news.id, )))
        self.assertEqual(response.status_code, 200)
        comments = response.context['comments']
        comment_dates = [comment.created_at for comment in comments]
        self.assertGreater(comment_dates[0],
                           comment_dates[1])
        self.assertEqual(comments[0], comment2)
        self.assertEqual(comments[1],comment1)







