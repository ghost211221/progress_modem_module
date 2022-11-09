import os
import re
import json

import pytesseract
import cv2
import matplotlib.pyplot as plt
from PIL import Image

root = 'screens/program'

data_dict = {}

for entity in os.listdir(root):
    path = os.path.join(root, entity)
    if os.path.isfile(path):
        continue
    for pict in os.listdir(path):
        file_path = os.path.join(path, pict)

        image = cv2.imread(file_path)
        # получаем строку
        string = pytesseract.image_to_string(image)
        string = re.sub(r'\n{2,2}', '', string)
        string = re.sub(r'\n{1,1}', ' ', string)
        data_dict[file_path] = string

with open('recognized.json', 'w') as f:
    f.write(json.dumps(data_dict, indent=4))