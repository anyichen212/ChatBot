# bot.py
import os
import requests
import time
import datetime
import json

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from responses import get_response
from character import get_character
from others import get_rng_traits

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()
ME_ID = int(os.getenv('ME_ID'))
TOKEN = os.getenv('DISCORD_TOKEN')
VC_CHAT_ID = int(os.getenv('VC_CHAT_ID'))
VC_ID = int(os.getenv('VC_ID'))
SERVER_ID = int(os.getenv('SERVER_ID'))

# Custom help command
class CustomHelpCommand(commands.HelpCommand):

    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="MyoBot Commands", color=0x7289da)
        bot_cmds = [
            ["donate [amount]", "Add to the community fund!"],
            ["profile", "Get your OC profile!"],
            ["profile [name]", "Get OC profile by name"]
        ]

        vgValue = ""
        for cmd in bot_cmds:
            s = "**m!" + cmd[0] + "** : " + cmd[1] + "\n"
            vgValue += s

        embed.add_field(
            name = "📖 VG General",
            value = vgValue,
            inline= False
        )

        embed.add_field(
            name = "📑 List",
            value = "*tbh...*",
            inline= False
        )

        rng_cmds = [
            ["character", "New Character generator!"],
            ["traits", "RNG a trait to hunt down!"]
        ]
        rngValue = ""
        for cmd in rng_cmds:
            s = "**m!" + cmd[0] + "** : " + cmd[1] + "\n"
            rngValue += s

        embed.add_field(
            name = "🎲 Others",
            value = rngValue,
            inline= False
        )
            
        channel = self.get_destination()  # this method is inherited from `HelpCommand`, and gets the channel in context
        await channel.send(embed=embed)
    
    async def send_cog_help(self, cog: commands.Cog):
        return await super().send_cog_help(cog)
    
    async def send_group_help(self, group):
        return await super().send_group_help(group)
    
    async def send_command_help(self, command):
        return await super().send_command_help(command)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='m!', intents=intents, help_command=CustomHelpCommand())
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
    me = await bot.fetch_user(int(ME_ID))
    await me.send("on")
    print(f"Start {bot.user}")

# shutdown command
@bot.command()
@commands.is_owner()
async def shut(ctx):
    await ctx.send(":sleeping:")
    await ctx.bot.close()

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
            

# time command - doesn't work
# @bot.command(brief="Get time, ex) 'Meet me at t:yy/mm/dd/hr/min/pm!")
# async def t(ctx, *message):
#     if not message:
#         currTime = "<t:" + str(int(time.time())) + ":f>"
#         await ctx.send("Current time is " + currTime)
#         return
    
#     mss = ""
#     for word in message:
#         # if start with t:, turn into unix code
#         if word.startswith("t:"):
#             try:
#                 extra = ""
#                 yy,mm,dd,hr,min,day = word[2:].split("/")

#                 if len(day) > 2:
#                     extra = day[2:]

#                 if hr == "12" and day.lower().startswith("am"):
#                     hr = "0"
#                 elif hr != "12" and day.lower().startswith("pm"):
#                     hr = int(hr) + 12

#                 dt = datetime.datetime( 2000+int(yy), int(mm), int(dd), int(hr), int(min))
#                 unix = int(time.mktime(dt.timetuple()))
#                 mss = mss + " <t:" + str(unix) + ":f>" + extra
#             except Exception as e:
#                 print(e)
#                 mss = mss + " " + word
#         else:
#             mss = mss + " " + word
    
    #resend the message after time is edit
#    await ctx.send(mss)
            

# random character generator
@bot.command(brief="randomly generates a character")
async def character(ctx):
    await ctx.reply(get_character())    
    

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


# random trait generator (vg)
@bot.hybrid_command(name="traits", description="Generate a trait to find.")
async def traits(ctx):
    trait = get_rng_traits()
    embed = discord.Embed(
            title="Look for...",
            description=trait, 
            color=0x7289da
            )

    await ctx.reply(embed=embed)  

