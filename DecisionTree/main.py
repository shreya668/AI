'''
Created on Nov 28, 2015

@author: shreya
'''
from ctypes.macholib.framework import test_framework_info
import math
import random
import sys

from DecisionTreeClass import DecisionTree
import Entropy
import numpy as np
import pandas as pd


if __name__ == '__main__':
    if len(sys.argv) < 1:
        print 'input not in correct format'
        exit(-1)
    #try:
    data_frame = pd.read_csv(sys.argv[1])
    
    features_continuous = ["B","C","H","K","N","O"]
    features_discrete = ["A","D","E","F","G","I","J","L","M"]
    
    ##handling missing values
    for feat in features_continuous:
        if len(data_frame[data_frame[feat].astype(str) == '?']) > 0:
            df = data_frame[data_frame[feat].astype(str) != '?']
            counts = pd.Series(df[feat]).value_counts()
            
            total_val = 0.0
            total_num = 0.0
            for val in counts:
                total_val += (val*counts[val])
                total_num = counts[val]
            
            mean_val = total_val/total_num
            data_frame.loc[data_frame[feat].astype(str) == '?', feat] = mean_val
    
    for feat in features_discrete:
        if len(data_frame[data_frame[feat].astype(str) == '?']) > 0:
            df = data_frame[data_frame[feat].astype(str) != '?']
            counts = pd.Series(df[feat]).value_counts()
            data_frame.loc[data_frame[feat].astype(str) == '?', feat] = counts.argmax()
    
    accuracy = 0.0

    ##dividing into training and testing data set into 80-20 ratio
    msk = np.random.rand(len(data_frame)) < 0.8

    data_frame_train = data_frame[msk]
    data_test_frame = data_frame[~msk]
    
    ##create decision tree
    dt = DecisionTree(data_frame_train, features_continuous, features_discrete)
    tree = dt.createTree(data_frame_train, None, features_continuous, features_discrete, "", "")
    
    dt.features_continuous = ["B","C","H","K","N","O"]
       
       
    ##testing decision tree
    i = 0
    count = 0
    count_none = 0
    while( i < len(data_test_frame)-2):
        
        label = dt.predict(tree, data_test_frame[i:i+1])
        i = i+1
        if label == data_test_frame[i:i+1]['P'].values[0]:
            count = count+1
        if not label:
            count_none = count_none+1
     
    accuracy += float(count)/float(len(data_test_frame))
    
    
    
    print "Accuracy:\t", float(accuracy)
        
