#!/usr/local/bin/python

from PIL import Image
import pytesseract
import cv2
import os
import argparse
import uuid
import imghdr

argp = argparse.ArgumentParser()
argp.add_argument("-p","--path", required=False, help="path to images folder")
args = vars(argp.parse_args())

imagesPath = "images/"
outPath = "out/"
preprocess = "blur"

allowedImages = ["jpeg", "jpg", "png", "bmp"]
ignoredFiles = [".DS_Store", ".gitkeep"]

if args["path"] != None:
  imagesPath = args["path"]

def isImage(img):
  return img not in ignoredFiles and imghdr.what("{path}{img}".format(path=imagesPath,img=img)) in allowedImages

# #TODO: find a way to determine if a image is blurry :) 

def extract(imageName, path, preprocess):
  imagePath = '{path}{imageName}'.format(path=path, imageName=imageName)
  image = cv2.imread(imagePath)
  gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  if preprocess == "thresh":
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
  elif preprocess == "blur":
    gray = cv2.medianBlur(gray, 3)
  filename = ".tmp/{}.png".format(uuid.uuid4())
  cv2.imwrite(filename, gray)
  text = pytesseract.image_to_string(Image.open(filename))
  os.remove(filename)
  return text.encode("utf-8")

def write(file, content):
  f = open(file,'w')
  f.write(content)
  f.close()

def execute(img):
  data = extract(img, imagesPath, preprocess)
  fileName = os.path.splitext(img)[0]
  fileFullName = "{outPath}{fileName}.txt".format(outPath=outPath, fileName=fileName)
  print fileFullName
  write(fileFullName, data)


images = os.listdir(imagesPath)
images = filter(isImage, images)

for img in images:
  execute(img)