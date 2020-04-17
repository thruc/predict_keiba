#coding:utf-8
import sys

from webscrape import scrapedata
from webscrape import scrapeurl

"""
ex)python main.py 2020 1 2020 2
2020年1月から2020年2月までのデータを取得

引数1：データを取得したい期間の最初の年
引数2：データを取得したい期間の最初の月
引数3：データを取得したい期間の最後の年
引数4：データを取得したい期間の最後の月
"""

if __name__ == "__main__":
    args = sys.argv
    print(args)
    urls = scrapeurl.get_urls(args)
    scrapedata.create_csv(urls)
