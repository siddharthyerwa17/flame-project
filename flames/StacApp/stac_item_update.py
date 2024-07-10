from rest_framework import viewsets
from rest_framework.response import Response
from pystac import Catalog
from rest_framework.decorators import api_view
import pystac
from Logger import logger
import os

class StacViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        try:
            # Assuming 'pk' is the ID of the STAC catalog
            catalog_path = f"./flames/stac-catalog/{pk}.json"
            catalog = Catalog.from_file(catalog_path)
            
            return Response({"status": "success", "data": catalog.to_dict()})
        except FileNotFoundError:
            return Response({"status": "error", "message": f"Catalog with ID {pk} not found"})
        except Exception as e:
            return Response({"status": "error", "message": f"An error occurred: {str(e)}"})
        
        
def get_items_from_catalog(catalog, seen_ids):
    all_items = []
    print("***************all_items",all_items)

    # Get items from the current catalog
    items = list(catalog.get_all_items())
    print("********items*******all_items",items)
    for item in items:
        if item.id not in seen_ids:
            seen_ids.add(item.id)
            all_items.append(item)

    # Recursively get items from nested catalogs and collections
    for child in catalog.get_children():
        if isinstance(child, pystac.Catalog):
            all_items.extend(get_items_from_catalog(child, seen_ids))
        elif isinstance(child, pystac.Collection):
            all_items.extend(get_items_from_collection(child, seen_ids))

    return all_items

def get_items_from_collection(collection, seen_ids):
    all_items = []

    # Get items from the current collection
    items = list(collection.get_all_items())
    for item in items:
        if item.id not in seen_ids:
            seen_ids.add(item.id)
            all_items.append(item)

    # Recursively get items from nested collections
    for child in collection.get_children():
        if isinstance(child, pystac.Collection):
            all_items.extend(get_items_from_collection(child, seen_ids))

    return all_items

@api_view(['GET'])
def get_all_stac_items(request):
    logger.debug(f"[API Call] {request.__class__.__name__} [data fetched successfully] ")
    catalog_path = "./stac-catalog"
    items = []
    excluded_folders = ['Projects', 'Resources_and_Publication', 'Shape_File_Data']
    # Iterate through each main subfolder (state, city, etc.) in the catalog
    for main_subfolder_name in os.listdir(catalog_path):
        main_subfolder_path = os.path.join(catalog_path, main_subfolder_name)

        # Check if the path is a directory and not in excluded folders list
        if os.path.isdir(main_subfolder_path) and main_subfolder_name not in excluded_folders:
            # Iterate through each subfolder within the main subfolder
            for subfolder_name in os.listdir(main_subfolder_path):
                subfolder_path = os.path.join(main_subfolder_path, subfolder_name)

                # Check if the path is a directory
                if os.path.isdir(subfolder_path):
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

                                    # Load the STAC item from the JSON file
                                    try:
                                        item = pystac.Item.from_file(file_path)
                                        items.append(item)
                                    except Exception as e:
                                        print(f"Error loading STAC item from {file_path}: {e}")

    # Format the items as needed
    formatted_items = [
        {
            "id": item.id,
            "major": item.properties.get("major", ""),
            "submajor": item.properties.get("submajor", ""),
            "minor": item.properties.get("minor", ""),
            "subminor": item.properties.get("subminor", ""),
            "grade": item.properties.get("grade", ""),
            "descr": item.properties.get("descr", ""),
            "year": item.properties.get("year", ""),
            "img_vis_url": item.properties.get("img_vis_url"),
            "shp_file_url": item.properties.get("shp_file_url"),
            "img_download_url": item.properties.get("img_download_url"),
            "urlalias": item.properties.get("urlalias"),
            "place_city": item.properties.get("place_city", ""),
            "publisher": item.properties.get("publisher", ""),
            
            # Add other fields accordingly
        }
        for item in items
    ]

    return Response({"status": "success", "message": "All Items Retrieved Successfully", "data": formatted_items})
        
        
def get_item_by_id(catalog, item_id):
    try:
        item = catalog.get_item(item_id)
        formatted_item = {
            "id": item.id,
            "major": item.properties.get("major", ""),
            "submajor": item.properties.get("submajor", ""),
            "minor": item.properties.get("minor", ""),
            "subminor": item.properties.get("subminor", ""),
            "grade": item.properties.get("grade", ""),
            "descr": item.properties.get("descr", ""),
            "year": item.properties.get("year", ""),
            "img_vis_url":item.properties.get("img_vis_url"),
            "shp_file_url":item.properties.get("shp_file_url"),
            "img_download_url":item.properties.get("img_download_url"),
            "urlalias": item.properties.get("urlalias"),
            "place_city":item.properties.get("place_city"),
            "publisher":item.properties.get("publisher")
            # Add other fields accordingly
        }
        return formatted_item
    except pystac.STACError as e:
        raise Exception(f"Item with ID {item_id} not found in the catalog.")

