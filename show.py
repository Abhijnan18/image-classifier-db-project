import os
import io
import mysql.connector
from PIL import Image
from IPython.display import display  # Use this for Jupyter Notebook or IPython environment

# Connect to MySQL
db_connection = mysql.connector.connect(
    host='Abhijnans-MacBook-Pro.local',
    user='root',
    password='189@2003ihba',
    database="ImageDatabase"
)
cursor = db_connection.cursor()

# Function to display images with labels
def display_images():
    cursor.execute("SELECT id, filename, description, image_data FROM Images")
    records = cursor.fetchall()

    for record in records:
        image_id, filename, description, img_data = record
        img = Image.open(io.BytesIO(img_data))
        
        # Display the image
        print(f"Image ID: {image_id}, Filename: {filename}, Label: {description}")
        display(img)  # Use this for Jupyter Notebook or IPython environment

if __name__ == "__main__":
    display_images()

    # Close the database connection
    cursor.close()
    db_connection.close()
