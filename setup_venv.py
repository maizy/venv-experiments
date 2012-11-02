# _*_ coding: utf-8 _*_

__doc__ = 'init or update python venv (python 3.3+)'

import venv
import os
import os.path as path
import sys
import urllib.request
import urllib.error
import subprocess
import glob


def download_file_if_not_exist(res_path, url):
    """Download file if not exist and put it to provisions_path"""
    if not path.exists(res_path):
        try:
            res = urllib.request.urlopen(url)
            output = open(res_path, 'wb')
            output.write(res.read())
            output.close()
        except (urllib.error.URLError, OSError):
            return False
    return True


class BuilderUtilsMixin(object):

    def run_in_venv(self, context, command, args=None, shell=False):
        """Run command in venv (emulate PATH=env_dir:PATH behavior)"""
        venv_command_path = path.join(context.bin_path, command)
        if path.exists(venv_command_path):
            command = venv_command_path
        call_args = [command]
        if args is not None:
            call_args.extend(args)
        try:
            return subprocess.call(call_args, shell=shell) == 0
        except (subprocess.SubprocessError, OSError):
            return False

    def install_pip_requirements(self, context, requirements_path):
        self.run_in_venv(context, 'pip', ['install', '-r', requirements_path])


class ImprovedEnvBuilder(venv.EnvBuilder, BuilderUtilsMixin):
    """Improved EnvBuilder

    Additional hooks:
     - post_upgrade(context)
    """

    def create(self, env_dir):
        """Overwrite create method (add more hooks)"""
        env_dir = path.abspath(env_dir)
        context = self.ensure_directories(env_dir)
        self.create_configuration(context)
        self.setup_python(context)
        if not self.upgrade:
            self.setup_scripts(context)
            self.post_setup(context)
        else:
            self.post_upgrade(context)

    def post_upgrade(self, context):
        pass


class EnvBuilder(ImprovedEnvBuilder):

    def __init__(self, system_site_packages=False, clear=False, symlinks=False, upgrade=False):
        super().__init__(system_site_packages, clear, symlinks, upgrade)
        self.provisions_path = path.dirname(__file__)

    def post_setup(self, context):
        self.post_upgrade(context)
        self.install_scripts(context, path.join(self.provisions_path, 'scripts'))

    def post_upgrade(self, context):
        if not path.exists(path.join(context.bin_path, 'pip')):
            if not self.install_distribute(context):
                return
            if not self.install_pip(context):
                return
        else:
            print('[*] Pip already installed, skip')
        print('[*] Install requirements')
        requirements_path = path.join(self.provisions_path, 'requirements.txt')
        self.install_pip_requirements(context, requirements_path)

    def install_distribute(self, context):
        print('[*] Installing distribute ... ', flush=True)
        res_path = path.join(self.provisions_path, 'distribute_setup.py')
        if not download_file_if_not_exist(res_path, 'http://python-distribute.org/distribute_setup.py'):
            sys.stdout.write('[!] Error: unable to download distribute install script\n')
            return False
        if not self.run_in_venv(context, context.python_exe, [res_path]):
            sys.stdout.write('[!] Error: when runnig distribute install script\n')
            return False
        return True

    def install_pip(self, context):
        print('[*] Installing pip ... ', flush=True)
        res = self.run_in_venv(context, 'easy_install', ['pip'])
        if not res:
            print('[!] Error', flush=True)
        return res



def main(args):
    if len(args) > 0:
        root_dir = args[0]
    else:
        root_dir = path.join(path.dirname(__file__), 'venv')
    root_dir = path.abspath(root_dir)
    upgrade = path.exists(path.join(root_dir, 'pyvenv.cfg'))
    if not upgrade:
        print('[*] Installing vevn on {}'.format(root_dir), flush=True)
    else:
        print('[*] Upgrating vevn on {}'.format(root_dir), flush=True)
    
    builder = EnvBuilder(upgrade=upgrade)
    builder.create(root_dir)

    print('[*] Done', flush=True)

if __name__ == '__main__':
    sys.exit( main(sys.argv[1:]) )