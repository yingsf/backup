## bakFile

[![License](https://img.shields.io/badge/License-MIT-red.svg)]()
[![OS](https://img.shields.io/badge/OS-MacOS%2C%20Linux-brightgreen.svg)]()
[![Python](https://img.shields.io/badge/Python-3.7.2-blue.svg)]()
[![version](https://img.shields.io/badge/Version-0.0.1-yellow.svg)]()

Synchronize my files to github private repository automatically. When I modify the file, immediately sync to the git repository

> 注意: 如果使用vim编辑文件的话, 因为vi缓存的机制, watchdog监控不到文件的修改. 所以需要先做如下配置:

在`~/.vimrc`文件中(如果没有就创建), 添加:

```bash
set nobackup
set noswapfile
set nowritebackup
set noundofile
```

### 使用帮助

#### 第一步:

在Github开一个私有库(私有库能保证你的文件私密性), 然后在该仓库的根目录创建`backup_config.json`文件(该文件会自动clone到本地, 然后按照该文件进行备份), 并填入如下内容(你想备份的文件):

```json
{
    "zsh配置": "/Users/yingsf/.zshrc",
    "Git配置": "/Users/yingsf/.gitconfig",
    "vim配置": "/Users/yingsf/.vimrc",
    "xxx配置": "",
    "xxx配置": "",
    "xxx配置": "",
    "xxx配置": "",
    "xxx配置": "",
    "xxx配置": "",
    "vscode用户配置": "/Users/yingsf/Library/Application Support/Code/User/settings.json",
    "pip打包配置": "/Users/yingsf/.pypirc"
}

```

#### 第二步:

从`git@github.com:yingsf/backup.git`clone程序到你喜欢的目录. 例如我放到`~/.secret`

修改`bak_to_git.py`文件的如下内容, 替换成你自己的目录和私有仓库:

```python
# 目录名(所有待备份的文件都会copy到这里, 然后上传至git)
BACKUP_TO_WHERE = '.backup_myfile'

# Git仓库地址
GIT_REPO = "git@github.com:XXXXX/backup_repo.git"
```

#### 第三步:Macos下添加到系统启动

编辑`com.yingsf.backup.plist`文件(首先就需要你重命名这个文件为自己的用户名)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC -//Apple Computer//DTD PLIST 1.0//EN http://www.apple.com/DTDs/PropertyList-1.0.dtd >
<plist version="1.0">
  <dict>
    <key>Label</key>
    <!-- 这里换一下你自己的名字 -->
    <string>com.yingsf.bakfile</string>
    <key>Program</key>
    <!-- 这里也要换 -->
    <string>/Users/yingsf/.secret/backup.sh</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>UserName</key>
    <string>yingsf</string>
    <key>StandardErrorPath</key>
    <!-- 这里也要换 -->
    <string>/Users/yingsf/.secret/bak_to_git_error.log</string>
    <key>StandardOutPath</key>
    <!-- 这里也要换 -->
    <string>/Users/yingsf/.secret/bak_to_git_output.log</string>
  </dict>
</plist>
```

然后:

  1. 将`com.yingsf.backup.plist`复制到`~/Library/LaunchAgents/`
  2. 执行`launchctl load -w ~/Library/LaunchAgents/com.yingsf.backup.plist`
  3. 取消执行`launchctl unload -w ~/Library/LaunchAgents/com.yingsf.backup.plist`
  4. 查看是否允许`launchctl list | grep com.yingsf.backup`
