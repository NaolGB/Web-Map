import requests
from bs4 import BeautifulSoup
import multiprocessing
from utils import secrets
import mysql.connector
import time
from tldextract import extract
from threading import Thread
import multiprocessing
import pandas as pd


db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = secrets.MYSQL_PWD,
        database = 'MapTheInternet',
        autocommit = True
    )


def generateChildLinks(child):
    session = requests.Session()
    try:
        # child is the url from which we want to extrach a list of other urls
        result = session.get(child, timeout=1)
        soup = BeautifulSoup(result.content, 'lxml')
        taggedElements = soup.find_all('a', href=True)
        # returns a list of <a> tags
        return taggedElements
    except Exception as e:
        return False
        # TODO extend to adress more exceptions like time out, refused conncections and more

def insertLink(parent, child):
    cursor = db.cursor()

    cursor.execute(f"""
        SELECT *
        FROM domains
        WHERE domain = '{child}'
    """)
    row = cursor.fetchall()

    if len(row) == 0:
        # if the domain does not exist in out database
        try:
            # try/except for duplicate entries protection (for multiprocess)
            cursor.execute(f"""
                INSERT INTO domains(domain, numIncomingLinks, numInternalLinks, connectionStatus)
                VALUES(
                    '{child}',
                    '1',
                    '0',
                    'fetched'
                )
            """)
        except:
            pass
    else:
        if parent == child:
            # if the domain exists but is internal link
            cursor.execute(f"""
                UPDATE domains
                SET numInternalLinks = '{int(row[0][3]) + 1}'
                WHERE domain = '{child}'
            """)
        else:
            # if the domain exixst but is coming form a different domain
            cursor.execute(f"""
                UPDATE domains
                SET numIncomingLinks = '{int(row[0][2]) + 1}'
                WHERE domain = '{child}'
            """)

    cursor.close()


def insertNewLinksIntoDb(parent, newLinks):
    """
        ### Explanation of the data format:
            - domain: the url of a website
                - https://www.google.com/search? has google.com and so does https://drive.google.com/
            - numIncomingLins: the number of times other websites linked to this website
                - if https://www.facebook.com/marketplace/?ref=bookmark has a link to  https://drive.google.com/ then the numIncomingLinks of google.com is increased by 1
            - numInternalLinks: the number of time a page has a link to another page with the same domain
                - if https://drive.google.com/ has a link to https://www.google.com/search? then the numIntenalLinks of google.com is increased by 1 since bothe pages are from the same domain
            - connectionStatus: a flag to indicate whether a website has been visited 
                - A website is crawled by domain instead of each page. For example when google.com is crwaled:
                    - the connectionStatus flag is set to 'child-generated' for google.com in the database
                    - pages from google.com are put into a list called childLinks in crawl()
                    - crawl() calls this function insertNewLinksIntoDb()
                    - for each child page passed to insertNewLinksIntoDb() through childLinks
                        - the domain is extracted and inserted into the database while updating both numIncomingLinks and numInternalLinks
                            - https://www.google.com/search?q=hi+there&rlz=... is inserted as google.com
    """
    for a in newLinks:
        if a['href'].startswith('http'):
            child = a['href']
            if child.startswith('https://'):
                hyper = 'https://'
            else:
                hyper = 'http://'

            # with sub domain
            # subdomain.domain.suffix
            subDomain, domain, suffix = extract(child)
            # without sub domain
            child = hyper + domain + '.' + suffix

            insertLink(parent=parent, child=child)

def crawl(repititions=100):
    # process repetetion number of pages
    cursor = db.cursor(buffered=True)

    for _ in range(repititions):
        cursor.execute("""
            SELECT *
            FROM domains
            WHERE connectionStatus = 'fetched' ORDER BY RAND() LIMIT 1;
        """)
        row = cursor.fetchone()
        
        cursor.execute(f"""
            UPDATE domains
            SET connectionStatus = 'children-generated'
            WHERE domain = '{row[1]}'
        """)
        
        childLinks = generateChildLinks(row[1])

        if childLinks != False:
            # if the links on parent page (row[1]) are extracted succesfully
            insertNewLinksIntoDb(row[1], childLinks)
            
    cursor.close()

def innitiatingScript():
    # data: list of top 50 websites from https://en.wikipedia.org/wiki/List_of_most_visited_websites (accessed Sept 22, 2022)
    # setup the databse with seed domains, these are popular domains from which we start searching other doamins (likely also popular)
    # this decreases the chance that we not explore some websites
    domains = pd.read_csv('data/top50DomainsWikipedia.csv')
    domains['Domain Name'] = 'https://' + domains['Domain Name']
    domainsList = domains['Domain Name'].tolist()

    # fill db with seed domains
    cursor = db.cursor()
    for link in domainsList:
        try:
            cursor.execute(f"""
                INSERT INTO domains(domain, numIncomingLinks, numInternalLinks, connectionStatus)
                VALUES(
                    '{link}',
                    '0',
                    '0',
                    'fetched'
                )
            """)
        except:
            pass

    # generate childred domains from each seed domain
    for link in domainsList:
        cursor.execute(f"""
            UPDATE domains
            SET connectionStatus = 'children-generated'
            WHERE domain = '{link}'
        """)
        
        childLinks = generateChildLinks(link)

        if childLinks != False:
            insertNewLinksIntoDb(link, childLinks)
    
    cursor.close()

def main():
    processes = []

    for _ in range(50):
        p = multiprocessing.Process(target=crawl)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

if __name__ == '__main__': 
            # # # innitiatingScript()

    start = time.time()
    for _ in range(10):
        main()
    end = time.time()

    print(end - start)

# data cost:
# 5715 -> 10_636 (4_921 domains) = 153 mb => 0.03mb/domain (for download)