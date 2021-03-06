#!/usr/bin/env python
import os

import sh

from .utils import normalize_filename

git = sh.git.bake('--no-pager', _cwd="pages")


def report_changes(conf, content):
    return PageHistory(conf).report_changes(content)


class PageHistory(object):
    STORAGE_DIR = "pages"

    def __init__(self, conf):
        self.cwd = os.path.join(
            self.STORAGE_DIR,
            normalize_filename(conf['name']),
        )
        self.target = os.path.join(self.cwd, "content")
        self.git = sh.git.bake(
            '--no-pager',
            _cwd=self.cwd,
        )
        self.ensure_repo_exists()

    def report_changes(self, content):
        self.write(content)
        if self.commit():
            return self.last_log()

    def write(self, content):
        with open(self.target, 'w') as fp:
            fp.write(content)

    def commit(self):
        self.git('add', '-A', '.')
        try:
            self.git.commit('-m', 'Web watch')
            return True
        except sh.ErrorReturnCode_1:
            return False

    def last_log(self):
        return self.git.log('-1', '-p', '--no-color').stdout

    def ensure_repo_exists(self):
        if not os.path.isdir(self.cwd):
            os.makedirs(self.cwd)
        if not os.path.isdir(os.path.join(self.cwd, ".git")):
            self.git.init()
