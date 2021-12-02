import requests


class HackNewsBackend:
    def __init__(self, item, **params):
        self.item = item
        base_url = "https://hacker-news.firebaseio.com/v0"
        self.stories_url = f"{base_url}/{self.item}.json"
        self.item_url = f"{base_url}/item"

    def get_all_stories(self):
        api_request = requests.get(self.stories_url)
        status_code = api_request.status_code
        if status_code == 200:
            return api_request.json()
        else:
            return {"Status Code": api_request.status_code}

    def get_a_story(self, story_id):
        story = f"{self.item_url}/{str(story_id)}.json"
        api_request = requests.get(story)
        status_code = api_request.status_code
        if status_code == 200:
            one_article = api_request.json()
            return one_article
        else:
            return {"Status Code": api_request.status_code}

    def getcomments(self, commentId):
        res = requests.get(f"{self.item_url}{commentId}.json")
        api_request = requests.get(res)
        status_code = api_request.status_code
        if status_code == 200:
            one_comment = api_request.json()
            return one_comment
        else:
            return {"Status": api_request.status_code}


# x = HackNewsBackend("topstories")
# print(x.get_all_stories())
# print(x.get_a_story(29360801))
