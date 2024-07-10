# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# import os
# import json
# import logging
# from django.http import JsonResponse
# from rest_framework.decorators import api_view
# from django.http import JsonResponse
# import os
# import json

# import os
# import json
# from django.http import JsonResponse
# from rest_framework.decorators import api_view

# from rest_framework.decorators import api_view
# from django.http import JsonResponse
# import os
# import json
# from rest_framework.decorators import api_view
# from django.http import JsonResponse
# import os
# import json
# logger = logging.getLogger(__name__)

# #To manipulate the response that coming in properties for all side search we are use this function
# # To manipulate the response that coming in properties for all side search we are use this function
# def format_item_data(item_data):
#     """
#     Function to format an individual item based on the specified structure.
#     """
#     properties = item_data.get('properties', {})
    
#     formatted_item = {
#         "Major": properties.get('major', ''),
#         "Submajor": properties.get('submajor', ''),
#         "Minor": properties.get('minor', ''),
#         "SubMinor": properties.get('subminor', ''),
#         "Grade": properties.get('grade', ''),
#         "File_formats": properties.get('file_formats', ''),
#         "Type": properties.get('type', ''),
#         "source_description": properties.get('source_description', ''),
#         "place_city": properties.get('place_city', ''),
#         "year": properties.get('year', ''),
#         "publisher": properties.get('publisher', ''),
#         "path": properties.get('path', ''),
#         "collection": properties.get('collection', ''),
#         "collection_type": properties.get('collection_type', ''),
#         "soi_toposheet_no": properties.get('soi_toposheet_no', ''),
#         "grade1": properties.get('grade1', ''),
#         "data_resolution": properties.get('data_resolution', ''),
#         "ownership": properties.get('ownership', ''),
#         "is_processed": properties.get('is_processed', ''),
#         "short_descr": properties.get('short_descr', ''),
#         "descr": properties.get('descr', ''),
#         "img_service": properties.get('img_service', ''),
#         "img_dw": properties.get('img_dw', ''),
#         "map_service": properties.get('map_service', ''),
#         "map_dw": properties.get('map_dw', ''),
#         "publish_on": properties.get('publish_on', ''),
#         "thumbnail": properties.get('thumbnail', ''),
#         "source": properties.get('source', ''),
#         "created_id": properties.get('created_id', ''),
#         "created_date": properties.get('created_date', ''),
#         "modified_id": properties.get('modified_id', ''),
#         "modified_date": properties.get('modified_date', ''),
#         "deleted_id": properties.get('deleted_id', ''),
#         "deleted_date": properties.get('deleted_date', ''),
#         "img_vis_url": properties.get('img_vis_url', ''),
#         "img_download_url": properties.get('img_download_url', ''),
#         "shp_file_url": properties.get('shp_file_url', ''),
#     }
#     return formatted_item
# # 



# @api_view(['POST'])
# def sb_searches2(request):
#     catalog_root = "./stac-catalog"
#     shape_file_root = os.path.join(catalog_root, "Shape_File_Data")
#     excluded_folders = ['Projects', 'Resources_and_Publication','Shape_File_Data']
#     items = []

#     # Parse JSON payload from the request body
#     payload = request.data

#     # Extract search, filter, pagination parameters from the payload
#     search_query_params = payload.get('search', [])
#     filter_params = payload.get('filter', {})
#     pagination_params = payload.get('pagination', {})
#     category = filter_params.get('category', 'raster')
#     category = filter_params.get('category', 'vector')
#     print("Category:", category)
#     # Convert search parameters to dictionaries
#     search_dicts = [param if isinstance(param, dict) else {param: ''} for param in search_query_params]

#     # Parse pagination parameters
#     page = int(pagination_params.get('page', 1))
#     page_size = int(pagination_params.get('pageSize', 10))
#     sort_field = pagination_params.get('sort', {}).get('field', None)
#     sort_order = pagination_params.get('sort', {}).get('order', 'asc')

