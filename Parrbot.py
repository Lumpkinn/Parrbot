# parrbot.py
import os, random as rand
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

GUILD = os.getenv("DISCORD_GUILD")

intent = discord.Intents.default()

intent.reactions = True

intent.message_content = True


bot = commands.Bot(command_prefix ='$', intents= intent)

#this array holds usernames. 
UserArr = []

#allows user to prompt out of polly's shenanigans
@bot.event
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
@bot.event
async def on_ready():
     print(f'{bot.user.name}', "has connected to discord." '\n f{guild.name}(id: {guild.id})')


#this is for storing a random message from a user 
@bot.event
async def on_message(message):
     
     #if ctx.author == client.user:
     #     print ("huh")
     #     return
     pollychance = rand.randrange(1,10)
     print(pollychance)
     if message.content[0] == '!':
          return
     if pollychance == 1:     
          #stores message to a text file
          UserArr.append(str(message.content))
          await message.add_reaction('🦜')
     print(UserArr) 
     await bot.process_commands(message)
 
@bot.command()
async def ping(ctx):
    """Replies with Pong! and the bot's latency."""
    latency = round(bot.latency * 1000)  # Latency in milliseconds
    await ctx.send(f'Pong! {latency}ms')
                
#test
@bot.event
async def message(ctx, message):
     botMessage = (str(message.author), ' just said ', str(message.content))
     print(botMessage)
     
          
     await bot.process_commands(message)


#Random message getter 
@bot.command(name="Parrot", help='Sends a random message from a anonymous user.')
async def Parrot(ctx):
     parrottedmsg = "I haven't heard anything yet."
     if ctx.author == bot.user:
          return

     if not UserArr:
          await ctx.channel.send(parrottedmsg + " SQUAWK!")
          return

     else:
          randmsg = rand.randrange(0,len(UserArr))
          parrottedmsg = UserArr[randmsg]

     await ctx.channel.send(parrottedmsg + " SQUAWK!")
     
     


#stitches random messages together. (make sure that this happens at a space, and not inside of a word)
@bot.command(name="Stitch", help="Stitches two messages together.")
async def stitch(ctx):
     parrottedmsg = "I haven't heard enough stuff yet."
     frankmsg = ""
     if ctx.author == bot.user:
          return
          
     if not UserArr:
          await ctx.channel.send(parrottedmsg + " SQUAWK!")
          
     else:
          for i in range(2):
               if (len(UserArr) < i):
                    await ctx.channel.send("I don't have enough messages to stitch. SQUAWK!") 
                    return
               
               randmsg = rand.randrange(0,len(UserArr))
               frankPart = UserArr[randmsg].split(" ")
               frankmsg = frankmsg + " " + frankPart[rand.randrange(1, len(frankPart))]
     
     frankmsg = frankmsg + "."               
     await asyncio.sleep(rand.uniform(5,9))
     await ctx.channel.send(frankmsg+ " SQUAWK!")

#reverses a random users message
@bot.command(name="Reverse", help="Reverses a user's message.")
async def reversal(cxt, message: str=None):
     if message == None:
          await cxt.send("I need some info with the command. SQUAWK!")
          return
     await asyncio.sleep(rand.uniform(5,9))
     await cxt.send(message[::-1])


#tells how long a message is to shame chronic yappers
@bot.command (name="MSGLen", help="Returns the length of a message")
async def MSGLen(cxt, *, message:str=None):
     if message == None:
          await cxt.send("I need a message to take the length of. SQUAWK!")
          return
     await asyncio.sleep(rand.uniform(5,6))
     messagelength =("This message is "+  str(len(message)) + " characters long. SQUAWK!")
     await cxt.send(messagelength)


#repeats what the user passed to it.
@bot.command(name='Repeat', help="Repeats the message that you gave it.")
async def repeat(ctx, message):
     if message == None:
          ctx.send("I need a message to repeat. SQUAWK!")
     await asyncio.sleep(rand.uniform(3,4))
     await ctx.send(message)

bot.run(os.getenv("DISCORD_TOKEN"))
