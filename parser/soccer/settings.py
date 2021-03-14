# Scrapy settings for soccer project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'soccer'

SPIDER_MODULES = ['soccer.spiders']
NEWSPIDER_MODULE = 'soccer.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'soccer (+http://www.oddsportal.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

SPLASH_URL = 'http://localhost:8050'

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# Pepelines
# The integer values you assign to classes in this setting determine the order in which they run: items go through from lower valued to higher valued classes. It’s customary to define these numbers in the 0–1000 range.
ITEM_PIPELINES = {
    'soccer.pipelines.SoccerPipeline': 300,
    # 'myproject.pipelines.JsonWriterPipeline': 800 #another pipline
}