#     # Determine the root directory based on the category
#     if category == "vector":
#         root_dir = shape_file_root
        
#         # Iterate through each subfolder in the Shape_File_Data directory
#         for subfolder_name in os.listdir(root_dir):
#             subfolder_path = os.path.join(root_dir, subfolder_name)

#             # Check if the path is a directory
#             if os.path.isdir(subfolder_path):
#                 # Iterate through each item folder in the subfolder
#                 for item_folder_name in os.listdir(subfolder_path):
#                     # Check if the folder name is in the expected format
#                     if item_folder_name.endswith('-item'):
#                         # Construct the full path to the item folder
#                         item_folder_path = os.path.join(subfolder_path, item_folder_name)

#                         # Access files within the item folder
#                         for file_name in os.listdir(item_folder_path):
#                             # Check if the file is a JSON file ending with '-item.json'
#                             if file_name.endswith('-item.json'):
#                                 file_path = os.path.join(item_folder_path, file_name)

#                                 with open(file_path, 'r') as json_file:
#                                     item_data = json.load(json_file)
#                                 properties = item_data.get('properties', {})

#                                 # Check if search parameters match
#                                 search_match = all(
#                                     any(properties.get(k, '') == v for k, v in search_dict.items())
#                                     for search_dict in search_dicts
#                                 ) if search_dicts else True

#                                 # Check if filter parameters match
#                                 # Check if filter parameters match
#                                 filter_match = all(
#                                     any(
#                                         (isinstance(properties.get(k, ''), str) and v == properties.get(k, ''))
#                                         or (isinstance(properties.get(k, ''), list) and v in properties.get(k, []))
#                                         for v in filter_params.get(k, [])
#                                     )
#                                     for k in filter_params.keys() if k != 'category'
#                                 ) if filter_params else True

#                                 print("Properties:", properties)
#                                 print("Search Match:", search_match)
#                                 print("Filter Match:", filter_match)
                                
#                                 # Append properties if all filter and search conditions are satisfied
#                                 if search_match and filter_match:
#                                     items.append(properties)
#                                 #    print("---------items------", items)

#         # Sort items if sort parameters are provided
#         if sort_field:
#             items.sort(key=lambda x: x.get(sort_field, ''), reverse=(sort_order == 'desc'))

#         # Paginate the result
#         start_index = (page - 1) * page_size
#         paginated_items = items[start_index:start_index + page_size]



# #         # Prepare the response
#         response_data = {"data": paginated_items, "count": len(items)}
#         return JsonResponse(response_data, status=200)
#     # Determine the root directory based on the category
#     if category == "raster":
#         root_dir = catalog_root
    
#     # Iterate through each main subfolder (state, city, etc.) in the catalog
#     for main_subfolder_name in os.listdir(catalog_root):
#         main_subfolder_path = os.path.join(catalog_root, main_subfolder_name)

#         # Check if the path is a directory and not in excluded folders list
#         if os.path.isdir(main_subfolder_path) and main_subfolder_name not in excluded_folders:
#             # Iterate through each subfolder within the main subfolder
#             for subfolder_name in os.listdir(main_subfolder_path):
#                 subfolder_path = os.path.join(main_subfolder_path, subfolder_name)
#                 subfolder_path = subfolder_path.replace("\\", "/")

#                 # Check if the path is a directory and not in excluded folders list
#                 if os.path.isdir(subfolder_path) and subfolder_name not in excluded_folders:
#                     # Iterate through each item folder in the sub-subfolder
#                     for item_folder_name in os.listdir(subfolder_path):
#                         # Check if the folder name is in the expected format
#                         if item_folder_name.endswith('-item'):
#                             # Construct the full path to the item folder
#                             item_folder_path = os.path.join(subfolder_path, item_folder_name)

#                             # Access files within the item folder
#                             for file_name in os.listdir(item_folder_path):
#                                 # Check if the file is a JSON file ending with '-item.json'
#                                 if file_name.endswith('-item.json'):
#                                     file_path = os.path.join(item_folder_path, file_name)

