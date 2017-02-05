#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import xml.etree.ElementTree as ET


ADMIN_ID = 74102915  # My ID
PIG_ID = 117797858
URL = 'https://api.telegram.org/bot'  # HTTP Bot API URL
PIG_LIST = ['cute', 'adorable', 'attractive',
            'beautiful', 'handsome', 'pretty',
            'gorgeous', 'lovely', 'foxy',
            'sexy', 'hot', 'babe']
CHAT_ID = 65

def getToken():
    tree = ET.parse('private_config.xml')
    root = tree.getroot()
    TOKEN = root.findall('token')[0].text
    return TOKEN


def get_train_list(MODE):
    if MODE == 1:
        f = open('data/legs.txt')

    elif MODE == 2:
        f = open('data/back.txt')

    elif MODE == 3:
        f = open('data/chest.txt')
    else:
        return 0
    train_list = []
    for line in f:
        train_list.append(line)
    f.close()
    return list(reversed(train_list))

def getInterval():
    tree = ET.parse('config.xml')
    root = tree.getroot()
    interval = float(root.findall('interval')[0].text)
    return interval

def getProxyPassword():
    tree = ET.parse('private_config.xml')
    root = tree.getroot()
    password = root.findall('proxy_password')[0].text
    return password

def getProxies():
    tree = ET.parse('private_config.xml')
    root = tree.getroot()
    proxy_url = root.findall('proxy')[0].text
    password = getProxyPassword()
    proxy_url = proxy_url.replace("PASSWORD", password)
    proxies = {
      "http": proxy_url,
      "https": proxy_url,
    }
    return proxies

def getProxyPassword():
    tree = ET.parse('private_config.xml')
    root = tree.getroot()
    password = root.findall('proxy_password')[0].text
    return password

def checkMode():
    import requests

    try:
            requests.get('https://www.ya.ru')
            return False
    except:
            proxies = getProxies()
            requests.get('https://www.ya.ru', proxies=proxies)
            return True

