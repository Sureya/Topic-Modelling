from os import walk
import os 
from random import randint
import pandas as pd
import re, string
import lda 
import numpy as np

def process_LDA_model(data,num_topics,num_top_words):
    model = lda.LDA(n_topics=num_topics, random_state=1, n_iter=100)
    mat = data.as_matrix()
    model.fit(mat)
    topic_word = model.topic_word_
    n_top_words = num_top_words+1
    vocab = list(data.columns.values)

    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))


class LDAModal(object):
    
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
        self.num_of_files = num_of_files

        self.readAllFiles()
        self.dataModel = self.makeDocumentTermMatrix()
        process_LDA_model(self.dataModel,self.num_topics,self.num_top_words)
        

    def readAllFiles(self):
        """
            Extracts all files from the given directory.

        """
        for (dirpath, dirnames, filenames) in walk(self.baseDirectory):
            self.fileNames.extend(filenames)
    
        self.fileNames  = self.fileNames[:self.num_of_files]

        for file_idx in range(len(self.fileNames)):
            temp = self.fileNames[file_idx]
            temp = self.baseDirectory + temp
            self.fileNames[file_idx] = temp


    def makeDocumentTermMatrix(self):
        docIndex = 0;
        AllWords = set()

        for name in self.fileNames:
            f = open(name,"r")
            content = f.read()
            words = content.rsplit()
            for wrd in words:
                out = re.sub('[%s]' % re.escape(string.punctuation), '', wrd)
                if out!='':
                    AllWords.add(out)

        self.data = pd.DataFrame(columns=list(AllWords))
        
        for x in range(self.num_of_files):
            row_idx = str("doc"+str(x))
            for y in AllWords:
                self.data.loc[row_idx,y] = 0
        
        for name in self.fileNames:
            f = open(name,"r")
            content = f.read()
            f.close()
            row_idx = str("doc"+str(docIndex))
            #print row_idx
            
            for word in list(self.data.columns.values):
                out = re.sub('[%s]' % re.escape(string.punctuation), '', word)

                if out != '':
                    if word in content:
                        self.data.loc[row_idx,word] = self.data.loc[row_idx,word]+1
                        
                       

            docIndex = docIndex+1
        self.data = self.data.fillna(0)
        
        
        return self.data

    


    

if __name__ == '__main__':

    direc = "/home/sureya/Documents/instamojo/scrapped"
    lda = LDAModal(direc,100,15,5)


                            