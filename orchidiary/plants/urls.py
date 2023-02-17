from django.urls import path

from .views import account_stats, orchids_list, add_orchid_view, orchid_detail_view, add_genre_view, my_genre_list_view, my_variety_list_view, add_variety_view, edit_instance_view, edit_genre_view, edit_variety_view, delete_genre_view, delete_instance_view, delete_variety_view

urlpatterns = [
    path('', account_stats, name="account_home"),
    path('orchids/list/<int:page>/<int:num>', orchids_list, name="orchids_list"),
    path('orchids/list/<int:page>/<int:num>/<int:variety>', orchids_list, name="orchids_list_f_variety"),
    path('orchids/add', add_orchid_view, name="add_orchid_instance"),
    path('orchids/view/<int:pk>', orchid_detail_view, name="instance_detail"),
    path('genres/list/<int:page>/<int:num>', my_genre_list_view, name="my_genres_list"),
    path('genres/add', add_genre_view, name="add_genre"),
    path('varieties/list/<int:page>/<int:num>', my_variety_list_view, name="my_variety_list"),
    path('varieties/list/<int:page>/<int:num>/<str:genre>', my_variety_list_view, name="my_variety_list_f_genre"),
    path('varieties/add', add_variety_view, name="add_variety"),
    path('orchids/edit/<int:pk>', edit_instance_view, name="edit_instance"),
    path('genres/edit/<str:pk>', edit_genre_view, name="edit_genre"),
    path('varieties/edit/<int:pk>', edit_variety_view, name="edit_variety"),
    path('genres/delete/<str:pk>', delete_genre_view, name="delete_genre"),
    path('varieties/delete/<int:pk>', delete_variety_view, name="delete_variety"),
    path('orchids/delete/<int:pk>', delete_instance_view, name="delete_instance"),
]