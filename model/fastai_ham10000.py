from fastai import *
from fastai.vision import *
import os

path = ('/home/craig/Downloads/')

learner = load_learner(path, 'export2')

print(learner.predict(open_image('/home/craig/Downloads/moles/melanoma.jpeg')))

