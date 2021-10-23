import argparse
from bs4 import BeautifulSoup
import json
import hashlib
import os 
import os.path as osp
import requests
import sys
import csv

#input: python3 scripts/scrape_courses.py -c <caching_dir> <page#>

#hashing cache function
def cache_func(dir, number):
    
    url = "https://www.mcgill.ca/study/2020-2021/courses/search?page="+number
    
    fname = hashlib.sha1(url.encode('utf-8')).hexdigest()
    full_fname = osp.join(dir, fname)

    contents = None
    if osp.exists(full_fname):
        print('Loading from cache')
    else:
        print('Loading from source')
        r = requests.get(url)
        contents = r.text
        with open(full_fname, 'w') as fh:
            fh.write(contents)

    return full_fname

def extract_info(filename):

    soup = BeautifulSoup(open(filename, 'r'), 'html.parser')

    field_list = soup.find_all("h4", class_="field-content")

    classes = []

    for element in field_list:
        for text in element.find_all('a'):
            classes.append(text.getText())

    return classes

#        Course ID = <word1> <word2>
#        Course # = the # from the end of the string "(# credits)"
#        Title = everything after word2, before the parentheses
#        Any name that can't be made to fit should be thrown out.
#        example: ANTH 412 Topics: Anthropological Theory (3 credits)

def format(classList):

    #print header - no spaces between columns as this is proper CSV format
    print ("CourseID,Course Name,# of credits")

    for c in classList:
        splitWords = c.split()

        #any course name should have at least 5 strings - course ID (2 words), course name (at least 1 word), # of credits (2 words)
        if (len(splitWords) <= 4):
            continue

        lastString = splitWords[-1]

        #some courses have 'CE' instead of credits -> skip these
        if (lastString != 'credits)'):
            continue

        #some courses have a newline at the end of the text so remove this
        if (lastString[:-2] == '\n'):
            lastString = lastString[:-2]
 
        #get second last index in list, this should be the number of credits
        numCredits = splitWords[-2]

        #make a copy of the string-split list so we can delete some elements
        courseName = splitWords.copy()

        #extract the course title -> delete first two words
        del courseName[0]
        del courseName[0]
        #delete last two words
        del courseName[-1]
        del courseName[-1]

        listToStr = ' '.join([str(word) for word in courseName])
    
        #print <word 1> and <word 2> (course ID), course name, and number of credits while skipping the '('
        print(splitWords[0] + " " + splitWords[1] + "," + listToStr + "," + numCredits[1:])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--caching_dir','-c', help='input a caching directory', required=True)
    parser.add_argument('page_number', help='input a page number')
    args = parser.parse_args()

    #check if the cache directory already exists - if it doesn't, then make it
    if not osp.exists(args.caching_dir):
        os.makedirs(args.caching_dir)
    
    htmlfile = cache_func(args.caching_dir, args.page_number)

    classList = extract_info(htmlfile)

    format(classList)

if __name__ == '__main__':
    main()


