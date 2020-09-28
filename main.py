import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import datetime
import pytz

#set time zone to US Eastern
est = pytz.timezone('America/New_York')

#import bot token from .env file
token= os.getenv('discord_bot_token')

#cset up command prefix that bot will look for
client = commands.Bot(command_prefix="#")

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

#when bot is mentioned it will list commands
@client.event
async def on_message(message):
  for  x in message.mentions:
    if x==client.user:
      await message.channel.send(f"Hello, my commands are: {list}")
  await client.process_commands(message)   

list = ['#dinner', '#play', '#coin', "#dice", '#bad']

@client.command()
async def HELP(ctx):
  await ctx.send(f'The commands are: {list }')
  
@client.command()
async def dinner(ctx):
  now = datetime.datetime.now(est)
  #print(now)
  #used dinner time from 6pm to 2am
  if 6 < now.hour > 22:
    await ctx.send('It\'s time for dinner!')
  else:
    await ctx.send('It\'s too early for dinner')



#randomly pick from list of games
@client.command()
async def play(ctx):
  games = ['Warzone', 'Cyber', 'Fall Guys', 'Golf with your Friends']
  print("play command called")
  await ctx.send(f'play {random.choice(games)}')

#flip a coin
@client.command()
async def coin(ctx):
  flip = ['heads', 'tails']
  print('coin command called')
  await ctx.send(f' {random.choice(flip)}')
  
# bot mentions user after command and tells them they are bad  
@client.command() 
async def bad (ctx, member):
  await ctx.send(f" {member} is bad")
@bad.error
async def bad_error(ctx, error):
  print('bad error')
  if isinstance(error, (commands.MissingRequiredArgument)):
    await ctx.send("Mention user after #bad \n e.g.: #bad @pacoman432")

#roll a dice with number of sides input by member  
@client.command()
async def dice(ctx,arg):
  length = len(arg)
  number = int(arg)
  
  if number <= 0:
    await ctx.send("Enter a number greater than 0")
    print('dice command needs number greater than 0')
  else:
    await ctx.send(f"A random number between 1 and {number} is: \n {random.randrange(1,number+1)}")
    print('dice command called') 
#error is user did not imput number after dice command    
@dice.error
async def dice_error(ctx, error):
  print('dice error')
  if isinstance(error, (commands.MissingRequiredArgument)):
    await ctx.send("Enter a number after #dice \n e.g.: #dice 100")

#error is user entered a command that is recognized by bot
@client.event
async def on_command_error(ctx,error):
  if isinstance(error, (commands.CommandNotFound)):
    await ctx.send("Command does not exist type #HELP or mention me to see all commands")


client.run(token)
