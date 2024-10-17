import scrapy


class MonitorSpider(scrapy.Spider):
    name = "monitor"
    allowed_domains = ["monitor.al"]
    start_urls = ["https://monitor.al/ekonomi/"]

    def __init__(self, *args, **kwargs):
        super(MonitorSpider, self).__init__(*args, **kwargs)
        self.categoriesList = []

    def parse(self, response):
        # Parse and populate categories
        self.parseNewsCategories(response)

        # Loop through each category link and send a request to parse articles in each category
        for category in self.categoriesList:
            yield scrapy.Request(
                url=category["category_link"],
                callback=self.parseNewsArticles
            )

    def parseNewsCategories(self, response):
        # Extract category links and names
        categories = response.css("#myUL li")
        for category in categories:
            category_name = category.css("a::text").get()
            category_link = category.css("a::attr(href)").get()
            # Store each category in the categories list
            self.categoriesList.append({
                "category_name": category_name,
                "category_link": response.urljoin(category_link)  # Ensure full URLs
            })

    def parseNewsArticles(self, response):
        # Parse highlighted newsletter
        newsletter = response.css(".category-hero-card")
        if newsletter:
            category = newsletter.css(".hammerhead::text").get()
            article_title = newsletter.css("h2 a::text").get()
            article_link = newsletter.css("h2 a::attr(href)").get()
            article_description = newsletter.css("p::text").get()
            time_of_post = newsletter.css(".news-read-time::text").get().strip()
            image_url = newsletter.css(".news-card-img img::attr(src)").get()

            # Request the article body page
            yield scrapy.Request(
                url=response.urljoin(article_link),
                callback=self.parseArticleBody,
                meta={
                    "type": "highlighted_newsletter",
                    "category": category,
                    "article_title": article_title,
                    "article_link": article_link,
                    "article_description": article_description,
                    "time_of_post": time_of_post,
                    "image_url": image_url
                }
            )

        # Parse other regular articles
        articles = response.css(".news-card-style-1, .news-card-style-2")
        for article in articles:
            category = article.css(".hammerhead::text").get()
            article_title = article.css("h3 a::text").get()
            article_link = article.css("h3 a::attr(href)").get()
            article_description = article.css("p::text").get()
            time_of_post = article.css(".news-read-time::text").get().strip()
            image_url = article.css(".news-card-img img::attr(src)").get()

            # Request the article body page
            yield scrapy.Request(
                url=response.urljoin(article_link),
                callback=self.parseArticleBody,
                meta={
                    "type": "regular_article",
                    "category": category,
                    "article_title": article_title,
                    "article_link": article_link,
                    "article_description": article_description,
                    "time_of_post": time_of_post,
                    "image_url": image_url
                }
            )

    def parseArticleBody(self, response):
        # Get article body content
        article_body = response.css(".standard-content p::text").getall()  # Updated CSS selector
        article_body_text = "\n".join(article_body)

        # Collect metadata and add article body
        article_data = response.meta
        article_data["article_body"] = article_body_text

        yield article_data
