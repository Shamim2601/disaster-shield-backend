import schemas

# Set your Cloudinary credentials
# ==============================
from dotenv import load_dotenv
load_dotenv()

# Import the Cloudinary libraries
# ==============================
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Import to format the JSON responses
# ==============================
import json

# Set configuration parameter: return "https" URLs by setting secure=True  
# ==============================
config = cloudinary.config(secure=True)

# Log the configuration
# ==============================
# print("****1. Set up and configure the SDK:****\nCredentials: ", config.cloud_name, config.api_key, "\n")

class ImageInfo():
    secure_url:str
    public_id:str
    def __init__(self,secure_url:str,public_id:str):
        self.secure_url=secure_url
        self.public_id=public_id

def uploadImage(data_bytes,*,width:int=100,height:int=100,folder_name='')->schemas.Image:
  response_dict=cloudinary.uploader.upload(data_bytes, unique_filename = False, overwrite=False,
                             folder=folder_name)
  image_info=ImageInfo(response_dict["secure_url"],response_dict["public_id"])
  image=schemas.Image(image_id=image_info.public_id,url=image_info.secure_url)
  return image

def deleteImage(image_id:str):
  # print("image_id ",image_id)  
  cloudinary.uploader.destroy(public_id=image_id)

  # Build the URL for the image and save it in the variable 'srcURL'
  # srcURL = cloudinary.CloudinaryImage("quickstart_butterfly").build_url()

  # Log the image URL to the console. 
  # Copy this URL in a browser tab to generate the image on the fly.
  # print("****2. Upload an image****\nDelivery URL: ", srcURL, "\n")
  