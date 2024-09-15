#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/13 17:58
# @Author  : 冉勇
# @Site    : 
# @File    : bot_util.py
# @Software: PyCharm
# @desc    : 机器人推送工具
import requests
import json
import base64
import hashlib
from enum import Enum


class MediaType(Enum):
    image = 'image'
    voice = 'voice'
    video = 'video'
    file = 'file'


class WxNotify:
    def __init__(self, corpid, corpsecret, agentid):

        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid
        self.access_token = self.__get_access_token(corpid, corpsecret)

    # 获取 access_token
    def __get_access_token(self, corpid, corpsecret):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        params = {
            'corpid': corpid,
            'corpsecret': corpsecret
        }
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        resp_json = resp.json()
        if 'access_token' in resp_json.keys():
            return resp_json['access_token']
        else:
            raise Exception('Please check if corpid and corpsecret are correct \n' + resp.text)

    # 上传临时素材
    def upload_media(self, file_path, media_type):
        url = ('https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={}&type={}'
               .format(self.access_token, media_type.value))

        files = {'file': open(file_path, 'rb')}
        result = requests.post(url, files=files)
        response = json.loads(result.text)
        return response['media_id']

    # https://developer.work.weixin.qq.com/document/path/90236
    # 发送文本消息
    def send_msg(self, text):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.access_token
        payload = {
            "touser": "@all",
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": text
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        resp = requests.post(url, data=json.dumps(payload))
        resp.raise_for_status()
        return resp.json()

    # 发送 Markdown 文本消息
    def send_msg_markdown(self, text):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.access_token
        payload = {
            "touser": "@all",
            "msgtype": "markdown",
            "agentid": self.agentid,
            "markdown": {
                "content": text
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        resp = requests.post(url, data=json.dumps(payload))
        resp.raise_for_status()
        return resp.json()

    # 发送图片消息
    def send_img(self, img_path):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.access_token
        payload = {
            "touser": "@all",
            "msgtype": "image",
            "agentid": self.agentid,
            "image": {
                "media_id": self.upload_media(img_path, MediaType.image)
            },
            "safe": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        resp = requests.post(url, data=json.dumps(payload))
        resp.raise_for_status()
        return resp.json()

    # 发送文件消息
    def send_file(self, file_path):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.access_token
        payload = {
            "touser": "@all",
            "msgtype": "file",
            "agentid": self.agentid,
            "file": {
                "media_id": self.upload_media(file_path, MediaType.file)
            },
            "safe": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        resp = requests.post(url, data=json.dumps(payload))
        resp.raise_for_status()
        return resp.json()

    # 发送文本卡片
    def send_text_card(self, title, description, link):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.access_token
        payload = {
            "touser": "@all",
            "msgtype": "textcard",
            "agentid": self.agentid,
            "textcard": {
                "title": title,
                "description": description,
                "url": link,
                "btntxt": "详情"
            },
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        resp = requests.post(url, data=json.dumps(payload))
        resp.raise_for_status()
        return resp.json()

    # 发送多项选择型-模板卡片
    def send_template_card_multiple_interaction(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.access_token
        payload = {
            "touser": "@all",
            "msgtype": "template_card",
            "agentid": self.agentid,
            "template_card": {
                "card_type": "multiple_interaction",
                "source": {
                    "icon_url": "https://wework.qpic.cn/wwpic3az/912274_J4eaf9eWSM-1Ip8_1714132855/",
                    "desc": "企业微信"
                },
                "main_title": {
                    "title": "欢迎使用企业微信",
                    "desc": "您的好友正在邀请您加入企业微信"
                },
                "task_id": "task_id",
                "select_list": [
                    {
                        "question_key": "question_key1",
                        "title": "选择器标签1",
                        "selected_id": "selection_id1",
                        "option_list": [
                            {
                                "id": "selection_id1",
                                "text": "选择器选项1"
                            },
                            {
                                "id": "selection_id2",
                                "text": "选择器选项2"
                            }
                        ]
                    }],
                "submit_button": {
                    "text": "提交",
                    "key": "key"
                }
            },
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        resp = requests.post(url, data=json.dumps(payload))
        resp.raise_for_status()
        return resp.json()


class WxWebhookNotify:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_msg(self, msg):
        url = self.webhook_url
        playload = {
            "msgtype": "text",
            "text": {
                "content": msg,
                # "mentioned_list": ["@all"],
                # "mentioned_mobile_list":["@all"]
            }
        }

        res = requests.post(url, data=json.dumps(playload))
        return res.json()

    def send_msg_markdown(self, msg):
        url = self.webhook_url
        playload = {
            "msgtype": "markdown",
            "markdown": {
                "content": msg,
                # "mentioned_list":["@all"],
                # "mentioned_mobile_list":["@all"]
            }
        }

        res = requests.post(url, data=json.dumps(playload))
        return res.json()

    def send_img(self, img_path):
        url = self.webhook_url
        img_base64, img_md5 = self.get_img_info(img_path)
        playload = {
            "msgtype": "image",
            "image": {
                "base64": img_base64,
                "md5": img_md5
            }
        }

        res = requests.post(url, data=json.dumps(playload))
        return res.json()

    def send_file(self, file_path):
        url = self.webhook_url
        playload = {
            "msgtype": "file",
            "file": {
                "media_id": self.upload_media(file_path)
            }
        }

        res = requests.post(url, data=json.dumps(playload))
        return res.json()

    def upload_media(self, file_path):
        key = self.webhook_url.split("key=")[1]
        url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type=file"

        files = {'file': open(file_path, 'rb')}
        result = requests.post(url, files=files)
        response = json.loads(result.text)
        return response['media_id']

    def get_img_info(self, img_path):
        with open(img_path, 'rb') as f:
            img = f.read()
            md5 = hashlib.md5(img).hexdigest()
            img_base64 = base64.b64encode(img).decode('utf-8')
        return img_base64, md5


if __name__ == '__main__':
    # # 企业ID
    # CORPID = 'wwe66d60c4b816adbe'
    # # 应用Secret
    # CORPSECRET = 'rX9siOAhflNBVI776PYgcdZEZoh5S_tPiBZPK_zu66I'
    # # 应用ID
    # AgentId = '1000002'
    #
    # wn = WxNotify(corpid=CORPID, corpsecret=CORPSECRET, agentid=AgentId)
    # wn.send_text_card(title="测试", description="描述", link="https://www.baidu.com")
    # wn.send_msg("test message")

    WEB_HOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=55e6d5bc-61fc-4d26-9615-01ab51c82801"
    wn_webhook = WxWebhookNotify(WEB_HOOK)
    # wn_webhook.send_msg("Hello")
    wn_webhook.send_msg_markdown(
        """
    **${name}**
项目：${project_name}
时间：${start_time} ～ ${end_date}
共测试：${run_count}次
通过数：${run_success_count}
异常数：${run_err_count}
失败数：${run_fail_count}
测试通过率：${rate}%
详细统计：[点击查看](${url})
        """
    )
