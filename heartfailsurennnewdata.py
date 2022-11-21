# -*- coding: utf-8 -*-
"""Copy of HeartFailsureNNNewData.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1joxkBucH3Nz4hprCa8TWeF0z1RrcqzIU
"""

#importing our libraries
import pandas as pd
import seaborn as sns
import numpy as np
from torch.utils.data import Dataset
import torch
from torch import *
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

import torch 
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import os
import torch
from torch import nn
from torch.utils.data import DataLoader,Dataset
from torchvision import datasets, transforms

!pip3 install torch==1.2.0+cu92 torchvision==0.4.0+cu92 -f https://download.pytorch.org/whl/torch_stable.html

"""## Loading our Heart Data"""

data=pd.read_excel('/content/heart_disease.xlsx')

data.drop(columns=['AgeCategory'],inplace=True)

data.info()

data.describe()

data.describe(include='object')

"""# Building a class to clean our ANN data"""

class CleanHeart():
  def __init__(self,datafile):
    self.datafile = datafile  
  def dum(self):
    dummy=pd.get_dummies(self.datafile,columns=['Smoking',	'AlcoholDrinking',	'Stroke',	'DiffWalking',	'Sex',
    'Race',	'Diabetic',	'PhysicalActivity',	'GenHealth',	'Asthma',	'KidneyDisease','SkinCancer'],drop_first=False)
    self.datafile.drop(self.datafile.columns[[1,2,3,4,7,8,9,10,11,12,13,14,15]],axis=1,inplace=True)
    return pd.concat([dummy],axis=1)
    dum(self.datafile)
    print(self.datafile)

"""#Calling our class and transforming it into a tensor for our model"""

data2=CleanHeart(data)
clean=data2.dum() #need to split x and y and turn why into 0,1
#cleanx=clean[:,1:39]
clean

clean['Heart_Dummy'] = clean.apply(lambda y: 1 if y['HeartDisease'] == 'Yes' else 0, axis=1) #turning y to o,1

clean.drop(columns=['HeartDisease'],inplace=True)
clean

"""#stepwise log regression for feature selection"""

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X=clean[:,1:52]
y=clean[:,0]




"""import statsmodels.api as sm
def get_log_Results():
  x_featTrain = X_train
  results = sm.Logit(y_train,X_train).fit()
  print(results.summary())
output = get_log_Results()
output"""

clean_tensor = torch.tensor(clean.values)
clean_tensor.shape

#importing more packages
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import torch.optim as optim
from torch.utils.data import DataLoader, random_split

print(torch.__version__)

"""# Building our Neural Network Architecture"""

#defining our nerual network architecture for training and test(based on values we will determine if we overfit our model and plan accordingly(early stopping or L1 / L2 REG))

class NeuralNet(nn.Module): # this is our parent class
  def __init__(self,n_features,Classes):
    super(NeuralNet,self).__init__()# this is our subclass that inherites attributes from nn.Module
    self.InputLayer=nn.Linear(n_features,38)
    self.HiddenLayer=nn.Linear(38,38)
    self.HiddenLayer2=nn.Linear(38,38)# second hidden layer
    self.Outter=nn.Linear(38,1)
    #layers of the network

    #so the issue here is with in the layers inputs and outputs (inputs in layer 1 = n vars, input to hidden layer needs to be 
    #figured out as well as the output to the outter layer)

  def forward(self,x): #this forward function specifies what will happen at each layer (computaion of our data)
    x = F.relu(self.HiddenLayer(x)) #setting our activation function for our hidden layer
    x = F.relu(self.HiddenLayer2(x))
    x = F.logsigmoid(self.Outter(x)) #setting our activation function for our output layer
    #x = self.Outter(x) #see if you need to define a loss funciton here 
    return x #returning the output layer values

"""#Storing our model in either a GPU or CPU"""

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

"""#HyperParamaters"""

#applying the model
#model = NeuralNet(n_features,Classes)