from rest_framework.response import Response
from rest_framework.decorators import api_view
import os
import pystac

@api_view(['GET'])
def get_stac_item_by_id(request, item_id):
    logger.debug(f"[API Call] {request.__class__.__name__} [data fetched successfully] ")
    catalog_path = "./stac-catalog"
    item = None

    # Iterate through each main subfolder (state, city, etc.) in the catalog
    for main_subfolder_name in os.listdir(catalog_path):
        main_subfolder_path = os.path.join(catalog_path, main_subfolder_name)

        # Check if the path is a directory
        if os.path.isdir(main_subfolder_path):
            # Iterate through each subfolder within the main subfolder
            for subfolder_name in os.listdir(main_subfolder_path):
                subfolder_path = os.path.join(main_subfolder_path, subfolder_name)

                # Check if the path is a directory
                if os.path.isdir(subfolder_path):
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

                                    # Load the STAC item from the JSON file
                                    try:
                                        item_data = pystac.Item.from_file(file_path)
                                        if item_data.id == item_id:
                                            item = item_data
                                            break
                                    except Exception as e:
                                        print(f"Error loading STAC item from {file_path}: {e}")
                            if item:
                                break
                    if item:
                        break
            if item:
                break

    if item:
        formatted_item = {
            "id": item.id,
            "major": item.properties.get("major", ""),
            "submajor": item.properties.get("submajor", ""),
            "minor": item.properties.get("minor", ""),
            "subminor": item.properties.get("subminor", ""),
            "grade": item.properties.get("grade", ""),
            "descr": item.properties.get("descr", ""),
            "year": item.properties.get("year", ""),
            "img_vis_url": item.properties.get("img_vis_url"),
            "shp_file_url": item.properties.get("shp_file_url"),
            "img_download_url": item.properties.get("img_download_url"),
            "urlalias": item.properties.get("urlalias"),
            "year": item.properties.get("year", ""),
            "publisher": item.properties.get("publisher", ""),
            "place_city":item.properties.get("place_city", ""),
            # Add other fields accordingly
        }
        return Response({"status": "success", "message": "Item Retrieved Successfully", "data": formatted_item})
    else:
        return Response({"status": "error", "message": f"Item With ID '{item_id}' Not Found"})
            
        
               
               
               
               
############ API TO UPDATE THE DATA STAC ITEM ###############
import os
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pystac

@api_view(['PUT'])
def update_stac_item(request, item_id):
    logging_data = dict(request.data)
    logger.debug(f"[API Call] {request.__class__.__name__} create Data: {logging_data}")
    try:
        # Assume that in request.data, we got the updated data
        updated_data = request.data
        catalog_path = "./stac-catalog"

        # List to hold the paths of item JSON files
        item_paths = []

        # Iterate through each main subfolder (state, city, etc.) in the catalog
        for main_subfolder_name in os.listdir(catalog_path):
            main_subfolder_path = os.path.join(catalog_path, main_subfolder_name)

            # Check if the path is a directory
            if os.path.isdir(main_subfolder_path):
                # Iterate through each subfolder within the main subfolder
                for subfolder_name in os.listdir(main_subfolder_path):
                    subfolder_path = os.path.join(main_subfolder_path, subfolder_name)

                    # Check if the path is a directory
                    if os.path.isdir(subfolder_path):
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
                                        item_paths.append(file_path)

        # Find the item with the specified item_id
        matched_item_path = None
        for item_path in item_paths:
            with open(item_path, 'r') as f:
                item_data = json.load(f)
                if item_data['id'] == item_id:
                    matched_item_path = item_path
                    break

        if matched_item_path:
            # Load the STAC item from the matched item JSON file
            item = pystac.Item.from_file(matched_item_path)

            # Update item properties with the existing data and the updated data
            item.properties.update(updated_data)

            # Save the updated item properties back to the JSON file
            with open(matched_item_path, 'w') as f:
                json.dump(item.to_dict(), f)

            return Response({
                "status": "success",
                "message": "Item Updated Successfully",
                "data": updated_data
            })
        else:
            return Response({
                "status": "error",
                "message": f"Item With ID {item_id} Not Found"
            }, status=404)

    except Exception as e:
        return Response({
            "status": "error",
            "message": f"Failed To Update Item: {str(e)}"
        }, status=500)

    
  #  except Exception as e:
       # return Response({"status": "error", "message": f"An error occurred: {str(e)}"})