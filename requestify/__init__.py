# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys
from urllib import parse


def get_data_dict(query):
    return dict(parse.parse_qsl(query))


class __Generate(object):
    def __init__(self, base_string):
        self.base_string = base_string.strip()
        self.url = ''
        self.method = 'get'
        self.headers = {}
        self.cookies = {}
        self.querys = {}
        self.data = None
        self.__post_handler = {
            '-d': lambda x: get_data_dict(x),
            '--data': lambda x: get_data_dict(x),
            '--data-ascii': lambda x: get_data_dict(x),
            '--data-binary': lambda x: bytes(x, encoding='utf-8'),
            '--data-raw': lambda x: get_data_dict(x),
            '--data-urlencode': lambda x: parse.quote(x)
        }
        self.__opt_list = []
        self.__generate()
        # self.__key_max_length = 0

    def to_file(self, filename, with_headers=True, with_cookies=True):
        self.__write_to_file(filename, with_headers=with_headers, with_cookies=with_cookies)

    def to_current_file(self, with_headers=True, with_cookies=True):
        current_filename = sys.argv[0].split('/')[-1]
        self.__write_to_file(current_filename, with_headers=with_headers, with_cookies=with_cookies)

    def __generate(self):

        meta = self.base_string.split(' ', 2)
        assert len(meta) == 3, 'Not validate curl data'

        profix, url, opts_string = meta
        self.url = url[1:-1]

        opts = re.findall(' (-{1,2}\S+) ?\$?\'([\S\s]+?)\'', opts_string)

        self.__set_opts(opts)

    def __set_opts(self, opts):

        headers = []
        for k, v in opts:
            if k == '-H':
                headers.append(v)
            elif k in self.__post_handler:
                self.method = 'post'
                self.data = self.__post_handler[k](v)

        self.__format_headers(headers)

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
                print(f'invalid data: {header}')
                pass
                # raise

            if k.lower() == 'cookie':
                self.__format_cookies(v)
            else:
                self.headers[k] = v
                # self.__update_length(k)
        return self.headers

    def __write_to_file(self, file, with_headers=True, with_cookies=True):
        request_options = ''
        wait_to_write = ['import requests', '\n']

        if with_headers:
            cute_headers = self.__beautify(self.headers)
            wait_to_write.append(f'headers = {cute_headers}')
            request_options += ', headers=headers'

        if with_cookies:
            cute_cookies = self.__beautify(self.cookies)
            wait_to_write.append(f'cookies = {cute_cookies}')
            request_options += ', cookies=cookies'

        if self.method == 'post':
            if type(self.data) == dict:
                cute_data = self.__beautify(self.data, space=8)
            else:
                cute_data = self.data
            wait_to_write.append(f'data = {cute_data}\n')
            request_options += ', data=data'

        wait_to_write.append(f'response = requests.{self.method}(\'{self.url}\'' + request_options + ')')
        wait_to_write.append('print(response.text)')
        with open(file, 'w') as f:
            f.write('\n'.join(wait_to_write) + '\n')

    @staticmethod
    def __beautify(data, space=11):
        blank = ' ' * space
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
    platform = sys.platform
    if platform == 'darwin':
        return os.popen('pbpaste').read()
    elif platform == 'win32' or platform == 'cygwin':
        try:
            import tkinter
            tk = tkinter.Tk()
            return tk.clipboard_get()
        except:
            raise IOError('Unable to read clipboard text')


from_clipboard = __Generate(__get_clipboard())


def from_string(base_string):
    return __Generate(base_string)


if __name__ == '__main__':
    test_string = '''
curl 'https://www.google.com/' -H 'authority: www.google.com' -H 'pragma: no-cache' -H 'cache-control: no-cache' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'x-client-data: CI62yQEIprbJAQjEtskBCKmdygEI153KAQioo8oB' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7' --compressed
    '''
    a = from_clipboard.to_file('1.py')

    # print(a.headers)
