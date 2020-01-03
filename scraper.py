import sys
import argparse
import urllib.request
import re
from bs4 import BeautifulSoup


def site_search(url):
    """Searches url's HTML for urls, emails, and phone #'s"""
    # Getting url html from and decoding it from bytes
    url_data = urllib.request.urlopen(url)
    url_bytes = url_data.read()
    url_str = url_bytes.decode("utf8")
    url_data.close()
    # Initializing ending lists that won't have dupes
    url_list = []
    email_list = []
    phone_numbers_list = []
    # Matching urls and appending to list without dupes
    urls = re.findall((r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%'
                      '[0-9a-fA-F][0-9a-fA-F]))+'), url_str)
    print("URLS:\n")
    [url_list.append(url) for url in urls if url not in url_list]
    for url in url_list:
        print(url)
    if len(urls) == 0:
        print("NONE")
    # Matching emails and appending to list without dupes
    emails = re.findall(r"\w+@\w+.\w+", url_str)
    print("\nEMAILS:\n")
    [email_list.append(email) for email in emails if email not in email_list]
    for email in email_list:
        print(email)
    if len(emails) == 0:
        print("NONE")
    # Matching phone numbers and appending to list without dupes
    phone_number = re.findall((r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)'
                               r'\s*\d{3}[-\.\s]??\d{4}'
                               r'|\d{3}[-\.\s]??\d{4})'), url_str)
    print("\nPHONE NUMBERS:\n")
    [phone_numbers_list.append(number) for number in phone_number if number
        not in phone_numbers_list]
    for number in phone_numbers_list:
        print(number)
    if len(phone_number) == 0:
        print("NONE\n")


def html_parser(url):
    """parse HTML for specific tags"""
    # Getting url html from and decoding it from bytes
    url_data = urllib.request.urlopen(url)
    url_bytes = url_data.read()
    url_str = url_bytes.decode("utf8")
    url_data.close()
    # Using BeautifulSoup just to get img or a tags
    page = BeautifulSoup(url_str, features="html.parser")
    print(page.findAll('img'))
    print(page.findAll('a'))


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='url to search for emails/urls/phone #s')

    return parser


def main(args):
    """Parse args, get data from url"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)
    site_search(parsed_args.url)
    html_parser(parsed_args.url)


if __name__ == '__main__':
    main(sys.argv[1:])
