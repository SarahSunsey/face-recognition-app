from PIL import Image
import os

def resize_images(folder_path, target_size=(216, 216)):
    """
    Resize images in the specified folder to the target size.

    Args:
        folder_path (str): Path to the folder containing images.
        target_size (tuple): Target size as (width, height) in pixels.

    Returns:
        None
    """
    # List all files in the folder
    files = os.listdir(folder_path)

    # Process each file in the folder
    for filename in files:
        # Check if the file is an image (e.g., PNG, JPG)
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            try:
                # Open the image file
                image_path = os.path.join(folder_path, filename)
                image = Image.open(image_path)

                # Resize the image
                resized_image = image.resize(target_size, Image.LANCZOS)

                # Save the resized image (overwrite the original)
                resized_image.save(image_path)

                print(f"Resized {filename} to {target_size}")

            except Exception as e:
                print(f"Error resizing {filename}: {e}")

if __name__ == "__main__":
    # Provide the path to the folder containing images
    folder_path = "images"

    # Specify the target size for resizing (e.g., 216x216 pixels)
    target_size = (216, 216)

    # Resize images in the specified folder
    resize_images(folder_path, target_size)
