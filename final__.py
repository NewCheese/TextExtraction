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
folder_path = 'Trial'

dir_path = 'Trial/'

# get a list of the image files in the directory and sort them in the desired order
file_list = os.listdir(dir_path)
file_list.sort()
# Create/Open a text file named 'extract.txt'


with open("extract.txt", "w") as file:
    for filename in file_list:
    # check if the file is a JPG file
        if filename.endswith('.jpg'):
        # get the full path to the file
            file_path = os.path.join(dir_path, filename)
            with io.open(file_path, 'rb') as image_file:
                content = image_file.read()

# Create an Image object and specify the image content
                image = vision_v1.types.Image(content=content)

# Use the Google Cloud Vision API to detect text in the image
                response = client.text_detection(image=image)

# Extract the text from the response
                text = response.text_annotations[0].description
                
        # load the image and apply OCR
                file.write(text)

    print("Text extraction completed. Check 'extract.txt' for the results.")
