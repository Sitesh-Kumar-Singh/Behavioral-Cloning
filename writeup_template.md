# **Behavioral Cloning** 

## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---

**Behavioral Cloning Project**

The goals / steps of this project are the following:
* Use the simulator to collect data of good driving behavior
* Build, a convolution neural network in Keras that predicts steering angles from images
* Train and validate the model with a training and validation set
* Test that the model successfully drives around track one without leaving the road
* Summarize the results with a written report


[//]: # (Image References)

[image1]: ./examples/placeholder.png "Model Visualization"
[image2]: ./examples/placeholder.png "Grayscaling"
[image3]: ./examples/placeholder_small.png "Recovery Image"
[image4]: ./examples/placeholder_small.png "Recovery Image"
[image5]: ./examples/placeholder_small.png "Recovery Image"
[image6]: ./examples/placeholder_small.png "Normal Image"
[image7]: ./examples/placeholder_small.png "Flipped Image"

## Rubric Points
### Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/432/view) individually and describe how I addressed each point in my implementation.  

---
### Files Submitted & Code Quality

#### 1. Submission includes all required files and can be used to run the simulator in autonomous mode

My project includes the following files:
* model.py containing the script to create and train the model
* drive.py for driving the car in autonomous mode
* model.h5 containing a trained convolution neural network 
* writeup_report.md or writeup_report.pdf summarizing the results

#### 2. Submission includes functional code
Using the Udacity provided simulator and my drive.py file, the car can be driven autonomously around the track by executing 
```sh
python drive.py model.h5
```

#### 3. Submission code is usable and readable

The model.py file contains the code for training and saving the convolution neural network. The file shows the pipeline I used for training and validating the model, and it contains comments to explain how the code works.

### Model Architecture and Training Strategy

#### 1. An appropriate model architecture has been employed

I have used nvidea deep learning model with some modification(line 83-104(model.py)) 
It consist of 3 Convolution layer of 5x5 strides and 3 Convolution layer with 3x3 strides and depth ranges from 24 to 64.

I have used ELU as activation function.

Model contain 3 fully connected network. 

Here is the summary of model

[image8]: ./examples/model_summary.PNG "Model Summary"

#### 2. Attempts to reduce overfitting in the model

The model contains dropout layers in order to reduce overfitting (model.py lines 99). 

The model was trained and validated on different data sets to ensure that the model was not overfitting (code line 74). The model was tested by running it through the simulator and ensuring that the vehicle could stay on the track.

#### 3. Model parameter tuning

The model used an adam optimizer, so the learning rate was not tuned manually (model.py line 107).

#### 4. Appropriate training data

Training data was chosen to keep the vehicle driving on the road. I used a combination of center lane driving, recovering from the left and right sides of the road.

I have feed all 3 camera images to network, along with some correction factor is measurement, also I have flipped the image and change the sign of measurement to create more data and make network more robust 

For details about how I created the training data, see the next section. 

### Model Architecture and Training Strategy

#### 1. Solution Design Approach

The overall strategy for deriving a model architecture was to ...

In order to gauge how well the model was working, I split my image and steering angle data into a training and validation set. I found that my first model had a low mean squared error on the training set but a high mean squared error on the validation set. This implied that the model was overfitting. 

To combat the overfitting, I modified the model and dropped 25% of data to prevent overfitting
 

The final step was to run the simulator to see how well the car was driving around track one. There were a few spots where the vehicle fell off the track
on the bridge and sharp left turn after the bridge, 
to improve the driving behavior in these cases, I used ELU as activation function instead of RELU

At the end of the process, the vehicle is able to drive autonomously around the track without leaving the road.

#### 2. Final Model Architecture

The final model architecture (model.py lines 83-103) consisted of a convolution neural network with the following layers and layer sizes 

[image9]: ./examples/model_summary.PNG "Model Summary"

![alt text][image1]

#### 3. Creation of the Training Set & Training Process

I have used training data provided by udactiy to train the model, I tried first with collecting data but my car was not able to stay on track after bridge.

![alt text][image2]

I then recorded the vehicle recovering from the left side and right sides of the road back to center so that the vehicle would learn to drive in every condition and get back to center from left and right lane. These images show what a recovery looks like starting from ... :

![alt text][image3]
![alt text][image4]
![alt text][image5]

Then I repeated this process on track two in order to get more data points.

To augment the data sat, I also flipped images and angles thinking that this would give more data set to train and model will perform good on both the curvatures
For example, here is an image that has then been flipped:

[image10]: ./examples/center_flipped "Flipped image"

After that I cropped the image 70 pixels from top and 25 pixels from bottom, top 70 pixel is filled with sky and trees and bottom 25 with car front section, as these were not neccessary to make decision and will confuse the network I have remove these pixels  


I finally randomly shuffled the data set and put 15  % of the data into a validation set. 

I used this training data for training the model. The validation set helped determine if the model was over or under fitting. The ideal number of epochs was 5 as evidenced by decreasing validation loss after each epoch. I used an adam optimizer so that manually training the learning rate wasn't necessary.
