from django.urls import path


from dynamic import views


urlpatterns = [
    path('<str:app_name>/<str:model_name>/',views.DynamicListView.as_view(),name='dynamic-list'),
    path('create/<str:app_name>/<str:model_name>/',views.DynamicCreateView.as_view(),name='dynamic-add'),
    path('detail/<str:app_name>/<str:model_name>/<int:pk>/',views.DynamicDetailView.as_view(),name='dynamic-view'),
    path('update/<str:app_name>/<str:model_name>/<int:pk>/',views.DynamicUpdateView.as_view(),name='dynamic-change'),
    path('delete/<str:app_name>/<str:model_name>/<int:pk>/',views.DynamicDeleteView.as_view(),name='dynamic-delete'),
]


