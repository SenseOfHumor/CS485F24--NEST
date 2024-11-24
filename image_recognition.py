import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from pathlib import Path

load_dotenv()
API_KEY = os.getenv("API")

def get_url_response(image_path):
    """
    Parse the image for handwritten text and extract usernames and passwords.

    Extended description of function:
    Parse the image for handwritten text, focusing on identifying usernames and their corresponding passwords. 
    The output should be formatted in JSON with username as the key and password as the value. 
    Ignore any irrelevant information or text outside the main content area.
    """
    ## config client
    genai.configure(api_key=API_KEY)
    
    ## image upload
    uploaded_file = genai.upload_file(Path(image_path))
    print(f"Uploaded file: {uploaded_file}")

    ## internal prompt
    prompt = """
    Please extract the data from this picture and return only in JSON format 
    """
    
    # Initialize the generative model
    model = genai.GenerativeModel("gemini-1.5-pro-latest")  # Change to the correct version if needed
    
    # Generate content using the uploaded file and prompt
    result = model.generate_content([uploaded_file, "\n\n", prompt])

    return result.text

def json_to_list(json_response):
    """
    Extract the username and password pairs from the image.

    Extended description of function: 
    Format the output as a JSON list, where each element is a dictionary with "username" and "password" keys.
    For example:
    [
        {"username": "swa2314@gmail.com", "password": "dog123"},
        {"username": "NSYNC", "password": "112swap341"},
        ...
    ]
    """
    if not isinstance(json_response, list):
        return []
    return [(item["username"], item["password"]) for item in json_response if "username" in item and "password" in item]

def main():
    image_path = "path_to_image.jpg"  # Update this path to your actual image file
    response = get_url_response("/Users/swap/Documents/GitHub/CS485--NEST--F2024/IMG_0520.jpeg")
    ## get res
    if response:
        print("Response received:", response)
    else:
        print("Failed to get a response from the API.")

if __name__ == "__main__":
    main()
