import os


def rename_images_in_folder(folder_path):
    # List all files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Sort files to ensure they are renamed in a consistent order
    files.sort()

    # Loop through each file and rename it
    for i, filename in enumerate(files, start=1):
        # Extract the file extension
        file_extension = os.path.splitext(filename)[1]

        # Create new filename in the format 'image1', 'image2', etc.
        new_filename = f"image{i}{file_extension}"

        # Get full paths for renaming
        src = os.path.join(folder_path, filename)
        dst = os.path.join(folder_path, new_filename)

        # Rename the file
        os.rename(src, dst)
        print(f"Renamed {src} to {dst}")


def rename_images_in_subfolders(dataset_folder):
    # Loop through all subfolders in the dataset folder
    for subdir in os.listdir(dataset_folder):
        subfolder_path = os.path.join(dataset_folder, subdir)

        if os.path.isdir(subfolder_path):  # Check if it's a folder
            print(f"Processing folder: {subfolder_path}")
            rename_images_in_folder(subfolder_path)


# Define the path to your dataset folder
dataset_folder = 'D:\\7th Semester\\FYP\\Datasets\\All data checked by Doctor'

# Call the function
rename_images_in_subfolders(dataset_folder)
