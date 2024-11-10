from django.urls import path, include


from invitations import views,functions

app_name = 'invitations'


urlpatterns = [
    path('',views.InvitationListView.as_view(),name='invitation-list'),
    path('create/',views.InvitationCreateView.as_view(),name='invitation-create'),
    path('detail/<int:pk>/',views.InvitationDetailView.as_view(),name='invitation-detail'),
    path('update/<int:pk>/',views.InvitationUpdateView.as_view(),name='invitation-update'),
    path('delete/<int:pk>/',views.InvitationDeleteView.as_view(),name='invitation-delete'),

    path('resend/invitation/<int:invitation_id>/',functions.resend_invitation,name='resend-invitation'),

]

