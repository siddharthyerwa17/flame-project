from rest_framework import routers

from django.urls import path , include
from .views import StacViewSet,add_item_to_stac,SourceDataViewSet,AttributeViewSet,All_AttributeViewSet#,SourceDataViewSet,add_item_to_stac
from .views import search_catalog_common_metadata_api
from .views import (search_catalog_metadata_by_key_api,
                    sb_collection,
                    sb_publisher,
                    sb_minor,sb_grade,sb_place,sb_subminor,sb_year,
                    search_side_bar,
                    combined_response,
                    search_catalog_metadata_for_combined_response,
                    sb_subcollection,sb_collection1)
from .stac_item_update import get_all_stac_items,get_stac_item_by_id,update_stac_item
from .shape_file_upload import (add_shape_files_to_stac,get_all_shape_file_items,get_shape_file_by_id,update_shape_file_items,
                                sb_shape_file_by_year,search_side_bar_shape_file,shape_file_main_section_data,
                                sb_shape_file_by_place,post_shape_file)

from .Resource_andProject import (add_Resources_and_Publication_stac,add_Projects_to_stac,
                                  get_Resources_and_Publication_stac,get_Projects_stac,
                                  get_filtered_pubndResource_stac_items,get_filtered_Projects_stac_items,
                                  FeedbackViewSet)
                                  
from .updated_apis import sb_searches                                  


router = routers.SimpleRouter()
router.register(r'stac', StacViewSet, basename='stac')
router.register(r'sourcedata', SourceDataViewSet,basename='SourceDataViewSet')
router.register(r'post_feedback', FeedbackViewSet,basename='FeedbackViewSet')

urlpatterns = [
    path('', include(router.urls)),
    path('add_item_to_stac/',add_item_to_stac),
    path('main_section_data/', search_catalog_common_metadata_api, name='search_catalog_common_metadata_api'),
    path('search_catalog_metadata_by_key_api/<str:key_to_search>/',search_catalog_metadata_by_key_api, name='search_catalog_metadata_by_key_api'),
    path('sb_collection/', sb_collection, name='sb_collection'),
    path('sb_subcollection/', sb_subcollection, name='sb_subcollection'),
    path('sb_minor/', sb_minor, name='sb_minor_pagination'), #/
    path('sb_subminor/', sb_subminor, name='sb_subminor'),   #/
    path('sb_grade/', sb_grade, name='sb_grade'),  #/
    path('sb_publisher/', sb_publisher, name='sb_publisher'), #/
    path('sb_place/', sb_place, name='sb_place'),  #/
    path('sb_year/', sb_year, name='sb_year'),  #/
    path('getside_searchdata/', search_side_bar, name='columnsearch'),
    path('meta_data_for_pagination/<str:query>/', combined_response, name='get_meta_data_with_pagination'), #/
    path('meta_data_for_pagination_wrongname/<str:query>/', search_catalog_metadata_for_combined_response, name='sb_year'),  #/
    path('get_shp_attribute_using_lat_long/', AttributeViewSet.as_view({'get': 'get_within_point'}), name='get_shp_attribute_using_lat_long'),
    path('get_all_stac_items/',get_all_stac_items),
    path('get_item_by_id/<str:item_id>/',get_stac_item_by_id),
    path('update_stac_item/<str:item_id>/',update_stac_item),
    path('Add_Shape_File/',post_shape_file),
    path('Get_all_Shape_File_item/',get_all_shape_file_items),
    path('get_shape_file_by_id/<str:item_id>/',get_shape_file_by_id),
    
    path('sb_shape_file_by_year/',sb_shape_file_by_year),
    path('search_side_bar_shape_file/',search_side_bar_shape_file),
    path('sb_shape_file_by_place/',sb_shape_file_by_place),
    path('shape_file_main_section_data/',shape_file_main_section_data),
    
    
    path('Add_ResourceAndPublication/',add_Resources_and_Publication_stac),
    path('Add_Projects/',add_Projects_to_stac),

    path('get_resourcesndpublication/', get_Resources_and_Publication_stac, name='get_resources'),
    path('get_projects/', get_Projects_stac, name='get_projects'),
    
    path('filtered_pubndResource_stac_items/', get_filtered_pubndResource_stac_items, name='filtered_pubndResource_stac_items'),
    path('filtered_Projects_stac_items/', get_filtered_Projects_stac_items, name='get_filtered_Projects_stac_items'),
    
    path('get_all_attributes/', All_AttributeViewSet.as_view(), name='get_all_attributes'),
    
    path('sidebar_search/', sb_searches, name='sb_search'),
    
    path('sb_collection1/', sb_collection1, name='sb_collection1'),
    
    ]