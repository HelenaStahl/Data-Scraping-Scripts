# Data-Scraping-Scripts
API and non-API-based Data Collection 

## Reddit API Scripts

- **collect_hottest.py** : collects the 500 hottest posts in the subreddit specified. Writes one post per line the JSON output file.
         
         python3 collect_hottest.py -o <output_file> <subreddit>
         
## Beautiful Soup Scripts

- **scrape_courses.py** : pulls courses off pages with URLs of the form: https://www.mcgill.ca/study/2020-2021/courses/search?page=X where X is a number. The courses are printed in CSV format to stdout with the following columns (header included): CourseID, Course Name, # of credits

- **collect_relationships.py** : collects the relationships for a set of celebrities from whosdatewho.com. Takes as input a JSON configuration file containing a single JSON dictionary with the following structure:

         {“cache_dir”: “.data/wdw_cache”, “target_people”: [ “robert-downey-jr”, “justin-bieber” ] }
 
    The script fetches all relationships for the target individuals. All pages visited are cached in the cache directory specified - if the script is run twice          with the same target people, it will use data exclusively from the cache the second time. The output format for the file is:

         { “robert-downey-jr”: [ “person-1”, “person-2”, “person-3” ], “justin-bieber”: [] }



