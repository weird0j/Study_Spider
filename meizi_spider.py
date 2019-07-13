#coding=utf-8
import requests,os
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
from concurrent.futures import as_completed
import threading

basepath = r'E:\妹子图\\'
ua = UserAgent()
head = {
    'User-Agent': ua.random
}
def header(referer):

    headers = {
        'Host': 'i.meizitu.net',
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': '{}'.format(referer),
    }

    return headers

def request_page(baseurl):
    try:
        response = requests.get(baseurl, headers=head)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

def get_page_urls():
    # 获取每一页的详情url
    urls = []
    for i in range(1,3):
        baseurl = 'https://www.mzitu.com/page/{}'.format(str(i))
        html = request_page(baseurl)
        soup = BeautifulSoup(html, 'lxml')
        lis = soup.find(class_='postlist').find_all('li')
        for li in lis:
            url = li.find('span').find('a').get('href')
            print('页面链接：%s' % url)
            urls.append(url)
    return urls

def download(url):
    html = request_page(url)
    soup = BeautifulSoup(html, 'lxml')
    total = soup.find(class_='pagenavi').find_all('a')[-2].find('span').string
    title = soup.find('h2').string
    image_lists = []
    for i in range(int(total)):
        html = request_page(url + '/%s' % (int(i) + 1))
        soup = BeautifulSoup(html, 'lxml')
        img_url = soup.find('img').get('src')
        # print(title,img_url)
        image_lists.append(img_url)
    download_Pic(title, image_lists)

def download_Pic(title, image_lists):
    # 新建文件夹
    if not os.path.exists(basepath+title):
        os.makedirs(basepath+title)
    j = 1
    # 下载图片
    for item in image_lists:
        filename = basepath + '%s/%s.jpg' % (title, str(j))
        print('downloading....%s : NO.%s' % (title, str(j)))
        with open(filename, 'wb') as f:
            img = requests.get(item, headers=header(item)).content
            f.write(img)
        j += 1

def download_all_images(list_page_urls):
    # works = len(list_page_urls)
    # with ThreadPoolExecutor(max_workers=5) as executor:
    #     for url in list_page_urls:
    #         executor.submit(download, url)

    threads = []
    for i in range(len(list_page_urls)):
        t = threading.Thread(target=download, args=(list_page_urls[int(i)],))
        threads.append(t)
    for i in threads:
        i.start()
    for i in threads:
        i.join()

if __name__ == '__main__':
    list_page_urls = get_page_urls()
    download_all_images(list_page_urls)
