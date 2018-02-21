import discord
from discord.ext import commands
import asyncio
import json

description = "The incorrect Java Autonomous Noob Enlighter"

data = json.load(open("token.json"))	
bot = commands.Bot(command_prefix='j!', description=description)
token = data["token"]


@bot.event
async def on_ready():
	print(bot.user.id)
	print(bot.user)
	print("I smell the gulag today")
	print("------")

@bot.group(pass_context=True)
async def gulag(ctx):
	if ctx.invoked_subcommand is None:
		if ctx.message.channel.permissions_for(ctx.message.author).manage_messages:
			await bot.send_file(ctx.message.channel, fp="gulag.png")

@gulag.command(pass_context=True)
async def mute(ctx, member : discord.Member):
	try:
		if ctx.message.channel.permissions_for(ctx.message.author).manage_messages:
			await bot.add_roles(member, discord.Role(server=discord.Server(id='160246330701250560'), id='377339046772604928'))
			await bot.send_file(ctx.message.channel, fp="gulag.png", content='{0.name} has been gulagged'.format(member))
	except Exception as e:
		await bot.say(e)

@gulag.command(pass_context=True)
async def unmute(ctx, member : discord.Member):
	try:
		if ctx.message.channel.permissions_for(ctx.message.author).manage_messages:
			await bot.remove_roles(member, discord.Role(server=discord.Server(id='160246330701250560'), id='377339046772604928'))
			await bot.say("{0.name} has been ungulagged".format(member))
	except Exception as e:
		await bot.say(e)

@bot.command(pass_context=True)
async def age(ctx, member : discord.User = None):
	if member is None:
		member = ctx.message.author
	await bot.say("{0.name}'s account is created at {0.created_at}".format(member))

@age.error
async def age_error():
	await bot.say("Something went wrong! Did you specify a user?")

	
@bot.command(pass_context=True)
async def say(ctx, *, text : str):
	if ctx.message.author.id == '157167815512555520':
		await bot.send_message(ctx.message.channel, text)
		await bot.delete_message(ctx.message)

@say.error
async def say_error(error, ctx):
	await bot.say("Error! Something went wrong!")


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
