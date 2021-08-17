import requests
from bs4 import BeautifulSoup, SoupStrainer
from collections import Counter
import string
from bs4.element import Comment
import urllib.request

import json

# What I would do if i had more time:
# Error handler to quit if nothing is found
# Test functions and connection to website
# Put user input for whichever location they are in, that way I can insert 'en-gb' or 'en-us' for the url
# as it might break if the user's location is in USA and this code trying to access the GB privacy policy page
# Make a mobile version because some things are viewable by mobile but not on desktop, e.g. MY CFC portal is
# still viewable on mobile despite being discontinued on July 14th 2021
# Prevented incorrect duplicates by making a dictionary that logged keys that were already in

# 1. Scrape the index webpage hosted at `cfcunderwriting.com`

# Insert URL of desired target for web scraper
url = "https://www.cfcunderwriting.com"
page = requests.get(url)
scraped_page = BeautifulSoup(page.content, "html.parser")

# Insert name of JSON files
external_resources_json = "external_resources"
word_frequency_count_json = "word_frequency"

# Variables to find internal resources on cfcunderwriting.com
cfc_name = "cfcunderwriting"
internal_folder_directory = "/"

# Known resources on a web page
external_resources_check_list = {"img": "src", "video": "src",
                                 "audio": "src", "embed": "src",
                                 "object": "data", "source": "src",
                                 "script": "src", "link": "href",
                                 "iframe": "src"}

# HTML tags that do not contain visible text and get rid of tag duplicates
no_text_html_tags = ['style', 'script',
                     'head', 'title',
                     'meta', '[document]',
                     'html', 'link',
                     'form', 'select',
                     'div', 'option',
                     'input', 'li',
                     'ul', 'svg',
                     'span', 'body',
                     'header', 'nav', 'iframe', 'noscript', 'label', 'main']


# 2. Writes a list of *all externally loaded resources*
# (e.g. images/scripts/fonts not hosted on cfcunderwriting.com) to a JSON output file.
def save_json_file(file_name, data):
    with open(file_name + ".json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        print("External resources have been exported to the JSON file named:", file_name)


def get_list_of_external_resources(tag, attribute, target_page):
    list_of_all_external_resources = []

    for x in target_page.findAll(tag):
        try:
            if cfc_name in x[attribute] or x[attribute][0] == internal_folder_directory:
                pass
            else:
                list_of_all_external_resources.append(x[attribute])
        except KeyError:
            pass
    return list_of_all_external_resources


def create_external_resources_list():
    data = []
    for key in external_resources_check_list:
        attributes = get_list_of_external_resources(key, external_resources_check_list[key], scraped_page)
        if not attributes:
            pass
        else:
            data.append({key: attributes})

    if not data:
        return print("No external resources on the web page")

    save_json_file(external_resources_json, data)


# 3. Enumerates the page's hyperlinks and identifies the location of the "Privacy Policy"
# page
def enumerate_hyperlinks():
    list_of_hyperlinks = []
    content = requests.get(url).content

    for link in BeautifulSoup(content, parse_only=SoupStrainer('a'), features="lxml"):
        if hasattr(link, "href"):
            try:
                list_of_hyperlinks.append(link["href"])
            except KeyError:
                pass

    if not list_of_hyperlinks:
        return print("No hyperlinks found on this page")

    return enumerate(list_of_hyperlinks)


def find_privacy_policy(enum_object):
    print("Hyperlinks have been enumerated")
    privacy_policy_link = ""
    for links in enum_object:
        if "privacy" in links[1]:
            print("The privacy policy page can be found at this link:", links[1])
            privacy_policy_link = links[1]
            return privacy_policy_link
    if not privacy_policy_link:
        return print("There is no privacy policy link on this page")


# 4. Use the privacy policy URL identified in step 3 and scrape the pages content.
# Produce a case-insensitive word frequency count for all of the visible text on the page.
# Your frequency count should also be written to a JSON output file...

def tag_visible(element):
    if element.parent.name in no_text_html_tags:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    print(visible_texts)
    return u" ".join(t.strip() for t in visible_texts)


def get_word_frequency_count(privacy_link):
    privacy_page = url + privacy_link
    page1 = requests.get(privacy_page)
    scraped_page1 = BeautifulSoup(page1.content, "html.parser")

    list_of_words = []
    tag_and_text_logger = {}
    # print(scraped_page1.find_all("div", class_="desc"))
    for tag in scraped_page1.findAll(True):
        if tag.name in no_text_html_tags:
            pass
        else:
            grandad = tag.parent.parent.name
            great_grandad = tag.parent.parent.parent.name
            if (tag.text, tag.name) == tag_and_text_logger.items():
                pass
            else:
                if grandad == 'form':
                    pass
                elif great_grandad == 'form':
                    pass
                elif grandad or great_grandad != 'form':
                    # print("text of tag", tag.text.strip(), "tag name", tag.name)
                    tag_and_text_logger[tag.text.strip()] = tag.name

    # print the keys, they should then be added to a list...
    for key in tag_and_text_logger:
        # if key not in list_of_words:
        list_of_words.append(key)

    str1 = ' '.join(list_of_words)
    str1 = str1.lower()
    str1.strip()

    str2 = str1.translate(str.maketrans('', '', string.punctuation))
    str2 = str2.replace("“", "")
    str2 = str2.replace("↑", "")
    str2 = str2.replace("©", "")
    print(str2)

    result = ''.join([i for i in str2 if not i.isdigit()])

    result1 = result.split()

    counts = Counter(result1)
    save_json_file(word_frequency_count_json, counts)
    #print(counts)
    return 1


def main():
    #   1. Create JSON file of external resources on cfcunderwriting.com
    create_external_resources_list()

    #   2. Return enumeration of page's hyperlinks to object
    enum_object = enumerate_hyperlinks()

    #   3. Find privacy policy link on page using enumeration object created above
    privacy_policy_link = find_privacy_policy(enum_object)

    #   4. Access and count the privacy policy page using the link obtained in the enumeration object
    get_word_frequency_count(privacy_policy_link)

    html = urllib.request.urlopen(url + privacy_policy_link).read()
    # print("this is the test from stack overflow: ", text_from_html(html))

    return print("Web scraping has been completed successfully")


if __name__ == '__main__':
    main()
