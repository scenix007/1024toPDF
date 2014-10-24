#!/bin/env python
#encoding=utf-8
# Author: shaolong - shaolong@sogou-inc.com
# Last modified: 2014-10-22 23:42
# Filename: cl.py
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
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 7777)
    socket.socket = socks.socksocket
    response = urllib2.urlopen(url)
    return response.read()

def find_image_urls(html):
    urls = re.findall(r'http://\S+\.jpg', html)
    if len(urls) == 0:
        print >> sys.stderr, "Can not find image urls"
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
        
class AppURLopener(urllib.FancyURLopener):
    pass
    version="Mozilla/5.0"

def down_load_single_image(image_url, index):
    print >> sys.stderr, "Start downloading image %d, url: %s" % (index, image_url)
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 7777)
    socket.socket = socks.socksocket
    try:
        urllib._urlopener = AppURLopener()
        urllib.urlretrieve(image_url, 'tmp/%d.jpg' % (index+1))
    except Exception,e:
        print >> sys.stderr, e
    print >> sys.stderr, "Finish downloading image %d, url: %s" % (index, image_url)
    


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

    





