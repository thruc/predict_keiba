#coding:utf-8
import sys

from webscrape import scrapedata
from webscrape import scrapeurl

"""
ex)python main.py 2020 1 2020 2
2020�N1������2020�N2���܂ł̃f�[�^���擾

����1�F�f�[�^���擾���������Ԃ̍ŏ��̔N
����2�F�f�[�^���擾���������Ԃ̍ŏ��̌�
����3�F�f�[�^���擾���������Ԃ̍Ō�̔N
����4�F�f�[�^���擾���������Ԃ̍Ō�̌�
"""

if __name__ == "__main__":
    args = sys.argv
    print(args)
    urls = scrapeurl.get_urls(args)
    scrapedata.create_csv(urls)