"""
    Google Sheet setup
"""
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_ID = os.getenv("SHEET_ID") #"1aja-o-wPhztpV-oEJbJzuDLq7WkYjBZhlZOi4_yiY8o"
RANGE_NAME = "Sheet1!A1"

creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first time.
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()



"""
    server commands
"""
PAN_ID = os.getenv("PAN_ID")
TIER_CHANNEL_ID = int(os.getenv("TIER_CHANNEL_ID"))
def is_in_guild(guild_id):
    async def predicate(ctx):
        return ctx.guild and ctx.guild.id in [guild_id, ME_ID]
    return commands.check(predicate)

BOAT_TOKEN = os.getenv('BOAT_TOKEN')

@bot.command()
@is_in_guild(SERVER_ID)
async def secretguilddata(ctx):
    """super secret stuff"""
    await ctx.send('secret stuff')

@bot.command()
@commands.is_owner()
async def sync(ctx):
    print("sync command")
    await bot.tree.sync()
    await ctx.send('Command tree synced.')

@bot.command()
@commands.is_owner()
async def update(ctx):
    await updateData()
    await ctx.send("VG data update!!")


# Add community fund, log fund to sheet, fetch current fund from sheet
@bot.hybrid_command(name="donate", description="Add to the community fund!")
@app_commands.describe(amount='Amount added to the community fund')
async def donate(ctx, amount: int=None):

    if amount is None or amount <= 0:
        await ctx.reply("Error, set a positive number")
        return

    # get cash amount and make sure user has enough to give
    try:
        api = f"https://unbelievaboat.com/api/v1/guilds/{SERVER_ID}/users/{ctx.author.id}"
        res = requests.get(api,headers={"Authorization": BOAT_TOKEN})
        cash = res.json().get("cash")
        if cash < amount:
            await ctx.reply("You don't have enough money :(")
            return
    except Exception as e:
        await dmError("addcommnuityfunds - boat get cash", e)
        await ctx.reply("Error...")
        return e

    # add to sheet and take from boat
    try:
        # fetch from sheet
        sheetData = sheet.values().batchGet(
            spreadsheetId=SHEET_ID, 
            ranges=["[Log]Community!A:E", "[Log]Community!J2", "[Log]Community!I5:J"], 
        ).execute().get("valueRanges")
        # print(sheetData)

        logData = sheetData[0].get("values")
        total = sheetData[1].get("values")
        tiers = sheetData[2].get("values")
        
        player = ctx.author #ctx.author.name

        # updated community log
        values = [[player.name, amount]]
        body = {"values": values}
        range = "[Log]Community!A1" if len(logData[-1]) >= len(logData[0]) else "[Log]Community!E1"
        result = (
            sheet
            .values()
            .append(
                spreadsheetId=SHEET_ID,
                range=range,
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )

        # create embed text to send to player
        embed = discord.Embed(
            title=":coin: MUNZE ADDED!",
            description=f"{player.mention} added {amount} MUNZE to the community funds!", 
            color=0x7289da
            )
        
        total = int(total[0][0])
        newTotal = total + amount
        currWallet = cash - amount
        embed.add_field(name="Current Total", value=newTotal)
        embed.add_field(name="Your Wallet", value=currWallet)

        # check tier, if hit notify admin
        idx = 0
        while idx < len(tiers):
            tier_val = int(tiers[idx][1])
            tier = tiers[idx][0]
            if total < tier_val and newTotal > tier_val:
                await tierHit(tier)
                break
            idx += 1

        # remove cash from boat
        api = f"https://unbelievaboat.com/api/v1/guilds/{SERVER_ID}/users/{ctx.author.id}"
        res = requests.patch(api, json={'cash':amount*-1}, headers={
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": BOAT_TOKEN})
        
        # all's good, send embed to discord
        await ctx.reply(embed=embed)

    except HttpError as error:
        await dmError("addcommnuityfunds - httpE", error)
        await ctx.reply("Http Error")
        return error
    except Exception as e:
        await dmError("addcommnuityfunds - end", e)
        await ctx.reply("Error...")
        return e

async def tierHit(tier):
    desc = f"We Hit **Tier {tier}**!! 🎉🎉🎉"
    embed = discord.Embed(
        title="Community Update",
        description=desc, 
        color=0x7289da
        )
    commu_channel = bot.get_channel(TIER_CHANNEL_ID)
    await commu_channel.send(f"<@{PAN_ID}>", embed=embed)
    return

# Show character profile and stats
@bot.hybrid_command(name="profile", description="Check character profile!")
@app_commands.describe(name='character first name/title')
async def profile(ctx, name: str=None):
    #open and read json
    try:
        with open('vgData.json', 'r') as file:
            data = json.load(file)
        
        charaKey = data["key"]
        chara = charaKey[name.lower()] if name else str(ctx.author.id)
    except Exception as e:
        await ctx.reply(f"'{name}' doesn't exist :/")
        return e
    
    try:
        mun = data[chara]["mun"]
        em_name = data[chara]["name"]
        title = f"🪪 {em_name}"
        footer = f"Mun @ {mun}"
        embed = discord.Embed(
            title=title,
            color=0x7289da,
        )
        embed.set_footer(text=footer)

        occupation = data[chara]["occupation"]
        embed.add_field(
            name=f"Role: {occupation}", 
            value="```> > > PROFILE...              ```", 
            inline=False
            )
        embed.add_field(
            name="AGE : ", 
            value=data[chara]["age"], 
            inline=True
            )
        embed.add_field(
            name="HEIGHT :", 
            value=data[chara]["height"], 
            inline=True
            )
        embed.add_field(
            name="PRONOUNS : ", 
            value=data[chara]["pronouns"], 
            inline=True
            )
        story = data[chara]["story"]
        embed.add_field(
            name=f"「*{story}*」", 
            value="```> > > STATS...              ```", 
            inline=False
            )
        embed.add_field(
            name="STR : ", 
            value=data[chara]["str"], 
            inline=True
            )
        embed.add_field(
            name="DEX : ", 
            value=data[chara]["dex"], 
            inline=True
            )
        embed.add_field(
            name="MAG : ", 
            value=data[chara]["mag"], 
            inline=True
            )
        embed.add_field(
            name="INT : ", 
            value=data[chara]["int"], 
            inline=True
            )
        embed.add_field(
            name="CHA : ", 
            value=data[chara]["cha"], 
            inline=True
            )
        embed.add_field(
            name="-",
            value="...", 
            inline=True
            )
        await ctx.reply(embed=embed)
    except Exception as e:
        await dmError("Profile - format and sent - ", e)
        await ctx.reply("Error...")
        return e

# update vgData.json data
async def updateData():
    sheetData = sheet.values().get(
        spreadsheetId=SHEET_ID, 
        range="[Log]Villagerdata!A3:O" 
    ).execute().get("values")

    for i,val in enumerate(sheetData[0]):
        new_val = val.split('.')[0]
        new_val = new_val.lower()
        sheetData[0][i] = new_val

    idx = 1
    sheet_len = len(sheetData)
    data = {"key":{}}
    while idx < sheet_len:
        chara_data = {}
        for i,val in enumerate(sheetData[0]):
            chara_data[val] = sheetData[idx][i]

        data["key"][chara_data["name"].lower()] = chara_data["id"]
        data["key"][chara_data["first name"].lower()] = chara_data["id"]
        data["key"][chara_data["alias"].lower()] = chara_data["id"]

        data[chara_data["id"]] = chara_data
        idx += 1
    with open("vgData.json", mode="w", encoding="utf-8") as write_file:
        json.dump(data, write_file, indent=4)
    
    return True

# errors
async def dmError(command, e):
    me = await bot.fetch_user(ME_ID)
    await me.send(f"Error in ${command}: \n ${e}")

bot.run(TOKEN)