# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018/11/28 20:55
# @Author  : 逗比
# @Project : music
# @File    : download_music.py
# @Software: PyCharm

import json
import requests
from urllib.request import unquote
from urllib.request import urlretrieve


def music_info(keyword):
    # 生成json的url
    url = f"https://c.y.qq.com/soso/fcgi-bin/client_search_cp?&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w={unquote(keyword)}"
    # 请求url
    response = requests.get(url)
    # 获取所有歌曲数据
    json_info = json.loads(response.text.strip("callback()[]"))["data"]["song"]["list"]

    # 存储所有歌曲的信息
    mid = []
    song_mid = []
    src = []
    song_names = []
    singers = []

    for each in json_info:
        try:
            mid.append(each["media_mid"])
            song_mid.append(each["songmid"])
            song_names.append(each["songname"])
            singers.append(each["singer"][0]["name"])
        except KeyError:
            pass

    for n in range(0, len(mid)):
        res2 = requests.get(

            f'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?&jsonpCallback=MusicJsonCallback&cid=205361747&songmid={song_mid[n]}&filename=C400{mid[n]}.m4a&guid=6612300644')
        jm2 = json.loads(res2.text)
        key = jm2['data']['items'][0]['vkey']
        song_src = f'http://dl.stream.qqmusic.qq.com/C400{mid[n]}.m4a?vkey={key}&guid=6612300644&uin=0&fromtag=66'
        src.append(song_src)

    print("**************************开始下载**************************")

    length = len(src)
    for m in range(0, length):
        print(f"{song_names[m]} - {singers[m]}.mp3  正在下载...")
        try:
            urlretrieve(src[m], f"music/{song_names[m]} - {singers[m]}.mp3")
        except:
            length -= 1
            print(f"{song_names[m]} - {singers[m]}.mp3  😔下载失败咯!\n")
        else:
            print(f"{song_names[m]} - {singers[m]}.mp3  (^_^)biu 下载成功...\n")

    print(f"[{keyword}] 下载完成 {length}首 !")
    print("**************************下载结束**************************")


music_info(input("请输入歌曲名称:   "))



