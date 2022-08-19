# -*- coding: utf-8 -*-
"""activate_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14U9CziW3MRggLqrTIirZzRYTeEkkNRLs
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import torch
from torchvision import datasets, models, transforms
import torch.nn as nn
from torch.nn import functional as F
import torch.optim as optim
import torchvision

from PIL import Image

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = models.resnet101(weights=None).to(device)
model.fc = nn.Sequential(
               nn.Linear(2048, 128),
               nn.ReLU(inplace=True),
               nn.Linear(128, 2)).to(device)

model.load_state_dict(torch.load("/content/drive/MyDrive/machine learning projects/monkey pox/weight/resnet(101).h5"), strict=False)

import os
test_mon= os.listdir("/content/drive/MyDrive/machine learning projects/training set/monkey pox/test/monkeypox")
print(test_mon)
test_oth= os.listdir("/content/drive/MyDrive/machine learning projects/training set/monkey pox/test/others")
print(test_oth)
classes = os.listdir("/content/drive/MyDrive/machine learning projects/training set/monkey pox/test")
print(classes)

mon_list = [Image.open( "/content/drive/MyDrive/machine learning projects/training set/monkey pox/test/monkeypox/" + img_path) for img_path in test_mon]
oth_list = [Image.open( "/content/drive/MyDrive/machine learning projects/training set/monkey pox/test/others/" +img_path) for img_path in test_oth]
print(oth_list)

normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])

data_transforms = {
    'train':
    transforms.Compose([
        transforms.Resize((224,224)),
        transforms.RandomAffine(0, shear=10, scale=(0.8,1.2)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        normalize
    ]),
    'test':
    transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        normalize
    ]),
}

validation_batch1 = torch.stack([data_transforms['test'](img).to(device)
                                for img in mon_list])
validation_batch2 = torch.stack([data_transforms['test'](img).to(device)
                                for img in oth_list])

pred_logits_tensor = model(validation_batch1)
pred_logits_tensor

pred_probs = F.softmax(pred_logits_tensor, dim=1).cpu().data.numpy()
pred_probs

fig, axs = plt.subplots(len(mon_list), 1, figsize=(150, 100))
for i, img in enumerate(mon_list):
    ax = axs[i]
    ax.axis('off')
    ax.set_title("{:.0f}% other, {:.0f}% monkeypox".format(100*pred_probs[i,0],
                                                            100*pred_probs[i,1]))
    ax.imshow(img)

pred_logits_tensor = model(validation_batch2)
pred_logits_tensor
pred_probs = F.softmax(pred_logits_tensor, dim=2).cpu().data.numpy()
pred_probs

fig, axs = plt.subplots(len(oth_list), 1, figsize=(150, 100))
for i, img in enumerate(oth_list):
    ax = axs[i]
    ax.axis('off')
    ax.set_title("{:.0f}% other, {:.0f}% monkeypox".format(100*pred_probs2[i,0],
                                                            100*pred_probs2[i,1]))
    ax.imshow(img)



