import os
import trello_lib_ism

API_KEY     = "52ddc855408d53fbb5331f8ceeb51ac7"
TOKEN       = "02b0056c76ee2d3f8dac21a6c849bd52ce82db2f82795a8353fe40a304dfbebc"
BOARD_NAME  = "RG310"
ORG_NAME    = "isafemobile1"

PARAM_CUSTOMER          = os.environ.get("PARAM_CUSTOMER")
PARAM_CUSTOM_PROFILE    = os.environ.get("PARAM_CUSTOM_PROFILE")
PARAM_BASEBAND          = os.environ.get("PARAM_BASEBAND")
PARAM_DESCRIPTION       = os.environ.get("PARAM_DESCRIPTION")
BUILD_NUMBER            = os.environ.get("BUILD_NUMBER")
JENKINS_URL             = os.environ.get("JENKINS_URL")

CARD_NAME = PARAM_CUSTOMER + "-" + BUILD_NUMBER + "-" + PARAM_BASEBAND
if PARAM_CUSTOM_PROFILE != "":
    CARD_NAME = CARD_NAME + "(" + PARAM_CUSTOM_PROFILE + ")"

LIST_NAME = PARAM_CUSTOMER if (PARAM_CUSTOM_PROFILE == "" or PARAM_CUSTOM_PROFILE == PARAM_CUSTOMER) else PARAM_CUSTOMER + '-' + PARAM_CUSTOM_PROFILE

trello = trello_lib_ism.TrelloUpdate(apikey=API_KEY, token=TOKEN, board_name=BOARD_NAME, org_name=ORG_NAME, list_name=LIST_NAME)
trello.new_card(card_name=CARD_NAME, desc=PARAM_DESCRIPTION)
trello.add_comment(card_name=CARD_NAME, comment=JENKINS_URL)
