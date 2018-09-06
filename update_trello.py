import requests
import json
import os

API_KEY=""
TOKEN=""
BOARD_NAME="RG310"
ORG_NAME="isafemobile1"

PARAM_CUSTOMER          = os.environ.get("PARAM_CUSTOMER")
PARAM_CUSTOM_PROFILE    = os.environ.get("PARAM_CUSTOM_PROFILE")
PARAM_BASEBAND          = os.environ.get("PARAM_BASEBAND")
PARAM_DESCRIPTION       = os.environ.get("PARAM_DESCRIPTION")
BUILD_NUMBER            = os.environ.get("BUILD_NUMBER")
JENKINS_URL             = os.environ.get("JENKINS_URL")

board_id=""
list_id=""


def initialize(apikey, token, board_name, org_name):
	global API_KEY
	API_KEY=apikey
	global TOKEN
	TOKEN=token
	global board_id
	board_id=get_boardid(board_name=board_name, org_name=org_name)
	

def get_boardid(board_name, org_name):
	try:
	  resp = requests.get("https://api.trello.com/1/organizations/%s/boards" % (org_name), params=dict(key=API_KEY, token=TOKEN))
	  resp.raise_for_status()
	  respo=json.loads(resp.content)
	  for board in respo:
	    if board_name==board['name']:
	       return ""+board['id']
	       break;
	except:
            print("get_boardid: operation failed")
	    exit(1)


def new_list(list_name):
	try:
	  if not isLexist(list_name):
	    resp=requests.post("https://api.trello.com/1/boards/%s/lists" % (board_id), params=dict(key=API_KEY, token=TOKEN), data=dict(name=list_name, pos="top"))
	    resp.raise_for_status()
	    respo=json.loads(resp.content)
	  else:
	    return
	except:
            print("new_list: operation failed")
	    exit(1)


def isLexist(list_name):
	try:
	  flagl=False
	  resp=requests.get("https://api.trello.com/1/boards/%s/lists" % (board_id), params=dict(key=API_KEY, token=TOKEN))
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
	except:
            print("isLexist: operation failed")
	    exit(1)


def isCexist(card_name):
	try:
	  flag=False
	  resp = requests.get("https://api.trello.com/1/lists/%s/cards" % (list_id), params=dict(key=API_KEY, token=TOKEN))
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
	except:
            print("isCexist: operation failed")
            print resp.content
            exit(1)
		

def get_listid(list_name):
	try:
	  resp = requests.get("https://api.trello.com/1/boards/%s/lists" % (board_id), params=dict(key=API_KEY, token=TOKEN))
	  resp.raise_for_status()
	  respo=json.loads(resp.content)
	  for li in respo:
		  if list_name==li['name']:
		    return ""+li['id']
	except:
            print("get_listid: operation failed")
	    exit(1)



def get_cardid(card_name):
	try:
	  resp = requests.get("https://api.trello.com/1/lists/%s/cards" % (list_id), params=dict(key=API_KEY, token=TOKEN))
	  resp.raise_for_status()
	  respo=json.loads(resp.content)
	  for ca in respo:
		  if card_name==ca['name']:
		    return ""+ca['id']
	except:
            print("get_cardid: operation failed")
	    exit(1)
 

def add_comment(card_name, comment):
	try:
	  cid=get_cardid(card_name)
	  resp = requests.post("https://api.trello.com/1/cards/%s/actions/comments" % (cid), params=dict(key=API_KEY, token=TOKEN), data=dict(text=comment))
	  resp.raise_for_status()
	  json.loads(resp.content)
	except:
            print("add_comment: operation failed")
	    exit(1)

	

def new_card(card_name, list_name, desc=None):
	try:
	  global list_id
	  list_id=get_listid(list_name)
	  if not isCexist(card_name):
	    resp = requests.post("https://api.trello.com/1/cards" % (), params=dict(key=API_KEY, token=TOKEN, idList=list_id), data=dict(pos="top", desc=desc, name=card_name))
	    resp.raise_for_status()
	    json.loads(resp.content)
	  else:
	    return
	except:
            print("new_card: operation failed")
	    exit(1)

def delete_card(card_name, list_name):
	try:
	  global list_id
	  list_id=get_listid(list_name)
	  cid=get_cardid(card_name)
	  resp = requests.delete("https://api.trello.com/1/cards/%s" % (cid), params=dict(key=API_KEY, token=TOKEN))
	  resp.raise_for_status()
	  json.loads(resp.content)
	except:
            print("delete_card: operation failed")
	    exit(1)

CARD_NAME = PARAM_CUSTOMER + "-" + BUILD_NUMBER + "-" + PARAM_BASEBAND
if PARAM_CUSTOM_PROFILE != "":
    CARD_NAME = CARD_NAME + "(" + PARAM_CUSTOM_PROFILE + ")"

LIST_NAME = PARAM_CUSTOMER if (PARAM_CUSTOM_PROFILE == "" or PARAM_CUSTOM_PROFILE == PARAM_CUSTOMER) else PARAM_CUSTOMER + '-' + PARAM_CUSTOM_PROFILE

initialize(apikey=API_KEY, token=TOKEN, board_name=BOARD_NAME, org_name=ORG_NAME)
new_list(list_name=LIST_NAME)
new_card(card_name=CARD_NAME, list_name=LIST_NAME, desc=PARAM_DESCRIPTION)
add_comment(card_name=CARD_NAME, comment=JENKINS_URL)
