import requests
import json

def get_posts(subreddit_name):

	num_posts = 100
	
	data = requests.get(f'http://api.reddit.com/r/{subreddit_name}/new?limit={num_posts}', headers={'User-Agent': 'mac:requests (by /u/helenastahl)'})
	
	content = data.json() #this is how we turn the content from a string to json dictionary objects

	content = data.json()['data']

	return content['children']


def main():

    #write 1000 posts to sample 1 file
    posts = get_posts('funny')
    output_file = open('../data/sample1.json', 'w')
    for line in posts:
        json.dump(line, output_file)
        output_file.write("\n")

    posts = get_posts('AskReddit')
    for line in posts:
        json.dump(line, output_file)
        output_file.write("\n")
    
    #we need the 100 posts from AskReddit in both sample json files
    output_file2 = open('../data/sample2.json', 'w')
    for line in posts:
        json.dump(line, output_file2)
        output_file2.write("\n")

    posts = get_posts('gaming')
    for line in posts:
        json.dump(line, output_file)
        output_file.write("\n")

    posts = get_posts('aww')
    for line in posts:
        json.dump(line, output_file)
        output_file.write("\n")
    
    posts = get_posts('pics')
    for line in posts:
        json.dump(line, output_file)
        output_file.write("\n")

    posts = get_posts('Music')
    for line in posts:
        json.dump(line, output_file)
        output_file.write("\n")

    posts = get_posts('science')
    for line in posts:
        json.dump(line, output_file)
        output_file.write("\n")
    
    posts = get_posts('worldnews')
    for line in posts:
        json.dump(line, output_file)
        output_file.write("\n")

    posts = get_posts('videos')
    for line in posts:
        json.dump(line, output_file)
        output_file.write("\n")
    
    posts = get_posts('todayilearned')
    for line in posts:
        json.dump(line, output_file)
        output_file.write("\n")
    
    output_file.close()

    #write 1000 posts to sample 2 file

    posts = get_posts('memes')
    for line in posts:
        json.dump(line, output_file2)
        output_file2.write("\n")

    posts = get_posts('politics')
    for line in posts:
        json.dump(line, output_file2)
        output_file2.write("\n")

    posts = get_posts('nfl')
    for line in posts:
        json.dump(line, output_file2)
        output_file2.write("\n")

    posts = get_posts('nba')
    for line in posts:
        json.dump(line, output_file2)
        output_file2.write("\n")

    posts = get_posts('wallstreetbets')
    for line in posts:
        json.dump(line, output_file2)
        output_file2.write("\n")

    posts = get_posts('teenagers')
    for line in posts:
        json.dump(line, output_file2)
        output_file2.write("\n")

    posts = get_posts('PublicFreakout')
    for line in posts:
        json.dump(line, output_file2)
        output_file2.write("\n")

    posts = get_posts('leagueoflegends')
    for line in posts:
        json.dump(line, output_file2)
        output_file2.write("\n")

    posts = get_posts('unpopularopinion')
    for line in posts:
        json.dump(line, output_file2)
        output_file2.write("\n")

    output_file2.close()


if __name__ == '__main__':
	main()