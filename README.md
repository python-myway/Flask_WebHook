## Flask WebHook
    
### 主要功能：
- 目前仅支持coding的webhook
- 可为多个分支设置处理逻辑
- 可自定义处理逻辑

### 环境要求：
- Python 3.3+

### 使用说明：
```
0. 下载安装：
pip install flask_webhook

1. 在项目的配置文件中，添加WEBHOOK相关配置，配置示例如下：
WEBHOOK = {
    'refs/heads/master': {
        # 配置coding的webhook的token
        'token': 'E96B8A88AC1A4E0CD5E626F862497F58',
        # 项目目录的全路径
        'file': '/home/data/projects/program',
        # 需要执行的命令
        'command': 'git pull origin master && sudo nginx -s reload',
        # 设置触发hook的活动，默认为push
        'event': [’push‘],
        }
    }
注意：'refs/heads/master'，一定要传全称，目前代码不支持编辑

2. 实例化WebHook，有两种方法：
法一：
    webhook = WebHook(app)
法二：
    webhook = WebHook()
    webhook.init_app(app)

3. 如果只是单纯的拉取代码，重启服务，已有的webhook方法已经足够，
    访问地址：{host}/webhook/

4. 也可以根据需求写自己的hook处理，继承这个类，添加以webhook开头的方法，如：
def webhook_dev(self, request):
    pass

```
