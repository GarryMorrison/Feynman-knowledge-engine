#!c:/Python34/python.exe

#######################################################################
# try to be more methodical in working through the mnist problem
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2017-05-07
# Update: 2017-5-18
# Copyright: GPLv3
#
# Usage: ./mnist-problem.py
#
#######################################################################


import os
import sys
import glob
from PIL import Image                 # if this line bugs out, you need to install Pillow, a python image library.
import numpy
numpy.set_printoptions(linewidth=120)

digit_filename = "work-on-handwritten-digits/phi-transformed-images-v2--10k-test--edge-enhanced-20/mnist-test-image-99--edge-enhanced-20.png"

digits_test_directory = "work-on-handwritten-digits/phi-transformed-images-v2--10k-test--edge-enhanced-20/"
digits_train_directory = "work-on-handwritten-digits/phi-transformed-images-v2--60k-train--edge-enhanced-20/"
digits_test_labels = "work-on-handwritten-digits/mnist_test_labels.csv"
digits_train_labels = "work-on-handwritten-digits/mnist_train_labels.csv"

error_images_destination_dir = "work-on-handwritten-digits/error_images/"

original_digits_test_directory = "work-on-handwritten-digits/test-images/"
original_digits_train_directory = "work-on-handwritten-digits/train-images/"
original_error_images_destination_dir = "work-on-handwritten-digits/original_error_images/"


def image_to_list(image):
  data = list(image.getdata())
  mode = image.mode
  print("data:",data)
  print("mode:",mode)
  if mode == "L":
    return numpy.array(data)
#    return data
  if mode in ["RGB","RGBA"]:
    r = []
    for value in data:
      R,G,B = value[:3]
      r.append(R)
      r.append(G)
      r.append(B)
    return numpy.array(r)
#    return r

def list_to_l_image(data, size):
  if len(data) != size*size:
    return None
  dim = (size, size)
#  data = [int(x) for x in rescale(data)]
  data = [int(x) for x in data]
  im = Image.new('L',dim)
  im.putdata(data)
  return im

def list_to_rgb_image(data, size):
  if len(data) != 3*size*size:
    return None
  dim = (size, size)
#  data = [int(x) for x in rescale(data)]
  data = [int(x) for x in data]
  im_data = [ (data[i],data[i+1],data[i+2]) for i in range(0,len(data),3) ]
  im = Image.new('RGB',dim)
  im.putdata(im_data)
  return im

def rescale(arr):
  arr = arr - arr.min()
  if arr.max() == 0:
    return arr
  arr = arr*255/arr.max()
  return arr


def guassian_blur_mode_L(image,k):
  width,height = image.size
  original_pixels = image.load()

  # create an image with a 1*1 border:
  border_image = image.crop((-1,-1,width + 1,height + 1))
  border_pixels = border_image.load()

  # load the border_image into a matrix:
  Matrix = [[border_pixels[w,h] for w in range(width+2)] for h in range(height+2)]

  def smooth_pixel(M,w,h):
    r = M[h-1][w-1]/16 + M[h][w-1]/16 + M[h+1][w-1]/16 + M[h-1][w]/16 + M[h][w]/2 + M[h+1][w]/16 + M[h-1][w+1]/16 + M[h][w+1]/16 + M[h+1][w+1]/16
    return r

  # smooth our image matrix:
  # NB: we have to work with matrices and not images because we need to preserve floats at each step of smooth. Otherwise it harms the algo.
  # first, define a work-space matrix:
  new_Matrix = [[0 for w in range(width+2)] for h in range(height+2)]

  # smooth k times:
  for _ in range(k):
    for h in range(height):
      for w in range(width):
        new_Matrix[h+1][w+1] = smooth_pixel(Matrix,w+1,h+1)
    Matrix = new_Matrix

  # print out the matrix:
  r = numpy.array(Matrix).reshape((30,30))
  print(r)

  # minimally massage a single pixel:
  def minimally_massage_pixel(x):
    if x < 0:
      x = 0
#    x *= 20
    x = int(x)
    if x > 255:
      x = 255
    return 255 - x

  # massage a single pixel:
  def massage_pixel(x):
    if x < 0:
      x = 0
    x *= 20
    x = int(x)
    if x > 255:
      x = 255
    return 255 - x

  # output the final matrix into image form:
  out_image = Image.new('L',(width,height))
  pixels = out_image.load()
  for h in range(height):
    for w in range(width):
