# -*- coding: utf-8 -*-
import numpy as np
from os import walk
import os 
from random import randint
import pandas as pd
import re, string

import sklearn.feature_extraction.text as text
from sklearn import decomposition

class Model(object):
	
	"""
	Input :

	    [argument 1] * directory = path to input files. 
	    [argument 2] * num_of_files = Number of files to process.
	    [argument 3] * num_topics = number of topics to divide.
	    [argument 4] * num_top_words = Number of important words to be fetched.
 	
 	Output :

 	  * Extracted topic and most "N" significant words from each topic.

	"""
	
	def __init__(self, directory, num_of_files,num_topics,num_top_words):
		
		self.baseDirectory = directory
		self.baseDirectory = self.baseDirectory.replace('\\','/')

		if self.baseDirectory[-1] != '/':
			self.baseDirectory = self.baseDirectory+'/'

		self.fileNames = []

		self.num_topics = num_topics
		self.num_top_words = num_top_words
		self.topic_words = []

		self.readAllFiles(num_of_files)
		self.extractTopic()

	def readAllFiles(self,num_of_files):
		"""
			Extracts all files from the given directory.

		"""
		for (dirpath, dirnames, filenames) in walk(self.baseDirectory):
			self.fileNames.extend(filenames)
    
		self.fileNames  = self.fileNames[:num_of_files]

	def extractTopic(self) :
		
		"""	* Tokenize the all words
			* Eliminates any word with less than two letters
			* Forms term frequency–inverse document frequency for each word
			* Generate Document-term_matrix
			* Classify topics based on Document-term_matrix and frequency–inverse document frequency 
			* Gathers first "N" numbers from each topic 
		"""


		self.vectorizer = text.CountVectorizer(input='filename', stop_words='english', min_df=2)
		
		for x in range(len(self.fileNames)):
		    temp = self.fileNames[x]
		    self.fileNames[x] = self.baseDirectory+temp 
		
		self.dtm = self.vectorizer.fit_transform(self.fileNames).toarray()
		self.vocab = np.array(self.vectorizer.get_feature_names())
		self.clf = decomposition.NMF(n_components=self.num_topics, random_state=1)

		self.doctopic = self.clf.fit_transform(self.dtm)



		for topic in self.clf.components_:
		         word_idx = np.argsort(topic)[::-1][0:self.num_top_words]
		         self.topic_words.append([self.vocab[i] for i in word_idx])

		for t in range(len(self.topic_words)):
		         print("Topic {}: {}".format(t, ' '.join(self.topic_words[t][:15])))





if __name__ == '__main__':
	
	direc = "/home/sureya/Documents/instamojo/scrapped"

	""" [argument 1] * directory = path to input files. 
	    [argument 2] * num_of_files = Number of files to process.
	    [argument 3] * num_topics = number of topics to divide.
	    [argument 4] * num_top_words = Number of important words to be fetched.
	"""
	
	W20 = Model(direc,100,15,5)