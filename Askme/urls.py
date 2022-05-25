from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="new"),

    path('ask/', views.ask, name="ask"),

    path('hot/', views.hot, name="hot"),

    path('question/<int:question_id>', views.question, name="question"),

    path('signup/', views.signup, name="signup"),

    path('login/', views.login, name="login"),

    path('profile/edit/', views.user_settings, name="user_settings"),

    path('tag/<str:tag>/', views.tag, name="tag"),

    path('logout', views.logout_view, name="logout"),

    path('like_question/', views.like_question, name="like_question"),
    path('dislike_question/', views.dislike_question, name="dislike_question"),

    path('like_answer/', views.like_answer, name="like_answer"),
    path('dislike_answer/', views.dislike_answer, name="dislike_answer")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
