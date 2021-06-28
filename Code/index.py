# -*- coding: utf-8 -*-

# ===== Import ===== #
import cooldown, discord
import os
import requests
import warnings
import asyncio
from datetime import datetime
from random import choice
from asyncio import TimeoutError
from pymongo import MongoClient
from bs4 import BeautifulSoup
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
from discordTogether import DiscordTogether
import re


# https://github.com/cheocho/Cooldown
# 노랑 : 0xf0d000
# 빨강 : 0xbd0a0a
# 초록 : 0x05b102
# 파랑 : 0x0999e1


# ===== 변수 선언 ===== #
client = discord.Client()
cooldown = cooldown.CooldownClient()
token = "Your token!"
prefix = "@"

# ===== DB ===== #
conn = MongoClient('mongodb://localhost:27017/')
user = conn.user
user_users = user.users
jusik = conn.jusik
jusik_jusiks = jusik.jusiks
togetherControl = DiscordTogether(client)

# ===== on_ready 처음 실행될 때 ===== #
@client.event
async def on_ready():
    print("[Online] 로그인")
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="@도움말  |  주식"))

# ===== on_message 메세지가 보내질 때 ===== #
@client.event
async def on_message(message):

    # ===== 예외 사항 ===== #
    if message.author.bot: return
    # if str(message.channel.type) != 'text': return
    if not message.content.startswith(prefix): return
    
    # ===== 변수 선언 ===== #
    cmd = message.content.split(prefix)[1].split(' ')[0]
    args = message.content.split(cmd)[1][1:].split(' ')
    id = message.author.id

    # 도움말
    if cmd == "도움말":
        embed=discord.Embed(title="도움말", description="====================", color=0x0999e1)
        embed.add_field(name="@가입\n@정보\n@돈\n@구걸\n@도박 <금액>\n@가위바위보 <금액>\n@주식 목록\n@주식 갱신\n@주식 정보 <주식이름>\n@주식 매수 <주식이름> <개수>\n@주식 매도 <주식이름> <개수>\n---------------------\n@유튜브\n@포커\n@체스\n@짭몽어스\n@낚시", value="====================", inline=False)
        await message.channel.send(embed=embed)

    # 삭제
    elif cmd == "삭제":
        limit = int(args[0])
        await message.channel.purge(limit = limit)

    # 가입
    elif cmd == "가입":
        try:
            user_users.insert_one({
                "_id": id,
                "money": 0, # .
                "삼성전자": 0,
                "한국전력": 0,
                "LG디스플레이": 0,
                "SK하이닉스": 0,
                "삼성SDI": 0, 
                "기아": 0,
                "현대차": 0,
                "KT": 0,
                "SK텔레콤": 0,
                "LG유플러스": 0,
                "HMM": 0,
                "카카오": 0,
                "NAVER": 0,
                "셀트리온": 0,
                "삼성바이오로직스": 0,
                "현대건설": 0,
                "KB금융": 0,
                "신한은행": 0
            })
            embed=discord.Embed(title="가입 완료!", color=0x05b102)
            await message.reply(embed=embed)
        except:
            embed=discord.Embed(title="이미 가입 되셨습니다!", color=0xbd0a0a)
            await message.reply(embed=embed)

    # 투게더
    elif cmd == "유튜브":
        link = await togetherControl.create_link(message.author.voice.channel.id, 'youtube')
        embed=discord.Embed(title="유튜브 투게더 | Youtube Together", description=f">>> {link} <<<", color=0xf0d000)
        await message.channel.send(embed=embed)
    elif cmd == "포커":
        link = await togetherControl.create_link(message.author.voice.channel.id, 'poker')
        embed=discord.Embed(title="포커 | Poker", description=f">>> {link}", color=0xf0d000)
        await message.channel.send(embed=embed)
    elif cmd == "체스":
        link = await togetherControl.create_link(message.author.voice.channel.id, 'chess')
        embed=discord.Embed(title="체스 | Chess", description=f">>> {link}", color=0xf0d000)
        await message.channel.send(embed=embed)
    elif cmd == "짭몽어스":
        link = await togetherControl.create_link(message.author.voice.channel.id, 'betrayal')
        embed=discord.Embed(title="짭몽어스 | Fake Amongus", description=f">>> {link}", color=0xf0d000)
        await message.channel.send(embed=embed)
    elif cmd == "낚시":
        link = await togetherControl.create_link(message.author.voice.channel.id, 'fishing')
        embed=discord.Embed(title="낚시 | Fishing", description=f">>> {link}", color=0xf0d000)
        await message.channel.send(embed=embed)

    # 주식 종목 추가
    elif cmd =="주식추가":
        jusik_jusiks.insert_one({
            "_id": args[0],
            "code": args[1],
            "price": args[2]
        })
        await message.channel.send("완료")


    # ================================================================ #


    # 가입여부 확인
    if not user_users.find_one({"_id": id}):
        embed=discord.Embed(title="먼저 가입을 진행해주세요", description="`\"@가입\"`을 통해 가입하실 수 있습니다.", color=0xf0d000)
        await message.reply(embed=embed)
        return 0
            
    # 구걸
    elif cmd == "구걸":
        data = cooldown.Cooldown(1200, message.author.id)
        if data == True:
            cooldown.CooldownUpdate(message.author.id) # 쿨타임을 새로 갱신해줍니다.
            embed=discord.Embed(title="구걸 성공", description="지나가던 행인이 `100,000원`을 던졌습니다.\n⏱ | 쿨타임 20분", color=0xf0d000)
            user_users.update_one({"_id": id}, {"$inc": {"money": 100000}})
            await message.channel.send(embed=embed)
        else:
            await message.reply(f"{data}초 남았습니다.")

    # 정보
    elif cmd == "정보":
        try:
            get_id = int(args[0])
            data = user_users.find_one({"_id": get_id})
            embed=discord.Embed(title=f"{get_id}님의 정보", description=f"보유 금액 : {data['money']}원\n\n**# 보유 주식**\n삼성전자: `{data['삼성전자']}`주\n한국전력: `{data['한국전력']}`주\nLG디스플레이: `{data['LG디스플레이']}`주\nKT: `{data['KT']}`주\nSK텔레콤: `{data['SK텔레콤']}`주\nLG유플러스: `{data['LG유플러스']}`주\nSK하이닉스: `{data['SK하이닉스']}`주\n삼성SDI: `{data['삼성SDI']}`주\nKB금융: `{data['KB금융']}`주\n신한은행: `{data['신한은행']}`주\n기아: `{data['기아']}`주\n현대차: `{data['현대차']}`주\n카카오: `{data['카카오']}`주\nNAVER: `{data['NAVER']}`주\n셀트리온: `{data['셀트리온']}`주\n삼성바이오로직스: `{data['삼성바이오로직스']}`주\nHMM: `{data['HMM']}`주\n현대건설: `{data['현대건설']}`주", color=0x0999e1)
            await message.reply(embed=embed)
        except:
            data = user_users.find_one({"_id": id})
            embed=discord.Embed(title=f"{message.author.name} 님의 정보", description=f"보유 금액 : {data['money']}원\n\n**# 보유 주식**\n삼성전자: `{data['삼성전자']}`주\n한국전력: `{data['한국전력']}`주\nLG디스플레이: `{data['LG디스플레이']}`주\nKT: `{data['KT']}`주\nSK텔레콤: `{data['SK텔레콤']}`주\nLG유플러스: `{data['LG유플러스']}`주\nSK하이닉스: `{data['SK하이닉스']}`주\n삼성SDI: `{data['삼성SDI']}`주\nKB금융: `{data['KB금융']}`주\n신한은행: `{data['신한은행']}`주\n기아: `{data['기아']}`주\n현대차: `{data['현대차']}`주\n카카오: `{data['카카오']}`주\nNAVER: `{data['NAVER']}`주\n셀트리온: `{data['셀트리온']}`주\n삼성바이오로직스: `{data['삼성바이오로직스']}`주\nHMM: `{data['HMM']}`주\n현대건설: `{data['현대건설']}`주", color=0x0999e1)
            await message.reply(embed=embed)

    # 돈
    elif cmd == "돈":
        try:
            get_id = int(args[0])
            data = user_users.find_one({"_id": get_id})
            embed=discord.Embed(title=f"{get_id}님의 정보", description=f"보유 금액 : {data['money']}원", color=0x0999e1)
            await message.reply(embed=embed)
        except:
            data = user_users.find_one({"_id": id})
            embed=discord.Embed(title=f"{message.author.name} 님의 정보", description=f"보유 금액 : {data['money']}원", color=0x0999e1)
            await message.reply(embed=embed)


    # 관리자돈설정
    elif cmd == "관리자돈추가":
        get_id = int(args[0])
        iargs = int(args[1])
        user_users.update_one({"_id": get_id}, {"$inc": {"money": iargs}})
        embed=discord.Embed(title="성공", description=f"`{iargs}원`으로 설정했습니다.", color=0x05b102)
        await message.channel.send(embed=embed)
    # 관리자돈설정
    elif cmd == "관리자돈설정":
        get_id = int(args[0])
        iargs = int(args[1])
        user_users.update_one({"_id": get_id}, {"$inc": {"money": iargs}})
        embed=discord.Embed(title="성공", description=f"`{iargs}원`으로 설정했습니다.", color=0x05b102)
        await message.channel.send(embed=embed)

    # 도박
    elif cmd == "도박":
        iargs = int(args[0])
        data = user_users.find_one({"_id": id})
        if iargs <= data['money']:
            if data['money'] <= 1000000:
                if iargs > 0:
                    random_list = [1, 2]
                    random_num = choice(random_list)
                    if random_num == 1:
                        user_users.update_one({"_id": id}, {"$inc": {"money": -iargs}})
                        embed=discord.Embed(title="실패", description=f"`{iargs}원`을 잃었습니다.", color=0xbd0a0a)
                        await message.channel.send(embed=embed)
                    elif random_num == 2:
                        user_users.update_one({"_id": id}, {"$inc": {"money": iargs}})
                        embed=discord.Embed(title="성공", description=f"`{iargs}원`을 얻었습니다.", color=0x05b102)
                        await message.channel.send(embed=embed)
                    else:
                        await message.reply("알 수 없는 오류")
                else:
                    await message.reply("음수 ㅗ")
            else:
                await message.reply("100만원 이하만 도박 가능합니다.")
        else:
            embed=discord.Embed(title="💰 | 금액 부족", description="베팅한 금액이 소유한 금액보다 많습니다!", color=0xbd0a0a)
            await message.channel.send(embed=embed)


    # 가위바위보
    elif cmd == "가위바위보":
        iargs = int(args[0])
        data = user_users.find_one({"_id": id})
        if iargs <= data['money']:
            if data['money'] <= 1000000:
                if iargs > 0:
            
                    user_users.update_one({"_id": id}, {"$inc": {"money": -iargs}})

                    rsp = ['👊', '✋', '✌']
                    res = choice(rsp)
            
                    embed=discord.Embed(title="가위바위보", description="⏱ | 15초 내로 선택하세요!", color=0xf0d000)
                    msg = await message.channel.send(embed=embed)
                    for r in rsp: await msg.add_reaction(r)

                    embed=discord.Embed(title="⏰ | 타임 아웃", description="금액은 다시 잔고로 돌아갑니다.", color=0xbd0a0a)
                    try: r = str(list(await client.wait_for('reaction_add', timeout = 15, check = (lambda r, u: str(r.emoji) in rsp and u == message.author)))[0].emoji)
                    except TimeoutError:
                        user_users.update_one({"_id": id}, {"$inc": {"money": iargs}})
                        return await msg.edit(embed=embed)

                    if r == res:
                        user_users.update_one({"_id": id}, {"$inc": {"money": iargs}})
                        embed=discord.Embed(title="비겼습니다", description=f"컴퓨터의 선택: {res}\n금액은 다시 잔고로 돌아갑니다.", color=0xf0d000)
                        return await msg.edit(embed=embed)

                    if r == '👊':
                        if res == '✋':
                            embed=discord.Embed(title="패배", description=f"컴퓨터의 선택: {res}", color=0xbd0a0a)
                            return await msg.edit(embed=embed)
                        else:
                            user_users.update_one({"_id": id}, {"$inc": {"money": iargs*2}})
                            embed=discord.Embed(title="승리", description=f"컴퓨터의 선택: {res}\n`{iargs}원`을 얻었습니다.", color=0x05b102)
                            return await msg.edit(embed=embed)

                    if r == '✋':
                        if res == '✌':
                            embed=discord.Embed(title="패배", description=f"컴퓨터의 선택: {res}", color=0xbd0a0a)
                            return await msg.edit(embed=embed)
                        else:
                            user_users.update_one({"_id": id}, {"$inc": {"money": iargs*2}})
                            embed=discord.Embed(title="승리", description=f"컴퓨터의 선택: {res}\n`{iargs}원`을 얻었습니다.", color=0x05b102)
                            return await msg.edit(embed=embed)

                    if r == '✌':
                        if res == '👊':
                            embed=discord.Embed(title="패배", description=f"컴퓨터의 선택: {res}", color=0xbd0a0a)
                            return await msg.edit(embed=embed)
                        else:
                            user_users.update_one({"_id": id}, {"$inc": {"money": iargs*2}})
                            embed=discord.Embed(title="승리", description=f"컴퓨터의 선택: {res}\n`{iargs}원`을 얻었습니다.", color=0x05b102)
                            return await msg.edit(embed=embed)
                else:
                    embed=discord.Embed(title="💰 | 금액 부족", description="베팅한 금액이 소유한 금액보다 많습니다!", color=0xbd0a0a)
                    await message.channel.send(embed=embed)

    # 주식
    elif cmd == "주식":
        if args[0] == "목록":
            j1 = jusik_jusiks.find_one({"_id": "삼성전자"})
            j2 = jusik_jusiks.find_one({"_id": "한국전력"})
            j3 = jusik_jusiks.find_one({"_id": "LG디스플레이"})
            j4 = jusik_jusiks.find_one({"_id": "SK하이닉스"})
            j5 = jusik_jusiks.find_one({"_id": "삼성SDI"})
            j6 = jusik_jusiks.find_one({"_id": "기아"})
            j7 = jusik_jusiks.find_one({"_id": "현대차"})
            j8 = jusik_jusiks.find_one({"_id": "KT"})
            j9 = jusik_jusiks.find_one({"_id": "SK텔레콤"})
            j10 = jusik_jusiks.find_one({"_id": "LG유플러스"})
            j11 = jusik_jusiks.find_one({"_id": "HMM"})
            j12 = jusik_jusiks.find_one({"_id": "카카오"})
            j13 = jusik_jusiks.find_one({"_id": "NAVER"})
            j14 = jusik_jusiks.find_one({"_id": "셀트리온"})
            j15 = jusik_jusiks.find_one({"_id": "삼성바이오로직스"})
            j16 = jusik_jusiks.find_one({"_id": "현대건설"})
            j17 = jusik_jusiks.find_one({"_id": "KB금융"})
            j18 = jusik_jusiks.find_one({"_id": "신한은행"})

            embed=discord.Embed(title='🗠 | 주식 목록', description='====================', color=0xf0d000)
            embed.add_field(name="삼성전자", value=f"{j1['price']}원", inline=True)
            embed.add_field(name="한국전력", value=f"{j2['price']}원", inline=True)
            embed.add_field(name="LG디스플레이", value=f"{j3['price']}원", inline=True)

            embed.add_field(name="KT", value=f"{j8['price']}원", inline=True)
            embed.add_field(name="SK텔레콤", value=f"{j9['price']}원", inline=True)
            embed.add_field(name="LG유플러스", value=f"{j10['price']}원", inline=True)

            embed.add_field(name="# 반도체", value=".", inline=True)
            embed.add_field(name="SK하이닉스", value=f"{j4['price']}원", inline=True)
            embed.add_field(name="삼성SDI", value=f"{j5['price']}원", inline=True)

            embed.add_field(name="# 금융", value=".", inline=True)
            embed.add_field(name="KB금융", value=f"{j17['price']}원", inline=True)
            embed.add_field(name="신한은행", value=f"{j18['price']}원", inline=True)

            embed.add_field(name="# 자동차", value=".", inline=True)
            embed.add_field(name="기아", value=f"{j6['price']}원", inline=True)
            embed.add_field(name="현대차", value=f"{j7['price']}원", inline=True)

            embed.add_field(name="# IT", value=".", inline=True)
            embed.add_field(name="카카오", value=f"{j12['price']}원", inline=True)
            embed.add_field(name="NAVER", value=f"{j13['price']}원", inline=True)

            embed.add_field(name="# 제약", value=".", inline=True)
            embed.add_field(name="셀트리온", value=f"{j14['price']}원", inline=True)
            embed.add_field(name="삼성바이오로직스", value=f"{j15['price']}원", inline=True)

            embed.add_field(name="# 운송, 건설", value=".", inline=True)
            embed.add_field(name="HMM", value=f"{j11['price']}원", inline=True)
            embed.add_field(name="현대건설", value=f"{j16['price']}원", inline=True)

            
            await message.channel.send(embed=embed)

        elif args[0] == "갱신":
            embed=discord.Embed(title='🗠 | 주식 갱신', description='0분(정각), 15분, 30분, 45분에 갱신 됩니다.\n모든 주식 가격이 갱신되는데 약 1분 정도 소요됩니다.', color=0xf0d000)
            await message.channel.send(embed=embed)
        
        elif args[0] == "정보":
            stock_name = args[1]
            if stock_name != None:
                try:
                    data = jusik_jusiks.find_one({"_id": stock_name})
                    code = data['code']
                    embed = discord.Embed(colour=0xbd0a0a)
                    embed.set_author(name=f"{stock_name}({code})의 주식 정보를 가져오는중..")
                    msg = await message.channel.send(embed=embed)
                    url = f'https://finance.naver.com/item/sise.nhn?code={code}'
                    html = urlopen(url)
                    bs = BeautifulSoup(html, 'html.parser')

                    price = bs.find('strong', {'class':'tah p11'}, {'id':'_nowVal'}).text.split('</span>')
                    price = ''.join(price)

                    rate = bs.find('strong', {'id':'_rate'}).text.split('</span>')
                    rate = '\n'.join(rate)
                    rate = rate.replace('\n', '')
                    rate = rate.replace('\t', '')

                    compared = bs.find('strong', {'id':'_diff'}).text.split('</span>')
                    compared = '\n'.join(compared)
                    compared = compared.replace('\n', '')
                    compared = compared.replace('\t', '')

                    if bs.find('em', {'class':'bu_p bu_pdn'}):
                        check = '🔻'
                        compared = compared.replace('하락', '')
                    else:
                        check = '🔺'
                        compared = compared.replace('상승', '')

                    sell = bs.find('span', {'id':'_quant'}).text.split('</span>')
                    sell = '\n'.join(sell)
                    sell = sell.replace('\n', '')
                    sell = sell.replace('\t', '')

                    embed = discord.Embed(colour=0xf0d000)
                    embed.set_author(name=f"{stock_name} ({code})", url=f'https://finance.naver.com/item/sise.nhn?code={code}')
                    embed.add_field(name="현재가", value=price)
                    embed.add_field(name="전일대비", value=f"{check}{compared}({rate})")
                    embed.add_field(name="거래량", value=sell)
                    embed.set_image(url=f"https://ssl.pstatic.net/imgfinance/chart/item/area/day/{code}.png")
                    await msg.edit(embed=embed)


                except Exception as e:
                    embed=discord.Embed(colour=0xbd0a0a)
                    embed.add_field(name="정확한 주식 이름을 입력해주세요", value="`\"@주식 목록\"`으로 정확한 이름을 확인하실수 있습니다.\n예) naver(x) -> NAVER(o)")
                    await message.channel.send(embed=embed)
        
        elif args[0] == "매수":
            if int(args[2]) > 0:
                com_name = args[1]
                if com_name != None:
                    com_getnum = int(args[2])
                    if com_getnum != None:

                        data_user = user_users.find_one({"_id": id})
                        data_jusik = jusik_jusiks.find_one({"_id": com_name})
                        c_price = data_jusik['price'].split(',')
                        com_price = int(''.join(c_price))
                        com_totalprice = com_price*int(com_getnum)

                        if com_totalprice <= int(data_user['money']):
                            user_users.update_one({"_id": id}, {"$inc": {"money": -com_totalprice}})
                            user_users.update_one({"_id": id}, {"$inc": {com_name: com_getnum}})
                            embed=discord.Embed(title="성공!", description=f"`{com_name}`을/를 `{com_getnum}`주 매수했습니다\n자세한 내용은 DM을 확인해주세요.", color=0x05b102)
                            await message.channel.send(embed=embed)
                            embed=discord.Embed(title="구매 영수증", description=f"`{com_name}`을/를 `{com_getnum}`주 매수했습니다.\n한 주: `{com_price}`원\n총 매수에 쓴 비용: `{com_totalprice}`원", color=0xf0d000)
                            await message.author.send(embed=embed)
                        else:
                            embed=discord.Embed(title="💰 | 금액 부족", description="가격이 소유한 금액보다 많습니다!", color=0xbd0a0a)
                            await message.channel.send(embed=embed)
                    else:
                        embed=discord.Embed(title="정확히 입력해주세요", description="`\"@주식 매수 <주식이름> <개수>\"`로 입력해주세요.", color=0xbd0a0a)
                        await message.channel.send(embed=embed)
                else:
                    embed=discord.Embed(title="정확히 입력해주세요", description="`\"@주식 매수 <주식이름> <개수>\"`로 입력해주세요.", color=0xbd0a0a)
                    await message.channel.send(embed=embed)
            else:
                await message.channel.send("음수 ㅗ")

        elif args[0] == "매도":
            if int(args[2]) > 0:
                com_name = args[1]
                if com_name != None:
                    com_outnum = int(args[2])
                    if com_outnum != None:

                        data_user = user_users.find_one({"_id": id})
                        data_jusik = jusik_jusiks.find_one({"_id": com_name})
                        c_price = data_jusik['price'].split(',')
                        com_price = int(''.join(c_price))
                        com_totalprice = com_price*int(com_outnum)

                        if data_user[args[1]] >= com_outnum:
                            user_users.update_one({"_id": id}, {"$inc": {"money": com_totalprice}})
                            user_users.update_one({"_id": id}, {"$inc": {com_name: -com_outnum}})
                            embed=discord.Embed(title="성공!", description=f"`{com_name}`을/를 `{com_outnum}`주 매도했습니다.\n자세한 내용은 DM을 확인해주세요.", color=0x05b102)
                            await message.channel.send(embed=embed)
                            embed=discord.Embed(title="판매 영수증", description=f"`{com_name}`을/를 `{com_outnum}`주 매도했습니다.\n한 주: `{com_price}`원\n총 매도 비용: `{com_totalprice}`원", color=0xf0d000)
                            await message.author.send(embed=embed)
                        else:
                            embed=discord.Embed(title="💰 | 주식 부족", description="판매할 주식의 개수가 보유한 개수보다 많습니다!", color=0xbd0a0a)
                            await message.channel.send(embed=embed)
                    else:
                        embed=discord.Embed(title="정확히 입력해주세요", description="`\"@주식 매도 <주식이름> <개수>\"`로 입력해주세요.", color=0xbd0a0a)
                        await message.channel.send(embed=embed)
                else:
                    embed=discord.Embed(title="정확히 입력해주세요", description="`\"@주식 매도 <주식이름> <개수>\"`로 입력해주세요.", color=0xbd0a0a)
                    await message.channel.send(embed=embed)
            else:
                await message.channel.send("음수 ㅗ")
                    
        
            

# # 전기, 전자**\n- 삼성전자\n- 한국전력\n- LG디스플레이\n**# 반도체**\n- SK하이닉스\n- 삼성SDI\n**# 자동차**\n- 기아차\n- 현대차\n**# 이동 통신**\n- KT\n- SK텔레콤\n- LG유플러스\n**# 조선**\n- HMM(현대상선)\n**# IT**\n- 카카오\n- 네이버\n**# 제약**\n- 셀트리온\n- 삼성바이오로직스\n**# 건설**\n- 현대건설\n**# 은행**\n- KB국민은행\n- 신한은행    

# ===== 토큰 ===== # 
client.run(token)
