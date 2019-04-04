import PIL
from PIL import Image, ImageDraw
import numpy as np
import math
#from py2app.recipes import scipy
#import scipy.misc
#from scipy import signal

import ncc
import os,zipfile

#1,1
cwd = os.getcwd()
#print(cwd)
#unzipped the folder

#1,2
#helper function, actually minimizes the image (by .75)
def Minimize(image):
    # h & w of image
    width, height = image.size

    #reducing the scale
    resized_image = image.resize((int(width * 0.75), int(height * 0.75)), Image.BICUBIC)

    return resized_image

#loop that checks the condition and adds to an array
def MakePyramid(image,minsize):
    all_images = []
    image = Image.open("/Users/leticianakajima/PycharmProjects/a2/" + image + ".jpg")
    width, height = image.size
    all_images.append(image)

#doesnt do this even once
    #loop that minimizes image + adds to all_images array
    while (width > minsize and height > minsize):
        image = Minimize(image)
        width, height = image.size
        all_images.append(image)

    return all_images

#1,3
#use imshow to display all images side by side
def ShowPyramid(pyramid):

    #making a blank vibe
    image_blank = Image.new("L", (sum([x.size[0] for x in pyramid][:]), pyramid[0].size[1]))
    #pasting the images into it
    offset = 0
    for x in pyramid:
        image_blank.paste(x, (offset, pyramid[0].size[1] - x.size[1]))
        offset = offset + x.size[0]
    #final_image_pyramid = Image.fromarray(pyramid.astype('uint8'))
    image_blank.save('pyramid_image.png', 'PNG')

#1,4
#find and mark all locations in the pyramid at which the normalized cross correlation (NCC)
# of the template with the image is above the threshold

def FindTemplate(pyramid, template, threshold):

    #reduce template to 15 pixels/define a constant for template width
    size_template = 15.0
    template = Image.open("/Users/leticianakajima/PycharmProjects/a2/" + template + ".jpg")
    width, height = template.size
    scaling_factor = size_template/min(width,height)
    new_height = scaling_factor * height
    new_width = scaling_factor * width

    new_template = template.resize((int(new_width),int(new_height)), PIL.Image.BICUBIC)
    matches_array = []
    #ncc-ing the template and all the pyramid images
    for x in pyramid:
        matches = np.where(ncc.normxcorr2D(x, new_template) > threshold)
        x = matches[1]
        y = matches[0]
        #adding the matches to this array
        matches_array.append(zip(x,y))
    #passing it into a helping draw function
    img = HelperDrawer(pyramid[0], matches_array)
    img.save('faces_recon.png', 'PNG')


def HelperDrawer(img,matches_array):
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)
    width, height = img.size
    #takes the matching points and the image on which to draw the rectangles on
    for pos in range(len(matches_array)):
        #scaling everything - because are being taken from diff. size images
        scaling_factor = 0.75**pos
        template_scale = scaling_factor-10
        for coord in matches_array[pos]:

            #scaling width and height
            new_h = height / template_scale
            new_w = width/template_scale

            # scaling x and y matches
            new_x = coord[0] / (scaling_factor)
            new_y = coord[1] / (scaling_factor)

            x1 = new_x - new_w
            x2 = new_x + new_w
            y1 = new_y - new_h
            y2 = new_y + new_h

            draw.line((x1, y1, x2, y1), fill="red", width=2)
            draw.line((x1, y2, x1, y1), fill="red", width=2)
            draw.line((x2, y1, x2, y2), fill="red", width=2)
            draw.line((x2, y2, x1, y2), fill="red", width=2)

    del draw
    return img

#print(MakePyramid("sports",1))
#ShowPyramid(MakePyramid("tree", 1))
FindTemplate(MakePyramid("family",1), "template", .56)





