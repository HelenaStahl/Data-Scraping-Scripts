import argparse
from bs4 import BeautifulSoup
import json
import hashlib
import os 
import os.path as osp
import requests

def extract_relationships_from_candidate_links(candidates, person_url):
    relationships = []

    for link in candidates:
        if 'href' not in link.attrs:
            print(f'skipping {link}')
            continue

        href = link['href']

        if href.startswith('/dating') and href != person_url:
            #skip the '/dating/' at the beginning of each string and append to list
            relationships.append(href[8:])
    
    return relationships

def extract_relationships(filename, person):

    relationships = []
    person_url = "/dating/"+person

    soup = BeautifulSoup(open(filename, 'r'), 'html.parser')

    status_h4 = soup.find('h4', 'ff-auto-status')

    key_div = status_h4.next_sibling

    candidate_links = key_div.find_all('a')

    relationships.extend(extract_relationships_from_candidate_links(candidate_links, person_url))

    if len(relationships) > 1:
        raise Exception('Too many relationships - should have only one')

    rels_h4 = soup.find('h4', 'ff-auto-relationships')

    sib = rels_h4.next_sibling

    while sib is not None and sib.name == 'p':
        candidate_links = sib.find_all('a')
        sib = sib.next_sibling

        relationships.extend(extract_relationships_from_candidate_links(candidate_links, person_url))

    return relationships

#hashing cache function
def cache_func(dir, person):
    
    url = 'https://www.whosdatedwho.com/dating/'+person

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


def main():
        parser = argparse.ArgumentParser()
        parser.add_argument('--input_file','-c', help='input a json config file', required=True)
        parser.add_argument('--output_file','-o', help='input a json output file', required=True)
        args = parser.parse_args()

        config_file = open(args.input_file, 'r')

        dict = json.load(config_file)
        cache_dir = dict['cache_dir']
        people = dict['target_people']

        #check if the cache directory already exists - if it doesn't, then make it
        if not osp.exists(cache_dir):
            os.makedirs(cache_dir)

        myDict = {}

        for person in people:
            #get the html file from source or cache
            htmlfile = cache_func(cache_dir, person)
            #get all relationships as a list
            relationships = extract_relationships(htmlfile, person)
            #place in dictionary
            myDict[person] = relationships
            
        #load dictionary into output file
        with open(args.output_file, 'w') as file:
            json.dump(myDict, file)

if __name__ == '__main__':
    main()


