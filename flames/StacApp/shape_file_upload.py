
import os
import urllib.parse
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pystac
import json
from rest_framework import status
from django.http import JsonResponse

from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
#from .models import Shape_Files
import os
import pystac
import urllib.parse
from Logger import logger
from django.db import connection
from pystac import Catalog

@api_view(['GET'])
def fetch_shape_files_from_db(request):
        logger.debug(f"[API Call] fetch_shape_files_from_db {request} [data fetched successfully] ")
  
        # Execute raw SQL query to fetch shape files data
        with connection.cursor() as cursor:
            cursor.execute("SELECT year, place_city, shape_file,shape_file_name FROM pub_shp_file_info WHERE is_uploaded = false")
            rows = cursor.fetchall()

        # Check if there are any shape files to upload
        if not rows:
            return Response({"status": "success", "message": "All shape files are already uploaded"})

        # Process the fetched data
        year_shape_files = {}
        for row in rows:
            year = row[0]  # Assuming the year is the first column in the table
            place_city = row[1]  # Assuming the city is the second column
            shape_file = row[2]  # Assuming the shape file URL is the third column
            shape_file_name=row[3]
            if year not in year_shape_files:
                year_shape_files[year] = []
            year_shape_files[year].append({"place_city": place_city, "shape_file": shape_file,"shape_file_name":shape_file_name})

        return Response({"status": "success", "shape_files_data": year_shape_files})
    


def process_shape_files_data(shape_files_data):
    logging_data = dict(shape_files_data)
    logger.debug(f"[API Call] {shape_files_data.__class__.__name__} create Data: {logging_data}")
    try:
        uploaded_files = []  # List to store details of uploaded shape files

        # Process the fetched data and create items in the STAC catalog
        catalog_root = "./stac-catalog/Shape_File_Data"

        for year, shp_file_data in shape_files_data.items():
            year_dir = os.path.join(catalog_root, str(year))
            os.makedirs(year_dir, exist_ok=True)

            try:
                catalog_path = os.path.join(year_dir, "catalog.json")
                catalog = pystac.Catalog.from_file(catalog_path)
            except FileNotFoundError:
                catalog = pystac.Catalog(id=f"{year}_stac-catalog", description=f"STAC Catalog for {year}")

            # Create a directory for Shape File Data
            shape_file_data_dir = os.path.join(year_dir, "Shape_File_Data")
            os.makedirs(shape_file_data_dir, exist_ok=True)

            for shp_file_info in shp_file_data:
                shp_file_url = shp_file_info["shape_file"]
                place_city = shp_file_info["place_city"]
                shape_file_name = shp_file_info["shape_file_name"]  # Using shape_file_name as item_id
                url_alias = shape_file_name.split(".")[0]  # Remove the file extension

                bbox = [0.0, 0.0, 1280.0, 720.0]  # Example bbox, replace with actual values
                geometry = {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [0.0, 720.0],
                            [0.0, 0.0],
                            [1280.0, 0.0],
                            [1280.0, 720.0],
                            [0.0, 720.0]
                        ]
                    ]
                }

                properties = {
                    "id": None,  # Replace with actual ID if available
                    "year": year,
                    "shp_file_url": shp_file_url,
                    "place_city": place_city,  # Assuming place_city is not available
                    "url_alias": url_alias  # Add url_alias field without the file extension
                    # Add other fields accordingly
                }

                # Construct item ID using shape_file_name
                item_id = f"{shape_file_name}-item"

                item = pystac.Item(
                    id=item_id,  # Using constructed item ID
                    geometry=geometry,
                    bbox=bbox,
                    datetime=datetime.now(),
                    properties=properties,
                )

                item.add_asset(
                    key="shape_file",
                    asset=pystac.Asset(
                        href=shp_file_url,
                        media_type=pystac.MediaType.GEOJSON  # Adjust media type based on your file type
                    )
                )

                catalog.add_item(item)
                # Update the is_uploaded status to True in the database
                uploaded_files.append({"place_city": place_city, "shape_file": shp_file_url, "id": item.id})

                # Update the is_uploaded status to True in the database
                update_is_uploaded_status(shp_file_url)

            # Save the catalog
            catalog.normalize_hrefs(year_dir)
            catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)

        return {"status": "success", "message": "Items added to STAC catalog and is_uploaded status updated", "data": uploaded_files}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def update_is_uploaded_status(shape_file_url):
    logger.debug(f"[API Call] update_is_uploaded_status [data fetched successfully] ")
    try:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE pub_shp_file_info SET is_uploaded = true WHERE shape_file = %s", [shape_file_url])
            connection.commit()
        return {"status": "success", "message": "is_uploaded status updated successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


from rest_framework.request import Request

@api_view(['POST'])
def add_shape_files_to_stac(request: Request):  # Specify Request type
    logging_data = dict(request.data)
    logger.debug(f"[API Call] post shape file as a item {request.data.__class__.__name__} create Data: {logging_data}")
    try:
        # Fetch shape files data from the request body
        shape_files_data = request.data.get('shape_files_data', {})
        
        # Process the fetched data and add shape files to the STAC catalog
        response = process_shape_files_data(shape_files_data)
        
        # Return the response
        return Response(response)
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=500)

    
    

