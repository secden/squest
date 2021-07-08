from django.urls import path

from resource_tracker import views

app_name = 'resource_tracker'

urlpatterns = [

    path('resource_group/', views.resource_group_list, name='resource_group_list'),
    path('resource_group/create/', views.resource_group_create, name='resource_group_create'),
    path('resource_group/<int:resource_group_id>/edit/', views.resource_group_edit,
         name='resource_group_edit'),
    path('resource_group/<int:resource_group_id>/delete/', views.resource_group_delete,
         name='resource_group_delete'),
    path('resource_group/<int:resource_group_id>/attributes/create/',
         views.resource_group_attribute_create,
         name='resource_group_attribute_create'),
    path('resource_group/<int:resource_group_id>/attributes/<int:attribute_id>/',
         views.resource_group_attribute_edit,
         name='resource_group_attribute_edit'),
    path('resource_group/<int:resource_group_id>/attributes/<int:attribute_id>/delete/',
         views.resource_group_attribute_delete,
         name='resource_group_attribute_delete'),
    path('resource_group/<int:resource_group_id>/resources/',
         views.resource_group_resource_list,
         name='resource_group_resource_list'),
    path('resource_group/<int:resource_group_id>/resources/create/',
         views.resource_group_resource_create,
         name='resource_group_resource_create'),
    path('resource_group/<int:resource_group_id>/resources/<int:resource_id>/delete/',
         views.resource_group_resource_delete,
         name='resource_group_resource_delete'),
    path('resource_group/<int:resource_group_id>/resources/<int:resource_id>/edit/',
         views.resource_group_resource_edit,
         name='resource_group_resource_edit'),

    path('resource_pool/', views.resource_pool_list, name='resource_pool_list'),
    path('resource_pool/create/', views.resource_pool_create, name='resource_pool_create'),
    path('resource_pool/<int:resource_pool_id>/edit/', views.resource_pool_edit,
         name='resource_pool_edit'),
    path('resource_pool/<int:resource_pool_id>/delete/', views.resource_pool_delete,
         name='resource_pool_delete'),
    path('resource_pool/<int:resource_pool_id>/attributes/create/', views.resource_pool_attribute_create,
         name='resource_pool_attribute_create'),
    path('resource_pool/<int:resource_pool_id>/attributes/<int:attribute_id>/delete/',
         views.resource_pool_attribute_delete,
         name='resource_pool_attribute_delete'),
    path('resource_pool/<int:resource_pool_id>/resources/<int:attribute_id>/edit/',
         views.resource_pool_attribute_edit,
         name='resource_pool_attribute_edit'),
    path('resource_pool/<int:resource_pool_id>/attributes/<int:attribute_id>/producers/',
         views.resource_pool_attribute_producer_list,
         name='resource_pool_attribute_producer_list'),
    path('resource_pool/<int:resource_pool_id>/attributes/<int:attribute_id>/consumers/',
         views.resource_pool_attribute_consumer_list,
         name='resource_pool_attribute_consumer_list'),

]