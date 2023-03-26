from operator import index
from bson import Timestamp
import nextcord
from nextcord.ext import commands, tasks, application_checks, menus
from nextcord import File, ButtonStyle, SlashOption, ChannelType, Interaction, Button
from nextcord.utils import find, get
from nextcord.abc import GuildChannel
from nextcord.ui import View, Button
import os, random
import datetime
import time
from datetime import datetime
import pprint
from itertools import cycle
import pymongo
import requests
from paginator import MyEmbedFieldPageSource, CustomButtonMenuPages
from bs4 import BeautifulSoup
import aiohttp
from googletrans import Translator
import asyncio
from PIL import Image, ImageDraw, ImageFont, ImageColor
from dotenv import load_dotenv
import pymongo


load_dotenv()
bot_token = ''

client = pymongo.MongoClient("")
db = client.discord

#database
claims = db.claims



embed_colour = 0xff0004
guild_id = 968527802569719888
intents = nextcord.Intents.all()
tick = "<:o_Tick:993073417446228039>"
announcement = "<:o_Announcement:993073166408745040>"
arrow = "<:o_arrow:991606565754904627>"
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('>'),
    case_insensitive=True,
    owner_id=769608367030403132,
    intents=nextcord.Intents.all()
)

statuses = cycle(['>help'])

@tasks.loop(seconds=15.0)
async def status_change():
    await bot.wait_until_ready()
    status = next(statuses)
    guild = bot.get_guild(968527802569719888)
    users = guild.member_count
    if status == 'ab':
        status = f'{users} people in Cluz\'s World!'

    await bot.change_presence(
        activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=status),
        status=nextcord.Status.do_not_disturb
    )

@bot.event
async def on_ready():
    print('Logged in as {}'.format(bot.user))
    status_change.start()
    
@bot.command(name='Ping')
async def ping(ctx):
    latency = round(bot.latency*1000, 4)
    embed = nextcord.Embed(title="Ping", description=f'the bot\'s ping is **{latency}** ms.', color=embed_colour)
    await ctx.send(embed=embed, reference=ctx.message, mention_author=False)

@bot.slash_command(name='ping', description='Shows the bot\'s ping', guild_ids=[guild_id])
async def ping(interaction:Interaction):
    latency = round(bot.latency*1000, 4)
    embed = nextcord.Embed(title="Ping", description=f'the bot\'s ping is **{latency}** ms.', color=embed_colour)
    await interaction.response.send_message(embed=embed)

@bot.command(aliases=['vl'])
@commands.has_any_role(968530743699587153, 971765595169247312)
async def viewlock(ctx, channel:nextcord.TextChannel=None, role:nextcord.Role=None):
    if not channel:
        channel = ctx.channel
    if role:
        guild = ctx.guild
        everyone_role = nextcord.utils.get(ctx.guild.roles, id=968527802569719888)
        overwrites = channel.overwrites
        overwrite_dict = {
            role: nextcord.PermissionOverwrite(view_channel=False),
            everyone_role: nextcord.PermissionOverwrite(view_channel=False)
            }
        overwrite_dict.update(overwrites)
        await channel.edit(overwrites=overwrite_dict)
        await ctx.send(f'{tick} viewlocked {channel.mention}')
    else:
        guild = ctx.guild
        everyone_role = nextcord.utils.get(ctx.guild.roles, id=971688570307883028)
        overwrites = channel.overwrites
        overwrite_dict = {
            everyone_role: nextcord.PermissionOverwrite(view_channel=False)
            }
        overwrite_dict.update(overwrites)
        await channel.edit(overwrites=overwrite_dict)
        await ctx.send(f'{tick} viewlocked {channel.mention}')

@bot.command(aliases=['uvl'])
@commands.has_any_role(968530743699587153, 971765595169247312)
async def unviewlock(ctx, channel:nextcord.TextChannel=None, role:nextcord.Role=None):
    if not channel:
        channel = ctx.channel
    if role:
        guild = ctx.guild
        everyone_role = nextcord.utils.get(ctx.guild.roles, id=968527802569719888)
        overwrites = channel.overwrites
        overwrite_dict = {
            role: nextcord.PermissionOverwrite(view_channel=True),
            everyone_role: nextcord.PermissionOverwrite(view_channel=False)
            }
        overwrite_dict.update(overwrites)
        await channel.edit(overwrites=overwrite_dict)
        await ctx.send(f'{tick} unviewlocked {channel.mention}')
    else:
        guild = ctx.guild
        everyone_role = nextcord.utils.get(ctx.guild.roles, id=971688570307883028)
        overwrites = channel.overwrites
        overwrite_dict = {
            everyone_role: nextcord.PermissionOverwrite(view_channel=True)
            }
        overwrite_dict.update(overwrites)
        await channel.edit(overwrites=overwrite_dict)
        await ctx.send(f'{tick} unviewlocked {channel.mention}')

@bot.command(aliases=['l'])
@commands.has_any_role(968530743699587153, 971765595169247312)
async def lock(ctx, channel:nextcord.TextChannel=None, role:nextcord.Role=None):
    if not channel:
        channel = ctx.channel
    if role:
        guild = ctx.guild
        everyone_role = nextcord.utils.get(ctx.guild.roles, id=968527802569719888)
        await channel.set_permissions(role, send_messages=False)
        await ctx.send(f'{tick} locked {channel.mention}')
    else:
        guild = ctx.guild
        everyone_role = nextcord.utils.get(ctx.guild.roles, id=971688570307883028)
        await channel.set_permissions(everyone_role, send_messages=False)
        await ctx.send(f'{tick} locked {channel.mention}')

