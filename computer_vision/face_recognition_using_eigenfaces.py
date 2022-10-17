# -*- coding: utf-8 -*-
"""face_recognition_using_eigenFaces.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1InXv7hbjSBRkuLZgpf9SCFQcxu2m924B

Used the approach mentioned in the research paper by Matthew Turk and Alex Pentland, for face recognition using Eigenfaces. The algorithm was implemented using basic matrix algebra and numpy. <br>
Link to the research paper: https://ieeexplore.ieee.org/document/139758 <br>
Google Colab Notebook: https://colab.research.google.com/drive/1InXv7hbjSBRkuLZgpf9SCFQcxu2m924B#scrollTo=Hj2uRB2ke4Vy
"""

!pip install opencv-python

# taken from this StackOverflow answer: https://stackoverflow.com/a/39225039
import requests

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

"""The dataset used was the AT&T dataset, where 10 different images of 40 distinct subjects were given. The 10 images of the same person were taken under varying circumstances, like different lighting, facial expressions and facial accessories. <br>

We took two images of each of the 40 people for testing. The model was trained on 8 images of the first 20 people. We did this so that we can calculate the accuracy for people both inside and outside our training set. <br>

On running the code, train_small.zip, test1.zip and test2.zip will appear in the contents folder. These signify the following:
<ol>
<li>train_small: training dataset, contains 8 images of 20 different people.</li><li>test1.zip: testing dataset, contains 2 images all people from the training dataset.</li>
<li>test2.zip: testing dataset, consisting of 2 images of 20 new people whose images weren't present in the training dataset.</li>

"""

# Downloading training dataset
file_id = '1Z9evWwUK4nTpARz67ZWraNe5sX2MNcFx'
destination = '/content/dataset.zip'
download_file_from_google_drive(file_id, destination)

!unzip -q dataset.zip
!rm -rf dataset.zip

# Downloading test1 dataset
test_file_id_1 = '1bIr_ikTxGuuZnJulykXeZz04pyb27S3f'
test_destination_1 = '/content/test1.zip'
download_file_from_google_drive(test_file_id_1, test_destination_1)

!unzip -q test1.zip
!rm -rf test1.zip

# Downloading test2 dataset
test_file_id_2 = '1Kj0QsxJ1m0n0UCPiaFskskUhM7fvxqS4'
test_destination_2 = '/content/test2.zip'
download_file_from_google_drive(test_file_id_2, test_destination_2)

!unzip -q test2.zip
!rm -rf test2.zip

# All images are supposed to be the same size, say, N*L
IMAGE_DIR = "/content/train_small"

# importing necessary libraries

import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import fnmatch
import re

def getClassFromName(fileName,lastSubdir=True):
        if lastSubdir:
            name = os.path.basename(os.path.dirname(fileName))
        else:
            name = os.path.basename(fileName)
        mat = re.match(".*(\d+).*", name)
        if mat != None:
            return int(mat.group(1))
        else:
            return name.__hash__()

image_names = []
image_dictionary = []

image_1D = []
for root, dirnames, filenames in os.walk(IMAGE_DIR):
    for filename in fnmatch.filter(filenames, "*.*"):
        image_names.append(os.path.join(root, filename))
for idx,image_name in enumerate(image_names):
    img = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE).astype(np.float64)
    if idx == 0:
        imgShape = img.shape
        vector_matrix = np.zeros((imgShape[0]*imgShape[1], len(image_names)),dtype=np.float64)
    image_dictionary.append((image_name,img,getClassFromName(image_name)))
    image_1D.append(img.flatten())

# print(image_1D)
print(len(image_1D))

"""Training Methodology:
<ol>
<li>We start by grayscaling the images and converting them into matrices of shape 112x92.</li><li>
Now each of these matrices was flattened and converted into a matrix of shape 10304x1. (Here 10304 comes from 112*92). All these vectors were stacked row wise into a single matrix (image_1D in our code).</li><li>
Now we normalize each row of this matrix by subtracting the row wise mean from each element of the corresponding row. This new matrix will be called AT, and the transpose of this matrix will be called A.</li><li>
Next we calculate the covariance matrix by doing ATxA.</li><li>
Next we calculate the eigenvalues and eigenvectors of the covariance matrix using the linalg.eig of numpy. </li><li>
Next step is dimensionality reduction. We choose a number K, and choose K eigen vectors corresponding to the K largest eigenvalues. </li><li>
Now we calculated the normalized training faces (face-average face) and represented each normalized face as a linear combination of the eigenvectors obtained in step 6. These w vectors were calculated using the np.linalg.lstsq function of numpy.
</li><li>
After calculating the weights (w vectors), we stacked those vectors </li>

Calculating the normalized image vectors.
"""

# We normalize each row of this matrix by subtracting the row wise mean from each element of the corresponding row. 
# This new matrix will be called AT
mean = []
a_transpose_norm = []
for i in range(len(image_1D[0])):
  mean.append(0)

  for j in range(len(image_1D)):
    mean[i] += image_1D[j][i]/len(image_1D)
    # print(sum)