@api_view(['GET'])
def get_all_shape_file_items(request):
    logger.debug(f"[API Call] get_all_shape_file_items {request} [data fetched successfully] ")
    # Path to the STAC catalog
    catalog_path = "./stac-catalog/Shape_File_Data"

    # List to store items
    items = []

    # Iterate through each main subfolder in the catalog
    for main_subfolder_name in os.listdir(catalog_path):
        main_subfolder_path = os.path.join(catalog_path, main_subfolder_name)
        print("--------main_subfolder_path----------", main_subfolder_path)

        # Check if the path is a directory
        if os.path.isdir(main_subfolder_path):
            # Iterate through each subfolder within the main subfolder
            for subfolder_name in os.listdir(main_subfolder_path):
                subfolder_path = os.path.join(main_subfolder_path, subfolder_name)
                print("--------subfolder_path----------", subfolder_path)

                # Check if the path is a directory
                if os.path.isdir(subfolder_path):
                    # Iterate through each item folder in the sub-subfolder
                    if subfolder_name.endswith('-item'):  # Check subfolder_name for expected format
                        item_folder_path = subfolder_path
                        print("--------item_folder_path----------", item_folder_path)

                        # Access files within the item folder
                        for file_name in os.listdir(item_folder_path):
                            # Check if the file is a JSON file
                            if file_name.endswith('-item.json'):
                                file_path = os.path.join(item_folder_path, file_name)

                                # Example: Read the content of JSON file
                                with open(file_path, 'r') as json_file:
                                    item_data = json.load(json_file)
                                    
                                    print("///-------item_data---------//",item_data)
                                    
                                    

                                    # Append item_data to the items list
                                    all_items=items.append(item_data)
# Format the items list into a desired structure for response
    formatted_items = []
    for item in items:
        formatted_item = {
            "id": item.get("id", ""),  # Assuming "id" is a key in the JSON
            "year": item.get("properties", {}).get("year", ""),  # Access "year" under "properties"
            "shp_file_url": item.get("properties", {}).get("shp_file_url", ""),  # Access "shp_file_url" under "properties"
            "urlalias": item.get("properties", {}).get("url_alias", ""),  # Access "urlalias" under "properties"
            # Add other fields accordingly
        }
        formatted_items.append(formatted_item)

    # Return the list of formatted items as part of the response data
    return Response({
        "status": "success",
        "message": "All items retrieved successfully",
        "data": formatted_items
    })                                  
    