@bot.command(aliases=['ul'])
@commands.has_any_role(968530743699587153, 971765595169247312)
async def unlock(ctx, channel:nextcord.TextChannel=None, role:nextcord.Role=None):
    if not channel:
        channel = ctx.channel
    if role:
        guild = ctx.guild
        everyone_role = nextcord.utils.get(ctx.guild.roles, id=968527802569719888)
        await channel.set_permissions(role, send_messages=True)
        await ctx.send(f'{tick} unlocked {channel.mention}')
    else:
        guild = ctx.guild
        everyone_role = nextcord.utils.get(ctx.guild.roles, id=971688570307883028)
        await channel.set_permissions(everyone_role, send_messages=True)
        await ctx.send(f'{tick} unlocked {channel.mention}')
            
@bot.command(name='Purge', aliases=['clear', 'p'])
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount:int):
    if amount > 1000:
        await ctx.send(f'Too many messages given, {amount}/1000')
    else:
        amt = amount + 1
        members = {}
        msgs = await ctx.channel.history(limit=amt).flatten()
        deleted = 0
        for msg in msgs:
            if str(msg.author) in members:
                members[str(msg.author)] += 1
            else:
                members[str(msg.author)] = 1
            deleted += 1
        if members[str(ctx.message.author)] == 1:
            members.pop(str(ctx.message.author))
        elif members[str(ctx.message.author)] > 1:
            members[str(ctx.message.author)] = members[str(ctx.message.author)] - 1
        final_list = []
        for x,y in members.items():
            final_list.append(f'**{x}**: {y}')
        string = '\n'.join(final_list)
        e = nextcord.Embed(
            title=f'**{deleted}** messages deleted',
            description=string,
            colour=embed_colour
        )
        await ctx.channel.purge(limit=amt)
        await ctx.send(embed=e, delete_after=7.0)

@bot.event
async def on_presence_update(before,after):
    role = before.guild.get_role(968541157359501392)
    channel = bot.get_channel(971794391561809960)
    if role not in after.roles and '/cluz' in str(after.activity):
        await after.add_roles(role)
        await channel.send(f'Added Supporter role to {after.name}#{after.discriminator} ({after.id}). Their status: `{after.activity}`')
    elif role in after.roles and '/cluz' not in str(after.activity):
        await after.remove_roles(role)
        await channel.send(f'Remove Supporter role from {after.name}#{after.discriminator} ({after.id}). Their status: `{after.activity}`')
    else:
        pass

@bot.event
async def on_member_update(before,after):
    role = before.guild.get_role(968541157359501392)
    channel = bot.get_channel(971794391561809960)
    if role not in after.roles and '/cluz' in str(after.activity):
        await after.add_roles(role)
        await channel.send(f'Added Supporter role to {after.name}#{after.discriminator} ({after.id}). Their status: `{after.activity}`')
    elif role in after.roles and '/cluz' not in str(after.activity):
        await after.remove_roles(role)
        await channel.send(f'Remove Supporter role from {after.name}#{after.discriminator} ({after.id}). Their status: `{after.activity}`')
    else:
        pass

def bot_check(m):
    return m.author.bot == True

@bot.event
async def on_message(message):
    if message.type == nextcord.MessageType.premium_guild_subscription:
        embed = nextcord.Embed(
            color=embed_colour,
            title='We have a new booster!',
            description=f'Thanks for boosting {message.author.mention}! We have now reached {message.guild.premium_subscription_count}'
        )
        await message.channel.send(embed=embed)
    
    content = message.content
    if '<@955055683722706985>' in message.content:
        await message.reply('Hey, My prefix is `>` or `@Cluz\'s Utilities` .')
    guild = message.guild
    staff = guild.get_role(968530717694914580)
    
    supporter = guild.get_role(968541157359501392)
    booster = guild.get_role(968527991099494432)
    claimtime = {
        supporter:5,
        booster:10,
    }
    if message.content.startswith("!greroll") or message.content.startswith("a!greroll") or message.content.startswith("g!greroll"):
        if staff in message.author.roles:
            def check(m):
                return m.author.bot == True
            try:
                msg = await bot.wait_for("message", timeout=10.0, check=check)
            except asyncio.exceptions.TimeoutError:
                pass
            winners = msg.mentions
            for winner in winners:
                claim = 10
                
                for role, extratime in claimtime.items():
                     if role in winner.roles:
                         claim = claim + extratime
                creation = winner.created_at
                create = round(creation.timestamp())

                embed = nextcord.Embed(
                    colour=embed_colour, 
                    title=f"Congratulation {winner.name}!", 
                    description=f"{arrow} You have won the giveaway! Dm {message.author.mention} in **{claim}** seconds to claim your prize.\n{arrow} **{winner.name}**'s account was created on <t:{create}:D> which was <t:{create}:R>")
                embed.set_thumbnail(url=message.guild.icon)

                await message.channel.send(embed=embed)



    

    else:
        await bot.process_commands(message)
       
