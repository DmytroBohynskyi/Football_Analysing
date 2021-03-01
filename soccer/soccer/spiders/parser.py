import scrapy
from scrapy_splash import SplashRequest


# https://www.oddsportal.com/soccer/poland/division-1/results/#/page/1/

class SoccerSpider(scrapy.Spider):
    name = 'parser'
    allowed_domains = ['oddsportal.com']
    start_urls = ['http://oddsportal.com']
    pages_count = 5

    def start_requests(self):
        for page in range(1, self.pages_count):
            url = f"https://www.oddsportal.com/soccer/poland/division-1/results/#/page/{page}/"
            yield SplashRequest(url, callback=self.parse, args={'wait': 3, })

    # def season_parse(self, response, **kwargs):

    def parse(self, response, **kwargs):
        match_day: str = "None"  # match day
        for tr_block in response.css(".center.nob-border, .deactivate"):
            # check block types, if block is "center nob-border" then save date values
            if tr_block.attrib.get('class') == "center nob-border":
                match_day = tr_block.css("span::text").get()
                continue
            # parse match title and split dana on different name
            title: str = "".join(tr_block.css("a ::text")[:-3].extract())
            first_club_name, second_club_name = title.split(" - ")
            # get result from tr block
            first_res, second_res = tr_block.css(".center.bold.table-odds.table-score ::text").get().split(":")

            url: str = f'{self.start_urls[0]}{tr_block.css("a::attr(href)").get()}'
            match_time: str = tr_block.css(".table-time ::text").get()

            yield {
                "title": title,
                "first_club_name": first_club_name,
                "second_club_name": second_club_name,
                "result": {
                    "first_club_res": first_res,
                    "second_club_res": second_res,
                },
                "date": f"{match_day}, {match_time}",
                "url": url
            }