@api_view(['GET'])
def get_shape_file_by_id(request, item_id):
    logger.debug(f"[API Call] get_shape_file_by_id {request} [data fetched successfully] ")
    # Path to the STAC catalog
    catalog_path = "./stac-catalog/Shape_File_Data"

    # List to store matched items
    matched_items = []

    # Iterate through each main subfolder in the catalog
    for main_subfolder_name in os.listdir(catalog_path):
        main_subfolder_path = os.path.join(catalog_path, main_subfolder_name)
        
        # Check if the path is a directory
        if os.path.isdir(main_subfolder_path):
            # Iterate through each subfolder within the main subfolder
            for subfolder_name in os.listdir(main_subfolder_path):
                subfolder_path = os.path.join(main_subfolder_path, subfolder_name)
                
                # Check if the path is a directory
                if os.path.isdir(subfolder_path):
                    # Check if the subfolder name matches the expected format
                    if subfolder_name.endswith('-item'):
                        item_folder_path = subfolder_path

                        # Access files within the item folder
                        for file_name in os.listdir(item_folder_path):
                            # Check if the file is a JSON file
                            if file_name.endswith('-item.json'):
                                file_path = os.path.join(item_folder_path, file_name)

                                # Read the content of JSON file
                                with open(file_path, 'r') as json_file:
                                    item_data = json.load(json_file)

                                    # Check if the item ID matches the requested ID
                                    if item_data.get("id") == item_id:
                                        matched_items.append(item_data)

    # Format the matched item into a desired structure for response
    formatted_items = []
    for item in matched_items:
        formatted_item = {
            "id": item.get("id", ""),
            "year": item.get("properties", {}).get("year", ""),
            "shp_file_url": item.get("properties", {}).get("shp_file_url", ""),
            "urlalias": item.get("properties", {}).get("urlalias", ""),
            # Add other fields accordingly
        }
        formatted_items.append(formatted_item)

    # Return the list of formatted items as part of the response data
    return Response({
        "status": "success",
        "message": f"Item with ID '{item_id}' retrieved successfully",
        "data": formatted_items
    })
    
    
#import settings
catalog_path = "./stac-catalog"

@api_view(['PUT'])
def update_shape_file_items(request):
    logger.debug(f"[API Call] update_shape_file_items {request} [data fetched successfully] ")
    try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog/Shape_File_Data"  # Use Django settings to get the catalog path

        # Assume that in request.data, we got the updated data
        updated_data = request.data
        
        # List to store individual item update responses
        item_update_responses = []

        # Function to update a specific STAC item
        def update_stac_item(item_path, updated_data):
            # Load the STAC item from the file path
            with open(item_path, 'r') as f:
                item_data = json.load(f)
                
            # Update item properties with the provided data
            item_data['properties']['id'] = updated_data.get('id', item_data['properties']['id'])
            item_data['properties']['year'] = updated_data.get('year', item_data['properties']['year'])
            item_data['properties']['shp_file_url'] = updated_data.get('shp_file_url', item_data['properties']['shp_file_url'])
            item_data['properties']['urlalias'] = updated_data.get('urlalias', item_data['properties']['urlalias'])
            # Add other fields accordingly
            
            # Write the updated item data back to the file
            with open(item_path, 'w') as f:
                json.dump(item_data, f, indent=4)  # Overwrite the file with updated data
            
            # Collect the updated properties and return success response
            updated_properties = item_data['properties']
            return {
                "status": "success",
                "message": f"Item updated successfully: {updated_properties['id']}",
                "data": updated_properties
            }

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
                                    # Check if the file is a JSON file
                                    if file_name.endswith('-item.json'):
                                        file_path = os.path.join(item_folder_path, file_name)

                                        # Update the STAC item with the provided data
                                        update_response = update_stac_item(file_path, updated_data)
                                        item_update_responses.append(update_response)

        # Return the collected item update responses in the overall response
        return Response({
            "status": "success",
            "message": "All items updated successfully",
            "data": item_update_responses
        })
    
    except Exception as e:
        return Response({"status": "error", "message": str(e)})
    


