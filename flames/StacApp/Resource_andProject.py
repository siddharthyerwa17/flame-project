from Logger import logger
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import pystac
import urllib.parse
from datetime import datetime
from .models import Feedback
from .serializer import FeedbackSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from django.db.models.signals import post_save
from django.dispatch import receiver
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.db.models.signals import post_save
from string import Template

#### Post api to post stac item for Resource and publication and this item will be saved in folder 
#Resources_and_Publication
@api_view(['POST'])
def add_Resources_and_Publication_stac(request):
    logging_data = dict(request.data)
    logger.debug(f"[API Call] add_Resources_and_Publication_Post {request.__class__.__name__} create Data: {logging_data}")
    data = request.data
    title = data.get("title", None)
    if title is None:
        return Response({"status": "error", "message": "Title is required."}, status=400)

    catalog_root = "./stac-catalog/Resources_and_Publication"  # Change the catalog root

    title_dir = os.path.join(catalog_root, title)
    os.makedirs(title_dir, exist_ok=True)

    try:
        catalog_path = os.path.join(title_dir, "catalog.json")
        catalog = pystac.Catalog.from_file(catalog_path)
    except FileNotFoundError:
        catalog = pystac.Catalog(id=f"{title}_stac-catalog", description=f"STAC Catalog for {title}")

    item_id = f"{title}-item"

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
        "id": data.get("id", None),
        "thumbnail": request.data.get("thumbnail", ""),
        "author": request.data.get("author", ""),
        "title": title,
        "description": request.data.get("description", "")
        # Add other fields accordingly
    }

    # Check if the item is a resource or a publication
    is_resource = data.get("is_resource", False)
    is_publication = data.get("is_publication", False)

    # Add is_resource and is_publication fields to properties
    properties["is_resource"] = is_resource
    properties["is_publication"] = is_publication

    item = pystac.Item(
        id=item_id,
        geometry=geometry,
        bbox=bbox,
        datetime=datetime.now(),
        properties=properties,
    )

    catalog.add_item(item)

    catalog.normalize_hrefs(title_dir)
    catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)

    return Response({"status": "success", "message": "Item added to STAC catalog", "data": properties})

#### Post api to post stac item for Projects and this item will be saved in folder 
#Projects
@api_view(['POST'])
def add_Projects_to_stac(request):
    data = request.data
    title = data.get("title", None)
    if title is None:
        return Response({"status": "error", "message": "Title is required."}, status=400)

    catalog_root = "./stac-catalog/Projects"  # Change the catalog root

    title_dir = os.path.join(catalog_root, title)
    os.makedirs(title_dir, exist_ok=True)

    try:
        catalog_path = os.path.join(title_dir, "catalog.json")
        catalog = pystac.Catalog.from_file(catalog_path)
    except FileNotFoundError:
        catalog = pystac.Catalog(id=f"{title}_stac-catalog", description=f"STAC Catalog for {title}")

    item_id = f"{title}-item"

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
        "id": data.get("id", None),
        "thumbnail": request.data.get("thumbnail", ""),
       # "author": request.data.get("author", ""),
        "title": title,
        "description": request.data.get("description", "")
        # Add other fields accordingly
    }

    item = pystac.Item(
        id=item_id,
        geometry=geometry,
        bbox=bbox,
        datetime=datetime.now(),
        properties=properties,
    )

    catalog.add_item(item)

    catalog.normalize_hrefs(title_dir)
    catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)

    return Response({"status": "success", "message": "Item added to STAC catalog","data":properties})


@api_view(['GET'])
def get_Resources_and_Publication_stac(request):
    catalog_root = "./stac-catalog/Resources_and_Publication"
    items = []
    
    resource_selected = request.query_params.get("resource", None)  # Check if resource is selected
    publication_selected = request.query_params.get("publication", None)  # Check if publication is selected
    
    for root, dirs, files in os.walk(catalog_root):
        for file in files:
            if file.endswith(".json"):
                item_path = os.path.join(root, file)
                try:
                    item = pystac.Item.from_file(item_path)
                    item_dict = item.to_dict()
                    properties = item_dict.pop("properties", {})  # Remove properties from item_dict
                    id_value = item_dict.pop("id", "")  # Extract ID from properties
                    properties["id"] = id_value  # Add ID to properties
                    
                    if resource_selected == "true" and properties.get("is_resource", False):
                        items.append({"properties": properties})  # Include resource data if selected
                    elif publication_selected == "true" and not properties.get("is_resource", False):
                        items.append({"properties": properties})  # Include publication data if selected

                except Exception as e:
                    # Handle if there's an error loading the item
                    print(f"Error loading item: {item_path}, {e}")

    if items:
        return Response({"status": "success", "items": items})
    else:
        return Response({"status": "error", "message": "No items found."}, status=404)
    
    
    
    
    
    
    
# GET API to retrieve information about items in the Projects catalog
@api_view(['GET'])
def get_Projects_stac(request):
    catalog_root = "./stac-catalog/Projects"
    items=[]
    for root, dirs,files in os.walk(catalog_root):
        for file in files:
            if file.endswith(".json") :
                item_path = os.path.join(root, file)
                try:
                    item = pystac.Item.from_file(item_path)
                    item_dict = item.to_dict()
                    properties = item_dict.pop("properties", {})  # Remove properties from item_dict
                    id_value = item_dict.pop("id", "")  # Extract ID from properties
                    properties["id"]=id_value  # Add ID to properties
                    items.append({"properties": properties})  # Include ID outside properties
                except Exception as e:
                    # Handle if there's an error loading the item
                    print(f"Error loading item: {item_path}, {e}")

    if items:
        return Response({"status": "success", "items": items})
    else:
        return Response({"status": "error", "message": "No items found."}, status=404)
    


