# parrbot.py
import os, random as rand
import discord
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

bot = commands.Bot(command_prefix ='!')

UserArr = []
userMsg = []
#stores messages from a user in a dict
def msgMaker():
     userMsgDict = {}
     for i in range(len(UserArr)):
          userMsgDict[UserArr[i]] = userMsg[i]
     return userMsgDict
#look over me to make sure that the reactions work properly (EMOJIS ARE WRONG TODO: FIX EMOJIS)
#allows user to prompt out of polly's shenanigans
@client.event
async def on_member_join(member):
     UserIsOptin = True
     await member.create_dm()
     await member.dm_channel.send(f"SQUAWK! I'm Polly! I like to parrot off what people say! If you don't want me to listen to you, please react to this message with an X. SQUAWK!")
     if discord.on_reaction_add(":heavy_multiplication_x:", member) or discord.on_reaction_add(":x:", member) or discord.on_reaction_add(":regional_indicator_x:",member):
          UserIsOptin = False
     if UserIsOptin == True:
          UserArr.append(member)


@client.event
async def on_ready():
     print(f'{client.user.name} has connected to discord.')

#gets list of users, so a dict can be created that'll let the user get a value
@client.event

#this is for storing a random message from a user
@client.event
async def on_message(message):
     if message.author == client.user:
          return
     pollychance = rand.randint(1,10)
     if pollychance == 1:
          #stores message to a text file
          file = open("messages.txt", 'a')
          file.write(message.content +'\n')
          file.close()
          await message.add_reaction('🦜')

#Random message getter
@bot.command(name="Parrot message", help='Sends a random message from a anonymous user.')
async def sendMsg(message):
     if message.author == client.user:
          return
     if message.content == "polly" or message.content == "Polly":
          parrottedmsg = rand.choice()
          if parrottedmsg == "":
               message.channel.send("I haven't heard anything yet. SQUAWK!")
          await message.channel.send(parrottedmsg + " SQUAWK!")
     elif message.content == 'raise-exception':
          raise discord.DiscordException

      

client.run(TOKEN)