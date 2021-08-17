# cfcunderwritingPythonProject
Name
CFC Underwriting web scraper

Description
This project is a technical task by CFC Underwriting.
Produce a program that:
1. Scrape the index webpage hosted at `cfcunderwriting.com`
2.Writes a list of *all externally loaded resources* (e.g. images/scripts/fonts not hosted
on cfcunderwriting.com) to a JSON output file.
3.Enumerates the page's hyperlinks and identifies the location of the "Privacy Policy"
page
4. Use the privacy policy URL identified in step 3 and scrape the pages content.
Produce a case-insentitive word frequency count for all of the visible text on the page.
Your frequency count should also be written to a JSON output file..

Installation
To install this file on your computer, enter this script into your terminal: gh repo clone https://github.com/ayubkk96/cfcunderwritingPythonProject
If you would like to install the file via a gui, please check out the docs on GitHub.com: https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository

How to run:
Run in IDE or navigate to src folder and enter and execute 'python main.py'

Usage
The usage of this program is to scrape the contents of a page and produce a json file containing external resources and a word count of a particular page.

Support
If you need support setting this project up, please contact my email address at 'ayubkaou@gmail.com'

Roadmap
1. Create tests of functions, such as testing the connection to the target website for scraping.
2. Create an error handler to fix and respond to error messages.
3. Create a user input function to take the region the user is located so that the program scrapes the specified region's page. e.g. 'CFCunderwriting.com/us/'.
4. Create a mobile version of the web scraper as the pages can contain different text depending on the size of the screen.
5. Convert the program to use Selenium so that the scraping can be more accurate. Selenium is better for scraping pages built on JavaScript. CFC underwriting uses ReactJS.
6. Import PythonDocs to create more sophisticated comments for the program.

Contributing
If anyone is willing to contribute or expand on this project, please contact me on ayubkaou@gmail.com
Anyone is welcome to clone this repo for their own purposes. All scraping must comply with CFC Underwriting's robots.txt file: https://www.cfcunderwriting.com/en-gb/robots.txt
