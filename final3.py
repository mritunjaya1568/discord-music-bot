import discord
import os
import youtube_dl
import requests
import music3
import asyncio

# install ffmpeg also from -> sudo apt install ffmpeg

token = "your_token_here"

PREFIX = ['!' , '?' , '@']
client = discord.Client()


help2 = """!play {song-name} (alias - !p {song-name})- to join the channel you are in and play your given song \n
!pause - to pause the current song \n
!resume / !res - to resume the song \n
!skip - to skip the current song \n
!skipall - to remove all songs from the queue \n
!recommend / !r n{no of songs to recommend} - to recommend next n songs based on current song \n
!loop - put loop on the current song \n
!unloop - to unloop the current song \n
!leave / !lv - to leave the channel and remove all songs from the queue \n"""


p1 = music3.Music(client)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content[0] not in PREFIX:
		return

	cmd = message.content[1:].split()[0]

	if cmd in ["join" , "j"]:
		await p1.join(message)
	elif cmd in ["leave", "lv"]:
		await p1.leave()
	elif cmd in ["play" , "p"]:
		await p1.play(message)
	elif cmd in ["pause"]:
		await p1.pause()
	elif cmd in ["resume", "res"]:
		await p1.resume()
	elif cmd in ["skip"]:
		await p1.skip()
	elif cmd in ["skipall" , "stop"]:
		await p1.skip_all()
	elif cmd in ["recommend", "r"]:
		p1.recommend(message)
	elif cmd in ["loop"]:
		await p1.loop()
	elif cmd in ["unloop"]:
		await p1.un_loop()
	else:
		await message.channel.send(help2)


client.run(token)



