from tkinter import font

resize = 'This is the resize function provided by OpenCV. ' \
         'It simply takes in a source image, and x & y values which simply equate to ' \
         'the scale factor. This scale factor ends up being a percentage, where the number ' \
         'on your slider is divided by 100 and put into the resize function. ' \
         'Any number between 0 and 1 will shrink the image, ' \
         'and anything above 1 will enlarge it.'

rotate = 'While openCV does not have a function simply labelled \'Rotate\', ' \
         'it does have the ability to rotate images using a geometric operation ' \
         'known as an Affine Transformation. \n-The first step is to get the proper ' \
         'rotation matrix, which is done through a function that takes in the angle ' \
         'of rotation and the scale. Since we do not want to image to be resized, ' \
         'the scale for this algorithm is 1, and the rotation is simply linked to ' \
         'your slider. \n-Step two is then running that matrix through a function that ' \
         'performs an Affine transform on the image itself. The end result ' \
         'of all this geometry is shown to the right!'

canny = 'This is the Canny edge detection algorithm.' \
        'It was developed in 1986 by John F. Canny.\n' \
        'Step 1: filter out any \'noise\' in the image.' \
        'For this algorithm we use a 3x3 kernel to perform the blur.\n' \
        'Step 2: Find the intensity gradient.\n' \
        'Step 3: Apply \'Non-maximum suppression\'. This removes pixels not considered part of an edge.' \
        'Generally only thin lines should remain.\n' \
        'Step 4: The final step is called \'Hysteresis\', which accepts a pixel between an upper and lower' \
        'threshold. \nCanny recommended an upper:lower ratio of 3:1, which is what is used in this instance.'

threshold = 'This is a simple thresholding function provided by openCV. The image must be in grayscale ' \
            'for this simple thresholding to work. All pixels in grayscale have a value between 0 and 255. ' \
            'Thresholding works off the property of either this pixel meets the threshold cutoff value, ' \
            'and then it will be set to the threshold value, or it does not, and it will be set to 0. ' \
            '\n-The threshold value slider is the cutoff value, where anything below will be 0. ' \
            '\n-The max value slider is the value that the pixel will be set at if it falls above ' \
            'the threshold value. \n-Clicking the Invert button will apply the inverted thresholding ' \
            'parameter to  the function.'


def get_resize():
    return resize


def get_rotate():
    return rotate


def get_canny():
    return canny


def get_threshold():
    return threshold
