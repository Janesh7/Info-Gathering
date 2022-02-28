from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re

user_url = str(input('[+} Enter Target URL to Scan : '))
urls = deque([user_url])  # perform deque

scraped_urls = set()
emails = set()
count = 0

try:
    while len(urls):
        count += 1
        if count == 100:  # scape only first 100 urls
            break
        url = urls.popleft()  # pop urls in deque
        scraped_urls.add(url)  # add to set

        parts = urllib.parse.urlsplit(url)  # splitting the url
        base_url = '{0.scheme}://{0.netloc}'.format(parts)  # format the splitted url

        path = url[:url.rfind('/') + 1] if '/' in parts.path else url  # list comprehensions
        print('[%d] Processing %s' % (count, url))

        try:
            response = requests.get(url)  # try getting the response
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue  # otherwise continue

        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text,
                                    re.I))  # regex expression to find all the strings with the specified pattern which is (anything)@(anything) in response in text form and re.I means simply just ignoring the case
        emails.update(new_emails)

        soup = BeautifulSoup(response.text, features='lxml')  # create bs object

        for anchor in soup.find_all("a"):  # find anchors
            link = anchor.attrs[
                'href'] if 'href' in anchor.attrs else ''  # find link which is after href if its there otherwise specify nothing
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            if not link in urls and not link in scraped_urls:
                urls.append(link)
except KeyboardInterrupt:
    print('[!!] Closing!')

for mail in emails:
    print(mail)

# note: pip3 install lxml
