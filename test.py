#coding:utf-8
from urllib.robotparser import RobotFileParser
 
def main():
    root_url = 'https://www.netkeiba.com/'
    rp = RobotFileParser()
 
    # robots.txtのurlを設定
    rp.set_url(root_url + 'robots.txt')
 
    rp.read()
 
    # Crawl-delayの取得
    print('Crawl-delay: ', rp.crawl_delay('*'))
 
    # クローリング許可があるか確認
    urls = [root_url, root_url + 'horse/2017100720.html']
    for url in urls:
        if rp.can_fetch('*', url):
            print('Crawling {} is allowed.'.format(url))
 
if __name__ == '__main__':
    main()