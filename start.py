#!/usr/bin/env python
#Author: PlanC
#Date: 2023-02-03 19:28:42
#LastEditTime: 2023-02-04 11:37:44
#FilePath: \dockbot\start.py
#

import botpy
import os
import re
import smms
import yaml

from botpy.message import Message
from dockertool import create_docker, remove_docker, stop_docker, start_docker, run_command
from PIL import Image, ImageDraw, ImageFont

class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        await self.api.post_message(channel_id=message.channel_id, content="已加入任务计划，请稍候...", msg_id=message.id)
        if "/创建" in message.content:
            create_docker(message.author.id)
            await self.api.post_message(channel_id=message.channel_id, content="已创建" + message.author.id, msg_id=message.id)
        elif "/删除" in message.content:
            docker_id = re.sub(r" +", r" ", message.content.strip()).split(" ")[2][2:-1]
            remove_docker(docker_id)
            await self.api.post_message(channel_id=message.channel_id, content="已删除" + message.author.id, msg_id=message.id)
        elif "/停止" in message.content:
            stop_docker(message.author.id)
            await self.api.post_message(channel_id=message.channel_id, content="已停止" + docker_id, msg_id=message.id)
        elif "/启动" in message.content:
            start_docker(message.author.id)
            await self.api.post_message(channel_id=message.channel_id, content="已启动" + message.author.id, msg_id=message.id)
        else:
            command = re.sub(r" +", r" ", message.content.strip()).split(" ")[1:]
            code, result = run_command(message.author.id, command)
            results = ""
            for each in result:
                results = results + each.decode()
            if results != "":
                image = Image.new("RGB", (960, 1920), (0, 0, 0))
                draw = ImageDraw.Draw(image)
                font = ImageFont.truetype(os.path.join("fonts", "CascadiaCode.ttf"), 20)
                draw.text((0, 0), results, font=font, fill="#ffffff")
                image.save(r"output/stdout.png")

                url = smms.SMMS().upload(r"output/stdout.png")
                print(url)
                await self.api.post_message(channel_id=message.channel_id, image=url, msg_id=message.id)
            else:
                await self.api.post_message(channel_id=message.channel_id, content="命令已成功执行但无输出", msg_id=message.id)

with open(r"config.yaml") as f:
    config = yaml.safe_load(f)

intents = botpy.Intents(public_guild_messages=True)
client = MyClient(intents=intents)
client.run(appid=config['qqbot']['appid'], token=config['qqbot']['token'])
