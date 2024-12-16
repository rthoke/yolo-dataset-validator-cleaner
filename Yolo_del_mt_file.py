import os

# Path to the dataset
dataset_path = 'Dataset_path'

# Folder to check ('train', 'valid', 'test')
folder = 'test'

# Paths to images and labels directories
labels_path = os.path.join(dataset_path, folder, 'labels')
images_path = os.path.join(dataset_path, folder, 'images')


def check_empty_labels(labels_path):
    """
    Checks for empty YOLO label files in the specified path.
    
    Args:
        labels_path (str): Path to the YOLO labels directory.
    
    Returns:
        list: List of empty label files.
    """
    empty_files = []
    total_files = 0

    for label_file in os.listdir(labels_path):
        if label_file.endswith('.txt'):
            total_files += 1
            label_path = os.path.join(labels_path, label_file)
            
            # Check if the file is empty (either 0 bytes or no content)
            if os.path.getsize(label_path) == 0:
                empty_files.append(label_file)
            else:
                with open(label_path, 'r') as f:
                    content = f.read().strip()
                    if not content:  # If the file has no content after stripping whitespace
                        empty_files.append(label_file)
    
    print(f"Total label files checked: {total_files}")
    if empty_files:
        print(f"⚠️ Empty label files found ({len(empty_files)}):")
        for empty_file in empty_files:
            print(f" - {empty_file}")
    else:
        print("✅ No empty label files found!")
    
    return empty_files


def delete_labels_and_images(empty_label_files, labels_path, images_path):
    """
    Deletes the empty label files and their corresponding image files.
    
    Args:
        empty_label_files (list): List of empty label files to delete.
        labels_path (str): Path to the YOLO labels directory.
        images_path (str): Path to the images directory.
    """
    for label_file in empty_label_files:
        # Delete the label file
        label_path = os.path.join(labels_path, label_file)
        if os.path.exists(label_path):
            os.remove(label_path)
            print(f"🗑️ Deleted label file: {label_file}")
        
        # Find the corresponding image file with the same name but different extension (.jpg, .jpeg, .png)
        image_name_without_ext = os.path.splitext(label_file)[0]
        for ext in ['.jpg', '.jpeg', '.png']:
            image_path = os.path.join(images_path, image_name_without_ext + ext)
            if os.path.exists(image_path):
                os.remove(image_path)
                print(f"🗑️ Deleted corresponding image file: {image_name_without_ext + ext}")


# Step 1: Check for empty label files
empty_label_files = check_empty_labels(labels_path)

# Step 2: Delete empty label files and their corresponding image files
delete_labels_and_images(empty_label_files, labels_path, images_path)
