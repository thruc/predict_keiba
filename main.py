#coding:utf-8
import sys

from webscrape import scrapedata
from webscrape import scrapeurl

def execute(year, mon):
    urls = scrapeurl.get_urls(year, mon)
    scrapedata.create_csv(year, mon, urls)


if __name__ == "__main__":
    args = sys.argv
    print(args)
    start_year = int(args[1])
    end_year = int(args[2])
    for year in range(start_year, end_year+1):
        for mon in range(1,13):
            execute(year, mon)
            

        

    
