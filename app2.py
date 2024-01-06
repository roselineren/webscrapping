import requests

# Define the API endpoint
api_endpoint = "https://data.ademe.fr/data-fair/api/v1/datasets/agribalyse-31-synthese/raw"
#https://data.ademe.fr/data-fair/api/v1/datasets/agribalyse-31-synthese/full

# Function to check the connection with the API
def check_api_connection(url):
    try:
        # Send a GET request to the API
        response = requests.get(url)
        
        # Check the Content-Type of the response
        content_type = response.headers.get('Content-Type')
        
        if 'application/json' in content_type:
            # Handle JSON response
            if response.status_code == 200:
                return {'status': 'success', 'data': response.json()}
            else:
                return {'status': 'failed', 'message': 'Could not connect to API', 'status_code': response.status_code}
        elif 'text/csv' in content_type or 'application/csv' in content_type:
            # Handle CSV response
            return {'status': 'success', 'data': response.text}
        else:
            return {'status': 'failed', 'message': 'Unknown response format', 'content_type': content_type}
        
    except Exception as e:
        # If an exception occurs, return failure with the exception message
        return {'status': 'failed', 'message': str(e)}

# Since I can't make the actual request, I'll return a simulated success response.
simulated_response = check_api_connection(api_endpoint)

print(simulated_response)

import json


aliments_interdits = ["amandes", "noix", "noix de coco", "noix de cajou", "châtaignes", "noisettes", "noix de macadamia", "noix de pécan", "pignons", "pistaches", "cacahuète"]

with open('recettes.json', 'r', encoding='UTF-8') as f:
    recettes = json.load(f)

for recette in recettes:
    if 'tags' not in recette:
        recette['tags'] = []
    
    if not any(aliment in ' '.join(recette['ingredients']).lower() for aliment in aliments_interdits):
        recette['tags'].append('sans arachide')

with open('recettes.json', 'w', encoding='UTF-8') as f:
    json.dump(recettes, f, ensure_ascii=False, indent=4)
