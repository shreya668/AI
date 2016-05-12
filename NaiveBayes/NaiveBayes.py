__author__ = 'arpita'
import sys
import numpy
import math

class NaiveBayes(object):
    def __init__(self):
        self.trainImages = {}
        self.trainLabels = []
        self.testImages = {}
        self.testLabels = []
        self.probClass = numpy.zeros(10)
        self.probPxClass = numpy.zeros((10,812))

    def readLabel(self,file,type):
        labels = open(file,'r')
        for label in labels:
            if type == "train":
                self.trainLabels.append(label.strip())
            else:
                self.testLabels.append(label.strip())
        labels.close()

    def readImage(self,file,type):
        images = open(file,'r')
        imgCnt = 0
        mat = numpy.zeros(28*29)
        j = 0
        for line in images:
            if not line.strip() and j + 29 <= (28*29-1):
                j += 29
            else:
                for letter in line:
                    if j > (28*29-1):
                        j = 0
                        if type == "train":
                            self.trainImages[imgCnt] = mat
                        else:
                            self.testImages[imgCnt] = mat
                        imgCnt += 1
                        mat = numpy.zeros(28*29)
                    if letter == ' ':
                        mat[j] = 0
                    if letter == '+':
                        mat[j] = 1
                    if letter == '#':
                        mat[j] = 2
                    j = j + 1
        if type == "train":
            self.trainImages[imgCnt] = mat
        else:
            self.testImages[imgCnt] = mat
        images.close()

    def trainModel(self):

        #calculate class probability
        for i in range(len(self.trainLabels)):
            cls = int(self.trainLabels[i])
            self.probClass[cls] = self.probClass[cls] + 1
        for i in range(len(self.probClass)):
            self.probClass[i] = (self.probClass[i])/len(self.trainLabels)

        #calculate probability of pixels given class
        for i in range(len(self.trainLabels)):
            cls = int(self.trainLabels[i])
            imgArray = self.trainImages[i] #812 pixels per image corresponding to label
            for j in range(len(imgArray)):
                #treating grey and black pixels similar
                if (imgArray[j] == 1 or imgArray[j] == 2):
                    self.probPxClass[cls][j] += 1

        for i in range(len(self.probPxClass)):
            for j in range(len(self.probPxClass[0])):
                denom =  (self.probClass[i]*len(self.trainLabels))
                self.probPxClass[i][j] = (self.probPxClass[i][j] + 1)/(denom + 2)

    def predictClass(self,img):
        result = numpy.zeros(len(self.probClass))
        for i in range(len(self.probClass)):
            ans = 0
            for j in range(len(img)):
                if (img[j] == 1 or img[j] == 2):
                    ans = ans + math.log(self.probPxClass[i][j],2)
                else:
                    ans += math.log(1 - self.probPxClass[i][j],2)
            result[i] = ans*math.log(self.probClass[i],2)
        return result.argmin()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'input not in correct format'
        exit(-1)

    nb = NaiveBayes()
    nb.readImage(sys.argv[1],"train")
    nb.readLabel(sys.argv[2],"train")
    nb.readImage(sys.argv[3],"test")
    nb.readLabel(sys.argv[4],"test")
    nb.trainModel()
    predicted = numpy.zeros(len(nb.testImages))

    accuracy = 0
    for i in range(len(nb.testImages)):
        predicted[i] = nb.predictClass(nb.testImages[i])
        if int(predicted[i]) == int(nb.testLabels[i]):
            accuracy += 1
    print "accuracy:",accuracy

    matrix = numpy.zeros((10,10))
    for i in range(len(nb.testLabels)):
        matrix[int(nb.testLabels[i])][int(predicted[i])] += 1
    print "confusion matrix:"
    print matrix

    precision = {}
    recall = {}
    for i in range(len(matrix)):
        tpfp = 0
        tpfn = 0
        for j in range(len(matrix)):
            num = matrix[i][i]
            tpfp += matrix[j][i]
            tpfn += matrix[i][j]
        precision[i] = num/tpfp
        recall[i] = num/tpfn
    print "precision for each digit",precision
    print "recall for each digit:",recall
