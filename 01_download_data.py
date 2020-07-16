#!env python

import requests
import argparse
from bs4 import BeautifulSoup as soup
import re

RE_YEAR = re.compile('([0-9]{4})', re.M)

def parse_args():
    parser = argparse.ArgumentParser(description='Download data.')
    parser.add_argument('--url', default='https://www.vero.fi/henkiloasiakkaat/auto/autoverotus/autoveron_maara/taulukoita_ajoneuvojen_sovelletuista_ve/')
    return parser.parse_args()


def foobar(asd):
    print(asd.__class__)
    if asd:
        print(asd)
    return True


def main(args):
    s = requests.Session()
    r = s.get(args.url)

    page = soup(r.text, 'lxml')
    #with open('sivu.html', 'r') as f:
    #    page = soup(f, 'lxml')

    year_links = page.select('h2:has(> a[id]):contains(Henkil) + ul > li:contains(xls) > a')
    for a in year_links:
        print(f'''{a['href']}, {RE_YEAR.findall(a.text)[0]}''')



if __name__=='__main__':
    main(parse_args())
