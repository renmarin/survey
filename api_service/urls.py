from django.urls import path
from . import views

from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Survey API",
        default_version="v1",
        description="Test description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

app_name = "api_service"

urlpatterns = [
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("questions/", views.QuestionsList.as_view()),
    path("questions/<int:pk>/", views.QuestionDetail.as_view()),
    path("questions/<int:pk>/options/", views.OptionsList.as_view()),
    path(
        "questions/<int:question_pk>/options/<int:option_pk>/",
        views.OptionDetail.as_view(),
    ),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
