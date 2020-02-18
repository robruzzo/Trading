# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 00:09:53 2020

@author: robru
"""
from ftplib import FTP

#domain name or server ip:
ftp = FTP('ftp.nasdaqtrader.com')
ftp.login(user='', passwd = '')
ftp.cwd('/symboldirectory/')

filenames=['nasdaqlisted.txt','otherlisted.txt']

def get_all_ticker_names():    
    for file in filenames:
        localfile = open(file, 'wb')
        ftp.retrbinary('RETR ' + file, localfile.write, 1024)
        localfile.close()
    ftp.quit()

get_all_ticker_names()