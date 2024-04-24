import ee
import geemap
import os
import time
import shutil
from PIL import Image
from IPython.display import display, Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import clear_output
import json
import sys
import subprocess

# folder_path = "C:\\Users\\nikhi\\Documents\\GitHub\\gvsu-gis\\"

# # # Initialize Earth Engine
# gee_project_id = 'ee-sharmani'

# Declare the variables at the global scope
folder_path = None
gee_project_id = None

def main():
    global folder_path, gee_project_id
    # Check if the folder path and GEE project ID were passed as arguments
    if len(sys.argv) >= 3:
        folder_path = sys.argv[1]  # The folder path is passed as the first argument
        gee_project_id = sys.argv[2]  # The GEE project ID is passed as the second argument
        print(f"Using folder path: {folder_path}")
        print(f"Using GEE project ID: {gee_project_id}")
        # Additional code to use folder_path and gee_project_id for operations
    else:
        print("Required arguments (folder_path and gee_project_id) were not provided.")

if __name__ == "__main__":
    main()
    # Here, you can use folder_path and gee_project_id if they were set
    if folder_path and gee_project_id:
        print(f"Folder path from global context: {folder_path}")
        print(f"GEE project ID from global context: {gee_project_id}")
        # Rest of the script where you can use these variables
        # ...


# Authenticate to Earth Engine account
ee.Authenticate()

# Installs geemap package
import subprocess

try:
    import geemap
except ImportError:
    print('geemap package not installed. Installing ...')
    subprocess.check_call(["python", '-m', 'pip', 'install', 'geemap'])

# Authenticates and initializes Earth Engine
import ee

try:
    ee.Initialize()
    ee.Initialize(project=gee_project_id)
except Exception as e:
    ee.Authenticate()
    ee.Initialize(project=gee_project_id)
    ee.Initialize()



# Path to your JSON file
json_path = folder_path + "data\\selected_coordinates.json"

# Load JSON data from the file
with open(json_path, 'r') as file:
    data = json.load(file)


# Folder Path
images_path = folder_path + '\\data\\images\\'


# Folder Path
video_path = folder_path + '\\data\\video\\'



# List all files in the folder
file_list = os.listdir(images_path)

# Delete all files in the folder
for file_name in file_list:
    file_path = os.path.join(images_path, file_name)
    os.remove(file_path)


# Main loop to continuously monitor the folder
while True:
    # List all files in the folder
    file_list = os.listdir(images_path)

    # Check if any files are present in the folder
    if len(file_list) > 0:
        print("Removing files from the folder:", file_list)
    else:
        print("All the content has been removed from the folder.")
        break;
    # Wait for some time before checking again
    time.sleep(10)  # Adjust the sleep duration as needed




coordinates = [[item['lng'], item['lat']] for item in data['coordinates']]
start_date = data['startDate']
end_date = data['endDate']
cloud_coverage = int(data['cloudCoverage'])

# Define the area
region = ee.Geometry.Polygon(coordinates)
image_collection = (ee.ImageCollection('LANDSAT/LC08/C02/T1_TOA')
                    .filterBounds(region)
                    .filterDate(start_date, end_date)
                    .filter(ee.Filter.lte('CLOUD_COVER', cloud_coverage)))

# Get the expected number of files to be downloaded
expected_num_files = image_collection.size().getInfo()


print("Total Number of images in the collection: ", expected_num_files)



# Iterate over each image in the collection
image_list = image_collection.toList(image_collection.size())
for i in range(image_list.size().getInfo()):
    image = ee.Image(image_list.get(i))

    # Select bands for RGB visualization
    selected_bands_image = image.select(['B4', 'B3', 'B2'])

    # Apply color correction
    corrected_image = selected_bands_image.visualize(**{
        'min': 0,
        'max': 0.3,
        'gamma': 1.4,
        'bands': ['B4', 'B3', 'B2']
    })

    # Set the parameters for the download
    download_params = {
        'image': corrected_image,
        'scale': 30,  # Adjust scale as needed
        'region': region.getInfo(),  # Make sure the region is in the right format
        'file_per_band': False
    }

    # Download the image to the local file system
    local_filename = f'{images_path}/landsat_image_{i}.tif'
    geemap.ee_export_image(corrected_image, filename=local_filename, scale=30, region=region.getInfo())

    # Print status
    print(f"Downloaded color-corrected image {i} to local path: {local_filename}")



# Initialize a variable to keep track of the number of .tif files downloaded
downloaded_tif_files = 0

# Loop until all .tif files are downloaded
while downloaded_tif_files < expected_num_files:
    # List files in the images folder ending with .tif
    tif_files = [file for file in os.listdir(images_path) if file.endswith('.tif')]

    # Update the number of .tif files downloaded
    downloaded_tif_files = len(tif_files)

    # Clear the output
    clear_output(wait=True)

    # Print progress
    print(f'{downloaded_tif_files} out of {expected_num_files} .tif files downloaded. Waiting for all .tif files to be downloaded...')

    # If not all .tif files are downloaded, wait for some time before checking again
    if downloaded_tif_files < expected_num_files:
        time.sleep(10)  # Adjust the sleep duration as needed

