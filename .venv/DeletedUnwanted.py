import os

# Define the paths to the directories containing original and segmented images
original_images_path = 'D:\\New folder\\Lesions MN(NV) masked data orignal'
segmented_images_path = 'D:\\New folder\\Maped Lesion Masked data MN(NV)'

# Get lists of the original and segmented images
original_images = set(f.replace('.jpg', '') for f in os.listdir(original_images_path) if f.endswith('.jpg'))
segmented_images = set(f.replace('_segmentation.png', '') for f in os.listdir(segmented_images_path) if f.endswith('_segmentation.png'))

# Identify segmented images that do not have corresponding original images
unmatched_segmented_images = segmented_images - original_images

# Delete unmatched segmented images
for unmatched_image in unmatched_segmented_images:
    file_path = os.path.join(segmented_images_path, unmatched_image + '_segmentation.png')
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    else:
        print(f"File not found: {file_path}")

print("Cleanup completed.")
