# -*- coding: utf-8 -*-
import urllib2, sys
from bs4 import BeautifulSoup
import unicodedata
import time


global baseURL,baseDomain,baseDir
#Link from where list of all movies and their links are obtained 
baseURL ="http://wogma.com/movies/basic/"
baseDomain = "http://wogma.com/"	
baseDir = "/home/sureya/Documents/instamojo/scrapped/"
 

def getReviewForMovie(url):
	"""
		Returns Movie comment for a given movie url.

	"""
	site= url
	header = {'User-Agent': 'Mozilla/5.0'}
	request = urllib2.Request(site,headers=header)
	page = urllib2.urlopen(request)

	# Ensuring the ASCII encoding for cleaner text in training data.
	soup = BeautifulSoup(page,from_encoding="UTF-8")
	divList  = soup.findAll("div",{"class":"review large-first-letter"})

	content = divList[0]
	allParas  = content.findAll("p")

	review  = ""
	
	for para in allParas :
	    review = review + para.getText() 


	if type(review) == unicode:
		normalizedReview = unicodedata.normalize('NFKD', review).encode('ascii','ignore')

	else:
		normalizedReview = review

	return normalizedReview



def gatherAllMovieURLs():
		"""
		Fetches list of all reviews by url in http://wogma.com/movies/basic/ page.

		"""


	site= baseURL
	header = {'User-Agent': 'Mozilla/5.0'}
	request = urllib2.Request(site,headers=header)
	page = urllib2.urlopen(request)
	soup = BeautifulSoup(page,from_encoding="UTF-8")
	aList  = soup.findAll("a")
	#Filtering tags that has Wogma Reviews
	reviewTags  = []
	for aTag in aList:
		if "title=\"wogma review of" in str(aTag):
			reviewTags.append(aTag)

	allMovieURLs = []

	for movie in reviewTags:
		url= str(movie).split("title")[0].split("href=")[1]
		allMovieURLs.append(url[1:-2])

	return allMovieURLs



if __name__ == '__main__':
	
	start_time = time.time()
	allMovieURLs = gatherAllMovieURLs()

	for reviewURL in allMovieURLs:

		fname = reviewURL.split("/")[-2]
		reviewContent = getReviewForMovie(baseDomain+reviewURL)

		File = open(baseDir+fname+".txt","w")
		File.write(reviewContent)
		File.close()
	print("--- %s minutes --- to scrape All Reviews"  % str((time.time() - start_time))/60)
    

      
    



    
