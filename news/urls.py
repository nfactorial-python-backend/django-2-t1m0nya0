from django.urls import path
from . import views
app_name = "news"
urlpatterns = [
    path('',views.news,name="news"),
    path('post/',views.post_news,name="post_news"),
    path('<int:news_id>/',views.detail,name="detail"),
    path('<int:news_id>/update/',views.UpdateNews.as_view(),name="update")
]