@api_view(['GET'])
def sb_shape_file_by_year(request, **kwargs):
    logger.debug(f"[API Call] sb_shape_file_by_year {request} [data fetched successfully] ")
    try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog/Shape_File_Data"

        # List to store filtered items
        filtered_items = []

        # Get the list of selected years from query parameters
        query_years = request.GET.getlist('selectedYears')
        query_years = [param.replace('%20', ' ') for param in query_years]

        # Get limit and offset from query parameters
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))

        # Iterate through each main subfolder (year) in the catalog
        for year_folder_name in os.listdir(catalog_path):
            year_folder_path = os.path.join(catalog_path, year_folder_name)

            # Check if the path is a directory (representing a year)
            if os.path.isdir(year_folder_path):
                # Iterate through each item folder in the year folder
                for item_folder_name in os.listdir(year_folder_path):
                    # Check if the folder name ends with '-item'
                    if item_folder_name.endswith('-item'):
                        # Construct the full path to the item folder
                        item_folder_path = os.path.join(year_folder_path, item_folder_name)

                        # Access files within the item folder
                        for file_name in os.listdir(item_folder_path):
                            # Check if the file is a JSON file
                            if file_name.endswith('-item.json'):
                                file_path = os.path.join(item_folder_path, file_name)

                                # Load the content of the JSON file
                                with open(file_path, 'r') as json_file:
                                    item_data = json.load(json_file)

                                    # Check if the 'properties' key is present and is a dictionary
                                    if 'properties' in item_data and isinstance(item_data['properties'], dict):
                                        # Extract the year from the folder name
                                        item_year = year_folder_name

                                        # Check if the item's year matches any of the selected years
                                        if item_year in query_years:
                                            # Extract specific fields for response
                                            response_item = {
                                                "id": item_data.get('id'),
                                                "year": item_year,
                                                "shp_file_url": item_data['properties'].get('shp_file_url'),
                                                "datetime": item_data['properties'].get('datetime'),
                                                "place_city": item_data['properties'].get('place_city')
                                            }
                                            filtered_items.append(response_item)

        # Apply limit and offset to the filtered items
        paginated_items = filtered_items[offset:offset + limit]

        # Return the paginated response with the count of total filtered items
        response_data = {"data": paginated_items, "count": len(filtered_items)}
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def sb_shape_file_by_place(request, **kwargs):
    logger.debug(f"[API Call] sb_shape_file_by_place {request} [data fetched successfully] ")
    try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog/Shape_File_Data"

        # List to store filtered items
        filtered_items = []

        # Get the list of selected place cities from query parameters
        query_cities = request.GET.getlist('selectedPlace')
        query_cities = [param.replace('%20', ' ') for param in query_cities]

        # Get limit and offset from query parameters
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))

        # Iterate through each main subfolder (year) in the catalog
        for year_folder_name in os.listdir(catalog_path):
            year_folder_path = os.path.join(catalog_path, year_folder_name)

            # Check if the path is a directory (representing a year)
            if os.path.isdir(year_folder_path):
                # Iterate through each item folder in the year folder
                for item_folder_name in os.listdir(year_folder_path):
                    # Check if the folder name ends with '-item'
                    if item_folder_name.endswith('-item'):
                        # Construct the full path to the item folder
                        item_folder_path = os.path.join(year_folder_path, item_folder_name)

                        # Access files within the item folder
                        for file_name in os.listdir(item_folder_path):
                            # Check if the file is a JSON file
                            if file_name.endswith('-item.json'):
                                file_path = os.path.join(item_folder_path, file_name)

                                # Load the content of the JSON file
                                with open(file_path, 'r') as json_file:
                                    item_data = json.load(json_file)

                                    # Check if the 'properties' key is present and is a dictionary
                                    if 'properties' in item_data and isinstance(item_data['properties'], dict):
                                        # Extract the place city from the item data
                                        place_city = item_data['properties'].get('place_city')
                                        print("**********place_city*************", place_city)

                                        # Check if the place city matches any of the selected cities
                                        if place_city in query_cities:
                                            # Extract specific fields for response
                                            response_item = {
                                                "id": item_data.get('id'),
                                                "year": year_folder_name,  # Use the year from the folder name
                                                "shp_file_url": item_data['properties'].get('shp_file_url'),
                                                "datetime": item_data['properties'].get('datetime'),
                                                "place_city": place_city
                                            }
                                            filtered_items.append(response_item)

        # Apply limit and offset to the filtered items
        paginated_items = filtered_items[offset:offset + limit]

        # Return the paginated response with the count of total filtered items
        response_data = {"data": paginated_items, "count": len(filtered_items)}
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 