# All .tif files are downloaded
print(f'All {expected_num_files} .tif files downloaded successfully.')








# List all files in the folder
file_list = os.listdir(video_path)

# Delete all files in the folder
for file_name in file_list:
    file_path = os.path.join(video_path, file_name)
    os.remove(file_path)



# Main loop to continuously monitor the folder
while True:
    # List all files in the folder
    file_list = os.listdir(video_path)

    # Check if any files are present in the folder
    if len(file_list) > 0:
        print("Removing files from the folder:", file_list)
    else:
        print("All the content has been removed from the folder.")
        break;
    # Wait for some time before checking again
    time.sleep(10)  # Adjust the sleep duration as needed



# Get a list of all .tif files in the directory
tif_files = [file_name for file_name in os.listdir(images_path) if file_name.endswith('.tif')]

# Confirm that the images are in the drive folder
print(f'Number of GeoTIFF files in the folder: {len(tif_files)}')

# Sort the GeoTIFF images by filename
sorted_tif_files = sorted(tif_files)

# Create a list to store full paths to the image files
image_paths = [os.path.join(images_path, img) for img in sorted_tif_files]

# Print out the sorted list of file paths
for img_path in image_paths:
    print(img_path)

# At this point, 'image_paths' contains the full sorted paths to each GeoTIFF image in your folder
# You can now proceed to use 'image_paths' for further processing like analysis, displaying info, etc.

# Example of further processing: Print the file size for each GeoTIFF file
for img_path in image_paths:
    print(f"The file size of '{os.path.basename(img_path)}' is {os.path.getsize(img_path)} bytes.")


# Read the first image to get dimensions
first_image = cv2.imread(image_paths[0])
height, width, layers = first_image.shape

# Specify the output video file path (ensure the directory exists)
interim_video_path = os.path.join(video_path, 'interim_video.mp4')

# Create the video using OpenCV
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use appropriate codec
video_writer = cv2.VideoWriter(interim_video_path, fourcc, 10, (width, height))

for image_path in image_paths:
    img = cv2.imread(image_path)
    video_writer.write(img)

video_writer.release()

# Confirm that the video is created
print(f'Video created: {interim_video_path}')



## Deleting all images after creating video

# List all files in the folder
file_list = os.listdir(images_path)

# Delete all files in the folder
for file_name in file_list:
    file_path = os.path.join(images_path, file_name)
    os.remove(file_path)



# Main loop to continuously monitor the folder
while True:
    # List all files in the folder
    file_list = os.listdir(images_path)

    # Check if any files are present in the folder
    if len(file_list) > 0:
        print("Removing files from the folder:", file_list)
    else:
        print("All the content has been removed from the folder.")
        break;
    # Wait for some time before checking again
    time.sleep(10)  # Adjust the sleep duration as needed





# Open the video file
cap = cv2.VideoCapture(interim_video_path)

# Initialize lists to store normalized differences and frame numbers
normalized_diffs = []
frame_numbers = []

# Read the first frame
ret, prev_frame = cap.read()
if not ret:
    print("Can't read the first frame or video may have only one frame.")
    cap.release()  # Release the video capture object
    sys.exit(1)  # Exit the script with an error code

prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
frame_number = 1

# Process each frame in the video
while True:
    # Read the next frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate the absolute difference between frames
    abs_diff = np.sum(np.abs(frame_gray - prev_frame_gray))

    # Append the absolute difference and frame number to the lists
    normalized_diffs.append(abs_diff)
    frame_numbers.append(frame_number)
    frame_number += 1

    # Update the previous frame
    prev_frame_gray = frame_gray

# Release the video capture object
cap.release()

# Check if any differences were calculated
if not normalized_diffs:
    print("No differences were calculated. The video may have only one frame.")
else:
    # Calculate the maximum absolute difference
    max_diff = max(normalized_diffs)

    # Normalize the differences
    normalized_diffs = [(100 * diff) / max_diff for diff in normalized_diffs]

    # Round the normalized differences to 2 decimal places
    normalized_diffs = [round(diff, 2) for diff in normalized_diffs]

    # Create a dictionary to store the data
    data = {'frame_numbers': frame_numbers, 'normalized_differences': normalized_diffs}
    # Create the JSON file path by joining the directory path with the file name
    json_file_path = os.path.join(video_path, 'frame_differences.json')

    # Write the data to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file)

    print(f"JSON file '{json_file_path}' created successfully.")


output_video_path = os.path.join(video_path, 'output_video.mp4')

# ffmpeg command
ffmpeg_command = (
    f'ffmpeg -i {interim_video_path} '
    f'-vf "scale=-1:1080,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black" '
    f'{output_video_path}'
)

# Run the command
try:
    subprocess.run(ffmpeg_command, shell=True, check=True)
    print("Video conversion successful.")
    
    # Delete the interim video file if conversion is successful
    os.remove(interim_video_path)
    print("Interim video has been deleted.")
    
except subprocess.CalledProcessError as e:
    print(f"An error occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred when trying to delete the interim file: {e}")


print("Python script completed!")
