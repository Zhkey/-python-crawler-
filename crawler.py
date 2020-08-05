import requests
from lxml import etree
import os


class DouBan:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        self.all_content = []

    def get_page(self, url):
        r = requests.get(url, headers=self.headers)
        html = etree.HTML(r.text)
        lis = html.xpath('//ol[@class="grid_view"]/li')
        for li in lis:
            url_project = li.xpath('.//div[@class="hd"]/a/@href')[0]
            print(url_project)
            self.get_project(url_project)
            # time.sleep(1)
            # break

    def get_project(self, url_project):
        r = requests.get(url_project, headers=self.headers)
        html = etree.HTML(r.text)
        title = html.xpath('//h1[1]/span[1]/text()')[0]
        img_url = html.xpath('//div[@id="mainpic"]//img/@src')[0]
        content = html.xpath('//span[@class="all hidden"]/text()')
        if content:
            content = content[0].strip()
        else:
            content = html.xpath('//div[@id="link-report"]/span[1]/text()')[0].strip()
        links = html.xpath('//ul[@class="bs"]/li')
        if not links:
            link = ''
        else:
            for each in links:
                source = each.xpath('./a/@data-cn')[0]
                if source == "腾讯视频":
                    link = each.xpath('./a/@href')[0]
                    break
            else:
                link = links[0].xpath('./a/@href')[0]
        # print(title, img_url, content, link)
        self.all_content.append((title, content, link))
        self.get_image(img_url, title)

    def get_image(self, image_url, image_name):
        r = requests.get(image_url, headers=self.headers)
        with open('image/{}.jpg'.format(image_name), 'wb') as f:
            f.write(r.content)
            f.close()

    def write_csv(self, filename):
        content = "标题,简介,播放链接\n"
        for each in self.all_content:
            content += (each[0] + ',' + each[1] + ',' + each[2] + '\n')
        with open(filename, 'w', encoding='utf8') as f:
            f.write(content)


if __name__ == '__main__':
    os.mkdir('image')
    demo = DouBan()
    for i in range(4):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(i * 25)
        demo.get_page(url)

    demo.write_csv('douban.csv')

