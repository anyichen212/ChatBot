# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from responses import get_response

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
VC_CHAT_ID = int(os.getenv('VC_CHAT_ID'))
VC_ID = int(os.getenv('VC_ID'))


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='myo!', intents=intents)
mute = False
#bot = discord.bot(intents=intents)

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Yes",style=discord.ButtonStyle.gray,emoji="🔇")
    async def gray_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        button.disabled=True
        vcChat = bot.get_channel(VC_ID)
        await vcChat.set_permissions(vcChat.guild.roles[0], speak=False)
        await interaction.response.edit_message(content="Mute Party! Lmk with ``myo!unmute`` if you want to unmute vc!", view=None)
        for member in vcChat.members:
            await member.move_to(vcChat)
        
    @discord.ui.button(label="No",style=discord.ButtonStyle.blurple,emoji="🎵")
    async def blurple_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        button.disabled=True
        vcChat = bot.get_channel(VC_ID)
        await vcChat.set_permissions(vcChat.guild.roles[0], speak=None)
        await interaction.response.edit_message(content="Not Muted Party! Lmk with ``myo!mute`` if you want to mute vc!", view=None)
        for member in vcChat.members:
            await member.move_to(vcChat)
    
    @discord.ui.button(label="Cancel",style=discord.ButtonStyle.red)
    async def red_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        button.disabled=True
        await interaction.response.edit_message(content=":3", view=None)

# start bot
@bot.event
async def on_ready():
    print(f"Start {bot.user}")

# voice chat state
@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel and after.channel and after.channel.name == "Quiet VC" and len(after.channel.members) == 1:
        # print(f'{member.display_name} has joined the vc')
        view = Buttons()
        quietChat = bot.get_channel(VC_CHAT_ID)
        await quietChat.send(f'<@{member.id}> Mute Party?', view=view)
    else:
        pass

@bot.command(brief='Fully mute quiet vc')
async def mute(ctx):
    vcChat = bot.get_channel(VC_ID)
    await vcChat.set_permissions(vcChat.guild.roles[0], speak=False)
    await ctx.send("Quiet VC is now fully muted!")
    for member in vcChat.members:
            await member.move_to(vcChat)

@bot.command(brief='Unmute quiet vc')
async def unmute(ctx):
    vcChat = bot.get_channel(VC_ID)
    await vcChat.set_permissions(vcChat.guild.roles[0], speak=None)
    await ctx.send("Quiet VC is not muted anymore!")
    for member in vcChat.members:
            await member.move_to(vcChat)

# chat command
async def send_message(message, userMessage):
    # if not userMessage:
    #     print("message is empty likely bc intents were not enable")
    #     return
    
    #isPrivate = userMessage[0] == '?'

    #if isPrivate:
        #userMessage = userMessage[1:]

    try:
        response = get_response(userMessage)
        #if isPrivate:
            #await message.author.send(response)  
        #else:
            
        await message.channel.send(response)
    except Exception as e:
        print(e)

@bot.command(brief='uhhhh ya...')
async def chat(ctx, * , message=''):
    print(message)
    #user = str(ctx.author)
    #channel = str(ctx.channel)

    #print(f'[{channel}] {user}: "{message}"')
    
    await send_message(ctx,message)

# shutdown command
@bot.command()
@commands.is_owner()
async def shut(ctx):
    await ctx.send(":sleeping:")
    await ctx.bot.close()

bot.run(TOKEN)