from scrapy import Spider, Request
from tv.items import TvItem


class tv_crawl(Spider):
    name = 'tv_crawl'
    allowed_urls = ['https://www.metacritic.com']
    genres = ['actionadventure', 'animation', 'arts', 'business', 'comedy', 'documentary', 'educational', 
    'eventsspecials','fantasy', 'foodcooking', 'gameshow', 'healthylifestyle','horror', 'kids', 'moviemini-series', 'music', 
    'news', 'newsdocumentary', 'reality', 'science', 'soap', 'sports', 'suspense', 'talkinterview', 
    'techgaming', 'travel','variety-shows']
    start_urls = [f'https://www.metacritic.com/browse/tv/genre/date/{j}?view=condensed' for j in genres]

    def parse (self, response):
        
        try: 
            num_pages = int(response.xpath('//li[@class="page last_page"]//text()').extract()[-1])
            full_urls = [response.url + f'&page={i}' for i in range(num_pages)]
        except:
            full_urls = [response.url + '&page=0']

        
        ##CHECKPOINT
        # for url in full_urls:
        #     print('='*50)
        #     print(url)
#             yield Request(url=url, callback=self.parse_show_page)

        for url in full_urls:
            yield Request(url=url, callback=self.parse_show_page)



        # # CHECKPOINT complete
        # for url in page_urls:
        #     print("=="*50)
        #     print(url)


    def parse_show_page(self, response):

        shows = response.xpath('//div[@class="basic_stat product_title"]//@href').extract()
        
        show_urls = [f'https://www.metacritic.com{show}' for show in shows]

        for url in show_urls:
            yield Request(url=url, callback=self.parse_detail_page)

        # # CHECKPOINT complete
        # print("==" * 50)
        # print(len(show_urls))
        # print("==" * 50)
        
    def parse_detail_page(self, response):

        title = response.xpath('.//div[@class="product_page_title oswald"]/h1/a/text()').extract_first()
        season = int(response.xpath('.//div[@class="product_page_title oswald"]/h1/text()').extract()[0].replace(": Season ",""))
        genre = response.xpath('.//div[@class="genres"]/span[2]/span/text()').extract()
        release_date = response.xpath('.//span[@class="release_date"]/span[2]/text()').extract_first()
        network = response.xpath('.//span[@class="distributor"]//text()').extract_first()

        # There are three types of designs for the scores, essentially "positive","negative","mixed". 
        # There is also "tbd" but that just means it doesnt have a rating therefore "not available"
        patterns_crit = ['.//div[@class="metascore_w larger tvshow positive"]//text()', './/div[@class="metascore_w larger tvshow negative"]//text()', './/div[@class="metascore_w larger tvshow mixed"]//text()']
        for pattern in patterns_crit:
            critic = response.xpath(pattern).extract_first()
            if critic:
                break
            if not critic:
                critic = "not available"
        
        patterns_user = ['.//div[@class="metascore_w user larger tvshow positive"]//text()','.//div[@class="metascore_w user larger tvshow negative"]//text()','.//div[@class="metascore_w user larger tvshow mixed"]//text()']
        for pattern_u in patterns_user:
            user = response.xpath(pattern_u).extract_first()
            if user:
                break
            if not user:
                user = "not available"

        # number of critics and users that rated the series
        num_critics = response.xpath('.//span[@class="based_on"]/text()').extract_first()

        try: 
            num_users = response.xpath('.//span[@class="based_on"]/text()').extract()[-1]
        except:
            num_users = 'not available'


#         # # CHECKPOINT complete
#         # print("=="*50)
#         # print(title)
#         # print(season)
#         # print(genre)
#         # print(release_date)
#         # print(network)
#         # print(critic)
#         # print(user)
#         # print(num_critics)
#         # print(num_users)

        item = TvItem()
        item ['Title'] = title
        item ['Season'] = season 
        item ['Genre'] = genre
        item ['Release_Date'] = release_date
        item ['Critic_Score'] = critic
        item ['Network'] = network 
        item ['User_Score'] = user
        item ['Critics_votes'] = num_critics
        item ['Users_votes'] = num_users
        yield item