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


def is_shell_mode(params):
    '''
    shell 利用判定
    '''
    return params.find(" ") > 0


def create_command_fragment(input_params, config):
    '''
    docker コマンドのためのパラメータ作成
    '''
    head = input_params[0]
    tail = input_params[1:]

    shell_mode = is_shell_mode(head)

    command_name = "/bin/sh" if shell_mode else head
    params = "-c '" + head + "'" if shell_mode else ' '.join(tail)

    image_key = head.split(" ")[0] if shell_mode else command_name
    if image_key not in config:
        raise ValueError('unknown command.')

    image_name = config[image_key]

    return (image_name, command_name, params)


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
        params)


def run_command(command_string):
    '''
    コマンドの実行
    '''
    subprocess.call(command_string, shell=True)


def edit_config():
    '''
    設定ファイルの編集
    '''
    run_command("vim {}".format(DEFAULT_CONFIG_FILEPATH))


def main(input_params, simulate=False):
    '''
    docker run wrapper.
    '''
    if not exists_docker():
        raise SystemException('Please install the Docker for Mac')

    image_name, command_name, params = \
        create_command_fragment(input_params, load_config())

    if command_name == "config":
        edit_config()
        return 0

    command = construct_command(image_name, command_name, params)
    if simulate:
        print(command)
        return 0

    run_command(command)
    return 0


def usage():
    print('''
NAME:
   drw - docker run wrapper

USAGE:
   drw [global options] command

   or

   drw [global options] 'commands'

COMMANDS:
   config                       configure
   help                         show help
   ANY_COMMAND                  run command

GLOBAL OPTIONS:
   --dry-run, --simulate, -s    dry run option
   --help, -h                   show help
''')


if __name__ == '__main__':
    argv = sys.argv
    if len(argv) < 2:
        usage()
        sys.exit(1)

    if argv[1] in ["-h", "--help", "help"]:
        usage()
        sys.exit(1)

    simulate = False
    if argv[1] in ["-s", "--simulate", "--dry-run"]:
        simulate = True
        argv.pop(0)
        if len(argv) == 1:
            usage()
            sys.exit(1)

    try:
        sys.exit(main(argv[1:], simulate))
    except ValueError, e:
        print(e.args[0])
        sys.exit(1)
