# -*- coding: utf-8 -*-
"""app.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rB-dGwnWPhCN4V6QiU6UN9lMvTTOl8P3
"""

import streamlit as st
import pickle
import numpy as np
from PIL import Image
import sklearn
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import TensorDataset, DataLoader, Dataset
import torch.optim as optim

class Dataset(Dataset):
    def __init__(self, data_df, transform=None):
        super().__init__()
        self.df = data_df
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, index):
        img = self.df[index]
        image = np.array(Image.open(img))
        if self.transform is not None:
            image = self.transform(image)
        return image

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=2),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=3, padding=2),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer3 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, padding=2),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer4 = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=3, padding=2),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer5 = nn.Sequential(
            nn.Conv2d(256, 512, kernel_size=3, padding=2),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.avg = nn.AvgPool2d(8)
        self.fc = nn.Linear(512 * 1 * 1, 2)

    def forward(self,x):
      x = self.layer1(x)
      x = self.layer2(x)
      x = self.layer3(x)
      x = self.layer4(x)
      x = self.layer5(x)
      x = self.avg(x)
      x = x.view(-1, 512 * 1 * 1)
      x = self.fc(x)
      return x

Transformations = transforms.Compose([transforms.ToPILImage(),
                                  transforms.Pad(64, padding_mode='reflect'),
                                  transforms.ToTensor(),
                                  transforms.Normalize(mean=[0.5, 0.5, 0.5],std=[0.5, 0.5, 0.5])])

path_to_model='model.ckpt'
def preprocess(data):
    data = [data]
    dataset_inp = Dataset(data_df = data,transform = Transformations)
    load_inp = DataLoader(dataset = dataset_inp,batch_size=1)
    #image = Transformations(np.array(Image.open(data)))
    return load_inp


from PIL import Image
image = Image.open("istockphoto-531314246-612x612.jpg")

st.set_page_config(page_title="Histopathological Cancer Detection")

# Divide page into two columns
col1, col2 = st.columns([1, 2])
with col1:
    st.image(image, use_column_width=True)

with col2:
    st.title("Histopathological Cancer Detection")

st.markdown("Histopathological Cancer using a Convoluted Neural Network")

wav = st.file_uploader("Upload your Image file (TIF)",type = ['tif'])
if wav is not None:
    st.image(Image.open(wav),width = 300)
    wav = preprocess(wav)
    model = CNN()
    model.load_state_dict(torch.load(path_to_model,map_location=torch.device('cpu')))
    model.to(torch.device('cpu'))
    model.eval()
    ans = 0
    with torch.no_grad():
        for img in wav:
            img = img.to(torch.device('cpu'))
            _,ans = torch.max(model(img).data,1)
    #ans = st.write(model(torch.tensor([wav])))
    st.write('The model predicts', 'that the sample is cancer positive' if ans == 1 else 'the sample doesn\'t have Cancer')
    
st.markdown("""
        <style>
            .css-znku1z.e16nr0p33 {
              margin-top: -75px;
              }
         </style>
      """, unsafe_allow_html=True)

st.sidebar.title("Sidebar")

st.sidebar.subheader("Github")
st.sidebar.markdown('https://github.com/sravan1023/cancer-detection')

# Add a section for key takeaways
st.sidebar.subheader("Key Takeaways")
st.sidebar.info("• The app is a Convolutional Neural Network (CNN) model that predicts whether a microscopic tissue is cancerous or not with an accuracy of over 84%.")
st.sidebar.info("• Users can upload an image to the app and receive a prediction.")
st.sidebar.info("• This project is a college project and not intended for real-world applications")
st.sidebar.info("• The code for the app is open-source and available on Github for further development and collaboration.")

# Add a section for collaboration
st.sidebar.subheader("Collaborator")
st.sidebar.write("Ch.Sravya- chayanam.nagasravya20@ifheindia.org")
st.sidebar.caption("• If you have any questions, feel free to contact")
st.sidebar.caption("• We welcome any feedback or suggestions for improvement!")
