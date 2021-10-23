import requests
import json
import argparse

def getRedditData(subreddit):
    content = []
    #when we first make the call, we are starting at the top of the subreddit so there is no after value
    after = "none"

    #request 100 posts 5 times
    for req in range(5):
        data = requests.get("https://api.reddit.com"+subreddit+"/hot.json?limit=100&after="+after, headers={'User-Agent': 'mac:requests (by /u/helenastahl)'})
        dataToJson = data.json()
        content.append(dataToJson)
        #update the after variable so we move to the following 100 posts instead of getting the same 100 posts when we loop again
        after = dataToJson["data"]["after"]

    return content


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--output_file','-o', help="input a .json output file argument", required=True)
    parser.add_argument('subreddit', help="input a subreddit")

    args = parser.parse_args()

    subreddit = args.subreddit
    file = args.output_file

    output_file = open(file, 'w')

    content = getRedditData(subreddit)

    #trim the data from the requests to just include the 'children' data with one post on each line
    for post in content:
        for x in range(100):
            json.dump(post['data']['children'][x], output_file)
            output_file.write("\n")
    

if __name__ == '__main__':
	main()

