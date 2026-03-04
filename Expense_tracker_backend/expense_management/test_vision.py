from google.cloud import vision
import os

# key  $env:GOOGLE_APPLICATION_CREDENTIALS="C:\Smart Expense Tracker\Expense_tracker_backend\google-vision-key.json"

client = vision.ImageAnnotatorClient()

with open("C:\Users\2001k\Desktop\sample_bill.jpeg","rb") as img:
    content=img.read()

image=vision.Image(content=content)
response=client.text_detection(image=image)
texts = response.text_annotations
print("Detected Text:")
if texts:
    print(texts[0].description)
else:
    print("No text found.")
