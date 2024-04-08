from PIL import Image
import random

# NOTE: Feel free to add in any constant values you find useful to use
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# NOTE: Feel free to add in any helper functions to organize your code but
#       do NOT rename any existing functions (or else, autograder
#       won't be able to find them!!)


# NOTE: The following function is already completed for you as an example
#       You can use the structure of this function as a guide for the rest
#       This function will NOT be graded, so no need to edit any of it.
def remove_red(img: Image) -> Image:
    """
    Given an Image, img, update the img to have all the reds in the original
    image turned to 0 intensity. Return img.
    """

    img_width, img_height = img.size
    pixels = img.load()  # create the pixel map

    # for every pixel    
    for i in range(img_width):
        for j in range(img_height):
            r, g, b = pixels[i, j]
            pixels[i, j] = (0, g, b)

    return img


# NOTE: The following function is already completed for you as well
#       This function will NOT be graded, so no need to edit any of it.
def scale_new_image(orig_img, goal_width: int = None, goal_height: int = None):
    """
    Create and return a new image which resizes the given original Image,
    orig_img to a the given goal_width and goal_height. If no goal dimensions
    are provided, scale the image down to half its original width and height.
    Return the new image.
    """

    orig_width, orig_height = orig_img.size
    orig_pixels = orig_img.load()

    if not goal_width and not goal_height:
        goal_width, goal_height = orig_width // 2, orig_height // 2

    img = Image.new('RGB', (goal_width, goal_height))
    new_pixels = img.load()

    width_factor = goal_width / orig_width
    height_factor = goal_height / orig_height

    for i in range(goal_width):
        for j in range(goal_height):
            new_pixels[i, j] = orig_pixels[i // width_factor, j // height_factor]
    return img


# NOTE: The following function is partially completed to get you started
#       Complete the function according to the docstring description
def greyscale(img: Image) -> Image:
    """
    Change the Image, img, to greyscale by taking the average color of each
    pixel in the image and set the red, blue and green values of the pixel
    with that average. Return img.
    """

    img_width, img_height = img.size
    pixels = img.load()  # create the pixel map

    # for every pixel
    for i in range(img_width):
        for j in range(img_height):
            r, g, b = pixels[i, j]
            pixels[i, j] = (avg(r, g, b), avg(r, g, b), avg(r, g, b))
    return img


# TODO: COMPLETE THE REST OF THE FUNCTIONS ACCORDING TO THEIR DOCSTRINGS
# NOTE: Remember, you can and should add in helper functions to organize
#       your code, when applicable

def black_and_white(img: Image) -> Image:
    """
    Given an Image, img, update the img to have ONLY black or white pixels.
    Return img.

    Hints:
    - Get the average color of each pixel
    - If the average is higher than the "middle" color (i.e. 255/2),
      change it to white; if it's equal to or lower, change it to black
    """

    img_width, img_height = img.size
    pixels = img.load()
    for i in range(img_width):
        for j in range(img_height):
            r, g, b = pixels[i, j]
            if avg(r, g, b) > (255 / 2):
                pixels[i, j] = WHITE
            else:
                pixels[i, j] = BLACK
    return img


def sepia(img: Image) -> Image:
    """
    Given an Image, img, update the img to have a sepia scheme.
    Return img.

    Hints:
    - Get the RGB value of the pixel.
    - Calculate newRed, newGree, newBlue using the formula below:
    
        newRed = 0.393*R + 0.769*G + 0.189*B
        newGreen = 0.349*R + 0.686*G + 0.168*B
        newBlue = 0.272*R + 0.534*G + 0.131*B
        (Take the integer value of each.)

        If any of these output values is greater than 255, simply set it to 255.
        These specific values are the recommended values for sepia tone.

    - Set the new RGB value of each pixel based on the above calculations
        (i.e. Replace the value of each R, G and B with the new value
              that we calculated for the pixel.)
    """

    img_width, img_height = img.size
    pixels = img.load()
    for i in range(img_width):
        for j in range(img_height):
            r, g, b = pixels[i, j]
            new_red = int(0.393 * r + 0.769 * g + 0.189 * b)
            new_green = int(0.349 * r + 0.686 * g + 0.168 * b)
            new_blue = int(0.272 * r + 0.534 * g + 0.131 * b)
            if new_red > 255:
                new_red = 255
            if new_green > 255:
                new_green = 255
            if new_blue > 255:
                new_blue = 255
            pixels[i, j] = (new_red, new_green, new_blue)
    return img


def normalize_brightness(img: Image) -> Image:
    """
    Normalize the brightness of the given Image img by:
    1. computing the average brightness of the picture:
        - this can be done by calculating the average brightness of each pixel
          in img (the average brightness of each pixel is the sum of the values
          of red, blue and green of the pixel, divided by 3 as a float division)
        - the average brightness of the picture is then the sum of all the
          pixel averages, divided by the product of the width and hight of img

    2. find the factor, let's call it x, which we can multiply the
       average brightness by to get the value of 128

    3. multiply the colors in each pixel by this factor x
    """

    img_width, img_height = img.size
    pixels = img.load()
    all_avg = 0
    for i in range(img_width):
        for j in range(img_height):
            r, g, b = pixels[i, j]
            all_avg += avg(r, g, b)
    avg_brightness = all_avg / (img_width * img_height)
    x = 128 / avg_brightness
    for k in range(img_width):
        for n in range(img_height):
            r, g, b = pixels[k, n]
            pixels[k, n] = (int(r * x), int(g * x), int(b * x))
    return img


def sort_pixels(img: Image) -> Image:
    """
    Given an Image, img, sort (in non-descending order) each row of pixels
    by the average of their RGB values. Return the updated img.

    Tip: When testing this function out, first choose the greyscale
    feature. This will make it easier to spot whether or not the pixels in each
    row are actually sorted (it should go from darkest to lightest in a
    black and white image, if the sort is working correctly).
    """

    img_width, img_height = img.size
    pixels = img.load()
    for j in range(img_height):
        row = {}
        repeat_pixels = []
        for i in range(img_width):
            r, g, b = pixels[i, j]
            if (r, g, b) in row.keys():
                repeat_pixels.append((r, g, b))
            else:
                row[(r, g, b)] = avg(r, g, b)
        k = n = 0
        while k < (len(row) + len(repeat_pixels)):
            if sorted(row, key=row.get)[n] in repeat_pixels:
                amount = repeat_pixels.count(sorted(row, key=row.get)[n])
                for times in range(amount + 1):
                    pixels[k + times, j] = sorted(row, key=row.get)[n]
                k += (amount + 1)
            else:
                pixels[k, j] = sorted(row, key=row.get)[n]
                k += 1
            n += 1
    return img


def blur(img: Image) -> Image:
    """Blur Image, img, based on the given pixel_size

    Hints:
    - For each pixel, calculate average RGB values of its neighbouring pixels
        (i.e. newRed = average of all the R values of each adjacent pixel, ...)
    - Set the RGB value of the center pixel to be the average RGB values of all
        the pixels around it
    
    Be careful at the edges of the image: not all pixels have 8 neighboring pixels!
    """

    img_width, img_height = img.size
    pixels = img.load()
    for i in range(img_width):
        for j in range(img_height):
            rgb = []
            for c in range(3):
                divider = 0
                single_color = 0
                for x in range(-1, 2):
                    if 0 <= (i + x) < img_width:
                        for y in range(-1, 2):
                            if 0 <= (j + y) < img_height:
                                single_color += pixels[i + x, j + y][c]
                                divider += 1
                rgb.append(single_color // divider)
            pixels[i, j] = tuple(rgb)
    return img


def rotate_picture_90_left(img: Image) -> Image:
    """Return a NEW picture that is the given Image img rotated 90 degrees
    to the left.

    Hints:
    - create a new blank image that has reverse width and height
    - reverse the coordinates of each pixel in the original picture, img,
        and put it into the new picture
    """

    img_width, img_height = img.size
    pixels = img.load()
    img = Image.new('RGB', (img_height, img_width))
    new_pixels = img.load()
    for i in range(img_width):
        for j in range(img_height):
            new_pixels[j, img_width - 1 - i] = pixels[i, j]
    return img


def rotate_picture_90_right(img: Image) -> Image:
    """
    Return a NEW picture that is the given Image img rotated 90 degrees
    to the right.
    """

    img_width, img_height = img.size
    pixels = img.load()
    img = Image.new('RGB', (img_height, img_width))
    new_pixels = img.load()
    for i in range(img_width):
        for j in range(img_height):
            new_pixels[img_height - 1 - j, i] = pixels[i, j]
    return img


def flip_horizontal(img: Image) -> Image:
    """
    Given an Image, img, update it so it looks like a mirror
    was placed horizontally down the middle.

    Tip: Remember Python allows you to switch values using a, b = b, a notation.
         You don't HAVE to use this here, but it might come in handy.
    """

    img_width, img_height = img.size
    pixels = img.load()
    for i in range(img_width):
        for j in range(img_height // 2):
            pixels[i, img_height - 1 - j], pixels[i, j] = \
                pixels[i, j], pixels[i, img_height - 1 - j]
    return img


def flip_vertical(img: Image) -> Image:
    """
    Given an Image, img, update it so it looks like a mirror
    was placed vertically down the middle.

    Tip: Remember Python allows you to switch values using a, b = b, a notation.
         You don't HAVE to use this here, but it might come in handy.
    """

    img_width, img_height = img.size
    pixels = img.load()
    for j in range(img_height):
        for i in range(img_width // 2):
            pixels[img_width - 1 - i, j], pixels[i, j] = \
                pixels[i, j], pixels[img_width - 1 - i, j]
    return img


def kaleidoscope(img: Image) -> Image:
    """
    Given an Image, img, update it to create a kaleidoscope.
    You must maintain the size dimensions of the original image.
    Return the updated img.

    The kaleidoscope effect should have this image repeated four times:
    - the original image will be in the lower left quadrant
    - the lower right will be the original image flipped on the vertical axis
    - the two top images will be the bottom two images flipped on the horizontal axis
    
    Tip: You may want to use helper functions to organize the code here.
            This filter can be broken down into a series of other operations, such as
            flip vertical / horizontal, scale / downscale, etc.
    """

    pixels = img.load()
    new_width, new_height = scale_new_image(img).size
    new_pixels = scale_new_image(img).load()
    for i in range(new_width):
        for j in range(new_height):
            pixels[i, j] = new_pixels[i, new_height - 1 - j]
            pixels[i, j + new_height] = new_pixels[i, j]
            pixels[i + new_width, j] = \
                new_pixels[new_width - 1 - i, new_height - 1 - j]
            pixels[i + new_width, j + new_height] = \
                new_pixels[new_width - 1 - i, j]
    return img


def draw_border(img: Image) -> Image:
    """
    Given an Image, img, update it to have a five pixel wide black border
    around the edges. Return the updated img.
    """

    img_width, img_height = img.size
    pixels = img.load()
    for i in range(img_width):
        for j in range(img_height):
            if i <= 4 or j <= 4 or img_width - 5 <= i or img_height - 5 <= j:
                pixels[i, j] = BLACK
    return img


def scramble(img: Image) -> Image:
    """
    Scramble the pixels in the image by re-assigning each color intensity
    value to a unique randomly generated number. Store information that can
    be used to decrypt (e.g. what each original intensity value is now mapped
    to) in a file named key.txt. Return the scrambled image.

    Note:
    Figure out a good way to assign each number from 0-255 to a specific
    new number (there should be a 1-1 relationship between the old number and
    a new one). Consider using random.randint to generate numbers.
    Then, go through each pixel in the image and reset each RGB value to the
    newly mapped number.

    You should use helper functions to clean up your code, if applicable.
    """

    random_num = random_number()
    save_key(random_num)
    img_width, img_height = img.size
    pixels = img.load()
    for i in range(img_width):
        for j in range(img_height):
            r, g, b = pixels[i, j]
            pixels[i, j] = (random_num[r], random_num[g], random_num[b])
    return img


def unscramble(img: Image) -> Image:
    """
    Unscramble the pixels in the image by re-assigning each color intensity
    value to its original value based on the information in file named "key.txt".

    If the file is empty, do nothing and just return the original image back.
    You may assume this file exists.

    Note:
        You can't just hard-code some calculations in to unscramble each pixel
        Your key.txt file must be formatted in a way that the data in it lets you
        revert each pixel, and that file data must be used in this function.
    """

    random_num = get_key()
    img_width, img_height = img.size
    pixels = img.load()
    for i in range(img_width):
        for j in range(img_height):
            r, g, b = pixels[i, j]
            pixels[i, j] = \
                (random_num.index(r), random_num.index(g), random_num.index(b))
    return img


# Helper function
def avg(r, g, b):
    return int((r + g + b) / 3)


def random_number():
    random_num = []
    while len(random_num) < 256:
        num = random.randint(0, 255)
        if num not in random_num:
            random_num.append(num)
    return random_num


def save_key(key_list):
    key_file = open('key.txt', 'w')
    for i in range(len(key_list)):
        key_file.write('{0}\n'.format(str(key_list[i])))
    key_file.close()


def get_key():
    key_list = []
    ori_list = open('key.txt').readlines()
    for i in range(len(ori_list)):
        key_list.append(int((ori_list[i]).strip()))
    return key_list


#############################################################
# ADD FUNCTIONS FOR CUSTOM FILTERS (PART 2) BELOW THIS LINE #
#############################################################

# Custom filter functions go here


# To add a custom filter to the menu, add key-value pair for it
# to the dictionary below. Key should be the label you want to
# add to the menu, and value should be the name of the function
# which you added to this file that applies your filter.

COMMANDS = {
    "Remove red": remove_red,
    "Downscale": scale_new_image,
    "Greyscale": greyscale,
    "Black and White": black_and_white,
    "Sepia": sepia,
    "Normalize Brightness": normalize_brightness,
    "Sort Pixels": sort_pixels,
    "Blur": blur,
    "Kaleidoscope": kaleidoscope,
    "Rotate Clockwise": rotate_picture_90_right,
    "Rotate Counter-clockwise": rotate_picture_90_left,
    "Flip Horizontal": flip_horizontal,
    "Flip Vertical": flip_vertical,
    "Add border": draw_border,
    "Scramble": scramble,
    "Unscramble": unscramble,
}
