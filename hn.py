from lxml import html
from lxml.cssselect import CSSSelector
from slugify import slugify
import requests
import os
import shutil
import subprocess
from time import sleep

JOB_TABLE_INDEX = 2
AD_DIR = 'job_ads'
URL = 'http://news.ycombinator.com/jobs'


def lint_hn(download_afresh=False):
    if download_afresh:
        parse_hn()
    filenames = os.listdir(AD_DIR)
    for f in filenames:
        filepath = AD_DIR + '/' + f
        print f
        subprocess.call(['joblint', filepath])


def parse_hn():
    r = requests.get(URL)

    if r.status_code == 200:
        text = r.text
        jobs = get_job_links(text)
        try:
            os.mkdir(AD_DIR)
        except OSError:
            # Directory exists, let's clear it out
            shutil.rmtree(AD_DIR)
            os.mkdir(AD_DIR)
        for link in jobs:
            r = requests.get(link, timeout=30.0)
            if r.status_code != 200:
                print "Warning, failed to get " + link
            else:
                text = r.text
                title = get_title(text)
                fout = open(AD_DIR + '/' + title + '.html', 'w')
                fout.write(text.encode('utf-8'))
                print "."
                sleep(3)
        return
    else:
        print "Error: HTTP status code %s. Is Hacker News down?" % (r.status_code,)


def get_job_links(text):
    parsed = html.fromstring(text)
    sel = CSSSelector('table')
    job_table = sel(parsed)[JOB_TABLE_INDEX]
    sel = CSSSelector('a')
    links = []
    for link in sel(job_table):
        url = link.get('href')
        if not url[:4] == 'http':
            # hacker news internal job posting
            url = URL + '?' + url
        links.append(url)
    return links


def get_title(text):
    parsed = html.fromstring(text)
    sel = CSSSelector('title')
    title = sel(parsed)[0].text_content()
    return slugify(title)

if __name__=='__main__':
    lint_hn(download_afresh=True)
