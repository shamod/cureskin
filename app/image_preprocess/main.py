import os
import re
import cv2
import numpy as np 
from google.colab.patches import cv2_imshow


img = []
i = 0
for root, dirnames, filenames in os.walk("drive/My Drive/imgInbox"): # Tested on colab, change once directory known
    for filename in filenames:
        if re.search("\.(jpg|jpeg|png|bmp|tiff)$", filename):
            filepath = os.path.join(root, filename)
            img = cv2.imread(filepath)       
            print(img.shape)
            imCopy = img.copy()
            imgOut = cv2.resize(imCopy,(224,224))
            print(imgOut.shape)
            cv2_imshow(imgOut)
            status = cv2.imwrite('drive/My Drive/imgOut/processed{:>02}.png'.format(i), imgOut)
            i += 1
