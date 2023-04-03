import io
import os

# Import the Google Cloud client libraries
from google.cloud import vision
from google.cloud import vision_v1



# Set the path to your Google Cloud credentials file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/prateekwadhwa/Downloads/password3.json'

# Initialize the Google Cloud Vision API client
client = vision.ImageAnnotatorClient()

# Set the path to your image file
file_name = 'Trial/Workload0001.jpg'

# Read the image file into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

# Create an Image object and specify the image content
image = vision_v1.types.Image(content=content)

# Use the Google Cloud Vision API to detect text in the image
response = client.text_detection(image=image)

# Extract the text from the response
text = response.text_annotations[0].description

# Print the extracted text
with open("extract.txt", "w") as file:
    # Write the text to the file
    file.write(text)
