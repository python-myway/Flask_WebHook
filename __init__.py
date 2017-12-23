""" Flask WebHook """

import os
import subprocess

from flask import jsonify


class WebHook:

    def __init__(self, app=None):
        self.app = app
        self.webhook = {}
        self.prefix = []
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # 检查是否配置了WebHook&WEBHOOK是否是字典
        try:
            self.app = app
            self.webhook.update(app.config['WEBHOOK'])
        except (KeyError, TypeError):
            raise Exception('未配置WEBHOOK')
        for key, value in app.config['WEBHOOK'].items():
            self.prefix.append(key)
            try:
                event = list(value['event'])
            except KeyError:
                event = ['push']
            value['event'] = event
        self.add_url()

    def add_url(self):
        # 将所有的webhook方法添加到flask的路由里
        for key, value in WebHook.__dict__:
            if key.startswith('webhook'):
                self.app.add_url_rule(rule='/{}/'.format(key), endpoint=key,
                                      view_func=value, methods=['POST'])

    def webhook(self, request):
        try:
            token = request.json['token']
            event = request.headers['X-Coding-Event']
            branch = request.json['ref']
        except KeyError:
            return jsonify({'status': 'error', 'message': '请求格式错误'})

        try:
            branchs = self.webhook[branch]
        except KeyError:
            return jsonify({'status': 'error', 'message': '请求分支错误'})

        if token == branchs.get('token') and event in branchs['event']:
            # 切换到项目目录执行命令
            os.chdir(branchs.get('file'))
            command = branchs['command']
            try:
                subprocess.check_call(command, shell=True)
            except subprocess.CalledProcessError:
                return jsonify({'status': 'error', 'message': '命令：{}执行错误'.format(command)})
            return jsonify({'status': 'success', 'message': '请求成功'})
        else:
            return jsonify({'status': 'error', 'message': '请求失败'})
