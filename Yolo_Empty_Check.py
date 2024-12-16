import os

# Path to the dataset
dataset_path = 'dataset_path'

# Folder to check ('train', 'valid', 'test')
folder = 'train'

# Path to the labels folder
labels_path = os.path.join(dataset_path, folder, 'labels')


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


# Run the function to check for empty label files
empty_files = check_empty_labels(labels_path)
