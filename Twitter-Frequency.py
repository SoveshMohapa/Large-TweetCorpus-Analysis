import sys
import re
import math
from collections import defaultdict
import random

def rand(hist):
	rnum = random.uniform(0,1)
	for x in hist:
		rnum -= hist[x]
		if rnum < 0: return x
	return x

def clean(line):
	#use the following syntax for all your replacements so that unicode is properly treated
	#line = re.sub(u'replace_regexp','with_regexp',line)

	#Replace all Twitter handles with @@@
	line = re.sub(u'\@\S+','@@@',line)

	#Replace the urls with www
	line = re.sub(u'https\S+', 'www', line)

	#Replace the hashtags with ###
	line = re.sub(u'\#\w*','###',line)

	#Removal of the punctuation from the tweets
	line = re.sub(u'[:;!?\.,]','',line)

	#Removal of the trailing and leading of whitespaces
	line = re.sub(u'^\s+|\s+$','',line)

	#Making of all characters into the lowercase
	for i in re.findall(u'([A-Z]+)', line):
    		line = line.replace(i,i.lower())
	return line

def normalize(hist):
	# this is a void function that normalizes the counts in hist
	# given a dictionary of word-frequency pairs, this function modifies the frequencies so that they sum to 1
	# remove the following print statment once you complete this function
	
	#Sum of all the word frequencies in the hist dictionary
	total_wordfrequencies = sum(hist.values())

	#Normalizing the frequencies of each word
	for word in hist:
		hist[word] = hist[word]/total_wordfrequencies
		
def get_freqs(f):
	wordfreqs = defaultdict(lambda: 0)
	lenfreqs = defaultdict(lambda: 0)

	for line in f.readlines():
		#print(line)
		line = clean(line)
		words = re.split(u'\s+|\s+[-]+\s+', line)
		lenfreqs[len(words)]+=1
		for word in words:
			wordfreqs[word.encode("utf8")]+=1
	
	normalize(wordfreqs)
	normalize(lenfreqs)
	return (wordfreqs,lenfreqs)

def save_histogram(hist,filename):
	#Rank of the Word in the hist dictionary
	rank = 1
	outfilename = re.sub("\.txt$","_out.txt",filename)
	outfile = open(outfilename,'w',encoding ="utf8" )
	print("Printing Histogram for", filename, "to", outfilename)
	for word, count in sorted(hist.items(), key = lambda pair: pair[1], reverse = True):

		#Adding the math library and using the log function from it
		output = u"%-13.6f\t%s\t%0.4f\t%0.4f\n" % (count,word.decode("utf8"),math.log(count),math.log(rank))

		outfile.write(output)

		#Changing the rank to the next consecutive for the processing
		rank += 1

def get_top(hist,N):
    sorted_list = sorted(hist.items(), key = lambda item: item[1], reverse = True)

    most_freqwords = []

	#Adding the for loop to process the slicing part
    for i in sorted_list[:N]:
	    most_freqwords.append(i[0])
	
	# return a list of the N most frequent words in hist
    return most_freqwords

def filter(hist,stop):
	for word in stop:
		if word in hist: hist.pop(word)
	normalize(hist)

def main():
	file1 = open(sys.argv[1],encoding="utf8")
	(wordf1, lenf1) = get_freqs(file1)
	stopwords = get_top(wordf1, 130)
	save_histogram(wordf1,sys.argv[1])
	
	for fn in sys.argv[2:]:
		file = open(fn,encoding="utf8")
		(wordfreqs, lenfreqs) = get_freqs(file)
		#filter(wordfreqs, stopwords)
		save_histogram(wordfreqs,fn)


		print("Printing random tweets from",fn)
		for x in range(5):
			n = rand(lenfreqs)
			print(n, "random words:")
			for i in range(n):
				print(' ',rand(wordfreqs), end='')
			print()

## This is special syntax that tells python what to do (call main(), in this case) if this  script is called directly
## this gives us the flexibility so that we could also import this python code in another script and use the functions
## we defined here
if __name__ == "__main__":
    main()