@bot.command(name='timedif', aliases=['snowflake', 'timediff'])
async def timedif(ctx, id1, id2=None):
    if id2 is None and ctx.message.reference is not None:
        id2 = ctx.message.reference.message_id
    try:
        id1 = int(id1)
        id2 = int(id2)
        
    except:
        await ctx.reply("Check your message ID's! They are incorrect!")
    
    
        
    time1 = nextcord.utils.snowflake_time(id=id1)
    time2 = nextcord.utils.snowflake_time(id=id2)
    ts1 = round(time1.timestamp())
    ts2 = round(time2.timestamp())
    
    ts_diff = time2 - time1
    secs = abs(ts_diff.total_seconds())
    days,secs=divmod(secs,secs_per_day:=60*60*24)
    hrs,secs=divmod(secs,secs_per_hr:=60*60)
    mins,secs=divmod(secs,secs_per_min:=60)
    secs=round(secs, 3)
    answer='{} secs'.format(secs)
    
    if mins > 0:
        answer = f'{int(mins)} mins {secs} secs'
    if hrs > 0:
        answer = f'{int(hrs)} hrs {int(mins)} mins {secs} secs'
    if days > 0:
        answer = f'{int(days)} days {int(hrs)} hrs {int(mins)} mins {secs} secs'



    
    embed = nextcord.Embed(title=answer, colour=embed_colour)
    embed.set_thumbnail(url=ctx.guild.icon)
    embed.add_field(name=f'{id1}',value=f'<t:{ts1}:R>', inline=False)
    embed.add_field(name=f'{id2}',value=f'<t:{ts2}:R>', inline=False)
    await ctx.send(embed=embed, reference=ctx.message, mention_author=False)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.reply("Invalid arguements.")
    else:
        raise error

@bot.command()
async def timestamp(ctx,*,time):
    pos = ["s", "m", "h", "d"]
    units = {'s':1, 'm':60, 'h':3600, 'd':86400}
    unit = time[-1]
    final_time = time[:-1]
    if unit not in pos:
        await ctx.send(f"Invalid unit. Please add `s,m,h,d` as a unit.")
        print("error")
    else:
        try:
            val = int(final_time)
            final_val = val*units[unit]

        except ValueError:
            await ctx.send("Please enter an integer followed by a unit. Use `s,m,h,d` as a unit.")
            print("Error")
    guildicon = ctx.guild.icon
    date = datetime.now()
    timestamp_now = round(date.timestamp())
    final_timestamp = timestamp_now + final_val

    embed = nextcord.Embed(colour=embed_colour, title="Timestamp")
    embed.set_thumbnail(url=ctx.guild.icon)
    embed.add_field(name="Short Time", value=f"<t:{final_timestamp}:t> ```<t:{final_timestamp}:t>```", inline=True)
    embed.add_field(name="Long Time", value=f"<t:{final_timestamp}:T> ```<t:{final_timestamp}:T>```", inline=True)
    embed.add_field(name="Date", value=f"<t:{final_timestamp}:d> ```<t:{final_timestamp}:d>```", inline=True)
    embed.add_field(name="Long Date", value=f"<t:{final_timestamp}:D> ```<t:{final_timestamp}:D>```", inline=True)
    embed.add_field(name="Short Date and Time", value=f"<t:{final_timestamp}:f> ```<t:{final_timestamp}:f>```", inline=True)
    embed.add_field(name="Long Date and Time", value=f"<t:{final_timestamp}:F> ```<t:{final_timestamp}:F>```", inline=True)
    embed.add_field(name="Relative Time", value=f"<t:{final_timestamp}:R> ```<t:{final_timestamp}:R>```", inline=True)

    await ctx.send(embed=embed)

