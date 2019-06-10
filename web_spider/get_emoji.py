import requests
import re
from bs4 import BeautifulSoup
import os
from hashlib import md5
import config
import bs4

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/74.0.3729.169 Safari/537.36'
}


def get_page(url):
    try:
        response = requests.get(url,headers=headers).text
    except:
        print('failed to catch the website')
        return None
    soup = BeautifulSoup(response, 'lxml')
    return soup


def download_images (images_url):
    if not os.path.exists(config.saving_path):
        os.makedirs(config.saving_path)
    for id in range(len(images_url)):
        try:
            image = requests.get(images_url[id])
            file_path = '{}.{}'.format(config.saving_path + '/'+ md5(image.content).hexdigest(),images_url[id][-3:])
            if not os.path.exists(file_path) :
                with open(file_path,'wb') as f:
                    f.write(image.content)
        except :
            print('download failed')


def parse_page(soup):
    images_list = soup.find_all(name='img',attrs={'class': "ui image lazy"})
    regex_str = '.*?data-original="(.*?)".*?'
    all_images_url = []
    for i in range(len(images_list)):
        try:
            each = str(images_list[i])
            image_data = re.match(regex_str, each)
            imageUrl = image_data.group(1)
            all_images_url.append(imageUrl)
        except:
            print('download failed')

    download_images(all_images_url)


def work():
    for i in range(config.page_num):
        url = config.url_base+str(i)+'.html'
        soup = get_page(url)
        parse_page(soup)
        print('already download page : ', str(i))


if __name__=='__main__':
    work();


