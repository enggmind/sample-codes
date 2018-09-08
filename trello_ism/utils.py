import requests
import json

class TrelloUpdate:
    def __init__(self, apikey, token, board_name, org_name, list_name):
        self.api_key    = apikey
        self.token      = token
        self.board_id   = self.get_boardid(board_name=board_name, org_name=org_name)
        self.new_list(list_name)
        self.list_id    = self.get_listid(list_name)

    def get_boardid(self, board_name, org_name):
        try:
            resp = requests.get("https://api.trello.com/1/organizations/%s/boards" % (org_name), params=dict(key=self.api_key, token=self.token))
            resp.raise_for_status()
            respo=json.loads(resp.content)
            for board in respo:
                if board_name==board['name']:
                    return "" + board['id']
                    break
        except requests.exceptions.RequestException as e:
            print("get_boardid: operation failed")
            print e
            exit(1)

    def new_list(self, list_name):
        try:
            if not self.isLexist(list_name):
                resp=requests.post("https://api.trello.com/1/boards/%s/lists" % (self.board_id), params=dict(key=self.api_key, token=self.token), data=dict(name=list_name, pos="top"))
                resp.raise_for_status()
                respo=json.loads(resp.content)
            else:
                return
        except requests.exceptions.RequestException as e:
            print("new_list: operation failed")
            print e
            exit(1)

    def isLexist(self, list_name):
        try:
            flagl=False
            resp=requests.get("https://api.trello.com/1/boards/%s/lists" % (self.board_id), params=dict(key=self.api_key, token=self.token))
            resp.raise_for_status()
            respo=json.loads(resp.content)
            for lst in respo:
                if list_name==lst['name']:
                    flagl=True
                else:
                    continue

            if flagl==True:
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            print("isLexist: operation failed")
            print e
            exit(1)


    def isCexist(self, card_name):
        try:
            flag=False
            resp = requests.get("https://api.trello.com/1/lists/%s/cards" % (self.list_id), params=dict(key=self.api_key, token=self.token))
            resp.raise_for_status()
            respo=json.loads(resp.content)
            for ca in respo:
                if card_name==ca['name']:
                    flag=True
                else:
                    continue

            if flag==True:
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            print("isCexist: operation failed")
            print e
            exit(1)


    def get_listid(self, list_name):
        try:
            resp = requests.get("https://api.trello.com/1/boards/%s/lists" % (self.board_id), params=dict(key=self.api_key, token=self.token))
            resp.raise_for_status()
            respo=json.loads(resp.content)
            for li in respo:
                if list_name==li['name']:
                    return ""+li['id']
        except requests.exceptions.RequestException as e:
            print("get_listid: operation failed")
            print e
            exit(1)

    def get_cardid(self, card_name):
        try:
            resp = requests.get("https://api.trello.com/1/lists/%s/cards" % (self.list_id), params=dict(key=self.api_key, token=self.token))
            resp.raise_for_status()
            respo=json.loads(resp.content)
            for ca in respo:
                if card_name==ca['name']:
                    return ""+ca['id']
        except requests.exceptions.RequestException as e:
            print("get_cardid: operation failed")
            print e
            exit(1)

    def add_comment(self, card_name, comment):
        try:
            cid = self.get_cardid(card_name)
            resp = requests.post("https://api.trello.com/1/cards/%s/actions/comments" % (cid), params=dict(key=self.api_key, token=self.token), data=dict(text=comment))
            resp.raise_for_status()
            json.loads(resp.content)
        except requests.exceptions.RequestException as e:
            print("add_comment: operation failed")
            print e
            exit(1)

    def new_card(self, card_name, desc=None):
        try:
            if not self.isCexist(card_name):
                resp = requests.post("https://api.trello.com/1/cards" % (), params=dict(key=self.api_key, token=self.token, idList=self.list_id), data=dict(pos="top", desc=desc, name=card_name))
                resp.raise_for_status()
                json.loads(resp.content)
            else:
                return
        except requests.exceptions.RequestException as e:
            print("new_card: operation failed")
            print e
            exit(1)

    def delete_card(self, card_name, list_name):
        try:
            cid=get_cardid(card_name)
            resp = requests.delete("https://api.trello.com/1/cards/%s" % (cid), params=dict(key=self.api_key, token=self.token))
            resp.raise_for_status()
            json.loads(resp.content)
        except requests.exceptions.RequestException as e:
            print("delete_card: operation failed")
            print e
            exit(1)
