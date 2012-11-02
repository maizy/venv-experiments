#!__VENV_PYTHON__
# _*_ coding: utf-8 _*_
import sys
import test_venv

if __name__ == '__main__':
    print('VENV_NAME', '__VENV_NAME__')
    print('VENV_DIR', '__VENV_DIR__')
    print('VENV_BIN_NAME', '__VENV_BIN_NAME__')
    print('VENV_PYTHON', '__VENV_PYTHON__')
    sys.exit(test_venv.main(sys.argv))