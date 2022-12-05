from django.urls import path
from .views import (ArticleView, myCategory, ArticleDetails,  article_details, 
                    Article_Create, Article_Update, Article_Delete, Search_Page,
                    Contact_Us, About_View)
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('', ArticleView.as_view( ), name='homepage'),
    path('create/', Article_Create.as_view( ), name='article_create'),
    path('about/', About_View.as_view( ), name='about_us'),
    path('contact/', Contact_Us.as_view(), name='contact_us'),
    path('search/', Search_Page.as_view(), name='search_page'),
    path('<slug:slug>/', article_details, name='blog_details'),
    path('update/<slug:slug>/', Article_Update.as_view(), name='blog_update'),
    path('delete/<slug:slug>/', Article_Delete.as_view(), name='blog_delete'),
    path('category/<slug:slug>/', myCategory, name='cathegories'),
    path('tags/<slug:tag_slug>/', ArticleView.as_view(), name='article_tags'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)