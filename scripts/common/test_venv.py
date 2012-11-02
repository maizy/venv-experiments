# _*_ coding: utf-8 _*_

__copyright__ = 'Copyright 2012 maizy.ru'
__author__ = 'Nikita Kovaliov <nikita@maizy.ru>'

import sys

def main(argv):
    for p in ('base_exec_prefix', 'exec_prefix', 'base_prefix', 'prefix', 'executable'):
        print('{} => {}'.format(p, getattr(sys, p)))

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))