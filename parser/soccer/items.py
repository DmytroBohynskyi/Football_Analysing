from scrapy import Field, Item


class SoccerItem(Item):
    # define the fields:
    season = Field()
    league = Field()
    country = Field()
    result = Field()
    date = Field()
    first_club_name = Field()
    second_club_name = Field()
    title = Field()
    clubs_name = Field()
    url = Field()