@api_view(['GET'])
def get_filtered_pubndResource_stac_items(request):
    logger.debug(f"[API Call] get_filtered_pubndResource_stac_items {request} [data fetched successfully] ")
    catalog_root = "./stac-catalog/Resources_and_Publication"
    items = []

    # Extract query parameters
    author_filter = request.query_params.get("author", None)
    title_filter = request.query_params.get("title", None)
    thumbnail_filter = request.query_params.get("thumbnail", None)

    for root, dirs, files in os.walk(catalog_root):
        for file in files:
            if file.endswith(".json"):
                item_path = os.path.join(root, file)
                try:
                    item = pystac.Item.from_file(item_path)
                    properties = item.properties

                    # Extract required fields
                    author = properties.get("author", "")
                    title = properties.get("title", "")
                    thumbnail = properties.get("thumbnail", "")
                    description = properties.get("description", "")  # Extract description

                    # Check if item matches all provided filters
                    if (not author_filter or author == author_filter) and \
                       (not title_filter or title == title_filter) and \
                       (not thumbnail_filter or thumbnail == thumbnail_filter):
                        items.append({
                            "author": author,
                            "title": title,
                            "thumbnail": thumbnail,
                            "description": description  # Include description in response
                            # Add other fields accordingly
                        })
                except Exception as e:
                    # Handle if there's an error loading the item
                    print(f"Error loading item: {item_path}, {e}")

    if items:
        return Response({"status": "success", "items": items})
    else:
        return Response({"status": "error", "message": "No items found."}, status=404)
    
@api_view(['GET'])
def get_filtered_Projects_stac_items(request):
    catalog_root = "./stac-catalog/Projects"
    items = []

    # Extract query parameters
    author_filter = request.query_params.get("author", None)
    title_filter = request.query_params.get("title", None)
    thumbnail_filter = request.query_params.get("thumbnail", None)

    for root, dirs, files in os.walk(catalog_root):
        for file in files:
            if file.endswith(".json"):
                item_path = os.path.join(root, file)
                try:
                    item = pystac.Item.from_file(item_path)
                    properties = item.properties

                    # Extract required fields
                    author = properties.get("author", "")
                    title = properties.get("title", "")
                    thumbnail = properties.get("thumbnail", "")

                    # Check if item matches all provided filters
                    if (not author_filter or author == author_filter) and \
                       (not title_filter or title == title_filter) and \
                       (not thumbnail_filter or thumbnail == thumbnail_filter):
                        items.append({
                            "author": author,
                            "title": title,
                            "thumbnail": thumbnail
                            # Add other fields accordingly
                        })
                except Exception as e:
                    # Handle if there's an error loading the item
                    print(f"Error loading item: {item_path}, {e}")

    if items:
        return Response({"status": "success", "items": items})
    else:
        return Response({"status": "error", "message": "No items found."}, status=404)


#  api to save the feed back and send an email to the user 
class FeedbackViewSet(ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

@receiver(post_save, sender=Feedback)
def send_feedback_email(sender, instance, created, **kwargs):
    logger.debug(f"[API Call] send_feedback_email {instance.email_id} [mail send successfully] ")
    if created:
        # Send email to your email
        to_email_themaplab = "contact.themaplab@gmail.com"
        subject_themaplab = "Feedback Received"
        message_themaplab = f"Feedback message: {instance.message}\n\nFrom: {instance.email_id}"
        send_email(to_email_themaplab, subject_themaplab, message_themaplab)

        # Send email to the user's email
        # to_email_user = instance.email_id
        # subject_user = "Feedback Confirmation"
        # message_user = "Thank you for your feedback!"
        # Send email to the user's email
        to_email_user = instance.email_id
        subject_user = "Feedback Confirmation"
        # Fill in the template with the user's name
        user_name = instance.name  # Assuming 'name' is a field in Feedback model
        message_user = Template(email_template).substitute(name=user_name)
        send_email(to_email_user, subject_user, message_user)

# 

# Define the email template
email_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Feedback Confirmation</title>
</head>
<body style="font-family: Arial, sans-serif;">

    <p>Hi $name,</p>

    <p>Thank you for writing into us today! This is an auto-reply to let you know that we have received your message. We will respond to you as soon as possible.</p>

    <p>You can also connect with us on <a href="https://www.flame.edu.in/research/centres/centre-for-sustainability-environment-and-climate-change">Linkedin</a>.</p>

    <p>Thank you,<br>Team Map Lab</p>

</body>
</html>
"""

# Function to send email
def send_email(to_email, subject, message):
    # Email credentials
    sent_from = "themaplaborg@gmail.com"
    sent_from_password = "wbqr qqtk pyfn cpac"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart()
    msg['From'] = sent_from
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach message to the email
    msg.attach(MIMEText(message, 'html'))

    try:
        # Set up the SMTP server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        # Login to the email server
        server.login(sent_from, sent_from_password)
        # Send email
        server.sendmail(sent_from, to_email, msg.as_string())
        # Close the SMTP server connection
        server.close()
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)

# Modified function to send feedback email
def send_feedback_email(sender, instance, created, **kwargs):
    if created:
        # Send email to your email
        to_email_themaplab = "contact.themaplab@gmail.com"
        subject_themaplab = "Feedback Received"
        message_themaplab = f"Feedback message: {instance.message}\n\nFrom: {instance.email_id}"
        send_email(to_email_themaplab, subject_themaplab, message_themaplab)

        # Send email to the user's email
        to_email_user = instance.email_id
        subject_user = "Feedback Confirmation"
        # Fill in the template with the user's name
        user_name = instance.name  # Assuming 'name' is a field in Feedback model
        email_message = Template(email_template).substitute(name=user_name)
        send_email(to_email_user, subject_user, email_message)

    

    