#      pix = massage_pixel(Matrix[h+1][w+1] - original_pixels[w,h])
#      pix = Matrix[h+1][w+1]
#      pix = massage_pixel(Matrix[h+1][w+1])
      pix = minimally_massage_pixel(Matrix[h+1][w+1])

      pixels[w,h] = pix
#  out_image.show()
  return out_image


# load image labels from the csv file, and return a dictionary:
#
def load_labels_from_csv(label_file, image_type):
  with open(label_file, 'r') as f:
    line = f.read()
    line = line.strip()
    labels = line.split(',')
  label_dict = {}
  for k,label in enumerate(labels):
    image_name = "%s-image-%s" % (image_type, str(k+1))
    label_dict[image_name] = label
  return label_dict

def load_images(digits_directory, filetype = 'png', extract_transformed_image_name = True):
  # eg: 'mnist-train-image-137--edge-enhanced-20.png' => 'train-image-137'
  def extract_transformed_image_name_from_file_name(s):
    s = os.path.basename(s)
    return s[6:-22]

  # eg: 'mnist-test-image-36.bmp' => 'test-image-36'
  def extract_image_name_from_file_name(s):
    s = os.path.basename(s)
    return s[6:-4]
  

  # check destination directory exists, if not exit:
  if not os.path.exists(digits_directory):
    print("digits_directory: %s not found" % digits_directory)
    sys.exit(0)
  
  # load files from directory into dictionary:
  image_dict = {}
  for file in glob.glob("%s/*.%s" % (digits_directory, filetype)):
    if extract_transformed_image_name:                                              # tidy this later!!
      image_name = extract_transformed_image_name_from_file_name(file)
    else:
      image_name = extract_image_name_from_file_name(file)

    #print("file_name: %s, image_name: %s " % (file, image_name))
    im = Image.open(file)
    image_dict[image_name] = image_to_list(im)

    # test it works: seems to...
    #print(image_to_list(im).reshape((28,28)))
    #break

  return image_dict


# rescaled list similarity measure:
def rescaled_list_simm(f,g):
  if len(f) != len(g):
    return 0
  the_len = len(f)

#  the_len = min(len(f),len(g))
#  f = f[:the_len]                     # remove this step?
#  g = g[:the_len]

# rescale step, first find size:
  s1 = sum(abs(f[k]) for k in range(the_len))
  s2 = sum(abs(g[k]) for k in range(the_len))

# if s1 == 0, or s2 == 0, we can't rescale:
  if s1 == 0 or s2 == 0:
    return 0

  wfg = sum(abs(f[k]/s1 - g[k]/s2) for k in range(the_len))

  return 1 - wfg/2


# return list version of pattern recognition:
def pattern_recognition_list(dict,pattern,t=0):
  result = []
  for label,list in dict.items():
    value = rescaled_list_simm(pattern, list)
    if value > t:
      result.append((label,value))
  return result


# print out score table:
def print_score_table(train_data, test_data, train_labels, test_labels, error_images_destination_dir):
  error_labels = []
  count = 0
  score = 0
  for label, pattern in test_data.items():
    print("label: %s" % label)
    count += 1
    correct_answer = test_labels[label]

    # find matching patterns:
    result_list = pattern_recognition_list(train_data, pattern, 0.8)  # put in 80% threshold. If prediction has value lower than this, then ignore.

    # sort the results:
    result = sorted(result_list, key = lambda x: float(x[1]), reverse = True)[:10]    # [:k] later
    #print("result: %s" % result)
    result = [x[0] for x in result]
    predicted_answers = [train_labels[train_label] for train_label in result ]

    # verbose data:
    print("answer: %s\tpredictions: %s" % (correct_answer, " ".join(predicted_answers)))

    star = ' '
    # simple find score:
    if correct_answer == predicted_answers[0]:
      score += 1
    else:
      star = '*'
      error_labels.append(label)
      im = list_to_l_image(pattern, 28)
      im.save("%s/%s--%s.png" % (error_images_destination_dir, label, correct_answer)) # assumes dest_dir exists


