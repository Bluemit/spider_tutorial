import scrapy
from bs4 import BeautifulSoup
import json
import codecs


class ShuaihaoshenSpider(scrapy.Spider):
    name = "shuaihaoshen"

    def start_requests(self):
        urls = [
        "https://www.zhihu.com/question/56654450"
		]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
		soup = BeautifulSoup(response.body, 'lxml')
		title = soup.find('title').get_text().strip()
		for item in soup.find_all('div', class_='zm-item-answer'):
			#print item
			vote_cnt = item.find('div', class_="zm-item-vote-info")['data-votecount']
			vote_cnt = eval(vote_cnt)
			if (vote_cnt >= 5000):
				name = item.find('div', class_='zm-item-rich-text')["data-author-name"]
				answer_url = 'https://www.zhihu.com' + item.find('link')["href"]
				item_dict = {"name": name, "vote_cnt": vote_cnt, "answer_url" : answer_url, "title" : title}
				for oneItem in item_dict.values():
					print oneItem,
				print
				with codecs . open("result.txt" ,'a+', 'utf8') as f:
					json.dump(item_dict, f,ensure_ascii=False)
					f.write('\n')
		if not soup.find('div', 'zh-question-related-questions'):
			yield
		for item in soup.find('div', 'zh-question-related-questions').find_all('a', class_='question_link'):
			new_url = 'https://www.zhihu.com' + item['href']
			yield scrapy.Request(url=new_url, callback=self.parse)
