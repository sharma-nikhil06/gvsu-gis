# Geo Spatial Data Analysis

## Description

This project utilizes geospatial images sourced from the Google Earth Engine based on user inputs such as location, date, and cloud coverage. It involves downloading these images and performing data analysis on them.

## Prerequisites

Before you begin, ensure you have the following libraries installed:
- Flask
- Flask-CORS
- os
- subprocess
- threading
- webbrowser
- time
- ee (Google Earth Engine)
- geemap
- PIL (Image)
- cv2 (OpenCV)
- numpy
- matplotlib
- IPython
- json
- sys
- FFmpeg: Download from [FFmpeg's official download page](https://ffmpeg.org/download.html). After downloading, extract in your C Drive and add the installation path (`C:\ffmpeg\bin`) to your system's Environment Variables.


You will also need a Google Earth Engine project ID (`gee_project_id`). You can use this link [Google Earth Engine](https://code.earthengine.google.com/register) to create your Google Earth Engine project ID.

## Installation

To set up this project, follow these steps:

### Step 1

Copy the code from `gvsu-gis/Scripts/Clone_Git.py` and paste it into your code editor.

### Step 2

Update the `target_dir` variable to specify where you want the `gvsu-gis` repository to be cloned.

### Step 3

Once cloned, open the `gvsu-gis/Scripts/Master.py` file from the cloned directory in your code editor. Update the `Folder_Path` variable to the directory where you have cloned the repository. Additionally, update the `GEE_Project_ID` with your Earth Engine project ID and save the file.

## Running the Project

### Step 4

Run the `Master.py` file. This will start the Flask server and automatically open the `Polygon.html` in your default web browser.

### Step 5

Click on the map and select the area for which you want to download images. Also, select the dates and the maximum cloud coverage you require. Once done, click on 'Save Data'.

After clicking 'Save Data', a JavaScript popup will appear in your web browser. Click 'OK', and it will save a JSON file with all the details you selected. It will then start downloading all the images into the `gvsu-gis/data/images/` folder for the selected area, date range, and maximum cloud coverage.

### Step 6

Once the images have been downloaded, a video named `output_video.mp4` will be created from these images, along with a JSON file containing the normalized frame differences of each frame in the video in the `gvsu-gis/data/video` folder. Once the video is created, the web browser will automatically open `video_player.html`, which will display the created video and the graph for normalized differences of the frames.
