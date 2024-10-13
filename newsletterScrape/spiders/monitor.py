import scrapy


class MonitorSpider(scrapy.Spider):
    name = "monitor"
    allowed_domains = ["monitor.al"]
    start_urls = ["https://monitor.al/ekonomi/"]

    def __init__(self, *args, **kwargs):
        super(MonitorSpider, self).__init__(*args, **kwargs)
        self.categoriesList = []

    # Scrape the categories
    # Scrape the categories name
    # Scrape the categories links
    # Scrape the categories articles
    # Scrape e articles


    def parse(self, response):
        # self.parseNewsCategories(response)
        category = {
            "category_name": "Ekonomi",
            "category_link": "https://monitor.al/ekonomi/"
        }
        self.categoriesList.append(category)
        # Make a request to the category link and handle the response in parseNewsArticles
        yield scrapy.Request(url=category["category_link"], callback=self.parseNewsArticles)

    def parseNewsCategories(self, response):
        categories = response.css("#myUL li")

        for category in categories:
            category_name = category.css("a::text").get()
            category_link = category.css("a::attr(href)").get()
            self.categoriesList.append({
                "category_name": category_name,
                "category_link": category_link
            })

    def parseNewsArticlesInCategory(self, newsCategories):

        for category in newsCategories:
            scrapy.Request(category["category_link"], callback=self.parseNewsArticles)

    def parseNewsArticles(self, response):
        newsletter = response.css(".category-hero-card")

        # Extract data from the newsletter section
        if newsletter:
            category = newsletter.css(".hammerhead::text").get()
            article_title = newsletter.css("h2 a::text").get()
            article_link = newsletter.css("h2 a::attr(href)").get()
            article_description = newsletter.css("p::text").get()
            time_of_post = newsletter.css(".news-read-time::text").get().strip()
            image_url = newsletter.css(".news-card-img img::attr(src)").get()

            # Yield the highlighted newsletter data
            yield {
                "type": "highlighted_newsletter",
                "category": category,
                "article_title": article_title,
                "article_link": article_link,
                "article_description": article_description,
                "time_of_post": time_of_post,
                "image_url": image_url
            }

        # Next, parse the other regular articles
        articles = response.css(".news-card-style-1")

        for article in articles:
            # Extract each piece of data from regular articles
            category = article.css(".hammerhead::text").get()
            article_title = article.css("h3 a::text").get()
            article_link = article.css("h3 a::attr(href)").get()
            article_description = article.css("p::text").get()
            time_of_post = article.css(".news-read-time::text").get().strip()
            image_url = article.css(".news-card-img img::attr(src)").get()

            # Yield each regular article data
            yield {
                "type": "regular_article",
                "category": category,
                "article_title": article_title,
                "article_link": article_link,
                "article_description": article_description,
                "time_of_post": time_of_post,
                "image_url": image_url
            }


        # Next, parse the other regular articles
        articles = response.css(".news-card-style-2")

        for article in articles:
            # Extract each piece of data from regular articles
            category = article.css(".hammerhead::text").get()
            article_title = article.css("h3 a::text").get()
            article_link = article.css("h3 a::attr(href)").get()
            article_description = article.css("p::text").get()
            time_of_post = article.css(".news-read-time::text").get().strip()
            image_url = article.css(".news-card-img img::attr(src)").get()

            # Yield each regular article data
            yield {
                "type": "regular_article",
                "category": category,
                "article_title": article_title,
                "article_link": article_link,
                "article_description": article_description,
                "time_of_post": time_of_post,
                "image_url": image_url
            }
