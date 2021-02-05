# -*- coding: utf-8 -*-
import scrapy
import json
import pprint

# base = "https://www.behance.net/search/projects/?ordinal="


class BehanceDataSpider(scrapy.Spider):
    name = 'reddit'
    # allowed_domains = ['www.gateway.reddit.com']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}

    # starting url requests
    def start_requests(self):
        yield scrapy.Request(url="https://gateway.reddit.com/desktopapi/v1/search?rtj=only&allow_over18=&include=structuredStyles%2CprefsSubreddit&q=python&sort=relevance&t=all&type=link%2Csr%2Cuser&after=t3_kvm8bc&b=true&search_correlation_id=427f40f9-9949-4a84-8d42-1aa6ee6156ac", callback=self.parse,
                             headers=self.headers)

    def parse(self, response):

        # loading response as json
        data = json.loads(response.body)

        post_order = data.get("postOrder")

        posts = data.get("posts")

        for i in range(len(post_order)):

            data = json.loads(response.body)

            post_order = data.get("postOrder")

            posts = data.get("posts")

            title = posts.get(post_order[i]).get("title")
            author = posts.get(post_order[i]).get("author")
            upvoteRatio = posts.get(post_order[i]).get("upvoteRatio")
            score = posts.get(post_order[i]).get("score")
            numComments = posts.get(post_order[i]).get("numComments")

            # getting award type, as some of post have no award...
            if posts.get(post_order[i]).get("allAwardings") != None:
                award = posts.get(post_order[i]).get(
                    "allAwardings")[0].get("awardType")
            else:
                award = "No Award Recorded"

            yield {

                'title': title,
                'Author': author,
                'Vote_Ratio': upvoteRatio,
                'score': score,
                'No_of_Comments': numComments,
                'Award': award


            }

        query_param = post_order[-1]
        next_url = "https://gateway.reddit.com/desktopapi/v1/search?rtj=only&allow_over18=&include=structuredStyles%2CprefsSubreddit&q=python&sort=relevance&t=all&type=link%2Csr%2Cuser&after={}&b=true&search_correlation_id=427f40f9-9949-4a84-8d42-1aa6ee6156ac".format(
            query_param)
        yield scrapy.Request(url=next_url, callback=self.parse)
