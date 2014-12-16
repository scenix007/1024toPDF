#!/bin/env python
#encoding=utf-8
# Author: Aaron
# Last modified: 2014-10-22 23:42
# Filename: 1024.py
# Description: 

import sys
import time
import socks
import socket
import urllib2
import urllib
import re
import os
import threading

SOCKS_PORT = 1080

def get_url():
    pass
    if len(sys.argv) != 3:
        print >> sys.stderr, "need a url and output name"
        sys.exit(-1)
    return sys.argv[1]

def get_outfname():
    pass
    if len(sys.argv) != 3:
        print >> sys.stderr, "need a url and output name"
        sys.exit(-1)
    return sys.argv[2]

def get_html(url):
    pass
    global SOCKS_PORT
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", SOCKS_PORT)
    socket.socket = socks.socksocket
    response = urllib2.urlopen(url)
    return response.read()

def find_image_urls(html):
    urls = re.findall(r'https?://\S+\.jpg', html)
    if len(urls) == 0:
        print >> sys.stderr, "Can not find image urls"

    domain_count = {}
    for url in urls:
        domain = url.split('/')[2]
        domain = '.'.join(domain.split('.')[-2:])
        if domain not in domain_count:
            domain_count[domain] = 1
        else:
            domain_count[domain] += 1
    domain_count = sorted(domain_count.items(), key=lambda x:x[1], reverse=True)

    top_domain = domain_count[0][0]

    urls = filter(lambda x : top_domain in x, urls)

    out_f = file('download_list.txt', 'w')
    for url in urls:
        out_f.write(url+'\n')
    out_f.close

    return urls


def download_images_wget(image_urls):
    os.system('rm -rf tmp; mkdir tmp')
    os.system("cd tmp; wget -i ../download_list.txt; cd -")

def download_images(image_urls):
    total_images_count = len(image_urls)
    os.system('rm -rf tmp; mkdir tmp')
    print >> sys.stderr, "Downloading %d images ..." % (total_images_count)
    threads = []
    for i in xrange(0, total_images_count):
        image_url = image_urls[i]
        t = threading.Thread(target=down_load_single_image, args=(image_url, i))
        threads.append(t)

    for t in threads:
        while threading.activeCount() > 11:
            time.sleep(1) 
        t.start()
    while threading.activeCount() > 1:
        time.sleep(1) 
        
class AppURLopener(urllib.FancyURLopener):
    pass
    version="Mozilla/5.0"

def down_load_single_image(image_url, index):
    global SOCKS_PORT
    max_retry = 3
    is_done = False
    for cur_try in xrange(1, max_retry+1):
        print >> sys.stderr, "Start downloading image %d attempt %d, url: %s" % (index,cur_try, image_url)
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", SOCKS_PORT)
        socket.setdefaulttimeout(20) 
        socket.socket = socks.socksocket
        try:
            urllib._urlopener = AppURLopener()
            urllib.urlretrieve(image_url, 'tmp/%d.jpg' % (index+1))
        except Exception,e:
            print >> sys.stderr, e
            continue
        print >> sys.stderr, "Finish downloading image %d on attempt %d, url: %s" % (index,cur_try, image_url)
        is_done = True
        return
    if False == is_done:
        print >> sys.stderr, "Failed downloading image %d, url: %s" % (index, image_url)
    


def create_pdf(fname):
    os.system("./convert tmp/*.jpg %s.pdf" % fname)


if __name__ == '__main__':
    url = get_url()
    html = get_html(url)
    image_urls = find_image_urls(html)
    download_images(image_urls)
    fname = get_outfname()
    create_pdf(fname)
    print "Thanks to Aaron, good person one life flat safe, 1024 Amen!"

    





