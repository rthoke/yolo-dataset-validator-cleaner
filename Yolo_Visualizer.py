
#Path to the dataset
dataset_path = 'Dataset_Path'

# Folder to visualize ('train', 'valid', 'test')
folder = 'train'

# Class names as per the YOLOv8 YAML file
class_names = ["Classses"]

# Path to images and labels
images_path = os.path.join(dataset_path, folder, 'images')
labels_path = os.path.join(dataset_path, folder, 'labels')


def draw_bounding_boxes(image, label_path, class_names):
    """
    Draws bounding boxes on an image from the YOLO label file.
    
    Args:
        image (ndarray): The loaded image (numpy array).
        label_path (str): Path to the YOLO label (.txt) file.
        class_names (list): List of class names corresponding to the YOLO label indices.
    """
    height, width, _ = image.shape
    
    if not os.path.exists(label_path):
        print(f"Label file not found: {label_path}")
        return image
    
    with open(label_path, 'r') as file:
        for line in file:
            try:
                # Parse each line in the YOLO label file
                class_id, x_center, y_center, box_width, box_height = map(float, line.strip().split())
                
                # Convert YOLO format (x_center, y_center, width, height) to (x1, y1, x2, y2)
                x1 = int((x_center - box_width / 2) * width)
                y1 = int((y_center - box_height / 2) * height)
                x2 = int((x_center + box_width / 2) * width)
                y2 = int((y_center + box_height / 2) * height)
                
                # Draw bounding box on the image
                color = (0, 255, 0)  # Green color for the bounding box
                cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
                
                # Draw class label
                class_name = class_names[int(class_id)] if int(class_id) < len(class_names) else f'Class {int(class_id)}'
                print("label_path = ", label_path)
                print(class_name,"== " ,class_id)

                cv2.putText(image, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            except Exception as e:
                print(f"Error parsing line in {label_path}: {line}. Error: {e}")
    
    return image


def visualize_annotations(num_images=5):
    """
    Randomly selects and visualizes images with their YOLO annotations.
    
    Args:
        num_images (int): Number of images to visualize.
    """
    image_files = [f for f in os.listdir(images_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    if len(image_files) == 0:
        print(f"No images found in {images_path}.")
        return
    
    # Randomly select images to visualize
    random_images = random.sample(image_files, min(num_images, len(image_files)))
    
    for image_file in random_images:
        image_path = os.path.join(images_path, image_file)
        label_path = os.path.join(labels_path, image_file.replace(os.path.splitext(image_file)[1], '.txt'))
        
        # Load image using OpenCV
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to load image: {image_path}")
            continue
        
        # Draw YOLO bounding boxes on the image
        image_with_boxes = draw_bounding_boxes(image, label_path, class_names)
        
        # Convert BGR (OpenCV) to RGB (for matplotlib)
        image_rgb = cv2.cvtColor(image_with_boxes, cv2.COLOR_BGR2RGB)
        
        # Display the image with matplotlib
        plt.figure(figsize=(8, 8))
        plt.imshow(image_rgb)
        plt.title(f"Image: {image_file}")
        plt.axis('off')
        plt.show()


# Visualize 5 random annotated images from the dataset
visualize_annotations(num_images=15)
