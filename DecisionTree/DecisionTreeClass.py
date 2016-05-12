from _ctypes import Array
from collections import OrderedDict
import copy
import operator

import Entropy
import numpy as np
import pandas as pd


class DecisionTree:
    def __init__(self, dataFrame, features_continuous, features_discrete):
        self.dataFrame = dataFrame
        self.features_continuous = features_continuous
        self.features_discrete = features_discrete
        self.data_dict = {}
        self.entropyObj = Entropy.Entropy()
    
      
    def pluralityValue(self,data):
        countPos = 0
        countNeg = 0
        for label in data:
            if label == '+':
                countPos += 1
            if label == '-':
                countNeg += 1
        
        if countPos >= countNeg : return '+'
        else: return '-'
            
            
    def createTree(self, examplesData, parentData, features_cont, features_disc, bestatt, value1):
        ##base cases for the decision tree
        if len(examplesData.index) == 0:
            return self.pluralityValue(parentData['P'])
        
        if len(pd.unique(examplesData['P'].values.ravel())) == 1:
            return (examplesData['P'].values)[0]
        
        if len(features_cont) == 0 and len(features_disc) == 0:
            return self.pluralityValue(examplesData['P'])
        else :
            bestAttribute,threshold, attribute_entropy = self.entropyObj.chooseAttribute(examplesData, features_cont, features_disc)
            data_dict = {bestAttribute:{}}
           
            if threshold != -1:
                ##pruning the tree according to entropy
                if attribute_entropy[1] == 0.0 or attribute_entropy[0] == 0.0:
                    return self.pluralityValue(examplesData['P'])
                
                features_cont_deep = copy.deepcopy(features_cont)
                features_disc_deep = copy.deepcopy(features_disc)
                
                index = features_cont_deep.index(bestAttribute)
                exs = pd.DataFrame()
                exs1 = pd.DataFrame()
                
                features_cont_deep.pop(index)
                exs1 = examplesData[pd.Series(examplesData[bestAttribute]).convert_objects(convert_numeric=True) > threshold]
                
                subtree = self.createTree(exs1, examplesData, features_cont_deep, features_disc_deep, bestAttribute,threshold)
                data_dict[bestAttribute]["+"+str(threshold)] = subtree
                
                features_cont_deep = copy.deepcopy(features_cont)
                features_disc_deep = copy.deepcopy(features_disc)
                
                exs = examplesData[pd.Series(examplesData[bestAttribute]).convert_objects(convert_numeric=True) <= threshold]
                
                features_cont_deep.pop(index)
                subtree = self.createTree(exs, examplesData, features_cont_deep, features_disc_deep, bestAttribute, threshold)
                data_dict[bestAttribute]["-"+str(threshold)] = subtree
                
            else:
                ##pruning the tree according to entropy
                
                if attribute_entropy[attribute_entropy.keys()[0]] == 0.0:
                    return self.pluralityValue(examplesData['P'])
                 
                for value in attribute_entropy.keys():
                    exs = examplesData.loc[examplesData[bestAttribute] == value]
                    
                    features_cont_deep = copy.deepcopy(features_cont)
                    features_disc_deep = copy.deepcopy(features_disc)
                    
                    index =  features_disc_deep.index(bestAttribute)
                    features_disc_deep.pop(index)
                    
                    subtree = self.createTree(exs, examplesData, features_cont_deep, features_disc_deep, bestAttribute, value)
                    
                    data_dict[bestAttribute][value] = subtree
                
        return data_dict
    
    
    def predict(self, decisionTree, test_tuple, default_class=None):
        #print "decision tree\t", decisionTree
        label = ''
        
        if not isinstance(decisionTree, dict):  # if the node is a leaf, return its class label
            return decisionTree
        
        if not decisionTree:  # if the node is empty, return the default class
            return default_class
        
        for key in decisionTree.keys():
            nextDict_tuple = ''
            if key in self.features_continuous:
                keys_cont = decisionTree[key].keys()
                
                key_num = keys_cont[0].replace("+","")
                key_num = key_num.replace("-","")
                
                test_value = test_tuple[key].values[0]
                
                
                if float(test_value) < float(key_num):
                    nextDict_tuple = decisionTree[key][('-'+str(key_num))]
                else:
                    nextDict_tuple = decisionTree[key][('+'+str(key_num))]
                    
            else :
                
                if str(test_tuple[key].values[0]) in decisionTree[key]:
                    nextDict_tuple = decisionTree[key][str(test_tuple[key].values[0])]
                else:
                    return default_class
           
            return self.predict(nextDict_tuple, test_tuple)
            
            
            
            

    
    
    

