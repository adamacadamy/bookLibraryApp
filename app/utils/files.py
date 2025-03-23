import os
import uuid

from app.config.uploads import ALLOWED_EXTENSIONS


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file_to_upload_folder(image_file):
    if image_file and allowed_file(image_file.filename):
        # Dynamically get the absolute path to the uploads folder
        upload_folder = os.path.join(os.path.dirname(__file__), "..", "uploads")
        upload_folder = os.path.abspath(upload_folder)

        # Ensure the uploads folder exists
        os.makedirs(upload_folder, exist_ok=True)

        # Generate a unique filename using UUID and preserve the file extension
        file_extension = os.path.splitext(image_file.filename)[
            1
        ]  # Get the file extension
        unique_filename = (
            f"{uuid.uuid4().hex}{file_extension}"  # Generate a unique filename
        )

        # Construct the full file path
        file_path = os.path.join(upload_folder, unique_filename)

        # Save the file
        image_file.save(file_path)

        # Return the URL to access the image
        return f"/api/Book/images/{unique_filename}"
    return None
