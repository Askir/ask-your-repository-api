import cv2

#from .color_descriptor import ColorDescriptor
from .eh_descriptor import EdgeHistogramDescriptor
from .hog_descriptor import HOGDescriptor


class FeatureExtractor():

    @classmethod
    def default(cls):
        descriptors = [
            HOGDescriptor(canny=True)
            #EdgeHistogramDescriptor(4, 4, canny=True)
            #ColorDescriptor([8, 12, 3])
        ]
        return FeatureExtractor(descriptors)

    def __init__(self, descriptors):
        self.descriptors = descriptors

    def extract(self, image_path):
        image = cv2.imread(image_path)
        features = {}
        for descriptor in self.descriptors:
            features[descriptor.name()] = (descriptor.describe(image))
        return features
