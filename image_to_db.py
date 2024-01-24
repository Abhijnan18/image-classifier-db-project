import os
import mysql.connector
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions

# Connect to MySQL
db_connection = mysql.connector.connect(
    host='Abhijnans-MacBook-Pro.local',
    user='root',
    password='189@2003ihba',
    database="ImageDatabase"
)
cursor = db_connection.cursor()

# Load pre-trained ResNet50 model
model = ResNet50(weights='imagenet')

# Function to classify an image
def classify_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = preprocess_input(img_array.reshape((1, 224, 224, 3)))
    predictions = model.predict(img_array)
    decoded_predictions = decode_predictions(predictions)[0]
    return decoded_predictions

# Function to process images in a folder
def process_images(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.jpeg', '.png','.webp')):
            img_path = os.path.join(folder_path, filename)
            predictions = classify_image(img_path)
            top_prediction = predictions[0]
            label = top_prediction[1]
            description = top_prediction[2]

            # Insert the classified image into the database
            sql = "INSERT INTO Images (filename, description, image_data) VALUES (%s, %s, %s)"
            with open(img_path, 'rb') as img_file:
                img_data = img_file.read()
                values = (filename, f"{label}: {description}", img_data)
                cursor.execute(sql, values)
                db_connection.commit()

if __name__ == "__main__":
    folder_path = "/Users/abhijnans/image-classifier-db-project/img"
    process_images(folder_path)

    # Close the database connection
    cursor.close()
    db_connection.close()
