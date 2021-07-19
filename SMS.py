# -*- coding: utf-8 -*-

import zhenzismsclient as smsclient

import random

class sms:

    def __init__(self):
        self.apiUrl = 'https://sms_developer.zhenzikj.com'
        self.appId = '107456'
        self.appSecret = 'bb3f909f-ef88-4343-8a19-9930e728a0f8'

    def send_message(self, telephone):
        code = ''

        for num in range(1, 5):
            code = code + str(random.randint(0, 9))

        print(code)

        client = smsclient.ZhenziSmsClient(self.apiUrl, self.appId,
                                           self.appSecret)

        params = {'number': telephone, 'templateId': '6039'}

        print(client.send(params))


# p = sms()
# p.send_message("18813019319")