for i in range(len(image_1D)):
  a_transpose_norm.append([])
  for j in range(len(mean)):
    a_transpose_norm[i].append(image_1D[i][j] - mean[j])
    # print(a_transpose_norm)

# print(len(a_transpose_norm))

# The transpose of the matrix computed above will be called A.
a_norm = np.transpose(a_transpose_norm)  #A
len(a_norm)

"""Calculating eigenvectors and eigenvalues of the covariance matrix formed by the image vectors."""

# We calculate the covariance matrix by doing ATxA.
cov_matrix = np.cov(a_transpose_norm) # At*A
# print(cov_matrix)
len(cov_matrix[0])

eigen = np.linalg.eig(cov_matrix) # returns eigen values and then all eigen vectors
# for i in range(len(eigen)):
#   print(eigen[i])
v_eigenvalues=eigen[0]
v=np.transpose(eigen[1])
# print(v_eigenvalues)
# print(v)
# print(len(v), len(v[0]))

u_transpose = []
for i in range(len(v)):
  array = np.matmul(a_norm,v[i])
  u_transpose.append(array)
u=np.transpose(u_transpose)
# print(len(u),len(u[0]))
print(len(u), len(u[0]))

eigen_values = eigen[0]
eigen_vectors=eigen[1]
# print(eigen_values)
eigen_d = {}
for i in range(len(eigen_values)):
  eigen_d[eigen_values[i]]=i
# eigen_d

"""Selecting the K eigenvectors of covariance matrix corresponding to the K largest eigenvalues. """

k=12

# sorting the dictionary of eigenvalues to get the corresponding eigenvectors.
from collections import OrderedDict
dict1 = OrderedDict(sorted(eigen_d.items(),reverse=True))
dict2=dict(dict1)
print(dict2)

# indexes of of k maximum eigenvalues
index_list=[]
for e in dict2:
  if(len(index_list)>=k):
    break
  index_list.append(dict2[e])
print(index_list)

# eigenvectors of k maximum eigenvalues
u_k=[]
for i in index_list:
  u_k.append(u_transpose[i])
print(u_k)

"""Plotting the mean vector."""

fig,axarr = plt.subplots()
axarr.set_title(" plot_mean_vector")
avg_image = np.reshape(mean, (imgShape))
axarr.imshow(avg_image, cmap=plt.cm.gray)

"""Plotting the k eigenfaces."""

for i in range(k):
  fig,axarr = plt.subplots()
  axarr.set_title(" plot_eigen_face_"+str(i+1))
  avg_image = np.reshape(u_k[i], (imgShape))
  axarr.imshow(avg_image, cmap=plt.cm.gray)

"""Projecting the image vector onto the eigenvector space for the training images."""

#storing the weights of each training image in an array.
w_array=[]
for i in range(len(cov_matrix[0])):
  w=np.linalg.lstsq(np.transpose(u_k),np.transpose(a_transpose_norm[i]))
  w_array.append(w[0])
print(len(w_array), len(w_array[0]))
# w_array

"""**Testing the algorithm.**
<ol>
<li>
We start by gray scaling and resizing the test image to fit our algorithm.
Next, we normalize the test image by subtracting the mean face from our unknown face. </li><li>
This normalized vector is projected into the eigenspace to obtain the linear combination of the eigenfaces.
</li><li>
We stack the w vectors obtained as follows:
</li><li>
We take the stacked w this vector and subtract it from the training images to get the minimum distance between the training vectors and testing vectors.
</li><li>
If this error comes out to be lower than the set threshold, then we find which face it is most similar to in the training images, else we report that the test image does not match with any image in the training set.
</li>

Run this after uploading a suitable PGM file to the colab runtime.
"""

# calculating the k weights of the testing image.
test_input_dir = '/content/test1/2.10.pgm'

img = (cv2.imread(test_input_dir, cv2.IMREAD_GRAYSCALE).astype(np.float64))
img2 = cv2.resize(img, (92,112)).flatten()
test_norm = []
for j in range(len(mean)):
    test_norm.append(img2[j] - mean[j])
    
w_test = np.linalg.lstsq(np.transpose(u_k),np.transpose(test_norm))
# w[0]
w_test[0]

"""Generating the output image by the weigted average of all eigenvectors. """

test_out = np.zeros([10304,1])
# print(len(test_out),len(test_out[0]) )
# print(len(eigen_vectors) , len(eigen_vectors[1]))

for i in range(10304):
  for j in range(k):
    test_out[i]+=u_k[j][i]*w_test[0][j]
  # temp = np.multiply(eigen_vectors[i], w[0][i])
  # test_out = np.add(test_out,temp)

test_out
# print(len(test_out) , len(test_out[1]))

fig,axarr = plt.subplots()
axarr.set_title(" plot_input_test_vector")
avg_image = np.reshape(img2, (imgShape))
axarr.imshow(avg_image, cmap=plt.cm.gray)

fig,axarr = plt.subplots()
axarr.set_title(" plot_generated_output_vector")
avg_image = np.reshape(test_out, (imgShape))
axarr.imshow(avg_image, cmap=plt.cm.gray)

"""Calculating error and finding out the most similar face in the training dataset that matches the given test image."""

