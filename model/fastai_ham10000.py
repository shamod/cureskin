from fastai import *
from fastai.vision import *
import os

fastai.defaults.device = torch.device('cpu')

classes = ['nv', 'mel', 'bkl', 'bcc', 'akiec', 'vasc', 'df']

lesion_dict = dict(               # quick online research states:
    nv='Melanocytic nevi',       # common mole
    mel='Melanoma',              # very bad
    bkl='Benign keratosis',      # benign is good
    bcc='Basal cell carcinoma',  # not so good
    akiec='Actinic keratoses',   # potential precancer
    vasc='Vascular lesions',     # could be benign or malignant
    df='Dermatofibroma',         # benign
)

# df['diagnosis'] = df.dx.map(lesion_dict)

img = open_image(path, '?????.jpg')

# Run this code only once to load model
data2 = ImageDataBunch.single_from_classes(
             path, classes, tfms = get.transforms(), 
                size = 224).normalize(imagenet.stats)
learn = create_cnn(data2, models.resnet50, metrics=[error_rate, Recall(), Precision(), FBeta(), MatthewsCorreff()])
learn.load(path, 'export2')

pred_class, pred_idx, outputs = learn.predict(img)

print(pred_class)


