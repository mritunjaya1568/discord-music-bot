import discord
import os
import youtube_dl
import requests
import asyncio
from pytube import YouTube

ydl_opts = {
'format':'bestaudio/best',
'postprocessors':[{
        'key':'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality':'192',
                    }],
            }


class Music:
	def __init__(self,client):
		self.client = client
		self.lest = []
		self.last = ""
		self.loop_flag = False

	async def join(self , message):
		if message.author.voice == None:
			await message.channel.send("You are not in a voice channel")
			return False
		author_channel = message.author.voice.channel
		if not self.client.voice_clients:
			self.lest = []
			self.loop_flag = False
			await author_channel.connect()
		else:
			if author_channel != self.client.voice_clients[0].channel:
				self.lest = []
				self.loop_flag = False
				await self.client.voice_clients[0].move_to(author_channel)
		return True

	#leave the voice channel
	async def leave(self):
		try:
			voice = self.client.voice_clients[0]
			await voice.disconnect()
		except:
			pass

	# pause the music
	async def pause(self):
		try:
			voice = self.client.voice_clients[0]
			voice.pause()
		except:
			pass

	# resume the music
	async def resume(self):
		try:
			voice = self.client.voice_clients[0]
			voice.resume()
		except:
			pass

	# skip the music 
	async def skip(self):
		try:
			voice = self.client.voice_clients[0]
			voice.stop()
		except:
			pass

	#skipall songs and stop the player from playing
	async def skip_all(self):
		try:
			voice = self.client.voice_clients[0]
			self.lest.clear()
			voice.stop()
		except:
			pass


	def search_query(self,msg):
	    # msg = message.content
	    if msg.find("http")!= -1:
	        url = msg.split(' ')[-1]
	    else:
	        r = f"https://www.youtube.com/results?search_query="

	        try:
	        	msg_req = msg[msg.find(' ')+1:].strip()
	        	if msg_req == "":
	        		return f"https://www.youtube.com/"
	        except:
	        	return f"https://www.youtube.com/"
	        msg_req = msg_req.replace(" ","+")

	        r = requests.get(r + msg_req)

	        x = r.text

	        k=x.find("watch?v=")
	        x=x[k:]
	        k=x.find('","')
	        x=x[:k]

	        url = f"https://www.youtube.com/" + f"{x}"
	    return url
	# find the duration of music 
	def duration(self,url):
		ydl = youtube_dl.YoutubeDL(ydl_opts)
		info_dict = ydl.extract_info(url , download = False)
		x = info_dict['duration']
		ydl.cache.remove()
		return int(x)

	def download(self):
		url = self.lest[0]
		os.system('rm -rf *.mp3')
		os.system('rm -rf *.m4a')
		os.system('rm -rf *.webm')

		my_video = YouTube(url)
		title = my_video.title
		print(title)
		my_video = my_video.streams.last()
		my_video.download()

		filename = f"{title}" + f".webm"

		os.system(f'mv *.webm song.mp3')


	async def queue(self,message):
		try:
			url = self.search_query(message.content)
			if url == "https://www.youtube.com/":
				await message.channel.send("Empty query or having error handling the query")
			else:
				self.lest.append(url)
				print(url)
		except:
			await message.channel.send("Error finding youtube url")


	def play_song(self):
		try:
			self.download()
			self.last = self.lest[0]
			self.lest = self.lest[1:]
			voice = self.client.voice_clients[0]
			voice.play(discord.FFmpegPCMAudio("song.mp3"),after = lambda x = None:self.play_song())
		except:
			pass


	async def play(self, message):
		if not await self.join(message):
			return

		await self.queue(message)

		voice = self.client.voice_clients[0]
		if not voice.is_playing() and not voice.is_paused():
			self.play_song()


	def loop_song(self):
		try:
			if self.loop_flag:
				voice = self.client.voice_clients[0]
				voice.play(discord.FFmpegPCMAudio("song.mp3"), after = lambda x = None:self.loop_song())
		except:
			pass


	async def loop(self):
		try:
			await self.skip_all()
			self.loop_flag = True
			# print(os.path.isfile("song.mp3"))
			voice = self.client.voice_clients[0]
			voice.play(discord.FFmpegPCMAudio("song.mp3"), after = lambda x = None:self.loop_song())
		except:
			print("Error in looping")

	async def un_loop(self):
		try:
			self.loop_flag = False
			await self.skip_all()
		except:
			print("Error in unlooping")

	def recommend(self,message):
	    try:
	        links = []
	        link = self.last
	        r = requests.get(link)
	        links.append(link)

	        x = r.text
	        i = 0
	        val = message.content.split(' ')[-1]
	        try :
	        	val = int(val)
	        	if (isinstance(val,int) == True and val<0) or (isinstance(val,int) != True):
	        		val = 3
	        except:
	        	val = 3

	        while i!=val:	
	            x = x[x.find("watch?v="):]
	            part = f"https://www.youtube.com/" + f"{x[:19]}"
	            if part not in links:
	                if self.duration(part)<=480:
	                    links.append(part)
	                    i += 1
	            x = x[1:]
	        links = links[1:]

	        for i in links:
	        	self.lest.append(i)
	        print(self.lest)

	    except:
	        print("Error in recommending")



		

