from django.urls import path


from profiles import views,functions 

urlpatterns = [
    path('profile/detail/<int:pk>', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/update/<int:pk>', views.ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/delete/<int:pk>', views.ProfileDeleteView.as_view(), name='profile-delete'),


    path('sb/',functions.get_profiles_data,name='profiles-sb'),
]
