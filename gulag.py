import discord
from discord.ext import commands
import asyncio
import json
import subprocess
import traceback
import fcntl,os

description = "The incorrect Java Autonomous Noob Enlighter"

#set some variables

data = json.load(open("token.json"))	
bot = commands.Bot(command_prefix='j!', description=description)
token = data["token"]
server = data["server"]
role = data["role"]
owner = data["owner"]
shell_running = False
cmd_buffer = []
shell_proc = None

@bot.event
async def on_ready():
	print(bot.user.id)
	print(bot.user)
	print("I smell the gulag today")
	print("------")

#the gulag command(basically mute/unmute)

@bot.group(pass_context=True)
async def gulag(ctx):
	if ctx.invoked_subcommand is None:
		if ctx.message.channel.permissions_for(ctx.message.author).manage_messages:
			await bot.send_file(ctx.message.channel, fp="gulag.png")

@gulag.command(pass_context=True)
async def mute(ctx, member : discord.Member):
	try:
		if ctx.message.channel.permissions_for(ctx.message.author).manage_messages:
			await bot.add_roles(member, discord.Role(server=discord.Server(id=server), id=role))
			await bot.send_file(ctx.message.channel, fp="gulag.png", content='{0.name} has been gulagged'.format(member))
	except Exception as e:
		await bot.say(e)

@gulag.command(pass_context=True)
async def unmute(ctx, member : discord.Member):
	try:
		if ctx.message.channel.permissions_for(ctx.message.author).manage_messages:
			await bot.remove_roles(member, discord.Role(server=discord.Server(id=server), id=role))
			await bot.say("{0.name} has been ungulagged".format(member))
	except Exception as e:
		await bot.say(e)

#Returns creation date		

@bot.command(pass_context=True)
async def age(ctx, member : discord.User = None):
	if member is None:
		member = ctx.message.author
	await bot.say("{0.name}'s account is created at {0.created_at}".format(member))

@age.error
async def age_error():
	await bot.say("Something went wrong! Did you specify a user?")

#Make the bot say something
	
@bot.command(pass_context=True)
async def say(ctx, *, text : str):
	if ctx.message.author.id == owner:
		await bot.send_message(ctx.message.channel, text)
		await bot.delete_message(ctx.message)

@say.error
async def say_error(error, ctx):
	await bot.say("Error! Something went wrong!")

@bot.command(pass_context=True)
async def access(ctx):
	if ctx.message.channel.id == "439139494684262400":
		member = ctx.message.author
		await bot.delete_message(ctx.message)
		if discord.Role(server=discord.Server(id=server), id="439138951916290059") not in member.roles:
			await bot.add_roles(member, discord.Role(server=discord.Server(id=server), id=439138951916290059))
			await bot.send_message(member, "You have recieved access! The IP for the server is starquest.spacebeaverstudios.com.")

@bot.command(pass_context=True)
async def science(ctx):
	if ctx.message.server.id == "160246330701250560":
		member = ctx.message.author
		if discord.Role(server=discord.Server(id=server), id="439700931932585987") not in member.roles:
			await bot.add_roles(member, discord.Role(server=discord.Server(id=server), id=439700931932585987))
			msg = await bot.send_message(ctx.message.channel, "You have recieved the Scientist role")
			await asyncio.sleep(10)
			await bot.delete_message(ctx.message)
			await bot.delete_message(msg)
			
		else:
			await bot.remove_roles(member, discord.Role(server=discord.Server(id=server), id="439700931932585987"))
			msg = await bot.say("You no longer have the Scientist role")
			await asyncio.sleep(10)
			await bot.delete_message(ctx.message)
			await bot.delete_message(msg)
#Execute shell commands	

@bot.command(pass_context=True)
async def eval(ctx, *, text : str):
	global shell_running,cmd_buffer,shell_proc
	if ctx.message.author.id == owner:
		if not shell_running:
			cmd_buffer = [text]
			shell_proc = None
			asyncio.run_coroutine_threadsafe(handle_cmd(ctx.message),bot.loop)
		else:
			cmd_buffer.append(text)

