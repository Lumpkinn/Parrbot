
#TODO: Message storage is busted, fix that, the other menial issues, make the art, and ship 

# parrbot.py
import os, random as rand
import discord
import asyncio
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

bot = commands.Bot(command_prefix ='!')

#these arrays are meant to hold usernames and messages
UserArr = []


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
     await asyncio.sleep(rand.uniform(5,9))
     await member.dm_channel.send(f"SQUAWK! I'm Polly! I like to parrot off what people say! If you don't want me to listen to you, please react to this message with an X. SQUAWK!")
     if discord.on_reaction_add(":heavy_multiplication_x:", member) or discord.on_reaction_add(":x:", member) or discord.on_reaction_add(":regional_indicator_x:",member):
          UserIsOptin = False
     if UserIsOptin == True:
          UserArr.append(member)

#informs me when bot is connected
@client.event
async def on_ready():
     print(f'{client.user.name} has connected to discord.')


#this is for storing a random message from a user TODO: make sure that people who've opted out are not included (I think that's already happened, but i need to trace to be sure)
@client.event
async def on_message(ctx, message):
     if message.author == client.user:
          return
     
     pollychance = rand.randint(1,10)
     if pollychance == 1:
          #stores message to a text file
          file = open("messages.txt", 'a')
          file.write(message.content +'\n')
          file.close()
          UserArr.append(message.author)
          await message.add_reaction('🦜')
          indexOfUser = UserArr.indexof(message.author)
          UserArr[indexOfUser] = [message]

          

#Random message getter 
@bot.command(name="Parrot message", help='Sends a random message from a anonymous user.')
async def sendMsg(message):

     if message.author == client.user:
          return
     
     if message.content == "polly" or message.content == "Polly":
          parrottedmsg = rand.choice(userMsg)
          if parrottedmsg == null:
               await asyncio.sleep(rand.uniform(2,3))
               message.channel.send("I haven't heard anything yet. SQUAWK!")

          await asyncio.sleep(rand.uniform(5,9))
          await message.channel.send(parrottedmsg + " SQUAWK!")
     
     elif message.content == 'raise-exception':
          raise discord.DiscordException


#stitches two random messages together. (make sure that this happens at a space, and not inside of a word)
@bot.command(name="Stitch", help="Stitches two messages together")
async def stitch(ctx, message):
     #ALRIGHT, If you wanna add this, you need to have the message storage handled first. after that, you can user .split(" ") <- (theres a space inbetween) to split all of them into different strings, and place them into a list. i think you can take it from there.
     await asyncio.sleep(rand.uniform(5,10))
     pass

#reverses a random users message
@bot.command(name="Reverse", help="reverses a user's message")
async def reversal(cxt, message):
     await asyncio.sleep(rand.uniform(5,9))
     await cxt.send(message[::-1])


#tells how long a message is to shame chronic yappers
@bot.command (name="MSGLen", help="returns the length of a message")
async def MSGLen(cxt, message):
     await asyncio.sleep(rand.uniform(5,6))
     await cxt.send("this message is ", len(message) , " letters long. SQUAWK!")

#repeats what the user passed to it.
@bot.command()
async def repeat(ctx, msg):
     await asyncio.sleep(rand.uniform(3,4))
     await ctx.send(msg)

client.run(TOKEN)