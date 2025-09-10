import sys
import os
import logging
from datetime import datetime
import json
from configparser import ConfigParser
from itertools import cycle
import werkzeug.serving
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, session

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ProxyCat import run_server
from modules.modules import load_config, check_proxies, get_message, load_ip_list
from modules.proxyserver import AsyncProxyServer
import asyncio
import threading
import time

app = Flask(__name__, 
           template_folder='web/templates',
           static_folder='web/static') 

werkzeug.serving.WSGIRequestHandler.log = lambda self, type, message, *args: None
logging.getLogger('werkzeug').setLevel(logging.ERROR)

config = load_config('config/config.ini')
server = AsyncProxyServer(config)

def get_config_path(filename):
    return os.path.join('config', filename)

log_file = 'logs/proxycat.log'
os.makedirs('logs', exist_ok=True)
log_messages = []
max_log_messages = 10000

class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        return datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')

def setup_logging():
    file_formatter = CustomFormatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    console_formatter = CustomFormatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    # 实际代码会继续执行剩余部分