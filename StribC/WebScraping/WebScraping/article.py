
class Article:
    def __init__(self, title, date, url):
        self.url = url
        self.date = date
        self.title = title

    def __eq__(self, other):
        return self.url == other.url

    def __hash__(self):
        return hash(self.url)