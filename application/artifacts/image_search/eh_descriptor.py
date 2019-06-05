import cv2
import numpy as np
import math

class EdgeHistogramDescriptor():

    def __init__(self, rows, cols, threshold=0, canny=False):
        sqrt2 = math.sqrt(2)
        self.kernels = (np.matrix([[1,1],[-1,-1]]), \
                np.matrix([[1,-1],[1,-1]]),         \
                np.matrix([[sqrt2,0],[0,-sqrt2]]),  \
                np.matrix([[0,sqrt2],[-sqrt2,0]]),  \
                np.matrix([[2,-2],[-2,2]]));
        self.bins = [len(self.kernels)]
        self.range = [0,len(self.kernels)]
        self.rows = rows
        self.cols = cols
        self.prefix = "EDH"
        self.threshold = threshold
        self.canny = canny

    def name(self):
        return "EdgeHistogram"

    def describe(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if self.canny:
            frame = cv2.Canny(frame, 100, 200)
        descriptor = []
        dominantGradients = np.zeros_like(frame)
        maxGradient = cv2.filter2D(frame, cv2.CV_32F, self.kernels[0])
        maxGradient = np.absolute(maxGradient)
        for k in range(1,len(self.kernels)):
            kernel = self.kernels[k]
            gradient = cv2.filter2D(frame, cv2.CV_32F, kernel)
            gradient = np.absolute(gradient)
            np.maximum(maxGradient, gradient, maxGradient)
            indices = (maxGradient == gradient)
            dominantGradients[indices] = k

        frameH, frameW = frame.shape
        for row in range(self.rows):
            for col in range(self.cols):
                mask = np.zeros_like(frame)
                mask[int(((frameH/self.rows)*row)):int(((frameH/self.rows)*(row+1))),int((frameW/self.cols)*col):int(((frameW/self.cols)*(col+1)))] = 255
                hist = cv2.calcHist([dominantGradients], [0], mask, self.bins, self.range)
                print(hist)
                hist = cv2.normalize(hist,None)
                print(hist)
                descriptor.append(hist)
        list = (np.concatenate([x for x in descriptor])).tolist()
        return_list = []
        for item in list:
            return_list.append(item[0])
        return return_list

    def distance(self, histSketch, histImage):
        d = 0
        for i in range(len(histImage)):
            # if histSketch[i]==0.0:
            #    continue
            d += math.pow(histImage[i] - histSketch[i], 2)
        return math.sqrt(d)