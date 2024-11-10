from django.urls import path, include


from companies import views,functions

app_name = 'companies'


urlpatterns = [
    path('',views.CompanyListView.as_view(),name='company-list'),
    path('create/',views.CompanyCreateView.as_view(),name='company-create'),
    path('detail/<int:pk>/',views.CompanyDetailView.as_view(),name='company-detail'),
    path('update/<int:pk>/',views.CompanyUpdateView.as_view(),name='company-update'),
    path('delete/<int:pk>/',views.CompanyDeleteView.as_view(),name='company-delete'),

    path('activate/profile/<int:company_id>/int<user_id>/',functions.activate_company_profile,name='activate-profile'),
    path('remove/profile/<int:company_id>/int<profile_id>/',functions.remove_company_profile,name='remove-profile'),
    path('assign-permissions/<int:company_id>/<int:user_id>/', views.assign_permissions, name='assign_permissions'),
    path('sb/', functions.get_company_for_sb, name='sb-companies'),
]