@api_view(['GET'])
def search_side_bar_shape_file(request, **kwargs):
    logger.debug(f"[API Call] shape_file_main_section_data {request} [data fetched successfully] ")
    try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog/Shape_File_Data"

        # List to store items
        items = []

        # Iterate through each year folder in the catalog
        for year_folder_name in os.listdir(catalog_path):
            year_folder_path = os.path.join(catalog_path, year_folder_name)

            # Check if the path is a directory (representing a year)
            if os.path.isdir(year_folder_path):
                # Iterate through each item folder in the year folder
                for item_folder_name in os.listdir(year_folder_path):
                    item_folder_path = os.path.join(year_folder_path, item_folder_name)

                    # Check if the item folder name ends with '-item'
                    if item_folder_name.endswith('-item'):
                        # Access files within the item folder
                        for file_name in os.listdir(item_folder_path):
                            file_path = os.path.join(item_folder_path, file_name)

                            # Check if the file is a JSON file
                            if file_name.endswith('-item.json'):
                                # Read the content of JSON file
                                with open(file_path, 'r') as json_file:
                                    item_data = json.load(json_file)
                                    
                                    # Extract relevant information from properties dictionary
                                    properties = item_data.get('properties', {})
                                    place_city = properties.get("place_city", "")
                                    year = year_folder_name

                                    items.append({"place_city": place_city, "year": year})

        # Count occurrences of each place_city and year
        place_city_counts = {}
        year_counts = {}
        for item in items:
            place_city = item.get("place_city", "")
            year = item.get("year", "")
            if place_city:
                place_city_counts[place_city] = place_city_counts.get(place_city, 0) + 1
            if year:
                year_counts[year] = year_counts.get(year, 0) + 1

        # Format response
        place_city_response = [{"subhead": city, "count": count} for city, count in place_city_counts.items()]
        year_response = [{"subhead": year, "count": count} for year, count in year_counts.items()]

        response_data = {
            "place_city": place_city_response,
            "year": year_response
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        
    
@api_view(['GET'])
def shape_file_main_section_data(request, **kwargs):
    logger.debug(f"[API Call] shape_file_main_section_data {request} [data fetched successfully] ")
    try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog/Shape_File_Data"

        # Get limit and offset from the request query parameters
        limit = int(request.query_params.get('limit', 10))  # Default to 10 items per page
        offset = int(request.query_params.get('offset', 0))

        # List to store items
        items = []

        # Iterate through each year folder in the catalog
        for year_folder_name in os.listdir(catalog_path):
            year_folder_path = os.path.join(catalog_path, year_folder_name)

            # Check if the path is a directory (representing a year)
            if os.path.isdir(year_folder_path):
                # Iterate through each item folder in the year folder
                for item_folder_name in os.listdir(year_folder_path):
                    item_folder_path = os.path.join(year_folder_path, item_folder_name)

                    # Check if the item folder name ends with '-item'
                    if item_folder_name.endswith('-item'):
                        # Access files within the item folder
                        for file_name in os.listdir(item_folder_path):
                            file_path = os.path.join(item_folder_path, file_name)

                            # Check if the file is a JSON file
                            if file_name.endswith('-item.json'):
                                # Read the content of JSON file
                                with open(file_path, 'r') as json_file:
                                    item_data = json.load(json_file)
                                    
                                    # Extract relevant information from properties dictionary
                                    properties = item_data.get('properties', {})
                                    response_data = {
                                        "id": item_data.get('id', ''),  # Assuming 'id' is directly under item_data
                                        "place_city": properties.get("place_city", ""),
                                        "year": year_folder_name,  # Use the year folder name as the year
                                        "shp_file_url": properties.get("shp_file_url", ""),
                                        "url_alias": properties.get("url_alias", ""),
                                    }

                                    items.append(response_data)

        # Apply limit and offset to the list of items
        paginated_items = items[offset: offset + limit]

        # Return the paginated response
        response_data = {"data": paginated_items, "count": len(items)}
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


import os
import logging
from datetime import datetime
import pystac
from pystac import Catalog, Item, Asset
from rest_framework.decorators import api_view
from rest_framework.response import Response

logger = logging.getLogger(__name__)

@api_view(['POST'])
def post_shape_file(request):
    logging_data = request.data
    logger.debug(f"[API Call] {request.__class__.__name__} create Data: {logging_data}")

    try:
        shape_files_data = logging_data.get('shape_files_data', [])
        uploaded_files = []  # List to store details of uploaded shape files

        # Process the fetched data and create items in the STAC catalog
        catalog_root = "./stac-catalog/Shape_File_Data"

        for shp_file_data in shape_files_data:
            year = shp_file_data["year"]
            year_dir = os.path.join(catalog_root, str(year))
            os.makedirs(year_dir, exist_ok=True)

            try:
                catalog_path = os.path.join(year_dir, "catalog.json")
                catalog = Catalog.from_file(catalog_path)
            except FileNotFoundError:
                catalog = Catalog(id=f"{year}_stac-catalog", description=f"STAC Catalog for {year}")

            # Create a directory for Shape File Data
            shape_file_data_dir = os.path.join(year_dir, "Shape_File_Data")
            os.makedirs(shape_file_data_dir, exist_ok=True)

            for shp_file_info in shp_file_data["files"]:
                shp_file_url = shp_file_info["shp_file_url"]
                place_city = shp_file_info.get("place_city", "Unknown")  # Provide a default value if not available
                shape_file_name = shp_file_info["shape_file_name"]  # Using shape_file_name as item_id
                url_alias = os.path.splitext(shape_file_name)[0]  # Remove the file extension

                bbox = [0.0, 0.0, 1280.0, 720.0]  # Example bbox, replace with actual values
                geometry = {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [0.0, 720.0],
                            [0.0, 0.0],
                            [1280.0, 0.0],
                            [1280.0, 720.0],
                            [0.0, 720.0]
                        ]
                    ]
                }

                properties = {
                    "year": year,
                    "shp_file_url": shp_file_url,
                    "place_city": place_city,
                    "url_alias": url_alias  # Add url_alias field without the file extension
                    # Add other fields accordingly
                }

                # Construct item ID using shape_file_name
                item_id = f"{shape_file_name}-item"

                item = Item(
                    id=item_id,
                    geometry=geometry,
                    bbox=bbox,
                    datetime=datetime.now(),
                    properties=properties,
                )

                item.add_asset(
                    key="shape_file",
                    asset=Asset(
                        href=shp_file_url,
                        media_type=pystac.MediaType.GEOJSON  # Adjust media type based on your file type
                    )
                )

                catalog.add_item(item)
                # Update the is_uploaded status to True in the database
                uploaded_files.append({"place_city": place_city, "shape_file": shp_file_url, "id": item.id})

                # Update the is_uploaded status to True in the database
                update_is_uploaded_status(shp_file_url)  # Ensure this function is defined elsewhere

            # Save the catalog
            catalog.normalize_hrefs(year_dir)
            catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)

        return Response({"status": "success", "message": "Items added to STAC catalog and is_uploaded status updated", "data": uploaded_files})
    except Exception as e:
        logger.error(f"Error in post_shape_file: {str(e)}")
        return Response({"status": "error", "message": str(e)}, status=500)



