from typing import Iterator

import scrapy
from scrapy_splash import SplashRequest
from soccer.items import SoccerItem


class SoccerSpider(scrapy.Spider):
    name = 'parser'
    allowed_domains = ['oddsportal.com']
    start_urls = ['https://www.oddsportal.com/soccer/poland', 'https://www.oddsportal.com/soccer/england']
    base_url = "https://www.oddsportal.com"

    def start_requests(self) -> Iterator[scrapy.Request]:
        """
        Start function.
        :return: Sends the collected data for parsing
        """
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_pages_leagues, cb_kwargs={"country": url.split("/")[-1]})

    def parse_pages_leagues(self, response, **kwargs) -> Iterator[scrapy.Request]:
        """
        This function parses league, it gets seasons name and they url.
        :param response:
        :param kwargs:
        :return: Sends the collected data for parsing to parse_season_in_page function
        """
        if response.status == 200:  # OK
            list_with_league_inf = response.xpath("//table[@id='country-tournaments-table']//td/a")
            for league_inf in list_with_league_inf:
                league_url = f"{self.base_url}{league_inf.attrib['href']}results/"
                league_name = league_inf.css("::text").get()
                yield scrapy.Request(league_url, callback=self.parse_season_in_page,
                                     cb_kwargs={"league": league_name, "200": True, **kwargs})

    def parse_season_in_page(self, response, **kwargs) -> Iterator[SplashRequest]:
        """
        This function parses seasons( 2021/2020, 2020/2019, ...) and gets seasons name and they url.
        :param response: HTML response
        :param kwargs: Page information
        :return: Sends the collected data for parsing to parse_page_number
        """
        if response.status == 200:  # OK
            list_with_season_inf = response.xpath("//div[@class='main-menu2 main-menu-gray']//a")
            for season_inf in list_with_season_inf:
                season_url = f"{self.base_url}{season_inf.attrib['href']}"  # get href
                season_name = season_inf.css("::text").get()  # get season name.
                yield SplashRequest(season_url, callback=self.parse_page_number, args={'wait': 5, },
                                    cb_kwargs={"season": season_name, "200": True, **kwargs})

    def parse_page_number(self, response, **kwargs) -> Iterator[SplashRequest]:
        """
        This function parses soccer match data, collects team names, result, league, time ...
        :param response: HTML response,
        :param kwargs: Page information
        :return: Sends the collected data for parsing.
        """
        if response.status == 200:  # OK
            page_button_list = response.xpath("//div[@id='pagination']//a/@href").re(r'/page/\s*(.*)/')
            # if the list has data take the last value else parse first page
            page_number = page_button_list[-1] if len(page_button_list) else 1
            # parse each page
            for page_inf in range(1, int(page_number)):
                page_url = f"{response.url}page/{page_inf}/"
                yield SplashRequest(page_url, callback=self.parse, args={"max-timeout": 3600, },
                                    cb_kwargs={"200": True, **kwargs})

    def parse(self, response, **kwargs) -> SoccerItem:
        """
        This function parses soccer match data, collects team names, result, league, time ...
        :param response: HTML response,
        :param kwargs: Page information
        :return: SoccerItem object.
        """
        match_day: str = "None"  # match day
        for tr_block in response.css(".center.nob-border, .deactivate"):
            # check block types, if block is "center nob-border" then save date values
            if tr_block.attrib.get('class') == "center nob-border":
                match_day = tr_block.css("span::text").get()
                continue

            item = SoccerItem()
            item = self.dict_to_item(item, kwargs)

            item["result"] = ",".join(tr_block.css(".center.bold.table-odds.table-score ::text").re("\d+"))

            item["url"] = f'{self.base_url}{tr_block.css("a::attr(href)").get()}'
            item["date"] = f'{match_day}, {tr_block.css(".table-time ::text").get()}'

            title = "".join(tr_block.css("a ::text").re("[a-zA-Z- ]+"))
            item["title"] = title
            item["first_club_name"], item["second_club_name"] = title.split(" - ")

            yield item

    @staticmethod
    def dict_to_item(item: SoccerItem, kwargs) -> SoccerItem:
        """
        This function write page information to item
        """
        item["season"] = kwargs["season"]
        item["league"] = kwargs["league"]
        item["country"] = kwargs["country"]
        return item
