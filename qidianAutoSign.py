# -*- coding: utf-8 -*-
import argparse
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from logging.handlers import TimedRotatingFileHandler

import schedule
import yaml

from driverTools.LinkAppium import LinkAppium
from mail.mail import Mail

# 解析命令行参数
parser = argparse.ArgumentParser(description='Run the script in test or production mode.')
parser.add_argument('--env', choices=['test', 'prod'], required=True, help='Specify the environment (test or prod)')
args = parser.parse_args()
# 读取配置文件


# 选择环境（测试环境或正式环境）
if args.env == 'test':
    environment = 'test'
    with open('qidian_config.yml', 'r', encoding='utf-8') as config_file:
        config = yaml.safe_load(config_file)
else:
    environment = 'prod'
    with open('./qidian/qidian_config.yml', 'r', encoding='utf-8') as config_file:
        config = yaml.safe_load(config_file)

# 读取配置
env_config = config[environment]

keys_to_delete = [key for key, value in env_config.items() if value is None]
for key in keys_to_delete:
    del env_config[key]

# 获取人名对应的邮箱
DICT_MAIL_TO_USERS = env_config.get('DICT_MAIL_TO_USERS', {})

# 获取是否为调试模式
DEBUG_MODE = env_config['DEBUG']

# 从配置中读取其他设置
thread_delay = env_config['THREAD_DELAY']

# 获取提示信息
TIP_MSG = env_config.get('TIP_MSG', {})

if DEBUG_MODE:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    log = logging.getLogger()
else:
    # 创建日志记录器
    log = logging.getLogger('my_logger')
    log.setLevel(logging.INFO)

    # 创建TimedRotatingFileHandler并设置时间间隔为一天
    log_file = 'qidian-console.log'
    handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=2)
    handler.suffix = '%Y%m%d'  # 添加日期后缀，如 app.log.20230730
    log.addHandler(handler)

    # 设置日志格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

# 邮件发送相关配置
MAIL_FROM_USER = '你的邮箱服务器账号@qq.com'
MAIL_FROM_PASSWORD = '你的邮箱服务器授权码'
MAIL_SMTP_SERVER = 'smtp.qq.com'
MAIL_SMTP_PORT = 465
MAIL_TO_USERS = ['收件人邮箱']


# 自定义异常类
class ErrorException(Exception):
    def __init__(self, message_str):
        self.message = message_str

    def __str__(self):
        return f"ErrorException: {self.message}"


# 消息推送类
class Message(object):
    """消息推送类"""

    def __init__(self):
        self.mail = Mail(MAIL_FROM_USER, MAIL_FROM_PASSWORD, MAIL_SMTP_SERVER, MAIL_SMTP_PORT)

    def send(self, names=None):
        """
        发送邮件给指定用户
        :param msg: 邮件内容
        :param names: 用户名列表
        """
        if names is None:
            names = DICT_MAIL_TO_USERS.keys()
        for name in names:
            email = DICT_MAIL_TO_USERS.get(name)
            msg = TIP_MSG.get(name) or linkAppium.auto_sign()
            if email:
                self.mail.send_html(email, '签到结果', msg)


# 数据处理类
class Qidian():
    def process_current(self):
        """处理当前任务"""
        try:
            names = DICT_MAIL_TO_USERS.keys()
            message.send(names)
        except Exception as e:
            log.error(e)
            message.send(str(e))


def run_task():
    # 初始化 oaTip 实例
    ntes = Qidian()
    # 使用线程池执行处理当前任务
    with ThreadPoolExecutor() as executor:
        executor.submit(ntes.process_current)
    next_run_time = schedule.next_run()

    log.info("当前线程已结束，下次任务执行时间：{}".format(next_run_time))


def run_process():
    # 初始化 oaTip 实例
    ntes = Qidian()
    # 直接处理当前任务
    ntes.process_current()


if __name__ == '__main__':
    try:
        log.info('开始执行')
        # 实例化消息推送类
        message = Message()
        linkAppium = LinkAppium()

        if DEBUG_MODE:
            # 测试模式下，立即执行任务一次
            run_process()
        else:
            # 非测试模式下，根据计划执行任务
            schedule.every().day.at("12:00").do(run_task)
            schedule.every().day.at("01:00").do(run_task)
            # 主循环
            while True:
                schedule.run_pending()
                # 更新下次执行时间
                schedule.next_run()
                time.sleep(1)

    except Exception as e:
        log.error(e)
    finally:
        if not DEBUG_MODE:
            log.info('结束执行')
