# -*- coding: utf-8 -*-
import urllib
from bs4 import BeautifulSoup
import unicodedata
import pandas as pd
import numpy as np
import time
def removeNonAscii(s):
    # Get rid of non ascii characters
    return "".join(i for i in s if ord(i)<128)

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

def headline_and_body(article_url):
    article_html = urllib.urlopen(article_url).read()
    postid_start_tag = 'postid-'
    postid_end_tag = ' js'
    postid_start_id = article_html.index(postid_start_tag)
    postid_end_id = article_html.index(postid_end_tag)
    postid_html = article_html[postid_start_id+len(postid_start_tag):postid_end_id]
    hl_start_tag = "<title>"
    hl_end_tag = "</title>"
    hl_start_id = article_html.index(hl_start_tag)
    hl_end_id = article_html.index(hl_end_tag)
    headline_html = article_html[hl_start_id:hl_end_id]
    b_start_tag = "</div></form></div></div><h2"
    b_end_tag = "<h3>Read More Stories About:</h3>"
    b_start_id = article_html.index(b_start_tag)
    b_end_id = article_html.index(b_end_tag)
    body_html = article_html[b_start_id:b_end_id]
    return postid_html, headline_html, body_html

def clean_HTML(html):
    html = removeNonAscii(html)
    soup = BeautifulSoup(html)
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '  '.join(chunk for chunk in chunks if chunk)

    """
    Get rid of erroneous square brackets and internal publicity
    """
    dic = {'[': '', ']':'', 'SIGN UP FOR OUR NEWSLETTER':'', u'\u201c':'', u'\u2014':'', u'\u201d':'', u'\u2018':"", u'\u2019':"'", u'\u2013':'', u'\u2026':''}
    text = replace_all(text, dic)
    return str(text)

def next_link(home_html, current_id):
    try:
        link_start_id = home_html.index(link_start_tag)
        link_end_id = link_start_id+home_html[link_start_id::].index(link_end_tag)
        article_link = home_html[link_start_id+len(link_start_tag):link_end_id]
        next_id = link_end_id+len(link_end_tag)
    except:
        print "Next Link not found, going to try and go to next page"
        article_link = False
        next_id = 0
    # return link and finishing index
    return article_link, next_id

data_dic = {}
home_url = "http://www.breitbart.com/big-government/"
link_start_tag = '<h2 class="title"><a href="'
link_end_tag = '" title='
home_html = urllib.urlopen(home_url).read()

# Initially, get the first link and end_id
article_link, next_id = next_link(home_html,0)
i = 0
while len(data_dic.keys()) < 100:
    #print article_link, next_id
    if article_link:
        try:
            article_url = "http://www.breitbart.com"+article_link
            article_url = article_url.replace("http://www.breitbart.comh", 'h')
            try:
                post_id, headline_html, body_html = headline_and_body(article_url)
            except:
                print article_url, " body or headline couldn't be found"
                post_id, headline_html, body_html = 0, '', ''
            try:
                headline_text, body_text = clean_HTML(headline_html), clean_HTML(body_html)
            except e:
                print e
            # store it in the dictionary
            data_dic[i] = np.array([post_id,headline_text, body_text, article_link])
            i+=1
            time.sleep(0.1)

            article_link, next_id = next_link(home_html, next_id)
            # update the hompage html file
            home_html = home_html[next_id::]
        except Exception as inst:
            print type(inst)
            # If the headline or body can't be stored for whatever reason, just skip it
            article_link, next_id = next_link(home_html, next_id)
            # This will be stored next time around
            # update the hompage html file
            home_html = home_html[next_id::]
    else:
        new_page_begin_tag = '<div class="alignleft"><a href="'
        new_page_end_tag = '" >older posts</a></div>'
        new_page_begin_id = home_html.index(new_page_begin_tag)+len(new_page_begin_tag)
        new_page_end_id = home_html.index(new_page_end_tag)
        home_url =home_html[new_page_begin_id:new_page_end_id]
        print "new page @ ", home_url
        home_html = urllib.urlopen(home_url).read()
        article_link, next_id = next_link(home_html,next_id)
#article_url = "http://www.breitbart.com/big-government/2017/02/28/target-down-30-percent-since-transgender-boycott-began/"
#article_url = "http://www.breitbart.com/big-government/2017/03/01/rabbi-shmuley-comparing-trump-hitler-desecrates-holocaust/"
#article_url = "http://www.breitbart.com/big-government/2017/03/01/trump-speech-offered-america-cathartic-moment-mourning/"



#df = pd.DataFrame(data_lib, index=range(len(data_lib.keys())),columns=['A','B','C'])
