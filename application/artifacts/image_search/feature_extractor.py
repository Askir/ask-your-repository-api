import cv2

#from .color_descriptor import ColorDescriptor
from .eh_descriptor import EdgeHistogramDescriptor
from .hog_descriptor import HOGDescriptor
import imutils

class FeatureExtractor():

    @classmethod
    def default(cls, sketch=False):
        descriptors = [
            HOGDescriptor(canny=True)
            #EdgeHistogramDescriptor(4, 4, canny=True)
            #ColorDescriptor([8, 12, 3])
        ]
        return FeatureExtractor(descriptors, sketch)

    def __init__(self, descriptors,sketch=False):
        self.descriptors = descriptors
        self.sketch = sketch

    def extract(self, image_path):
        image = cv2.imread(image_path)
        if image.shape[0] > image.shape[1]:
            image = imutils.resize(image, width=256)
        else:
            image = imutils.resize(image, height=256)
        bordersize = 32
        image = cv2.copyMakeBorder(image, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize,
                                   borderType=cv2.BORDER_CONSTANT, value=[0, 0, 0])
        win_shape = (256,256)

        descriptor = HOGDescriptor(canny=True)
        if not self.sketch:
            features = []
            for x,y,window in descriptor.sliding_window(image, 16, win_shape):
                if window.shape[0] != win_shape[0] or window.shape[1] != win_shape[1]:
                    continue
                features.append(descriptor.describe(window))
            if len(features) == 0:
                raise Exception("NO FEATURES FOUND")
            return features
        else:
            return descriptor.describe(image)
        return features
