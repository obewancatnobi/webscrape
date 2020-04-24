from scrapy import Spider, Request
from tv.items import TvItem
import re
import math

"""The passes is essentially to go through the different genres. I wasnt comfortable to do everything
in one go because i was still doing other things simultaneously as well. I started from the most 
genre."""

class tv_crawl(Spider):
    name = 'tv_crawl'
    allowed_urls = ['https://www.metacritic.com']
    
    # # First Pass: Drama
    # start_urls = ['https://www.metacritic.com/browse/tv/genre/name/drama?view=condensed']
    
    # # Second Pass: Action and Adventure
    # start_urls = ['https://www.metacritic.com/browse/tv/genre/name/actionadventure?view=condensed']

    # # Third Pass: Suspense
    # start_urls = ['https://www.metacritic.com/browse/tv/genre/name/suspense?view=condensed']
    
    # # Fourth Pass: Comedy
    # start_urls = ['https://www.metacritic.com/browse/tv/genre/name/comedy?view=condensed']
    
    # # Fifth Pass: Movie/Mini-Series
    # start_urls = ['https://www.metacritic.com/browse/tv/genre/name/moviemini-series?view=condensed']

    # # Sixth Pass: Fantasy
    # start_urls = ['https://www.metacritic.com/browse/tv/genre/name/fantasy?view=condensed']

    # # Seventh Pass: Animation
    # start_urls = ['https://www.metacritic.com/browse/tv/genre/name/animation?view=condensed']

    # # Eighth Pass: Documentary
    # start_urls = ['https://www.metacritic.com/browse/tv/genre/name/documentary?view=condensed']

    # # Ninth Pass: Food and Cooking
    start_urls = ['https://www.metacritic.com/browse/tv/genre/name/foodcooking?view=condensed']

    # # Tenth Pass: Kids
    # start_urls = ['https://www.metacritic.com/browse/tv/genre/name/kids?view=condensed']

    # # Eleventh Pass: Science Fiction
    # start_urls = ['https://www.metacritic.com/browse/tv/genre/name/sciencefiction?view=condensed']

    # # Twelfth Pass: Horror
    # start_urls = ['https://www.metacritic.com/browse/tv/genre/name/horror?view=condensed']

    # # Thirteenth Pass: Reality
    # start_urls = ['https://www.metacritic.com/browse/tv/genre/name/reality?view=condensed']


    def parse (self, response):
        num_pages = int(response.xpath('.//a[@class="page_num"]//text()').extract()[-1])
        
        # #First Pass: Drama 
        # page_urls = [f'https://www.metacritic.com/browse/tv/genre/name/drama?view=condensed&page={i}' for i in range(num_pages)]
 
        # # Second Pass: Action and Adventure
        # page_urls = [f'https://www.metacritic.com/browse/tv/genre/name/actionadventure?view=condensed&page={i}' for i in range(num_pages)]
        
        # # Third Pass: Suspense
        # page_urls = [f'https://www.metacritic.com/browse/tv/genre/name/suspense?view=condensed&page={i}' for i in range(num_pages)]
        
        # # Fourth Pass: Comedy
        # page_urls = [f'https://www.metacritic.com/browse/tv/genre/name/comedy?view=condensed&page={i}' for i in range(num_pages)]

        # # Fifth Pass: Movie/Mini-Series
        # page_urls = [f'https://www.metacritic.com/browse/tv/genre/name/moviemini-series?view=condensed&page={i}' for i in range(num_pages)]

        # # Sixth Pass: Fantasy
        # page_urls = [f'https://www.metacritic.com/browse/tv/genre/name/fantasy?view=condensed&page={i}' for i in range(num_pages)]

        # # Seventh Pass: Animation
        # page_urls = [f'https://www.metacritic.com/browse/tv/genre/name/animation?view=condensed&page={i}' for i in range(num_pages)]

        # # Eighth Pass: Documentary
        # page_urls = [f'https://www.metacritic.com/browse/tv/genre/name/documentary?view=condensed&page={i}' for i in range(num_pages)]

        # # Ninth Pass: Food and Cooking
        page_urls = [f'https://www.metacritic.com/browse/tv/genre/name/foodcooking?view=condensed&page={i}' for i in range(num_pages)]

        # # Tenth Pass: Kids
        # page_urls = [f'https://www.metacritic.com/browse/tv/genre/name/kids?view=condensed&page={i}' for i in range(num_pages)]

        # # Eleventh Pass: Science Fiction
        # page_urls = [f'https://www.metacritic.com/browse/tv/genre/name/sciencefiction?view=condensed&page={i}' for i in range(num_pages)]

        # # Twelfth Pass: Horror
        # page_urls = [f'https://www.metacritic.com/browse/tv/genre/name/horror?view=condensed&page={i}' for i in range(num_pages)]

        # # Thirteenth Pass: Reality
        # page_urls = [f'https://www.metacritic.com/browse/tv/genre/name/reality?view=condensed&page={i}' for i in range(num_pages)]


        for url in page_urls:
            yield Request(url=url, callback=self.parse_show_page)

    def parse_show_page(self, response):

        shows = response.xpath('//div[@class="basic_stat product_title"]//@href').extract()
        
        show_urls = [f'https://www.metacritic.com{show}' for show in shows]

        for url in show_urls:
            yield Request(url=url, callback=self.parse_detail_page)

        # # CHECKPOINT #1 : Complete
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
        num_users = response.xpath('.//span[@class="based_on"]/text()').extract()[-1]

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