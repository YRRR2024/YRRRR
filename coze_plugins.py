# encoding:utf-8

import requests
import plugins
from bridge.reply import Reply, ReplyType
from common.log import logger

@plugins.register(
    name="RenderHtmlAsImage",
    desire_priority=66,
    hidden=False,
    desc="将网页代码渲染成图片并上传到 SM.MS 图床。",
    version="1.0",
    author="YRRR",
)
class RenderHtmlAsImage(Plugin):
    def __init__(self):
        super().__init__()
        try:
            self.handlers[Event.ON_DECORATE_REPLY] = self.on_decorate_reply
            logger.info("[RenderHtmlAsImage] inited.")
        except Exception as e:
            logger.warn("[RenderHtmlAsImage] init failed, ignore.")
            raise e

    def on_decorate_reply(self, e_context: EventContext):
        html_code = e_context["reply"].content.strip()  # 假设回复内容是 HTML 代码
        image_path = self.render_html_to_image(html_code)  # 自定义方法，将 HTML 渲染为图片

        if image_path:
            image_url = self.upload_image(image_path)
            if image_url:
                e_context["reply"] = Reply(ReplyType.TEXT, image_url)  # 返回图片链接
            else:
                e_context["reply"] = Reply(ReplyType.TEXT, "上传图片失败。")
        else:
            e_context["reply"] = Reply(ReplyType.TEXT, "渲染图片失败。")

    def render_html_to_image(self, html_code):
        # 实现 HTML 渲染为图片的逻辑
        # 返回生成的图片路径
        pass

    def upload_image(self, image_path):
        url = 'https://sm.ms/api/v2/upload'
        with open(image_path, 'rb') as image_file:
            files = {'smfile': image_file}
            response = requests.post(url, files=files)
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    return data['data']['url']  # 返回图片链接
                else:
                    logger.warn(f"[RenderHtmlAsImage] upload_image failed, error={data['message']}")
                    return None
            else:
                logger.warn(f"[RenderHtmlAsImage] upload_image failed, status_code={response.status_code}, response={response.text}")
                return None

    def get_help_text(self, **kwargs):
        return "将网页代码渲染成图片并上传到 SM.MS 图床，返回图片链接。"