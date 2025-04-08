import os


def rename_imgs_ascending(image_folder):
    image_files = sorted(os.listdir(image_folder))
    image_files = [f for f in image_files if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    for idx, old_name in enumerate(image_files, start=1):
        new_name = f"image_{idx:04d}{os.path.splitext(old_name)[-1]}"  # Preserve the file extension

        old_path = os.path.join(image_folder, old_name)
        new_path = os.path.join(image_folder, new_name)

        os.rename(old_path, new_path)

        print(f"Renamed: {old_name} -> {new_name}")

    print("Renaming complete!")

def delete_alternate(image_folder):
    """
    If the dataset is huge, it can be convenient to delete the alternate images.
    This assumes that the images are in continuous fashion, and very minor difference
    between consecutive images.
    """
    # Start and end indices
    start = 1
    end = len(os.listdir(image_folder))
    image_files = sorted(os.listdir(image_folder))

    # Filter out files that don't match the expected pattern (image_0001 to image_1400)
    image_files = [f for f in image_files if f.startswith("image_") and f[6:10].isdigit()]

    for idx in range(start, end + 1):
        image_name = f"image_{idx + 1:04d}.jpg"  # Name of the image to keep or delete
        
        if image_name not in image_files:
            continue  # Skip if the file is not in the folder

        if (idx + 1) % 2 == 0:  # Delete odd-numbered images
            image_path = os.path.join(image_folder, image_name)
            try:
                os.remove(image_path)
                print(f"Deleted: {image_name}")
            except Exception as e:
                print(f"Error deleting {image_name}: {e}")

    print("Alternate images deleted successfully.")

if __name__ == "__main__":
    image_folder = "" 
    rename_imgs_ascending(image_folder)