#                                     with open(file_path, 'r') as json_file:
#                                         item_data = json.load(json_file)
#                                         properties = item_data.get('properties', {})
#                                         print("*****properties********",properties)
#                                         # Check if search parameters match
#                                         search_match = all(
#                                             any(properties.get(k, '') == v for k, v in search_dict.items())
#                                             for search_dict in search_dicts
#                                         ) if search_dicts else True

#                                         # Check if filter parameters match
#                                         # Check if filter parameters match
#                                         filter_match = all(
#                                             any(
#                                                 (isinstance(properties.get(k, ''), str) and v == properties.get(k, ''))
#                                                 or (isinstance(properties.get(k, ''), list) and v in properties.get(k, []))
#                                                 for v in filter_params.get(k, [])
#                                             )
#                                             for k in filter_params.keys() if k != 'category'
#                                         ) if filter_params else True

#                                         print("Properties:", properties)
#                                         print("Search Match:", search_match)
#                                         print("Filter Match:", filter_match)
                                

#                                         # Append properties if all filter and search conditions are satisfied
#                                         if search_match and filter_match:
#                                                     items.append(properties)

#     # Sort items if sort parameters are provided
#     if sort_field:
#         items.sort(key=lambda x: x.get(sort_field, ''), reverse=(sort_order == 'desc'))

#     # Paginate the result
#     start_index = (page - 1) * page_size
#     paginated_items = items[start_index:start_index + page_size]

#     # Format the items
#     formatted_items = [format_item_data(item) for item in paginated_items]
#     # Prepare the response
#     response_data = {"data": formatted_items, "count": len(items)}
#     return JsonResponse(response_data, status=200)


import os
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
import re

def formated_vector_data(item_data):
    """
    Function to format an individual item based on the specified structure.
    """
    properties = item_data.get('properties', {})
    
    formatted_item = {
        "year": properties.get('year', ''),
        "shp_file_url": properties.get('shp_file_url', ''),
        "place_city": properties.get('place_city', ''),
        "url_alias": properties.get('url_alias', ''),
       
    }
    return formatted_item

def format_item_data(item_data):
    """
    Function to format an individual item based on the specified structure.
    """
    properties = item_data.get('properties', {})
    
    formatted_item = {
        "Major": properties.get('major', ''),
        "Submajor": properties.get('submajor', ''),
        "Minor": properties.get('minor', ''),
        "SubMinor": properties.get('subminor', ''),
        "Grade": properties.get('grade', ''),
        "File_formats": properties.get('file_formats', ''),
        "Type": properties.get('type', ''),
        "source_description": properties.get('source_description', ''),
        "place_city": properties.get('place_city', ''),
        "year": properties.get('year', ''),
        "publisher": properties.get('publisher', ''),
        "path": properties.get('path', ''),
        "collection": properties.get('collection', ''),
        "collection_type": properties.get('collection_type', ''),
        "soi_toposheet_no": properties.get('soi_toposheet_no', ''),
        "grade1": properties.get('grade1', ''),
        "data_resolution": properties.get('data_resolution', ''),
        "ownership": properties.get('ownership', ''),
        "is_processed": properties.get('is_processed', ''),
        "short_descr": properties.get('short_descr', ''),
        "descr": properties.get('descr', ''),
        "img_service": properties.get('img_service', ''),
        "img_dw": properties.get('img_dw', ''),
        "map_service": properties.get('map_service', ''),
        "map_dw": properties.get('map_dw', ''),
        "publish_on": properties.get('publish_on', ''),
        "thumbnail": properties.get('thumbnail', ''),
        "source": properties.get('source', ''),
        "created_id": properties.get('created_id', ''),
        "created_date": properties.get('created_date', ''),
        "modified_id": properties.get('modified_id', ''),
        "modified_date": properties.get('modified_date', ''),
        "deleted_id": properties.get('deleted_id', ''),
        "deleted_date": properties.get('deleted_date', ''),
        "img_vis_url": properties.get('img_vis_url', ''),
        "img_download_url": properties.get('img_download_url', ''),
        "shp_file_url": properties.get('shp_file_url', ''),
    }
    return formatted_item