#    # find top 10 score:
#    r = superposition()
#    for answer in predicted_answers:
#      r.add(answer)
#    prediction = r.coeff_sort().select_top(1).get_label()
#    if correct_answer == prediction:
#      score += 1

    # print running result:
    #if count % 1 == 0:
    print("%s\t%s / %s = %.3f" % (star, score, count, 100 * score / count), flush = True )

    # test code, quit after finding 10 error images:
    #if len(error_labels) == 10:
    #  return error_labels

#  score = score_tally
  print("%s / %s = %.3f" % (score, count, 100 * score / count) )
  return error_labels


# save images to disk:
def save_list_of_images(data, size, image_mode, destination_dir, file_prefix, ext):
  # check destination directory exists, if not create it:
  if not os.path.exists(destination_dir):
    print("Creating %s directory." % destination_dir)
    os.makedirs(destination_dir)

  count = 0
  for label, image_list in data.items():
    try:
      if image_mode == "RGB":
        im = list_to_rgb_image(image_list, size)
      else:
        im = list_to_l_image(image_list, size)
      #im.save("%s/%s-%s.%s" % (destination_dir, file_prefix, count, ext))
      im.save("%s/%s.%s" % (destination_dir, label, ext))
      count += 1
    except Exception as e:
      print("save_list_of_images exception reason:",e)
      continue

def find_error_images(test_images, error_labels):
  image_dict = {}
  for label, image_list in test_images.items():
    if label in error_labels:
      image_dict[label] = image_list
  return image_dict


# first experiment, try Gaussian blur of a digit:
# NB: currently doesn't work. Not sure if this is correct behaviour,
# or a bug in the Gaussian blur code. Fixed. Mistake was in using massage_pixel().
#
def experiment_1(filename):
  im = Image.open(filename)
  #im.show()
  im2 = guassian_blur_mode_L(im, 10)
  im2.show()

  # print out image matrices:
  r1 = image_to_list(im).reshape((28,28))
  r2 = image_to_list(im2).reshape((28,28))
  print(r1)
  print(r2)


# load images into a dictionary of lists,
# then with no processing, essentially, find MNIST score
# I suspect it will be higher than anticipated.
# Yup. After a week! of computation we have the answer:
# 96.510 % or 3.49% error.
# NB: this is for the phi-transformed/edge-enhanced images.
# raw images almost certainly worse than this! Maybe test that next.
# Also, optimization of this code would be nice.
#
def experiment_2(train_directory, train_labels_csv, test_directory, test_labels_csv, error_images_destination_dir):
  # load images:
  train_images = load_images(train_directory)
  test_images = load_images(test_directory)

  # load labels:
  train_labels = load_labels_from_csv(train_labels_csv, 'train')
  test_labels = load_labels_from_csv(test_labels_csv, 'test')

  # quick check loading works:
  #print(train_images)
  #print(train_labels)
  #print(test_labels)
  #print(len(train_labels))
  #print(len(test_labels))

  # print score:
  error_labels = print_score_table(train_images, test_images, train_labels, test_labels, error_images_destination_dir)

  # save a copy of error images so we can focus on them to improve results:
  # now inside print_score function. So redundant.
  #error_images = find_error_images(test_images, error_labels)
  #save_list_of_images(error_images, 28, 'L', error_images_destination_dir, None, 'png')


# load images into a dictionary of lists,
# then with no processing, essentially, find MNIST score
# this time, using the raw/original/untransformed digits.
# I expect this to be significantly worse than experiment 2.
# Result in: 95.250% success, or 4.75% error.
#
def experiment_3(train_directory, train_labels_csv, test_directory, test_labels_csv, error_images_destination_dir):
  # load images:
  train_images = load_images(train_directory, 'bmp', False)
  test_images = load_images(test_directory, 'bmp', False)

  # load labels:
  train_labels = load_labels_from_csv(train_labels_csv, 'train')
  test_labels = load_labels_from_csv(test_labels_csv, 'test')

  # quick check loading works:
  #print(train_images)
  #print(train_labels)
  #print(test_labels)
  #print(len(train_labels))
  #print(len(test_labels))

  # print score:
  print_score_table(train_images, test_images, train_labels, test_labels, error_images_destination_dir)

  # print goodbye message:
  print("That concludes experiment 3 ... ")

experiment_1(digit_filename)
#experiment_2(digits_train_directory, digits_train_labels, digits_test_directory, digits_test_labels, error_images_destination_dir)

#experiment_3(original_digits_train_directory, digits_train_labels, original_digits_test_directory, digits_test_labels, original_error_images_destination_dir)
