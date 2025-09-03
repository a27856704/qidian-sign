#!/bin/sh
# 确保脚本在遇到错误时终止
set -e
sleep 2

# 执行命令
echo "开始执行起点自动签到..."
nohup python -m pip install --upgrade pip && pip install --index-url=https://mirrors.aliyun.com/pypi/simple -r qidian/requirements.txt && python qidian/qidianAutoSign.py --env=prod > /proc/1/fd/1 2> /proc/1/fd/2
echo "起点自动签到启动成功..."

#command3

# 执行主命令（如果有的话）
exec "$@"

