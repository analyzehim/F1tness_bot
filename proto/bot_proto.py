# -*- coding: utf-8 -*-
import requests
import time
import socket

from bot_const import *

# requests.packages.urllib3.disable_warnings()  # Подавление InsecureRequestWarning, с которым я пока ещё не разобрался


class Telegram:
    def __init__(self):
        self.proxy = checkMode()
        self.TOKEN = getToken()
        self.URL = 'https://api.telegram.org/bot'
        if self.proxy:
            self.proxies = getProxies()
        self.chat_id = 74102915
        self.offset = 0
        self.host = socket.getfqdn()
        self.Interval = getInterval()
        if not self.proxy:
            log_event("Init completed, host: " + str(self.host))
        if self.proxy:
            log_event("Init completed with proxy, host: " + str(self.host))

    def get_updates(self):
        data = {'offset': self.offset + 1, 'limit': 5, 'timeout': 0}
        if not self.proxy:
            request = requests.post(self.URL + self.TOKEN + '/getUpdates', data=data)
        if self.proxy:
            request = requests.post(self.URL + self.TOKEN + '/getUpdates', data=data, proxies=self.proxies)
        if (not request.status_code == 200) or (not request.json()['ok']):
            return False

        if not request.json()['result']:
            return
        parametersList = []
        for update in request.json()['result']:
            self.offset = update['update_id']

            if 'message' not in update or 'text' not in update['message']:
                continue

            from_id = update['message']['chat']['id']  # Chat ID
            author_id = update['message']['from']['id']  # Creator ID
            message = update['message']['text']
            date = update['message']['date']
            try:
                name = update['message']['chat']['first_name']
            except:
                name = update['message']['from']['first_name']
            parameters = (name, from_id, message, author_id, date)
            parametersList.append(parameters)
            try:
                log_event('from %s (id%s): "%s" with author: %s; time:%s' % parameters)
            except:
                pass
        return parametersList

    def send_text_with_keyboard(self, chat_id, text, keyboard):
        try:
            log_event('Sending to %s: %s; keyboard: %s' % (chat_id, text, keyboard))  # Logging
        except:
            log_event('Error with LOGGING')
        json_data = {"chat_id": chat_id, "text": text,
                     "reply_markup": {"keyboard": keyboard, "one_time_keyboard": True}}
        if not self.proxy:  # no proxy
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', json=json_data)  # HTTP request

        if self.proxy:
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', json=json_data,
                                    proxies=self.proxies)  # HTTP request with proxy

        if not request.status_code == 200:  # Check server status
            return False
        return request.json()['ok']  # Check API

    def send_text(self, chat_id, text):
        try:
            log_event('Sending to %s: %s' % (chat_id, text))  # Logging
        except:
            log_event('Error with LOGGING')
        data = {'chat_id': chat_id, 'text': text}  # Request create
        if not self.proxy:
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', data=data)  # HTTP request

        else:
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', data=data,
                                    proxies=self.proxies)  # HTTP request with proxy

        if not request.status_code == 200:  # Check server status
            return False
        return request.json()['ok']  # Check API

    def ping(self):
        log_event('Sending to %s: %s' % (self.chat_id, 'ping'))
        data = {'chat_id': self.chat_id, 'text': 'ping'}
        if not self.proxy:
            requests.post(self.URL + self.TOKEN + '/sendMessage', data=data)  # HTTP request

        if self.proxy:
            requests.post(self.URL + self.TOKEN + '/sendMessage', data=data,
                                    proxies=self.proxies)  # HTTP request with proxy


def log_event(text):
    f = open('log.txt', 'a')
    event = '%s >> %s' % (time.ctime(), text)
    print event + '\n'
    f.write(event+'\n')
    f.close()
    return
