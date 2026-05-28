from django.urls import path
from ctapp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
path("",views.index,name="index"),
path("index",views.index,name="index"),
path("user_login",views.user_login,name="user_login"),
# path("user_registration",views.user_registration,name="user_registration"),
path('user_action', views.user_action,name="user_action"),
path('chat/', views.chat, name='chat'),
path('chat_api/<int:id>/messages', views.chat_room_messages_api, name='chat_room_messages_api'),
path('user_chat/', views.user_chat, name='user_chat'),
path('user_chat/<int:id>', views.user_chat, name='user_chat_room'),
path('panic_send', views.panic_send, name='panic_send'),
path("login_action",views.login_action,name="login_action"),
path('admin_logout', views.admin_logout,name="admin_logout"),
path('user_logout',views.user_logout,name="user_logout"),
path("user_registration",views.user_registration,name="user_registration"),
path('admin_home',views.admin_home,name="admin_home"),
path('adm_panic_alerts', views.adm_panic_alerts, name="adm_panic_alerts"),
path('adm_forward_panic/<int:id>', views.adm_forward_panic, name="adm_forward_panic"),
path('user_home',views.user_home,name="user_home"),

path('add_category', views.add_category,name="add_category"),
path('save_category', views.save_category,name="save_category"),
path('edit_category/<int:id>', views.edit_category,name="edit_category"),
path('update_category/<int:id>', views.update_category,name="update_category"),
path('delete_category/<int:id>', views.delete_category,name="delete_category"),


path('users_list', views.users_list,name="users_list"),
path('profile', views.profile,name="profile"),



path('add_police_station',views.add_police_station,name="add_police_station"),
path('save_station',views.save_station,name="save_station"),  # station self-registration
path('admin_save_station',views.admin_save_station,name="admin_save_station"),
path('display_district',views.display_district,name="display_district"),   
path('list_police_station',views.list_police_station,name="list_police_station"),   
path('edit_police_station/<int:id>', views.edit_police_station,name="edit_police_station"),
path('update_police_station/<int:id>', views.update_police_station,name="update_police_station"),
path('delete_police_station/<int:id>', views.delete_police_station,name="delete_police_station"),

path('add_complaints', views.add_complaints,name="add_complaints"),
path('submit_complaint', views.submit_complaint,name="submit_complaint"),
path('display_police_station', views.display_police_station,name="display_police_station"),
path('view_complaints', views.view_complaints,name="view_complaints"),
path('crime_more/<int:id>', views.crime_more,name="crime_more"),
path('profile', views.profile,name="profile"),
path('view_feedback', views.view_feedback,name="view_feedback"),
path('feedback_replied_list', views.feedback_replied_list,name="feedback_replied_list"),
path('adm_reply_feedback/<int:id>', views.adm_reply_feedback,name="adm_reply_feedback"),
path('feedback', views.feedback,name="feedback"),
path('save_feedback', views.save_feedback,name="save_feedback"),
path('delete_feedback/<int:id>', views.delete_feedback,name="delete_feedback"),
path('add_reply_feedback/<int:id>', views.add_reply_feedback,name="add_reply_feedback"),


path('police_registration',views.police_registration,name="police_registration"),

# Police station approval (admin)
path('submitted_stations',views.submitted_stations,name="submitted_stations"),
path('approve_station/<int:id>',views.approve_station,name="approve_station"),
path('reject_station/<int:id>',views.reject_station,name="reject_station"),


path('submitted_crimes',views.submitted_crimes,name="submitted_crimes"),
path('adm_station_pending_cases', views.adm_station_pending_cases, name="adm_station_pending_cases"),
path('adm_to_assign_station/<int:id>', views.adm_to_assign_station, name="adm_to_assign_station"),
path('adm_assign_station/<int:id>', views.adm_assign_station, name="adm_assign_station"),
path('assign_crimes/<int:id>',views.assign_crimes,name="assign_crimes"),
path('to_assign_crimes/<int:id>',views.to_assign_crimes,name="to_assign_crimes"),
path('assigned_crimes',views.assigned_crimes,name="assigned_crimes"),

path('adm_crime_more/<int:id>',views.adm_crime_more,name="adm_crime_more"),

path('display_police',views.display_police,name="display_police"),

path('transfer',views.transfer,name="transfer"),
path('transfer_details',views.transfer_details,name="transfer_details"),
path('save_transfer',views.save_transfer,name="save_transfer"),

path('p_assigned_crimes',views.p_assigned_crimes,name="p_assigned_crimes"),
path('police_home',views.police_home,name="police_home"),

# Police Station portal
path('station_home', views.station_home, name="station_home"),
path('station_panic_alerts', views.station_panic_alerts, name="station_panic_alerts"),
path('station_officers', views.station_officers, name="station_officers"),
path('station_officers/add', views.station_add_officer, name="station_add_officer"),
path('station_officers/save', views.station_save_officer, name="station_save_officer"),
path('station_officers/delete/<int:id>', views.station_delete_officer, name="station_delete_officer"),
path('station_officers/edit/<int:id>', views.station_edit_officer, name="station_edit_officer"),
path('station_officers/update/<int:id>', views.station_update_officer, name="station_update_officer"),
path('station_complaints', views.station_complaints, name="station_complaints"),
path('station_complaints/<int:id>', views.station_complaint_detail, name="station_complaint_detail"),
path('station_complaints/<int:id>/assign', views.station_assign_complaint, name="station_assign_complaint"),
path('station_complaints/<int:id>/update', views.station_update_case, name="station_update_case"),
path('station_complaints/<int:id>/fir', views.station_add_fir, name="station_add_fir"),
path('station_complaints/<int:id>/fir/save', views.station_save_fir, name="station_save_fir"),
path('station_complaints/<int:id>/fir/view', views.station_view_fir, name="station_view_fir"),
path('station_chat', views.station_chat_list, name="station_chat_list"),
path('station_chat/<int:id>', views.station_chat_room, name="station_chat_room"),

path('crime_updates/<int:id>',views.crime_updates,name="crime_updates"),
path('save_updates/<int:id>',views.save_updates,name="save_updates"),

path('p_crime_more/<int:id>',views.p_crime_more,name="p_crime_more"),

path('adm_updates/<int:id>',views.adm_updates,name="adm_updates"),

path('district_wise',views.district_wise,name="district_wise"),
path('display_district/', views.display_district, name="display_district"),

path('place_wise',views.place_wise,name="place_wise"),

path('adm_google_map_view_spot/<str:latitude>/<str:longitude>/', views.adm_google_map_view_spot, name='adm_google_map_view_spot'),

path('p_google_map_view_spot/<str:latitude>/<str:longitude>/', views.p_google_map_view_spot, name='p_google_map_view_spot'),

path('save_fir/<int:id>',views.save_fir,name="save_fir"),
path('add_fir/<int:id>',views.add_fir,name="add_fir"),
path('view_fir/<int:id>',views.view_fir,name="view_fir"),

path('p_profile',views.p_profile,name="p_profile"),


path('p_other_crimes',views.p_other_crimes,name="p_other_crimes"),
path('police_chat', views.police_chat_list, name="police_chat_list"),
path('police_chat/<int:id>', views.police_chat_room, name="police_chat_room"),
path('forget_password/', views.forget_password),

path('send_otp/', views.send_otp),
path('check_otp_action/', views.check_otp_action),
path('change_psd/', views.change_psd),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