err_list=[]
err_ind=-1
for i in range(len(w_array)):
  err_list.append(np.linalg.norm(w_array[i]-w_test[0]))
print(err_list)
for i in range(len(err_list)):
  if err_list[i]==min(err_list):
    err_ind = i
    print(err_ind)
print(min(err_list), max(err_list))

r=0
for idx,image_name in enumerate(image_names):
    
    if r==err_ind:
      print(image_name)
      similar_image = image_name
      name = image_name[18:20]
      if name[-1] == '/':
       name = name[0]
      # print(int(name))
    r=r+1

img_sim = (cv2.imread(similar_image, cv2.IMREAD_GRAYSCALE).astype(np.float64))
img_similar = cv2.resize(img_sim, (92,112)).flatten()

fig,axarr = plt.subplots()
axarr.set_title(" plot_most_similar_vector")
avg_image = np.reshape(img_similar, (imgShape))
axarr.imshow(avg_image, cmap=plt.cm.gray)

"""Accuracy calculation on the test dataset.

"""

IMAGE_DIR_TEST = '/content/test1'
image_names_test = []
image_dictionary_test = []

image_1D_test = []
for root, dirnames, filenames in os.walk(IMAGE_DIR_TEST):
    for filename in fnmatch.filter(filenames, "*.*"):
        image_names_test.append(os.path.join(root, filename))
for idx,image_name in enumerate(image_names_test):
    img = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE).astype(np.float64)
    if idx == 0:
        imgShape = img.shape
    image_dictionary_test.append((image_name,img,getClassFromName(image_name)))
    image_1D_test.append(img.flatten())
a_transpose_norm_test = []

for i in range(len(image_1D_test)):
  a_transpose_norm_test.append([])
  for j in range(len(mean)):
    a_transpose_norm_test[i].append(image_1D_test[i][j] - mean[j])
w_array_test=[]
for i in range(len(image_1D_test)):
  w=np.linalg.lstsq(np.transpose(u_k),np.transpose(a_transpose_norm_test[i]))
  w_array_test.append(w[0])
print(len(w_array_test), len(w_array_test[0]))
err_ind_test=[]
errors=[]
for i in range(len(image_1D_test)):
  err_list_test=[]
  for j in range(len(image_1D)):
    err_list_test.append(np.linalg.norm(w_array[j]-w_array_test[i]))
  for k in range(len(err_list_test)):
    if err_list_test[k]==min(err_list_test):
      err_ind_test.append(k)
  errors.append(min(err_list_test))
  # print(min(err_list_test))
print(err_ind_test)
print(errors)
print(min(errors), max(errors))

IMAGE_DIR_TEST = '/content/test2'

image_names_test = []
image_dictionary_test = []

image_1D_test = []
for root, dirnames, filenames in os.walk(IMAGE_DIR_TEST):
    for filename in fnmatch.filter(filenames, "*.*"):
        image_names_test.append(os.path.join(root, filename))
for idx,image_name in enumerate(image_names_test):
    img = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE).astype(np.float64)
    if idx == 0:
        # the shape of the image. They are sopposed to be the same
        imgShape = img.shape
        # the normalized image matrix. it will be normalized by subtracting from the average image later
    #img = cv2.pyrDown(img)
    image_dictionary_test.append((image_name,img,getClassFromName(image_name)))
    image_1D_test.append(img.flatten())

# print(image_dictionary_test)

# print(image_1D)  # 92x112
print(len(image_1D_test))

a_transpose_norm_test = []

for i in range(len(image_1D_test)):
  a_transpose_norm_test.append([])
  for j in range(len(mean)):
    a_transpose_norm_test[i].append(image_1D_test[i][j] - mean[j])
    # print(a_transpose_norm)

# print(len(a_transpose_norm))

#storing the weights of each training image in an array.
w_array_test=[]
for i in range(len(image_1D_test)):
  w=np.linalg.lstsq(np.transpose(u_k),np.transpose(a_transpose_norm_test[i]))
  w_array_test.append(w[0])
print(len(w_array_test), len(w_array_test[0]))
# w_array_test

err_ind_test2=[]
errors2=[]
for i in range(len(image_1D_test)):
  err_list_test=[]
  for j in range(len(image_1D)):
    err_list_test.append(np.linalg.norm(w_array[j]-w_array_test[i]))
  for k in range(len(err_list_test)):
    if err_list_test[k]==min(err_list_test):
      err_ind_test2.append(k)
  errors2.append(min(err_list_test))
  # print(min(err_list_test))
print(err_ind_test2)
print(errors2)
print(min(errors2), max(errors2))

tp=0  # true positive
tn=0  # true negative
fp=0  # false poaitive
fn=0  # false negative
threshold = (min(errors) + max(errors))/2

for i in range(len(errors)):
  if errors[i] > threshold :
    fn+=1
  elif errors[i] <= threshold:
    tp+=1 

for i in range(len(errors2)):
  if errors2[i] > threshold :
    tn+=1
  elif errors2[i] <= threshold:
    fp+=1 

incorrect_classifications = fp+fn
print(incorrect_classifications)