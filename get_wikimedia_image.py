import requests
import os
from PIL import Image, ImageOps
from io import BytesIO

def get_wikimedia_image(person_name, save_path):
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": person_name,
        "prop": "pageimages",
        "format": "json",
        "pithumbsize": 1920  # Specify thumbnail size (1920 pixels wide)
    }
    response = requests.get(url, params=params)
    
    # Debug: Print status code and response content
    print(f"Request URL: {response.url}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    
    if response.status_code != 200:
        print("Failed to retrieve data from Wikimedia API.")
        return None
    
    data = response.json()

    pages = data.get('query', {}).get('pages', {})
    if pages:
        page = next(iter(pages.values()))  # Get the first page (should be only one)
        if 'thumbnail' in page:
            image_url = page['thumbnail']['source']
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            image_response = requests.get(image_url, headers=headers)
            
            # Debug: Print image request status code
            print(f"Image Request URL: {image_response.url}")
            print(f"Image Status Code: {image_response.status_code}")
            
            if image_response.status_code == 200:
                image = Image.open(BytesIO(image_response.content))
                
                # Resize and crop the image to fill the entire expected resolution
                expected_resolution = (1080, 1920)  # Example resolution
                image = ImageOps.fit(image, expected_resolution, Image.LANCZOS)
                
                # Save the image to the specified save_path
                image.save(save_path)
                print(f"Image saved to {save_path}")
                return save_path
            else:
                print("Failed to retrieve the image.")
                return None
    else:
        print("No pages found for the given person name.")
        return None