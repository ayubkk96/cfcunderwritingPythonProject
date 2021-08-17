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
# Could have done docstring if more time

# 1. Scrape the index webpage hosted at `cfcunderwriting.com`.


# Name of JSON files.
external_resources_json = "external_resources"
word_frequency_count_json = "word_frequency"

# URL of target page.
url = "https://www.cfcunderwriting.com"

# Variables to find internal resources on 'cfcunderwriting.com'.
cfc_name = "cfcunderwriting"
internal_folder_directory = "/"

# Known resources on a web page.
external_resources_check_list = {"img": "src", "video": "src",
                                 "audio": "src", "embed": "src",
                                 "object": "data", "source": "src",
                                 "script": "src", "link": "href",
                                 "iframe": "src"}

# HTML tags that do not contain visible text and get rid of tag duplicates.
no_text_html_tags = ['style', 'script',
                     'head', 'title', 'meta', '[document]',
                     'html', 'link', 'form', 'select',
                     'div', 'option', 'input', 'li',
                     'ul', 'svg', 'span', 'body', 'header', 'nav',
                     'iframe', 'noscript', 'label', 'main']


def scrape_page(url):
    page = requests.get(url)
    scraped_page = BeautifulSoup(page.content, "html.parser")
    return scraped_page


def save_json_file(file_name, data):
    # Takes file name and saves data into JSON format in a file
    with open(file_name + ".json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        print("External resources have been exported to the JSON file named:", file_name)


def get_list_of_external_resources(tag, attribute, target_page):
    # Loops through soup of page and appends attributes if they do not have cfc name or '\' folder directory
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


def create_external_resources_list(scraped_page):
    # Takes the list of attributes and checks them with the list of external resources tags to determine if it is
    # external
    data = []
    for key in external_resources_check_list:
        attributes = get_list_of_external_resources(key, external_resources_check_list[key], scraped_page)
        if not attributes:
            pass
        else:
            data.append({key: attributes})

    if not data:
        return print("No external resources on the web page")

    return data


def enumerate_hyperlinks(target_page):
    # Returns hyperlinks enumerated by checking if the link has 'href'
    list_of_hyperlinks = []
    content = requests.get(target_page).content

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
    # Loops through the enum object to find the privacy page link
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

def get_privacy_policy_soup(privacy_policy_link):
    # Create privacy page link and new scraped page soup.
    privacy_page = url + privacy_policy_link
    privacy_page = requests.get(privacy_page)
    page_soup = BeautifulSoup(privacy_page.content, "html.parser")

    return page_soup


def get_dict_of_words(page_soup):
    # Get the visible text of the page into a dictionary and return the dictionary.
    # The tag names will be compared with html tags that do not have text.
    dictionary = {}
    for tag in page_soup.findAll(True):
        if tag.name in no_text_html_tags:
            pass
        else:
            # Assign inheritance of tags to variables
            grandad = tag.parent.parent.name
            great_grandad = tag.parent.parent.parent.name
            if (tag.text, tag.name) == dictionary.items():
                pass
            else:
                if grandad == 'form':
                    pass
                elif great_grandad == 'form':
                    pass
                elif grandad or great_grandad != 'form':
                    # Assign text to key in dictionary
                    # to prevent text from being overridden by incorrect duplicates.
                    dictionary[tag.text.strip()] = tag.name
    return dictionary


def get_list_of_words(dictionary):
    # Append the text to list
    list_of_words = []

    for key in dictionary:
        list_of_words.append(key)
    return list_of_words


def clean_list(list_of_words):
    # Remove punctuation, spaces and other ASCII characters from list.
    str1 = ' '.join(list_of_words)
    str1 = str1.lower()
    str1.strip()

    str2 = str1.translate(str.maketrans('', '', string.punctuation))
    str2 = str2.replace("“", "")
    str2 = str2.replace("↑", "")
    str2 = str2.replace("©", "")

    result = ''.join([i for i in str2 if not i.isdigit()])
    list_of_words = result.split()

    return list_of_words


def get_word_frequency_count(list_of_words):
    counts = Counter(list_of_words)
    save_json_file(word_frequency_count_json, counts)
    print("Count of word frequency has been uploaded to the JSON file named:", word_frequency_count_json)
    return 1


def main():
    #   1.Scrape the index webpage hosted at `cfcunderwriting.com`
    page_soup = scrape_page(url)

    #   2. Create JSON file of external resources on cfcunderwriting.com
    external_resources_data = create_external_resources_list(page_soup)
    save_json_file(external_resources_json, external_resources_data)

    #   3. Return enumeration of page's hyperlinks to object and
    #   find privacy policy link on page using enumeration object created
    enum_object = enumerate_hyperlinks(url)
    privacy_policy_link = find_privacy_policy(enum_object)

    #   4. Access and count the privacy policy page's 'visible' text using the link obtained in the enumeration object
    privacy_page = get_privacy_policy_soup(privacy_policy_link)
    dictionary = get_dict_of_words(privacy_page)
    list_of_words = get_list_of_words(dictionary)
    clean_list_of_words = clean_list(list_of_words)
    get_word_frequency_count(clean_list_of_words)

    return print("Web scraping has been completed successfully")


if __name__ == '__main__':
    main()
