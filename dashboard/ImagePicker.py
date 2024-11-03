import glob,os
import pandas as pd
from datetime import datetime
import numpy as np

def move_images():
    _images=os.listdir("dashboard/static/images/randomImages/unclassified")

    for _image in _images:
        if "IMG_" in _image:
            print(_image)
            os.rename(os.path.join("dashboard/static/images/randomImages/unclassified",_image), os.path.join("dashboard/static/images/randomImages/unclassified",_image.replace("IMG_",'')))

    for i in range(1,13):
        _path=os.path.join('dashboard','static','images','randomImages',str(i))
        if not os.path.exists(_path):
            os.mkdir(_path)

    for _image in _images:
        print(_image)
        date = datetime.strptime(_image[:8], '%Y%m%d')
        month=date.month

        old_image = os.path.join("dashboard","static","images","randomImages","unclassified",_image)
        new_image = os.path.join("dashboard","static","images","randomImages",str(month),_image)
        try:
            os.rename(old_image, new_image)
        except FileExistsError as fee:
            print(new_image, 'Already Exists')
            os.remove(old_image)

def get_random_image():
    potentialImagesFolder = os.path.join('dashboard','static','images','randomImages',str(datetime.now().month))
    potentialImages = os.listdir(potentialImagesFolder)
    print(potentialImages)
    randomImage = potentialImages[np.random.randint(len(potentialImages))]
    print(randomImage)
    image = os.path.join('images','randomImages',str(datetime.now().month), randomImage)
    image=image.replace("\\","/")
    return image, randomImage