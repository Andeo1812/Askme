from django.contrib import admin
from django.urls import path

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

    path('logout', views.logout_view, name="logout")
]