@bot.command(pass_context=True)
async def ceval(ctx): #Send CTRL-C to shell
	global shell_proc
	if ctx.message.author.id == owner:
		shell_proc.send_signal(subprocess.signal.SIGINT)

@bot.command(pass_context=True)
async def keval(ctx): #Kill shell
	global shell_proc
	if ctx.message.author.id == owner:
		shell_proc.send_signal(subprocess.signal.SIGKILL)

def nbread(fd):
	try:
		return fd.read()
	except:
		return ''

async def handle_cmd(msg):
	global shell_running,cmd_buffer,shell_proc
	try:
		p = subprocess.Popen(["/bin/bash"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,universal_newlines=True)
		shell_proc = p
		shell_running = True
		fl = fcntl.fcntl(p.stdout.fileno(), fcntl.F_GETFL)
		fcntl.fcntl(p.stdout.fileno(), fcntl.F_SETFL, fl | os.O_NONBLOCK)
		fl = fcntl.fcntl(p.stderr.fileno(), fcntl.F_GETFL)
		fcntl.fcntl(p.stderr.fileno(), fcntl.F_SETFL, fl | os.O_NONBLOCK)
		while shell_running:
			if p.poll() != None:
				shell_running = False
				break
			if cmd_buffer:
				p.stdin.write(cmd_buffer[0]+"\n")
				cmd_buffer.remove(cmd_buffer[0])
			p.stdin.flush()
			stdout = nbread(p.stdout)
			stderr = nbread(p.stderr)
			if stdout:
				if len(stdout) > 1500:
					strs = [stdout[i:i+1500] for i in range(0, len(stdout), 1500)]
					for i in strs:
						await bot.send_message(msg.channel,"``\n" + i + "\n``")
						await asyncio.sleep(0.1)
				else:
					await bot.send_message(msg.channel,"``\n" + stdout + "\n``")
			if stderr:
				if len(stderr) > 1500:
					strs = [stderr[i:i+1500] for i in range(0, len(stderr), 1500)]
					for i in strs:
						await bot.send_message(msg.channel,"``\n" + i + "\n``")
						await asyncio.sleep(0.5)
				else:
					await bot.send_message(msg.channel,"``\n" + stderr + "\n``")
			await asyncio.sleep(0.5)
		await bot.send_message(msg.channel,"Shell terminated")
	except:
		tb = traceback.format_exc()
		print("Error:\n%s"%tb)
		await bot.send_message(msg.channel,"Error:\n```%s```"%tb)

#To lazy to properly code all this
@bot.event
async def on_message(message):
	if message.content.startswith("j!galug"):
		if message.channel.permissions_for(message.author).manage_messages:
			await bot.send_file(message.channel, fp="galug.png")
	if message.content.startswith("j!haha"):
		if message.channel.permissions_for(message.author).manage_messages:
			await bot.send_file(message.channel, fp="haha.png")
	if message.channel.id == "326711493674532864":
		await bot.add_reaction(message, '👍')
		await bot.add_reaction(message, '👎')	
		await bot.add_reaction(message, discord.Emoji(id=405404517358764043, server=discord.Server(id=160246330701250560)))
	if message.content.lower() == "jane fly sun":
		await bot.send_message(message.channel, "No you can not fly into the sun, you will most certainly burn up and die")
	if message.content.lower() == "jane dynmap link":
		await bot.send_message(message.channel, "http://starquest.spacebeaverstudios.com:8123")
	if message.content.lower() == "thanks jane":
		await bot.send_message(message.channel, "You're welcome :)")
	if message.content.lower() in ["jane resourcepack link", "jane respack link", "jane texturepack link"]:
		await bot.send_message(message.channel, "https://www.dropbox.com/s/diobsw0vcdiuj3o/SQLite.zip?dl=0")

	await bot.process_commands(message)
bot.run(token)
