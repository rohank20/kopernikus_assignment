# Kopernikus Interview Assignment

Kopernikus Automotive Deduplication algorithm task

To run the deduplication algorithm using the following command:

`python3 deduplicate.py --dir_path <PATH_TO_IMAGES>`

Regarding the answers to the questions in the task document:

1) **What did you learn after looking on our dataset?**

The dataset had variations in terms of naming, resolution, brightness, light and shadows, exposure and also in the 
camera angles. These variations could be important based on application demands and need to be dealt with appropriately.

2) **How does your program work?**

My program just gives a structure to the preprocessing and comparison functions which were already provided by you. It 
takes in the dataset directory as an input through the CLI interface, normalizes the images for any naming abnormalities, 
processes the images before finding the differences between adjacent images sorted by time and camera ID and finally 
deletes the images which fall below a certain `uniqueness_score` threshold.

3) **What values did you decide to use for input parameters and how did you find these values?**

The input parameters `gaussian_blur_radius_list`, `min_cnt_area` and `uniqueness_score` thereshold are selected by using
the area of the input image. Firstly, after normalizing the image resolution, I calculate the area of the image in square 
pixels. Using this area as a reference, after taking difference between the adjacent frames and calculating the contours,
I calculate the `min_cnt_area`, which is a threshold for adding the detected contour areas in the `score` parameter. This 
value is considered as 0.01% of the image area. After all detected contours are collected and summed up, I compare
them with a threshold of 1% of the image area. If this `uniqueness_score` is less than 1%, the image is considered 
duplicate/almost duplicate and then deleted.

After setting these parameters, I set the `gaussian_blur_radius_list` parameter as a list of 3 odd kernel radius values
which are in ascending order to achieve denoising and smoothening so the contours are free from noise. I selected the
values which provided better performance in the final deduplication result.

4) **What you would suggest to implement to improve data collection of unique cases in future?**

First and foremost, I would standardize some stuff like the file naming system, image resolution etc. Once that is normalized,
I would create a dynamic time interval data acquisition process which acquires data in time intervals according to if 
motion is detected in the cameras, which would reduce the dataset size and improve quality of the dataset. For example, 
a object tracking algorithm can be used to acquire data at a shorter time interval when there is motion and in longer intervals
when the image is static in nature.

5) **Any other comments about your solution?**

My aim was to make the solution as easy to use as possible. Hence, I have added CLI execution possibility as well as a progress
bar in the code. I hope that this will make executing the code easy and could also be used on remote servers and clouds.