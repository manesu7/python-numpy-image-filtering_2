import numpy as np
import cv2   


# Project: Simple Image Filter Application using NumPy for mathematical operations and OpenCV for image processing.

# Provide the path to your image file
image_path = 'image.png'
image = cv2.imread(image_path)

# Convert the image from BGR to RGB color format.
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Display the image using OpenCV's imshow function.
# While OpenCV handles the display mechanism, the image itself is still represented in memory as a NumPy array.
cv2.imshow('Original Image', image)

cv2.waitKey(0)


# Basic Image Manipulations

alpha = 1.2  # Contrast control (1.0 means no change)
beta = 50    # Brightness control (0 means no change)

# convertScaleAbs scales, calculates the absolute values, and converts the result to 8-bit.
# This operation increases the brightness and enhances the contrast of the image.
adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

cv2.imshow('Adjusted Image', adjusted)
cv2.waitKey(0)

# Applying Custom Kernels

sharpen_kernel = np.array([[-1,-1,-1], 
                           [-1, 9,-1],
                           [-1,-1,-1]])
# The sum of all weights in the kernel must be 1.


# Apply the sharpening filter to the image using OpenCV's filter2D function.
# The '-1' parameter means the output image will have the same depth as the source image.
sharpened = cv2.filter2D(image, -1, sharpen_kernel)

# Display the sharpened image. The displayed image is the result of the convolution operation 
# and will appear more sharpened compared to the original due to the edge enhancement introduced by our sharpening kernel.
cv2.imshow('Sharpened Image', sharpened)

cv2.waitKey(0)


# Build a kernel that blurs the image.
blur_kernel = np.array([[1,1,1],
                        [1,1,1],
                        [1,1,1]]) / 9
blurred = cv2.filter2D(image, -1, blur_kernel)
cv2.imshow('Blurred Image', blurred)
cv2.waitKey(0)


# Aggregation: Image Statistics
# One useful aspect of image analysis is obtaining statistics on pixel values providing insights into the nature of the image, for example, its brightness or contrast.

# Calculate the mean and standard deviation for each channel (R, G, B)
mean_values = np.mean(image, axis=(0, 1))
std_values = np.std(image, axis=(0, 1))

print(f"Mean values for R, G, B: {mean_values}")
print(f"Standard deviation values for R, G, B: {std_values}")

# Displaying the mean color of the image
mean_color_image = np.ones_like(image) * mean_values.astype(np.uint8)
cv2.imshow('Mean Color of Image', mean_color_image)
cv2.waitKey(0)


# Boolean Masking
# Setting a threshold value for pixel intensity 
threshold_value = 200

# Create a mask where any pixel in the image exceeds the threshold in any channel
mask = np.any(image > threshold_value, axis=-1)

# Visualizing the mask
cv2.imshow('Pixel Intensity Threshold Mask', mask.astype(np.uint8) * 255)  # Convert the boolean mask to an image
cv2.waitKey(0)

# Using the mask to set pixels above the threshold to a specific color (e.g., red)
highlighted_image = image.copy()
highlighted_image[mask] = [255, 0, 0]
cv2.imshow('Highlighted Image', highlighted_image)
cv2.waitKey(0)


# Building an Interactive GUI for Filter Application
# The GUI will allow users to:
# 1. Adjust brightness and contrast.
# 2. Apply a sharpening filter.
# 3. Display the mean color of the image.
# 4. Highlight pixels above a set threshold.

# Define a callback function for trackbar position changes
def update_image(x):
    # Read trackbar positions
    alpha = cv2.getTrackbarPos('Contrast', 'App') / 50.0
    beta = cv2.getTrackbarPos('Brightness', 'App') - 50
    apply_sharpen = cv2.getTrackbarPos('Toggle Sharpening', 'App')
    show_mean_color = cv2.getTrackbarPos('Toggle Mean Color', 'App')
    highlight_threshold = cv2.getTrackbarPos('Toggle Highlighting', 'App')

    output = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    if apply_sharpen:
        output = cv2.filter2D(output, -1, sharpen_kernel)
    if show_mean_color:
        mean_values = np.mean(output, axis=(0, 1)) # Calculate mean color values
        output = np.ones_like(output) * mean_values.astype(np.uint8)
    if highlight_threshold:
        mask = np.any(output > threshold_value, axis=-1)
        output[mask] = [255, 0, 0]

    cv2.imshow('App', output)

cv2.namedWindow('App')
cv2.createTrackbar('Brightness', 'App', 50, 100, update_image)
cv2.createTrackbar('Contrast', 'App', 50, 100, update_image)
cv2.createTrackbar('Toggle Sharpening', 'App', 0, 1, update_image)
cv2.createTrackbar('Toggle Mean Color', 'App', 0, 1, update_image)
cv2.createTrackbar('Toggle Highlighting', 'App', 0, 1, update_image)

cv2.imshow('App', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
