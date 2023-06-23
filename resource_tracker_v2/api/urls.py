from django.urls import path

from resource_tracker_v2.api.views.attribute_definition_api_views import AttributeDefinitionList, \
    AttributeDefinitionDetails
from resource_tracker_v2.api.views.resource_api_view import ResourceListCreate, ResourceDetails
from resource_tracker_v2.api.views.resource_group_api_views import ResourceGroupList, ResourceGroupDetails
from resource_tracker_v2.api.views.transformer_api_views import TransformerListCreate, TransformerDetails

urlpatterns = [
    # attribute definition
    path('attributes/', AttributeDefinitionList.as_view(), name='api_attribute_definition_list_create'),
    path('attributes/<int:pk>/', AttributeDefinitionDetails.as_view(), name='api_attribute_definition_details'),

    # resource group
    path('resource_group/', ResourceGroupList.as_view(), name='api_resource_group_list_create'),
    path('resource_group/<int:pk>/', ResourceGroupDetails.as_view(), name='api_resource_group_details'),

    # resource
    path('resource_group/<int:resource_group_id>/resources/', ResourceListCreate.as_view(),
         name='api_resource_list_create'),
    path('resource_group/<int:resource_group_id>/resources/<int:pk>/', ResourceDetails.as_view(),
         name='api_resource_details'),

    # transformer
    path('resource_group/<int:resource_group_id>/attributes/', TransformerListCreate.as_view(),
         name='api_transformer_list_create'),
    path('resource_group/<int:resource_group_id>/attributes/<int:pk>/', TransformerDetails.as_view(),
         name='api_transformer_details'),

]