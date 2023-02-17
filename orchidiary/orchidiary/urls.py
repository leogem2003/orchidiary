"""orchidiary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import homepage, signup, logout_view, login_view, orchids_sections_view
from plants.views import genre_list_view, genre_detail_view, variety_list_view, variety_detail_view, filtered_search

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('signup', signup, name='signup'),
    path('logout', logout_view, name='logout'),
    path('login', login_view, name='login'),
    path('orchids', orchids_sections_view, name="orchids_sections"),
    path('genres/list/<int:page>/<int:num>', genre_list_view, name="genres_list"),
    path('genres/view/<str:pk>', genre_detail_view, name="genre_detail"),
    path('varieties/list/<int:page>/<int:num>', variety_list_view, name="variety_list"),
    path('varieties/list/<int:page>/<int:num>/<str:genre>', variety_list_view, name="variety_list_f_genre"),
    path('varieties/view/<int:pk>', variety_detail_view, name="variety_detail"),
    path('search', filtered_search, name="filtered_search"),
    path('my-orchids/', include("plants.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)