@bot.slash_command(description='Gives you a timestamp', guild_ids=[guild_id])
async def timestamp(interaction:Interaction, time:str = SlashOption(name='time', description='the user whose info i should fetch!', required=True)):
    pos = ["s", "m", "h", "d"]
    units = {'s':1, 'm':60, 'h':3600, 'd':86400}
    unit = time[-1]
    final_time = time[:-1]
    if unit not in pos:
        await interaction.response.send_message(f"Invalid unit. Please add `s,m,h,d` as a unit.")
        print("error")
    else:
        try:
            val = int(final_time)
            final_val = val*units[unit]

        except ValueError:
            await interaction.response.send_message("Please enter an integer followed by a unit. Use `s,m,h,d` as a unit.")
            print("Error")
    guildicon = interaction.guild.icon
    date = datetime.now()
    timestamp_now = round(date.timestamp())
    final_timestamp = timestamp_now + final_val

    embed = nextcord.Embed(colour=embed_colour, title="Timestamp")
    embed.set_thumbnail(url=guildicon)
    embed.add_field(name="Short Time", value=f"<t:{final_timestamp}:t> ```<t:{final_timestamp}:t>```", inline=True)
    embed.add_field(name="Long Time", value=f"<t:{final_timestamp}:T> ```<t:{final_timestamp}:T>```", inline=True)
    embed.add_field(name="Date", value=f"<t:{final_timestamp}:d> ```<t:{final_timestamp}:d>```", inline=True)
    embed.add_field(name="Long Date", value=f"<t:{final_timestamp}:D> ```<t:{final_timestamp}:D>```", inline=True)
    embed.add_field(name="Short Date and Time", value=f"<t:{final_timestamp}:f> ```<t:{final_timestamp}:f>```", inline=True)
    embed.add_field(name="Long Date and Time", value=f"<t:{final_timestamp}:F> ```<t:{final_timestamp}:F>```", inline=True)
    embed.add_field(name="Relative Time", value=f"<t:{final_timestamp}:R> ```<t:{final_timestamp}:R>```", inline=True)

    await interaction.response.send_message(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    channel = ctx.channel
    new = await channel.clone(name=f"{channel.name}", reason=f"action by {ctx.author.name}")
    await channel.delete(reason=f"action by {ctx.author.name}")
    await new.edit(position=channel.position, reason=f"action by {ctx.author.name}")
    
    await new.send(f"Nuked by `{ctx.author}`")

@bot.slash_command(description='Deletes the channel and creates a new one with the same settings.', guild_ids=[guild_id])
@application_checks.has_permissions(administrator=True)
async def nuke(interaction:Interaction):
    channel = interaction.channel
    new = await channel.clone(name=f"{channel.name}", reason=f"action by {interaction.user}")
    await channel.delete(reason=f"action by {interaction.user.name}")
    await new.edit(position=channel.position)
    
    await new.send(f"Nuked by `{interaction.user}`")

@bot.slash_command(name="userinfo", description='Gives information about a user', guild_ids=[guild_id])
async def userinfo(interaction:Interaction, member:nextcord.Member=SlashOption(name='user', required=False, default=None)):
    if not member:
        member = interaction.user
    badge_dict = {
        'staff': '<:staff:978286671206432808>',
        'partner': '<:partner:978286850168979516>',
        'hypesquad': '<:hypesquad_events:978287051722080286>',
        'bug_hunter': '<:bug_hunter:978288472274137108>',
        'hypesquad_bravery': '<:hypesquad_bravery:978287234484670535>',
        'hypesquad_brilliance': '<:hypesquad_brilliance:978287332983734282>',
        'hypesquad_balance': '<:hypesquad_balance:978286962416959488>',
        'early_supporter': '<:early_supporter:978287457902661693>',
        'bug_hunter_level_2': '<:bug_hunter_level_2:978288106857975838>',
        'verified_bot_developer': '<:verified_bot_developer:978288304082522142>',
        'discord_certified_moderator': '<:discord_certified_moderator:978288379584217088>'
    }
    flags = member.public_flags.all()
    badges_list = []
    #[<UserFlags.hypesquad_balance: 256>]
    for badge in flags:
        badge = str(badge)
        badge = badge[10:]
        
        badge_list = badge.split(':')
        badge = badge_list[0]
        badges_list.append(badge)
        
    created = member.created_at
    created_timestamp = round(created.timestamp())
    roles = []
    for role in member.roles:
        roles.append(role.mention)
    
    roles.reverse()
    final_roles = ""
    for role in roles:
        final_roles += role
    
    badges = ''
    for badge1 in badges_list:
        emoji = badge_dict[badge1]
        badges += emoji

    pfp = member.avatar
    user = await bot.fetch_user(member.id)
    banner = user.banner
    print(banner)

    if pfp.is_animated() and banner!=None:
        nitro = '<:nitro_badge:978322685295747073>'
        boost = '<a:boost_badge:978356849336262788>'
        badges += nitro
        badges += boost
    elif pfp.is_animated() or banner!=None:
        nitro = '<:nitro_badge:978322685295747073>'
        badges += nitro
    else:
        pass
        
    
    if banner!=None and '<a:boost_badge:978356849336262788>' not in badges:
        boost = '<a:boost_badge:978356849336262788>'
        badges += boost
    else:
        pass

    status_dict = {
        'online': '<:online:978556987455467530> Online',
        'offline': '<:offline:978557243937157120> Offline',
        'idle': '<:idle:978556853061554186> Idle',
        'dnd': '<:do_not_disturb:978557127201271878> Do Not Disturb'
    }

    status1 = member.status
    status_name = str(status1)
    #print(status_name)
    status = status_dict[status_name]




        
    em = nextcord.Embed(description=f"{member.mention}", colour=embed_colour)
    em.set_author(icon_url=f"{member.avatar}",name=f"{member}")
    em.set_thumbnail(url=f"{member.avatar}")
    em.add_field(name="ID", value=f"{member.id}", inline=False)
    em.add_field(name="Badges", value=f"{badges}", inline=False)
    em.add_field(name="Status", value=f"{status}", inline=False)
    em.add_field(name="Created Date", value=f"<t:{created_timestamp}:F> ( <t:{created_timestamp}:R> )")
    em.add_field(name="Roles", value=f"{final_roles}", inline=False)
    #em.add_field(name='Perms', value=member.guild_permissions.all(), inline=False)
    if member.activity is not None:
        em.add_field(name="Activity", value=f"{member.activity.name}", inline=False)
    
    
    if banner!=None:
        em.set_image(url=banner.url)
    
    await interaction.response.send_message(embed=em)

@bot.command(name="userinfo", aliases=["ui", "whois", "info", 'user'])
async def userinfo(ctx, member:nextcord.Member=None):
    if not member:
        member = ctx.author
    badge_dict = {
        'staff': '<:staff:978286671206432808>',
        'partner': '<:partner:978286850168979516>',
        'hypesquad': '<:hypesquad_events:978287051722080286>',
        'bug_hunter': '<:bug_hunter:978288472274137108>',
        'hypesquad_bravery': '<:hypesquad_bravery:978287234484670535>',
        'hypesquad_brilliance': '<:hypesquad_brilliance:978287332983734282>',
        'hypesquad_balance': '<:hypesquad_balance:978286962416959488>',
        'early_supporter': '<:early_supporter:978287457902661693>',
        'bug_hunter_level_2': '<:bug_hunter_level_2:978288106857975838>',
        'verified_bot_developer': '<:verified_bot_developer:978288304082522142>',
        'discord_certified_moderator': '<:discord_certified_moderator:978288379584217088>'
    }
    flags = member.public_flags.all()
    badges_list = []
    #[<UserFlags.hypesquad_balance: 256>]
    for badge in flags:
        badge = str(badge)
        badge = badge[10:]
        
        badge_list = badge.split(':')
        badge = badge_list[0]
        badges_list.append(badge)
        
    if not member:
        member = ctx.author
    created = member.created_at
    created_timestamp = round(created.timestamp())
    roles = []
    for role in member.roles:
        roles.append(role.mention)
    
    roles.reverse()
    final_roles = ""
    for role in roles:
        final_roles += role
    
    badges = 'None'
    for badge1 in badges_list:
        emoji = badge_dict[badge1]
        badges += emoji

    pfp = member.avatar
    user = await bot.fetch_user(member.id)
    banner = user.banner

    if pfp.is_animated() and banner is not None:
        nitro = '<:nitro_badge:978322685295747073>'
        boost = '<a:boost_badge:978356849336262788>'
        badges += nitro
        badges += boost
    elif pfp.is_animated() or banner is not None:
        nitro = '<:nitro_badge:978322685295747073>'
        badges += nitro
    else:
        pass
        
    
    if banner is not None and '<a:boost_badge:978356849336262788>' not in badges:
        boost = '<a:boost_badge:978356849336262788>'
        badges += boost
    else:
        pass

    status_dict = {
        'online': '<:online:978556987455467530> Online',
        'offline': '<:offline:978557243937157120> Offline',
        'idle': '<:idle:978556853061554186> Idle',
        'dnd': '<:do_not_disturb:978557127201271878> Do Not Disturb'
    }

    status1 = member.status
    status_name = str(status1)
    status = status_dict[status_name]



        
    em = nextcord.Embed(description=f"{member.mention}", colour=embed_colour)
    em.set_author(icon_url=f"{member.avatar}",name=f"{member}")
    em.set_thumbnail(url=f"{member.avatar}")
    em.add_field(name="ID", value=f"{member.id}", inline=False)
    em.add_field(name="Badges", value=f"{badges}", inline=False)
    em.add_field(name="Status", value=f"{status}", inline=False)
    em.add_field(name="Created Date", value=f"<t:{created_timestamp}:F> ( <t:{created_timestamp}:R> )")
    em.add_field(name="Roles", value=f"{final_roles}", inline=False)
    if member.activity!=None:
        em.add_field(name="Activity", value=f"{member.activity.name}", inline=False)
    
    
    if banner!=None:
        em.set_image(url=banner.url)
    
    await ctx.send(embed=em)

class ReactRolesButtons(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Announcement Ping", style=nextcord.ButtonStyle.blurple, row=0, emoji=announcement)
    async def announcement_callback(self, button, interaction):
        role = interaction.guild.get_role(968822213597868062)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"removed {role.mention} role.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"added {role.mention} role.", ephemeral=True)
    
    @nextcord.ui.button(label="Nitro Giveaway Ping", style=nextcord.ButtonStyle.blurple, row=1, emoji='<:o_Boost:969103340438966332>')
    async def nitro_callback(self, button, interaction):
        role = interaction.guild.get_role(968822773055115304)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"removed {role.mention} role.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"added {role.mention} role.", ephemeral=True)
    @nextcord.ui.button(label="Crypto Giveaway Ping", style=nextcord.ButtonStyle.blurple, row=2, emoji='🪙')
    async def crypto_callback(self, button, interaction):
        role = interaction.guild.get_role(968823002068320256)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"removed {role.mention} role.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"added {role.mention} role.", ephemeral=True)
    @nextcord.ui.button(label="Poll Ping", style=nextcord.ButtonStyle.blurple, row=3, emoji='<:o_CatHm:969104794528665740>')
    async def Poll_callback(self, button, interaction):
        role = interaction.guild.get_role(968823147979739136)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"removed {role.mention} role.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"added {role.mention} role.", ephemeral=True)
    @nextcord.ui.button(label="Event Ping", style=nextcord.ButtonStyle.blurple, row=4, emoji='<:c_event:972094650015965204>')
    async def event_callback(self, button, interaction):
        role = interaction.guild.get_role(968823221346533450)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"removed {role.mention} role.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"added {role.mention} role.", ephemeral=True)


@bot.command()
@commands.is_owner()
async def reactroles(ctx):
    views = ReactRolesButtons()
    embed = nextcord.Embed(title="Ping Roles",
    colour=embed_colour,
    description=f"{announcement} ➤ <@&968822213597868062>\n> Get Pinged for all our announcements and stay Up to date! (recommended)\n\n<:o_Boost:969103340438966332> ➤ <@&968822773055115304>\n> Get Pinged for Nitro Giveaways! Dont miss out on this! (recommended)\n\n:coin: ➤ <@&968823002068320256>\n> Get pinged for crypto currency giveaways!\n\n<:o_CatHm:969104794528665740> ➤ <@&968823147979739136>\n> Take part in deciding the upcoming changes in the server! (recommended)\n\n<:c_event:972094650015965204> ➤ <@&968823221346533450>\n> Get pinged for fun events!"
    )
    embed.set_thumbnail(url=ctx.guild.icon)
    await ctx.send(
        content="All roles taken here are temporary and can be removed simply by reclicking the corresponding button! To Get any of the roles here, you have to react on the corresponding button.",
        embed=embed, 
        view=views
        )

captcha_characters = ["0","1","2","3","4","5","6","7","8","9"]

class verifybutton(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Verify", style=nextcord.ButtonStyle.green)
    async def verify_callback(self, button, interaction):
        role = interaction.guild.get_role(971688570307883028)
        captcha_chars = ""
        for i in range(6):
            letter = random.choice(captcha_characters)
            captcha_chars += letter
        channel = interaction.guild.get_channel(971692011788857345)
        
        
        thread = await channel.create_thread(name=f"{interaction.user.display_name}'s Verification", message=interaction.message, auto_archive_duration=60)
        await interaction.response.send_message("Thread created", ephemeral=True)
        await thread.add_user(interaction.user)
        
        
        img = Image.open("C:\\Users\\91984\\Documents\\python\\image.png")
        font = ImageFont.truetype("arial.ttf", 24)
        draw = ImageDraw.Draw(img)
        text = str(captcha_chars)
        #print(captcha_chars)
        int_captcha_chars = int(captcha_chars)
        #print(int_captcha_chars)
        x_captcha = random.randint(0,160)
        y_captcha = random.randint(0,160)
        draw.text((x_captcha,y_captcha), text, (0,0,0), font=font)
        img.save("text.png")
        

        emb = nextcord.Embed(
            colour=embed_colour,
            title="Complete this captcha to prove you are human.", 
            description="<:c_arrow:972039518540668968> Send the number below in the picture in order to gain access to the server.")
        emb.set_image(url="attachment://text.png")
        await thread.send(file=nextcord.File("text.png"), embed=emb)
        #await thread.send(file=nextcord.File("text.png"))

        def checks(m):
            return m.author.id == interaction.user.id

        try:
            captcha_result = await bot.wait_for("message", check=checks, timeout=120.0)
        except asyncio.TimeoutError:
            await thread.send(f"{interaction.user.mention} since you have not complete the captcha this thread will be closed in the next 10 seconds")
            await asyncio.sleep(10.0)
            await thread.delete() 
        #print(captcha_result)
        try:
            int_captcha = int(captcha_result.content)
            print("int successful")

        except:
             await thread.send(f"You have failed the verification {interaction.user.mention}. Please try again later.")
             await asyncio.sleep(3.0)
             await thread.delete()
             print("converting to int failed")
        print(int_captcha)
        if int_captcha == int_captcha_chars:
            await interaction.user.add_roles(role)
            await thread.send(f"Thanks for verifying {interaction.user.mention}.")
            await asyncio.sleep(2.0)
            await thread.delete()
        else:
            await thread.send(f"You have failed the verification {interaction.user.mention}. Please try again later.")
            await asyncio.sleep(3.0)
            await thread.delete()
            

@bot.command()
@commands.is_owner()
async def verify(ctx):
    view = verifybutton()
    data =     {
      "title": "Verify Yourself",
      "description": "<:c_arrow:972039518540668968> In order to verify, Click the green button below.\n<:c_arrow:972039518540668968> After that you will be added to a thread and i will send you a captcha. \n<:c_arrow:972039518540668968> Complete this captcha in less than 2 minutes or you will be kicked from the server.",
      "color": 11665663,
      "thumbnail": {
        "url": "https://images-ext-1.discordapp.net/external/Cj3m-NPd18MJxCN0mnqn97MELCxueFMAKJnnIcIeeRc/%3Fsize%3D1024/https/cdn.discordapp.com/icons/968527802569719888/a_d76af6a54a4a2abbabe0f17de40d305d.gif"
      }
    }
    em = nextcord.Embed.from_dict(data)
    await ctx.send(embed=em, view=view)

class TicketView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Create Ticket", style=nextcord.ButtonStyle.green, custom_id="0001")
    async def ticket_callback(self, button, interaction):
        ticket_number = int(button.custom_id)
        guild = interaction.guild
        moderator = interaction.guild.get_role(971765595169247312)
        everyone_role = interaction.guild.default_role
        overwrites = {
            moderator: nextcord.PermissionOverwrite(view_channel=True),
            everyone_role: nextcord.PermissionOverwrite(view_channel=False),
            interaction.user: nextcord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True)
        }
            
        ticket_category = nextcord.utils.get(interaction.guild.categories, id=973150022864633867)
        
        
        channel = await guild.create_text_channel(f"ticket-{ticket_number}", overwrites=overwrites, category=ticket_category, topic=f"{interaction.user.name} ({interaction.user.id})'s Ticket.")
        await interaction.response.send_message(f"Created your ticket. {channel.mention}", ephemeral=True)
        e = nextcord.Embed(
            colour=embed_colour, 
            description="Our Support team will be with you shortly. Please **DO NOT PING** anyone, if you ping anyone of our staff members Your ticket will be ignored."
        )
        e.set_thumbnail(url=interaction.guild.icon)
        await channel.send(f"{interaction.user.mention} Welcome!\nWe are sending help you way!\n<@&971765595169247312>", embed=e)
        new_tn = ticket_number + 1
        if new_tn < 10:
            final_tn = '000' + new_tn
        if new_tn < 100:
            final_tn = '00' + new_tn
        if new_tn < 1000:
            final_tn = '0' + new_tn

        
        button.custom_id = final_tn
        



@bot.command()
@commands.is_owner()
async def tickets(ctx):
    data =     {
      "title": "Ticket Support",
      "description": "<:c_arrow:972039518540668968> To create a ticket, Click the green button below.\n<:c_arrow:972039518540668968> Please do not ping anyone after opening your ticket, Our team will be there to assist you as soon as possible.",
      "color": 11665663,
      "thumbnail": {
        "url": "https://images-ext-1.discordapp.net/external/Cj3m-NPd18MJxCN0mnqn97MELCxueFMAKJnnIcIeeRc/%3Fsize%3D1024/https/cdn.discordapp.com/icons/968527802569719888/a_d76af6a54a4a2abbabe0f17de40d305d.gif"
      }
    }
    embed = nextcord.Embed.from_dict(data)
    views = TicketView()
    await ctx.send(embed=embed, view=views)

@bot.command()
@commands.has_any_role(968530743699587153, 968530717694914580, 971765595169247312)
async def close(ctx):
    channel = ctx.channel
    ticket_category = nextcord.utils.get(ctx.guild.categories, id=973150022864633867)
    if channel.category == ticket_category:
        await ctx.send(f"Closing {channel.mention}")
        moderator = ctx.guild.get_role(971765595169247312)
        everyone_role = ctx.guild.default_role
        overwrites = {
            moderator: nextcord.PermissionOverwrite(view_channel=True),
            everyone_role: nextcord.PermissionOverwrite(view_channel=False)
        }
        ticket_name = ctx.channel.name
        ticket_number = ticket_name[6:]
        await channel.edit(name=f"closed-{ticket_number}", overwrites=overwrites)
        await ctx.send("DONE!")
    else:
        await ctx.send("You can only close a ticket.")

@bot.command()
@commands.has_any_role(968530743699587153, 968530717694914580, 971765595169247312)
async def delete(ctx):
    channel = ctx.channel
    ticket_category = nextcord.utils.get(ctx.guild.categories, id=973150022864633867)
    if channel.category == ticket_category:
        await ctx.send(f"Deleting {channel.mention}")
        await asyncio.sleep(2.0)
        await channel.delete()  

@bot.slash_command(guild_ids=[guild_id])
async def invite(interaction:Interaction):
    pass
@invite.subcommand(name='info', description='Gives info about an invite')
async def info(interaction:Interaction, info:str=SlashOption(name='invite', required=True)):
    
    invite = await bot.fetch_invite(info, with_counts=True, with_expiration=True)

    #await interaction.response.send_message(type(invite))
    
    e = nextcord.Embed(
            colour=embed_colour,
            title=f"{invite.guild}",
            description=f'Member Count - **{invite.approximate_member_count}**\nOnline - **{invite.approximate_presence_count}**'
        )
    if invite.guild.description is not None:
        e.add_field(name='Description', value=f'{invite.guild.description}', inline=False)

    e.add_field(name='Channel', value=f'[{invite.channel.name}](https://discord.com/channels/{invite.channel.id})')
    e.add_field(name='Link', value=f'[{invite.code}]({invite})')
    e.add_field(name='Uses', value=invite.uses)
    e.add_field(name='Inviter', value=f'**{invite.inviter}**')
    e.add_field(name='Inviter ID', value=f'{invite.inviter.id}')
    e.add_field(name='Owner', value=f'{invite.guild.owner}')
    e.set_thumbnail(url=invite.guild.icon)
    if invite.guild.banner is not None:
        e.set_image(url=invite.guild.banner.url)
    await interaction.response.send_message(embed=e)
 
@bot.command(aliases=["inviteinfo"])
async def invite_info(ctx, invite:nextcord.Invite):
    if isinstance(invite, nextcord.Invite):
        pass
    else:
        await ctx.send("Send an invite please.")
    
    

    inv = str(invite)
    
    
    #created_at = invite.created_at
    #timestamp = created_at
    e = nextcord.Embed(
        colour=embed_colour,
        title=f"{invite.guild}",
    )
    
    e.add_field(name='Inviter', value=f'**{invite.inviter.name} ({invite.inviter.id})**')
    e.set_thumbnail(url=invite.guild.icon)
    await ctx.send(embed=e, reference=ctx.message, mention_author=False)

@bot.command(aliases=["ts"])
async def translate(ctx, *, content=None):
    ref = ctx.message.reference
    if isinstance(ref, nextcord.MessageReference) and not content:
        msg = ref.cached_message
        content = msg.content
    content = str(content)
    translator = Translator()
    language = translator.detect(content)
    lang = language.lang
    result = translator.translate(f'{content}', dest='en')
    LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
    }
    final_lang = LANGUAGES[lang]
    e = nextcord.Embed(title="Translator", colour=embed_colour)
    e.add_field(name=f'Language Detected = {final_lang}', value=f'{content}', inline=False)
    e.add_field(name=f'Translated To English', value=f'{result.text}', inline=False)

    await ctx.send(
        embed=e,
        reference=ctx.message,
        mention_author=False
        )

def get_code(code:str):
    if code.startswith('```') and code.endswith('```'):
        code = code[3:-3]
        if code.startswith('python'):
            code = code[6:]
        elif code.startswith('py'):
            code = code[2:]
        else:
            pass
    else:
        pass
    return code

@bot.command()
@commands.has_any_role(971765595169247312, 968530743699587153)
async def role(ctx, role:nextcord.Role, everyone:nextcord.Member='e'):
    guild = ctx.guild
    r = guild.get_role(968530743699587153)
    members = 0
    if everyone == 'e':
        if r in ctx.author.roles:
            msg = await ctx.send(f'Adding {role.name} to everyone.')
            time = datetime.now()
            ts = time.timestamp()


            for member in guild.members:
                
                await member.add_roles(role)
                members += 1
            time2 = datetime.now()
            ts2 = time2.timestamp()
            results = ts2 - ts
            result = round(results, 3)
            await msg.edit(f'{tick} added {role.name} to {members} members. It took {result} seconds.')
            return
               
                
        else:
            await ctx.send(f'You can\'t use this.')
            return
    else:
        
            
        await everyone.add_roles(role)
        await ctx.send(f'{tick} added {role.name} to {everyone.name}')



@bot.command(name='cryptolb', aliases=['lbcrypto', 'lb crypto', 'crypto lb'])
async def cryptolb(ctx):
    response = requests.get('https://www.coingecko.com/').text
    soup = BeautifulSoup(response, 'html.parser')
    table_ = soup.find('table', {'class': 'sort table mb-0 text-sm text-lg-normal table-scrollable'}).find('tbody')
    trs_list = table_.find_all('tr')

    

    embed_fields = []


    for index_, tr in enumerate(trs_list):
        spans = tr.find_all('span')
        name_ = tr.find('span', {'class': 'lg:tw-flex font-bold tw-items-center tw-justify-between'}).get_text().strip()
        #<span class="lg:tw-flex font-bold tw-items-center tw-justify-between">Bitcoin</span>
        symbol_ = spans[1].get_text().strip()
        #<span class="d-lg-inline font-normal text-3xs tw-ml-0 md:tw-ml-2 md:tw-self-center tw-text-gray-500 dark:tw-text-white dark:tw-text-opacity-60">BTC</span>
        price = tr.find('span', {'class': 'no-wrap'}).get_text().strip()
        change_1h = tr.find('td', {'class': 'td-change1h change1h stat-percent text-right col-market'}).get_text().strip()
        change_24h = tr.find('td', {'class': 'td-change24h change24h stat-percent text-right col-market'}).get_text().strip()
        Marketcap = tr.find('td', {'class': 'td-market_cap cap col-market cap-price text-right'}).get_text().strip()

        #print(name_ + ' '+  symbol_ + '  ' + price + ' ' + change_1h + ' ' + change_24h + '  ' + Marketcap)
        info = f'{index_ + 1}. {name_} ({symbol_})'
        
        info_value = f'PRICE : **{price}**\nCHANGE IN 1 HOUR: **{change_1h}**, CHANGE IN 24 HOURS: **{change_24h}**\nMARKET CAP: **{Marketcap}**'
        embed_fields.append((info, info_value))
        
        
    
    pages = menus.ButtonMenuPages(
        source=MyEmbedFieldPageSource(embed_fields),
        disable_buttons_after=True,
    )
    await pages.start(ctx)

@bot.slash_command(guild_ids=[guild_id])
async def crypto(interaction:Interaction):
    pass

@crypto.subcommand(description='shows the information about the top crypto currencies.')
async def leaderboard(interaction:Interaction):
    await interaction.response.defer()
    response = requests.get('https://www.coingecko.com/').text
    soup = BeautifulSoup(response, 'html.parser')
    table_ = soup.find('table', {'class': 'sort table mb-0 text-sm text-lg-normal table-scrollable'}).find('tbody')
    trs_list = table_.find_all('tr')

    

    embed_fields = []

    for index_, tr in enumerate(trs_list):
        spans = tr.find_all('span')
        name_ = tr.find('span', {'class': 'lg:tw-flex font-bold tw-items-center tw-justify-between'}).get_text().strip()
        #<span class="lg:tw-flex font-bold tw-items-center tw-justify-between">Bitcoin</span>
        symbol_ = spans[1].get_text().strip()
        #<span class="d-lg-inline font-normal text-3xs tw-ml-0 md:tw-ml-2 md:tw-self-center tw-text-gray-500 dark:tw-text-white dark:tw-text-opacity-60">BTC</span>
        price = tr.find('span', {'class': 'no-wrap'}).get_text().strip()
        change_1h = tr.find('td', {'class': 'td-change1h change1h stat-percent text-right col-market'}).get_text().strip()
        change_24h = tr.find('td', {'class': 'td-change24h change24h stat-percent text-right col-market'}).get_text().strip()
        Marketcap = tr.find('td', {'class': 'td-market_cap cap col-market cap-price text-right'}).get_text().strip()



 

        #print(name_ + ' '+  symbol_ + '  ' + price + ' ' + change_1h + ' ' + change_24h + '  ' + Marketcap)
        info = f'{index_ + 1}. {name_} ({symbol_})'
        
        info_value = f'PRICE : **{price}**\nCHANGE IN 1 HOUR: **{change_1h}**, CHANGE IN 24 HOURS: **{change_24h}**\nMARKET CAP: **{Marketcap}**'
        embed_fields.append((info, info_value))
        
        
    
    pages = menus.ButtonMenuPages(
        source=MyEmbedFieldPageSource(embed_fields),
        disable_buttons_after=True,
    )
    await pages.start(interaction=interaction)

@bot.command(name='Calculate', aliases=['calc'])
async def calc(ctx, *, code:str):
    ans = eval(code)
    await ctx.reply(ans)


@bot.slash_command(name='calculate', guild_ids=[guild_id])
async def calc_slash(interaction:Interaction, code:str=SlashOption(name='expression', description='the expression you want to calculate', required=True)):
    ans = eval(code)
    await interaction.response.send_message(ans)





bot.load_extension('jishaku')
bot.run(bot_token)



