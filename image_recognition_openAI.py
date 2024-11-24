import os
import base64
import datetime
from pymongo import MongoClient
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


## Keys and Clients
API_KEY = os.getenv("OAPI")
MONGO_URI = os.getenv("MONGO_URI")

## Initialize clients
openai_client = OpenAI(api_key=API_KEY)
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["password_manager"]  # db name
collection = db["credentials"]         # collection name

def extract_platforms_usernames_and_passwords(image_path):
    """
    Extract platforms, usernames, and passwords from an image using OpenAI API.

    Extended description of function:
    This function takes an image path as input, 
    uploads the image to the OpenAI API, and prompts the model to extract 
    platforms, usernames, and passwords from the image. 
    The extracted data is then returned in a structured format.

    Returns:
        list: A list of dictionaries containing platforms, usernames, and passwords.
    """
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    base64_image = encode_image(image_path)

    prompt = '''You will see a sample test image with randomly written platforms, usernames, and passwords.
    Your task is to extract the platforms, usernames, and passwords from the image and return them in a plain text format.
    Each line must be formatted as: platform:username:password
    Only use colons to separate fields. No extra text apart from platform, username, and password should be returned.
    '''

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }
    ]

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=500
    )

    result_text = response.choices[0].message.content
    res = (result_text.split("\n"))
    res = [line for line in res if ':' in line and line.strip()]

    return [
        {
            "platform": item.split(':')[0].strip(),
            "username": item.split(':')[1].strip(),
            "password": item.split(':')[2].strip()
        }
        for item in res
    ]

def upload_to_mongo(image_path):
    """
    Extract credentials and upload them to MongoDB.

    Extended description of function:
    This function takes an image path as input,
    extracts platforms, usernames, and passwords from the image using OpenAI API,
    and uploads the extracted data to a MongoDB collection.
    
    returns:
        None
    """
    credentials = extract_platforms_usernames_and_passwords(image_path)
    timestamp = datetime.datetime.utcnow()
    for cred in credentials:
        cred.update({
            "source_image": image_path,
            "created_at": timestamp,
            "updated_at": timestamp
        })
    collection.insert_many(credentials)
    print(f"Uploaded {len(credentials)} records to MongoDB.")

def search_credentials(query):
    """
    Search for credentials based on a query string.

    Extended description of function:
    This function searches the MongoDB collection for credentials
    that match the query string in either the platform or username fields.
    
    returns:
        list: A list of matching documents
    """
    results = collection.find({
        "$or": [
            {"username": {"$regex": query, "$options": "i"}},
            {"platform": {"$regex": query, "$options": "i"}}
        ]
    })
    return list(results)

def update_credential(platform, username, new_password):
    """
    Update a credential with a new password.

    Extended description of function:
    This function updates the password of a credential in the MongoDB collection
    based on the platform and username. It sets the new password and updates the
    "updated_at" field with the current timestamp.
    
    returns:
        dict: The updated document
    """
    updated_doc = collection.find_one_and_update(
        {"platform": platform, "username": username},
        {"$set": {"password": new_password, "updated_at": datetime.datetime.utcnow()}},
        return_document=True
    )
    return updated_doc

## TODO: Add option to use camera to take a picture and upload it

## TODO: Add function to suggest a strong password using OpenAI API
''' 
WorkFlow:
- when retrieving the credentials, check if the password is weak
- add a score between 0 - 9 to the password
- if below 5 (weak password), suggest a strong password
- if above 5 (strong password), do nothing
- if weak, suggest a strong password
- update the password in the database upon users request (optional)
- use alert to notify the user of the weak password and suggest a strong password
'''



