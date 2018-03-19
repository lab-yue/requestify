# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys


class __Generate(object):
    def __init__(self, base_string):
        self.base_string = base_string
        self.url = ''
        self.headers = {}
        self.cookies = {}
        self.__generate()
        # self.__key_max_length = 0

    def to_file(self, filename, with_headers=True, with_cookies=True):
        self.__write_to_file(filename, with_headers=with_headers, with_cookies=with_cookies)

    def to_current_file(self, with_headers=True, with_cookies=True):
        current_filename = sys.argv[0].split('/')[-1]
        self.__write_to_file(current_filename, with_headers=with_headers, with_cookies=with_cookies)

    def __generate(self):
        para_reg = re.compile('\'(.+?)\'')
        para = re.findall(para_reg, self.base_string)
        if not para:
            raise ValueError('Not validate curl data')
        self.url = para[0]
        self.__format_headers(para[1:])

    def __write_to_file(self, file, with_headers=True, with_cookies=True):
        request_parameter = ''
        wait_to_write = ['import requests', '\n']
        if with_headers:
            cute_headers = self.__beautify(self.headers)
            wait_to_write.append(f'headers = {cute_headers}')
            request_parameter += ', headers=headers'
        if with_cookies:
            cute_cookies = self.__beautify(self.cookies)
            wait_to_write.append(f'cookies = {cute_cookies}')
            request_parameter += ', cookies=cookies'

        wait_to_write.append(f'response = requests.get(\'{self.url}\'' + request_parameter + ')')
        with open(file, 'w') as f:
            f.write('\n'.join(wait_to_write) + '\n')

    def __format_cookies(self, text):
        cookies = text.split('; ')
        for cookie in cookies:
            try:
                k, v = cookie.split('=', 1)
                self.cookies[k] = v
            except ValueError:
                raise
                # self.__update_length(k)
        return self.cookies

    def __format_headers(self, headers):
        for header in headers:
            try:
                k, v = header.split(': ', 1)
            except ValueError:
                raise
            if k.lower() == 'cookie':
                self.__format_cookies(v)
            else:
                self.headers[k] = v
                # self.__update_length(k)
        return self.headers

    @staticmethod
    def __beautify(data):
        blank = ' ' * 11
        # print(self.__key_max_length)
        _ = str(data).replace('\', \'', f'\',\n{blank}\'')[:-1] + f'\n{blank}}}\n'
        return _
        # return re.sub("\'.+?\':", self.align, _)

        # def __update_length(self, k):
        #    if len(k) > self.__key_max_length:
        #        self.__key_max_length = len(k)

        # def align(self, x):
        #    key = x.group()
        #    pad = ' ' * (self.__key_max_length - len(key))
        #    return key.replace(':', f'{pad}:')


def __get_clipboard():
    return os.popen('pbpaste').read()


from_clipboard = __Generate(__get_clipboard())


def from_string(base_string):
    return __Generate(base_string)
