import json
from json import JSONEncoder

class Comment(JSONEncoder):

    def __init__(self, username, date, text, article, parent):
        self.text = text        
        self.article = article
        self.username = username
        self.date = date
        self.parent = parent

        self.children = []
    
    def __eq__(self, item):
        if isinstance(item, Comment):
            return self.username == item.username and self.date == item.date and self.text == item.text
        else:
            return False

    def __hash__(self):
        return self.text + self.username

    