@api_view(['POST'])
def sb_searches(request):
    catalog_root = "./stac-catalog"
    shape_file_root = os.path.join(catalog_root, "Shape_File_Data")
    excluded_folders = ['Projects', 'Resources_and_Publication', 'Shape_File_Data']
    items = []

    # Parse JSON payload from the request body
    payload = request.data

    # Extract search, filter, pagination parameters from the payload
    search_keyword = payload.get('search', '')
    filter_params = payload.get('filter', {})
    pagination_params = payload.get('pagination', {})
    category = filter_params.get('category', 'raster')

    # Parse pagination parameters
    page = int(pagination_params.get('page', 1))
    page_size = int(pagination_params.get('pageSize', 10))
    sort_field = pagination_params.get('sort', {}).get('field', None)
    sort_order = pagination_params.get('sort', {}).get('order', 'asc')

    # Compile the search keyword into a regex pattern
    search_pattern = re.compile(search_keyword, re.IGNORECASE) if search_keyword else None

    def filter_and_search_items(root_dir):
        # Iterate through directories and files to find matching items
        for root, dirs, files in os.walk(root_dir):
            for file_name in files:
                if file_name.endswith('-item.json'):
                    file_path = os.path.join(root, file_name)

                    with open(file_path, 'r') as json_file:
                        item_data = json.load(json_file)
                        properties = item_data.get('properties', {})

                        # Check if filter parameters match
                        filter_match = all(
                            properties.get(k) == v for k, v in filter_params.items() if k != 'category'
                        ) if filter_params else True

                        # Search within the properties
                        search_match = any(
                            search_pattern.search(str(value)) for key, value in properties.items()
                        ) if search_pattern else True

                        # Print the values within the filter parameters and search results
                        if filter_match and search_match:
                            for k, v in filter_params.items():
                                if k != 'category':
                                    prop_value = properties.get(k, None)
                                    print(f"Key: {k}, Filter Value: {v}, Property Value: {prop_value}")
                                    if isinstance(prop_value, str):
                                        print(f"Property value for key '{k}' is a string: {prop_value}")
                                    elif isinstance(prop_value, list):
                                        print(f"Property value for key '{k}' is a list: {prop_value}")

                            print(f"*** Filter match result: {filter_match} ***")
                            print(f"*** Search match result: {search_match} ***")

                            # Append properties if all filter and search conditions are satisfied
                            if filter_match and search_match:
                                items.append(item_data)

    # Determine the root directory based on the category
    # if category == "vector":
    #     filter_and_search_items(shape_file_root)
    # Determine the root directory based on the category
    if category == "vector":
        root_dir = shape_file_root

        # Iterate through each subfolder in the Shape_File_Data directory
        for subfolder_name in os.listdir(root_dir):
            subfolder_path = os.path.join(root_dir, subfolder_name)

            # Check if the path is a directory
            if os.path.isdir(subfolder_path):
                # Iterate through each item folder in the subfolder
                for item_folder_name in os.listdir(subfolder_path):
                    # Check if the folder name is in the expected format
                    if item_folder_name.endswith('-item'):
                        # Construct the full path to the item folder
                        item_folder_path = os.path.join(subfolder_path, item_folder_name)

                        # Access files within the item folder
                        for file_name in os.listdir(item_folder_path):
                            # Check if the file is a JSON file ending with '-item.json'
                            if file_name.endswith('-item.json'):
                                file_path = os.path.join(item_folder_path, file_name)

                                with open(file_path, 'r') as json_file:
                                    item_data = json.load(json_file)
                                    properties = item_data.get('properties', {})

                                # Check if filter parameters match
                                    filter_match = all(
                                        properties.get(k) == v for k, v in filter_params.items() if k != 'category'
                                    ) if filter_params else True

                                    # Search within the properties
                                    search_match = any(
                                        search_pattern.search(str(value)) for key, value in properties.items()
                                    ) if search_pattern else True

                                    # Print the values within the filter parameters and search results
                                    if filter_match and search_match:
                                        for k, v in filter_params.items():
                                            if k != 'category':
                                                prop_value = properties.get(k, None)
                                                print(f"Key: {k}, Filter Value: {v}, Property Value: {prop_value}")
                                                if isinstance(prop_value, str):
                                                    print(f"Property value for key '{k}' is a string: {prop_value}")
                                                elif isinstance(prop_value, list):
                                                    print(f"Property value for key '{k}' is a list: {prop_value}")

                                    print(f"*** Filter match result: {filter_match} ***")
                                    print(f"*** Search match result: {search_match} ***")

                                    # Append properties if all filter and search conditions are satisfied
                                    if filter_match and search_match:
                                        items.append(item_data)

        # Sort items if sort parameters are provided
        if sort_field:
            items.sort(key=lambda x: x.get('properties', {}).get(sort_field, ''), reverse=(sort_order == 'desc'))

        # Paginate the result
        start_index = (page - 1) * page_size
        paginated_items = items[start_index:start_index + page_size]

        # Format the items
        formatted_items = [formated_vector_data(item) for item in paginated_items]

        # Prepare the response
        response_data = {"data": formatted_items, "count": len(items)}
        return JsonResponse(response_data, status=200)


    if category == "raster":
        root_dir = catalog_root

    # Iterate through each main subfolder (state, city, etc.) in the catalog
    for main_subfolder_name in os.listdir(catalog_root):
        main_subfolder_path = os.path.join(catalog_root, main_subfolder_name)

        # Check if the path is a directory and not in excluded folders list
        if os.path.isdir(main_subfolder_path) and main_subfolder_name not in excluded_folders:
            # Iterate through each subfolder within the main subfolder
            for subfolder_name in os.listdir(main_subfolder_path):
                subfolder_path = os.path.join(main_subfolder_path, subfolder_name)
                subfolder_path = subfolder_path.replace("\\", "/")

                # Check if the path is a directory and not in excluded folders list
                if os.path.isdir(subfolder_path) and subfolder_name not in excluded_folders:
                    # Iterate through each item folder in the sub-subfolder
                    for item_folder_name in os.listdir(subfolder_path):
                        # Check if the folder name is in the expected format
                        if item_folder_name.endswith('-item'):
                            # Construct the full path to the item folder
                            item_folder_path = os.path.join(subfolder_path, item_folder_name)

                            # Access files within the item folder
                            for file_name in os.listdir(item_folder_path):
                                # Check if the file is a JSON file ending with '-item.json'
                                if file_name.endswith('-item.json'):
                                    file_path = os.path.join(item_folder_path, file_name)

                                    with open(file_path, 'r') as json_file:
                                        item_data = json.load(json_file)
                                        properties = item_data.get('properties', {})

                                        filter_match = all(
                                            properties.get(k) == v for k, v in filter_params.items() if k != 'category'
                                        ) if filter_params else True

                                        # Search within the properties
                                        search_match = any(
                                            search_pattern.search(str(value)) for key, value in properties.items()
                                        ) if search_pattern else True

                                        # Append properties if all filter and search conditions are satisfied
                                        if search_match and filter_match:
                                            items.append(item_data)

    # Sort items if sort parameters are provided
    if sort_field:
        items.sort(key=lambda x: x.get('properties', {}).get(sort_field, ''), reverse=(sort_order == 'desc'))

    # Paginate the result
    start_index = (page - 1) * page_size
    paginated_items = items[start_index:start_index + page_size]

    # Format the items
    formatted_items = [format_item_data(item) for item in paginated_items]

    # Prepare the response
    response_data = {"data": formatted_items, "count": len(items)}
    return JsonResponse(response_data, status=200)
