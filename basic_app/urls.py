from django.conf.urls import url
from basic_app import views

"""
Application namespaces of included URLconfs can be specified in two ways.
Firstly, you can set an app_name attribute in the included URLconf module, at the same level as the urlpatterns attribute. You have to pass the actual module, or a string reference to the module, to include(), not the list of urlpatterns itself.
"""
# TEMPALTE URL!
#
app_name = 'basic_app'

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
]
