# インストールした discord.py を読み込む
import discord
import random

from serviceKey import serviceKey

TOKEN = serviceKey["TOKEN"]

# 接続に必要なオブジェクトを生成
client = discord.Client()

# Channel's ID
ServerId = serviceKey["ServerId"]
VoiceChannelId = serviceKey["VoiceChannelId"]
DeadChannelId = serviceKey["DeadChannelId"]
GeneralId = serviceKey["GeneralId"]


async def say_hello():
    channel = client.get_channel(GeneralId)
    await channel.send('Among Us Bot Activated \n .listと送信して機能の確認')


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    await say_hello()
    print('Logged In')


# list of dead
deadList = []

# メッセージ受信時に動作する処理


@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '.neko':
        await message.channel.send('にゃーん')

    # clap
    if message.content == '.8':
        await message.channel.send('88888888')

    # ランダムにチーム分けする機能（LOL用)
    if message.content.startswith('.divide'):
        member_list = []
        for member in message.mentions:
            member_name = member.name
            member_list.append(member_name)

        member_num = len(member_list)
        divide_num = int(message.content[-1])

        if divide_num > member_num:
            await message.channel.send("人数が足りません")
            return

        divide_list = [[] for i in range(divide_num)]
        for i in range(member_num):
            random.shuffle(member_list)
            divide_list[i % divide_num].append(member_list.pop())

        for i in range(divide_num):
            members = ' , '.join(divide_list[i])
            await message.channel.send(f"チーム{i+1}は、{members}")

    if message.content.startswith('.choose'):
        if len(message.mentions) == 0:
            await message.channel.send("No one is mentioned")
        else:
            selected = random.choice(message.mentions)
            await message.channel.send(selected.mention)

    # killされたときに、Among Us!チャネルからDeadチャネルに移動させる
    if message.content.startswith('.kill'):
        if len(message.mentions) == 0:
            await message.channel.send("No one is mentioned")
        else:
            DeadChannel = client.get_channel(DeadChannelId)
            for member in message.mentions:
                # add member to deadlist
                deadList.append(member.name)
                # Notify
                await message.channel.send(f'{member.name} is dead')
                # move member to dead channel
                await member.move_to(DeadChannel)

    # '.mute'もしくは'.m'と入力するとミュート
    if message.content == '.mute' or message.content == '.m':
        VoiceChannel = client.get_channel(VoiceChannelId)
        await message.channel.send("SHHHHHHH!")
        for member in VoiceChannel.members:
            await member.edit(mute=True)

    # '.unmute'もしくは'.u'と入力するとアンミュート
    if message.content == '.unmute' or message.content == '.u':
        VoiceChannel = client.get_channel(VoiceChannelId)
        await message.channel.send("DISCUSS!!")

        # もしDeadだったら、unmuteされない
        for member in VoiceChannel.members:
            if not member.name in deadList:
                await member.edit(mute=False)

    if message.content == '.list':
        description = ".mute もしくは .mでチャンネル内の全員をミュートします\n"\
            ".unmute もしくは .uでチャンネル内の全員をアンミュートします\n"\
            ".kill @名前1 @名前2 ... で、チャンネル内のメンバーをDeadチャンネルに移動\n"\
            ".choose @名前1 @名前2 ... で、その中からランダムにメンバーを表示\n"\
            ".end でDeadチャンネルのメンバーを全員戻す"
        await message.channel.send(description)

    # 終了
    if message.content == '.end':
        VoiceChannel = client.get_channel(VoiceChannelId)
        DeadChannel = client.get_channel(DeadChannelId)
        deadList.clear()
        for member in DeadChannel.members:
            await member.move_to(VoiceChannel)


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
