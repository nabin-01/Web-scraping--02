import scrapy
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from urllib.parse import urljoin
# from scrapy_splash import SplashRequest
from ..items import TourRadarItem


class TourRadar(scrapy.Spider):
    name = 'tours_nepal'

    start_urls = []
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'Tour_radar.csv'
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        page_url = 'https://www.tourradar.com/d/nepal?page='
        for page in range(1, 131):
            self.start_urls.append(page_url + str(page))

    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = f'Tourradar-{page}.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(response.text))
        for link in response.xpath("//a[contains(text(),'View tour')]/@href").getall():
            base_url = 'https://www.tourradar.com'
            final_url = urljoin(base_url, link)
            yield scrapy.Request(url=final_url, callback=self.parse_inner, encoding='utf-8')

    def parse_inner(self, response):
        load = ItemLoader(item=TourRadarItem(), selector=response, response=response)
        load.add_xpath('Package_Title', '//h1')
        load.add_xpath('Url', '//a/@href')
        load.add_xpath('Price', '//div[@class="ao-tour-above-fold__main-price"]/span')
        load.add_xpath('Duration', '//div[@class="ao-tour-above-fold__length"]')
        load.add_xpath('Rating', '//div[@class="ao-tour-above-fold__rating--number"]')
        load.add_xpath('Reviews', '//div[@class="ao-tour-above-fold__rating--count"]')
        load.add_xpath('Group_size', '//dd[@class="ao-tour-above-fold__properties-list--description ao-tour-above-fold__properties-list--group-size"]')
        load.add_xpath('Highlights', '//li[@class="ao-tour-highlights__facts-item"]')
        load.add_xpath('Itinerary', '//ol[2]/li/span')
        yield load.load_item()
