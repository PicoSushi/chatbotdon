#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
import re
from getpass import getpass
from os.path import exists
from mastodon import Mastodon

CLIENT_SECRET_FILE_NAME = 'client.dat'
USER_SECRET_FILE_NAME = 'user.dat'
CONFIG_FILE_NAME = 'config.json'


def get_credential(**config):
    api_base_url = config.get('instance_url')
    if not api_base_url:
        raise Exception('Correctly specify instance_url on {}.'.format(CONFIG_FILE_NAME))
    if not exists(CLIENT_SECRET_FILE_NAME):
        Mastodon.create_app(
            client_name=config.get('app_name') or 'chatbotdon',
            website=config.get('website') or 'https://github.com/kakakaya/chatbotdon',
            to_file=CLIENT_SECRET_FILE_NAME,
            api_base_url=api_base_url,
        )

    access_token = None
    if exists(USER_SECRET_FILE_NAME):
        access_token = USER_SECRET_FILE_NAME
    m = Mastodon(client_id=CLIENT_SECRET_FILE_NAME, access_token=access_token, api_base_url=api_base_url)
    if not access_token:
        m.log_in(
            username=config.get('username'),
            password=config.get('password'),
            to_file=USER_SECRET_FILE_NAME,
        )
    return m


def main():
    with open(CONFIG_FILE_NAME) as f:
        config = json.load(f)
    if not exists(USER_SECRET_FILE_NAME):
        # need to ask username/password
        print('Please enter Username and Password for {}.'.format(config.get('instance_url')))
        config['username'] = input('Username:')
        config['password'] = getpass()
    mstdn = get_credential(**config)
    html_pattern = re.compile('<.*?>')
    for toot in mstdn.timeline('local'):
        print(
            '[{} {}] {}'.format(
                toot['account']['username'], toot['account']['display_name'],
                re.sub(html_pattern, '', toot['content']).strip()
            )
        )


if __name__ == '__main__':
    main()
