#Usage: python script.py <xml-path> <job-name> <build-number>
import xml.etree.ElementTree as ET
import re
import os
import sys
import ism_trello_utils as mf

API_KEY     = os.environ.get("TRELLO_API_KEY")
TOKEN       = os.environ.get("TRELLO_TOKEN")
ORG_NAME    = os.environ.get("TRELLO_ORG_NAME")
BOARD_NAME  = os.environ.get("TRELLO_BOARD_NAME")

URL_PREFIX      = "https://build.isafe-mobile.com/job/"
XML_FILE_PATH   = sys.argv[1]
JOB_NAME        = sys.argv[2]
BUILD_NUM       = sys.argv[3].zfill(4)

def get_baseband(x):
    return {
            'E520_GSMQ_WB18_LTEB3_B5_B8_B40_GPSTCXO': '900mhz',
            'USA_NEW': '850mhz',
            'USA_NEW1': '850mhz',
            'simcom72_cwet_a_kk_hspa': '900mhz',
            'simcom72_cwet_a_kk_hspa_125': '850mhz',
            'simcom72_cwet_a_kk_hspa_RGSM900_EU': '900mhz',
            'simcom72_wet_jb3_hspa_p36_128': '900mhz',
            'simcom72_wet_jb3_hspa_p36': '850mhz',
            'hexing89_we_jb2_md1_hspa_band_1_2_8': '900mhz',
            'ztb89_we_jb2_md1_hspa_band125': '850mhz'
            }.get(x, x) #if you cant map, return the original string

def get_xml_value(root, key):
    XML_ELEMENT_PATH_PREFIX = "actions/hudson.model.ParametersAction/parameters/hudson.model.StringParameterValue/"
    return (root.findall(XML_ELEMENT_PATH_PREFIX + "[name='" + key + "']"))[0].find("value").text

def get_xml_text_value(root, key):
    XML_ELEMENT_PATH_PREFIX = "actions/hudson.model.ParametersAction/parameters/hudson.model.TextParameterValue/"
    return (root.findall(XML_ELEMENT_PATH_PREFIX + "[name='" + key + "']"))[0].find("value").text

try:
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
except:
    print("Error: Failed parsing xml: " + XML_FILE_PATH)
    exit(1)

PARAM_CUSTOMER = ""
try:
    PARAM_CUSTOMER = get_xml_value(root, "PARAM_CUSTOMER")
except IndexError:
    print("Error: customer not found for xml: " + XML_FILE_PATH)
    exit(1)

PARAM_BASEBAND = ""
try:
    PARAM_BASEBAND_STR = get_xml_value(root, "PARAM_BASEBAND")
    PARAM_BASEBAND = get_baseband(PARAM_BASEBAND_STR)
except IndexError:
    PARAM_BASEBAND = "900mhz(guessed)"

PARAM_CUSTOM_PROFILE = ""
try:
    PARAM_CUSTOM_PROFILE = get_xml_value(root, "PARAM_CUSTOM_PROFILE")
except IndexError:
    PARAM_CUSTOM_PROFILE = ""

PARAM_DESCRIPTION = ""
try:
    PARAM_DESCRIPTION = get_xml_text_value(root, "Description")
except IndexError:
    PARAM_DESCRIPTION = ""

PARAM_DESCRIPTION = PARAM_DESCRIPTION.replace("<b>", "**")
PARAM_DESCRIPTION = PARAM_DESCRIPTION.replace("</b>", "**")
PARAM_DESCRIPTION = PARAM_DESCRIPTION.replace("<pre>","")
PARAM_DESCRIPTION = PARAM_DESCRIPTION.replace("</pre>","")

CARD_NAME = PARAM_CUSTOMER + "-" + BUILD_NUM + "-" + PARAM_BASEBAND
if PARAM_CUSTOM_PROFILE != "":
    CARD_NAME = CARD_NAME + "(" + PARAM_CUSTOM_PROFILE + ")"

LIST_NAME = PARAM_CUSTOMER if (PARAM_CUSTOM_PROFILE == "" or PARAM_CUSTOM_PROFILE == PARAM_CUSTOMER) else PARAM_CUSTOMER + '-' + PARAM_CUSTOM_PROFILE

JENKINS_URL = URL_PREFIX + JOB_NAME + "/" + BUILD_NUM + "/"

mf.initialize(apikey=API_KEY, token=TOKEN, board_name=BOARD_NAME, org_name=ORG_NAME)
mf.new_list(list_name=LIST_NAME)
mf.new_card(card_name=CARD_NAME, list_name=PARAM_CUSTOMER, desc=PARAM_DESCRIPTION)
mf.add_comment(card_name=CARD_NAME, comment=JENKINS_URL)
