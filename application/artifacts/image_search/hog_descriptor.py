import cv2
import numpy as np
import math
import imutils


class HOGDescriptor:

    def __init__(self, canny=False):
        self.canny = canny
        pass

    def describe(self, image):
        image = cv2.resize(image, (256, 256))
        if self.canny:
            image = cv2.Canny(image, 100, 200)
        winSize = (256, 256)
        blockSize = (64, 64)
        blockStride = (32, 32)
        cellSize = (32, 32)
        nbins = 8
        derivAperture = 1
        winSigma = 4.
        histogramNormType = 0
        L2HysThreshold = 2.0000000000000001e-01
        gammaCorrection = 0
        nlevels = 64
        hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins, derivAperture, winSigma,
                                histogramNormType, L2HysThreshold, gammaCorrection, nlevels)

        # hog = cv2.HOGDescriptor()
        winStride = (16, 16)
        padding = (0, 0)
        locations = ((0, 0), (0, 16), (0, 32))
        # winStride, padding, locations
        hist = hog.compute(image)

        return_list = []
        for item in hist:
            return_list.append(abs(float(item[0])))
        return return_list

    def name(self):
        return "HistogramOfOrientedGradients"

    def distance(self, histSketch, histImage):
        d = 0
        skip = 0
        for i in range(len(histSketch)):
            # if skip >0:
            #    skip -=1
            #    continue
            # if i%9==0:
            #    if histSketch[i]==0.0 and histSketch[i+1]==0.0 and histSketch[i+2]==0.0 and histSketch[i+3]==0.0 and histSketch[i+4]==0.0 and histSketch[i+5]==0.0 and histSketch[i+6]==0.0 and histSketch[i+7]==0.0:
            #        skip = 7
            #        continue
            if (histSketch[i] == 0.0):
                continue
            d += math.pow(histImage[i] - histSketch[i], 2)
        return math.sqrt(d)

    def pyramid(self, image, scale=2, minSize=(30, 30)):
        # yield the original image
        yield image

        # keep looping over the pyramid
        while True:
            # compute the new dimensions of the image and resize it
            w = int(image.shape[1] / scale)
            image = imutils.resize(image, width=w)

            # if the resized image does not meet the supplied minimum
            # size, then stop constructing the pyramid
            if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
                break

            # yield the next image in the pyramid
            yield image

    def sliding_window(self, image, stepSize, windowSize):
        # slide a window across the image
        for y in range(0, image.shape[0], stepSize):
            for x in range(0, image.shape[1], stepSize):
                # yield the current window
                yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])