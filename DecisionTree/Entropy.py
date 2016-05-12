from collections import OrderedDict
import math
import operator


class Entropy:
    
    def calculateThreshold(self, data):
        i = 0
        data_sort = []
        for val in data:
            if val != '?':
                data_sort.append(float(val))
            i = i+1
        
        data_sort = sorted(data_sort)
        threshold = []
        
        for i in range(len(data_sort)-1):
            threshold.append(float(data_sort[i]+data_sort[i+1])/float(2))
        
        
        ##removing duplicates from the threshold values
        threshold = sorted(set(threshold))
        
        return threshold
        
        
    def calculateEntropyContinuous(self,data, labels):
        thresholdArray = self.calculateThreshold(data)
        thresholdMin = 0.0
        entropyMin = float("inf")
        
        #print "threshold array length\t", len(thresholdArray)
        
        for threshold in thresholdArray:
            entropy = 0.0
            i = 0
            attribute_count = [0,0,0]
            label_positive_count = [0,0,0]
            label_negative_count = [0,0,0]
            for attribute_value in data:
                index = 1
                
                if attribute_value == "?":
                    index = 2
                elif float(attribute_value) <= threshold:
                    index = 0
                
                attribute_count[index] += 1
                
                if labels[i] == '+':
                    label_positive_count[index] += 1
                else:
                    label_negative_count[index] += 1
                
                i = i+1
              
            attribute_entropy = {}
            attribute_entropy[0] = 0.0  
            attribute_entropy[1] = 0.0 
            attribute_entropy[2] = 0.0 
            for index in range(3):
                total = label_positive_count[index] + label_negative_count[index]
                if total!= 0:
                    #print "total instances\t",total
                    xPos = float(label_positive_count[index])/float(total)
                    if xPos != 0:
                        xPos = xPos*math.log(xPos,2)
                    
                    xNeg = float(label_negative_count[index])/float(total)
                    if xNeg != 0:
                        xNeg = xNeg*math.log(xNeg,2)
                    
                    attribute_entropy[index] = -(xPos+xNeg)
                
            
            for index in range(3): 
                #print "entropy\t", index,(float(attribute_count[index])/float(i))*attribute_entropy[index]
                entropy += (float(attribute_count[index])/float(i))*attribute_entropy[index]
            
            if entropy < entropyMin:
                entropyMin = entropy
                thresholdMin = threshold
                #print "assigning minimum entropy for threshold\t",entropy, threshold
       
        return entropyMin,thresholdMin, attribute_entropy
    
    def calculateEntropyDiscrete(self, data, labels):   
        
        entropy = 0.0
        i = 0
        attribute_count = {}
        label_positive_count = {}
        label_negative_count = {}
        attribute_entropy = {}
        
        for attribute_value in data:
            #print "attribute value data\t", attribute_value
            if attribute_value in attribute_count:
                attribute_count[attribute_value] += 1
            else:
                attribute_count[attribute_value] = 1
            #print "labels\t", labels[i]
            if labels[i] == "+": 
                if attribute_value in label_positive_count:
                    label_positive_count[attribute_value] = label_positive_count[attribute_value] + 1
                else:
                    label_positive_count[attribute_value] = 1
            else :
                #print "increasing negative count\n"
                if attribute_value in label_negative_count:
                    label_negative_count[attribute_value] = label_negative_count[attribute_value] + 1
                else:
                    label_negative_count[attribute_value] = 1
            
             
            i = i+1   
        
        for attribute_value in attribute_count:
            if attribute_value not in label_positive_count:
                label_positive_count[attribute_value] = 0
            if attribute_value not in label_negative_count:
                label_negative_count[attribute_value] = 0
            
            total = label_positive_count[attribute_value] + label_negative_count[attribute_value]
            xPos = float(label_positive_count[attribute_value])/float(total)
            
            if xPos != 0:
                xPos = xPos*math.log(xPos,2)
            
            xNeg = float(label_negative_count[attribute_value])/float(total)
            if xNeg != 0:
                xNeg = xNeg*math.log(xNeg,2)
            
            attribute_entropy[attribute_value] = -(xPos+xNeg)
            
        
        for attribute in attribute_entropy:
            entropy += (float(attribute_count[attribute])/float(i))*attribute_entropy[attribute]
        
        return entropy, attribute_entropy
    
    
    def chooseAttribute(self, dataframe, features_continuous, features_discrete):  
        attribute_entropy = {}
        entropy_min = float("inf")
        featureSplit = ""
        thresholdMin = -1
        
        if features_discrete!= None:
            for features in features_discrete:
                entropy, temp = self.calculateEntropyDiscrete(dataframe[features].values, dataframe["P"].values)
                if entropy < entropy_min:
                    entropy_min = entropy
                    featureSplit = features
                    attribute_entropy = temp
        
        if features_continuous != None:
            for features in features_continuous:
                entropy,threshold,temp = self.calculateEntropyContinuous(dataframe[features].values, dataframe["P"].values)
                
                if entropy < entropy_min:
                    entropy_min = entropy
                    featureSplit = features
                    thresholdMin = threshold
                    attribute_entropy = temp
                    
        attribute_entropy = OrderedDict(sorted(attribute_entropy.items(), key = operator.itemgetter(1))[:])
        return featureSplit, thresholdMin, attribute_entropy 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    