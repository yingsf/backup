# -*- coding: utf-8 -*-

import json
import os
import re
import time
from subprocess import call
from shutil import copy
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# 用户根目录
USER_HOME = os.path.expandvars('$HOME')

# 目录名(所有待备份的文件都会copy到这里, 然后上传至git)
BACKUP_TO_WHERE = '.backup_myfile'

# Git仓库地址
GIT_REPO = "git@github.com:yingsf/backup_repo.git"

# Git仓库名
REPO_NAME = ''.join(re.findall(r'/(\w+)*', GIT_REPO))

# 将USER_HOME, BACKUP_TO_WHERE, REPO_NAME组合成完整路径
PARENT_FOLDER = os.path.join(USER_HOME, BACKUP_TO_WHERE)
TO_GIT_FOLDER = os.path.join(PARENT_FOLDER, REPO_NAME)


def create_git_folder():
    """ 如果本地没有git备份的目录, 则创建, 同时clone仓库到该目录 """
    if not os.path.isdir(TO_GIT_FOLDER):
        os.makedirs(PARENT_FOLDER, exist_ok=True)
        os.chdir(PARENT_FOLDER)
        git_clone_cmd = "git clone " + GIT_REPO
        call(git_clone_cmd, shell=True)


create_git_folder()


def read_bak_list():
    """ 读取待备份的文件清单 """
    os.chdir(TO_GIT_FOLDER)
    result = []
    with open("backup_config.json", 'r', encoding='utf-8') as f:
        content = json.load(f)
        for k, v in content.items():
            result.append(v)
    return result


# 待备份的文件
BACKUP_LIST = read_bak_list()


class FileChangeHandler(FileSystemEventHandler):
    """ 复制到git目录下提交 """

    def on_modified(self, event):
        src = event.src_path
        if src in BACKUP_LIST:
            copy(src, TO_GIT_FOLDER)
            os.chdir(TO_GIT_FOLDER)
            git_add_cmd = "git add -A"
            git_commit_cmd = f'git commit -m "Modify {os.path.basename(src)}"'
            git_push_cmd = "git push"
            call(
                git_add_cmd + "&&" +
                git_commit_cmd + "&&" +
                git_push_cmd,
                shell=True
            )


if __name__ == "__main__":
    observer = Observer()
    event_handler = FileChangeHandler()

    for file_path in BACKUP_LIST:
        copy(file_path, TO_GIT_FOLDER)
        observer.schedule(event_handler, path=os.path.dirname(os.path.realpath(file_path)), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