#Setting our model hyperparameters
n_features= 38 #features in our dataset
Classes = 1 #our binary outcome var
Learning_rate = 0.1
Batch_Size = 200 #number of obs we want at each training epoch
Epochs = 1 #number of time we want our data to pass through our neural network

loss_func = nn.CrossEntropyLoss()

model = NeuralNet(n_features=n_features,Classes=Classes).to(device)

optimizer = optim.Adam(model.parameters(),lr = Learning_rate)

#using this class to transform our data to tensors and run a x and y split
class HeartFailureData():  # this method is best when using custom datasets i.e data that is not offered by pytorch 
  def __init__(self):
    self.x = clean_tensor.float()
    self.y = clean_tensor[:,[37]]
    self.n_samples=self.x.shape[0]
  
  def __getitem__(self,index):
      return self.x[index],self.y[index]

  def __len__(self):
      return self.n_samples #new dataset

"""#X,Y split Test code"""

class HeartFailureData1():  # this method is best when using custom datasets i.e data that is not offered by pytorch 
  def __init__(self):
    self.x = clean_tensor.float()
    self.y = clean_tensor[:,[6]]
    self.n_samples=self.x.shape[0]
  
  def __getitem__(self,index):
      return self.x[index],self.y[index]

  def __len__(self):
      return self.n_samples

# do a train test split for x and y vals and load them in the dataloarder
y = clean_tensor[:,[6]]

#x = clean_tensor

x = clean_tensor[:,np.r_[7:,0:20]] 

#y = x[:, np.r_[:3, 4:36]]
#need to skip columns 6 using index....

#clean_tensor!=clean_tensor[:,[6]]


#x_train = int(x.shape[0] * 0.8)

x.shape, clean_tensor.shape#why is tensor size different?

"""#Loading the data using DataLoader"""

dataset=HeartFailureData() #using dataloader and dataset to load our data into our pytorch nerual net
train_dataloader = DataLoader(dataset=dataset,batch_size=Batch_Size,shuffle=True) #issue here is that train_loader is only giving 46 obs when batch size > 1
#loading the training data

#figure out this train test split
#train_dataset = datasets(train=True,download=False)
#train,test=random_split(train_dataset[600,318]) #do a 70/30 split for the data 70 train, 30 test
#transforming train dataloader to a dataset...do the same for test set as well 

#test_dataloader = DataLoader(dataset=dataset,batch_size=Batch_Size,shuffle=True)

"""#Training our Model using Gradient Descent"""

for epoch in torch.arange(Batch_Size): #pytorch will remove the use of the range function in future updates instead the new function will be torch.arange
  for Batch in train_dataloader:
    xval,targetvar=Batch
    xval=xval.to(device=device)
    targetvar=targetvar.to(device=device) 
   #stores both the x and y values in our cpu device
    print(xval.shape) #is the shape based on n rows and n columns or n_dimention and n_columns?
    
    #xval=xval.reshape(918,21).to(device=device)
    #targetvar=targetvar.reshape(918,21).to(device=device)
    
    #forward pass
    acurcy_score = model(xval.float()) #try to employ early stopping here 
    loss = loss_func(acurcy_score,targetvar)

    #backward propagation
    optimizer.zero_grad()
    loss.backward() 
   

    #gradient decent
    optimizer.step()

#checking model accuracy and determine overfitting 

def accuracy(train_dataloader,model):
  accurate = 0
  num_sample = 0
  model.eval()

  with torch.no_grad():
    for X_train,y_train in train_dataloader:
      X_train=X_train.to(device=device)
      y_train=y_train.to(device=device)
      
      acurcy_score = model(X_train)
      _,pred = acurcy_score.max(0)
      accurate +=(pred == y_train).sum()
      num_sample += pred.size(0)
      print(f'got {accurate}/{num_sample} with accuracy rate of ,{float(accurate)/float(num_sample)*100:.2f} at epoch {Epochs}')
    model.train()
    #return max(accurate) 
    #return max(float(accurate)/float(num_sample)) can try this to show where accuracy is greatest

    # implement early stopping for the network to prevent model overfitting

accuracy(train_dataloader,model)
