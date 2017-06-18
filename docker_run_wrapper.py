#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
docker run wrapper.
'''

import os
import subprocess
import sys


DEFAULT_CONFIG_FILEPATH = '~/.config/drw/config.toml'
VOLUME_NAME = '/drw/'


def config_filepath():
    '''
    設定ファイルパスの取得
    '''
    filepath = os.path.expanduser(DEFAULT_CONFIG_FILEPATH)
    if 'DRW_CONFIG_FILEPATH' in os.environ:
        filepath = os.environ['DRW_CONFIG_FILEPATH']

    if not os.path.isfile(filepath):
        raise ValueError('not found.')

    return filepath


def parse(line):
    '''
    toml ファイルのパース
    '''
    return [column.strip().strip('\"') for column in line.split('=')]


def correct_format(lines):
    '''
    設定ファイルの型式確認
    '''
    return len([x for x in lines if x != ""]) >= 2


def load_config():
    '''
    設定の読み込み
    '''
    with open(config_filepath(), 'r') as f:
        return {
            parse(i)[0]: parse(i)[1]
            for i in f if correct_format(parse(i))
        }


def exists_docker():
    '''
    docker コマンドの存在確認
    '''
    try:
        subprocess.check_call('/usr/bin/which docker > /dev/null', shell=True)
        return True
    except subprocess.CalledProcessError:
        return False


def construct_command(image, command_name, params):
    '''
    docker command の構築
    '''
    template = 'docker run --rm -it -w {} -v $(pwd):{} {} {} {}'
    return template.format(
        VOLUME_NAME,
        VOLUME_NAME,
        image,
        command_name,
        ' '.join(params))


def run_command(command_string):
    '''
    コマンドの実行
    '''
    subprocess.call(command_string, shell=True)


def edit_config():
    '''
    設定ファイルの編集
    '''
    subprocess.call("vim {}".format(DEFAULT_CONFIG_FILEPATH), shell=True)


def main(input_params):
    '''
    docker run wrapper.
    '''
    if not exists_docker():
        raise SystemException('Please install the Docker for Mac')

    command_name = input_params[0]
    params = input_params[1:]

    if command_name == "config":
        edit_config()
        return 0

    config = load_config()
    if command_name not in config:
        raise ValueError('unknown command.')

    command = construct_command(config[command_name], command_name, params)
    run_command(command)
    return 0


if __name__ == '__main__':
    argv = sys.argv
    if (len(argv) < 2):
        print('Usage:\n\t{} command [option..]'.format(argv[0]))
        sys.exit(1)

    try:
        sys.exit(main(argv[1:]))
    except ValueError, e:
        print(e.args[0])
        sys.exit(1)
