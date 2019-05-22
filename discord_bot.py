import asyncio
import discord
from discord.ext import commands
import random
import feedparser
import html2text
import re
from datetime import datetime
import time

import Discord_Bot.discor_config as cfg

from Discord_Bot.google_sheet import *

bot = commands.Bot(command_prefix='!!', description='A bot that greets the user back.')
client = discord.Client()

class Slapper(commands.Converter):
    async def convert(self, ctx, argument):
        to_slap = random.choice(ctx.guild.members)

        return '{0.author} slapped <@{1}> because *{2}*'.format(ctx, to_slap.id, argument)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')




@bot.command()
async def LovePotion(ctx, a: str):
    if a == "%":
        title, table = icy_epi_test()
        await ctx.send(f"{title}")
    elif a == "Total":
        title, table = icy_epi_test()
        await ctx.send(f"{title}\n```\n{table}```")

@bot.command()
async def NewsFeed(ctx):
    NewsFeed = feedparser.parse("http://forums.playredfox.com/index.php?forums/announcements.11/index.rss")
    h = html2text.HTML2Text()
    h.ignore_links = False
    for entry in NewsFeed.entries[0:5]:
        if "summary" in entry.keys():
            text = h.handle(re.sub(r'<a href(.+?)</a>', "", entry.summary.split("<br />", 1)[1]))
            await ctx.send(f"{entry.title}\n```{text}\n```")

@bot.command()
async def KunlunDeco(ctx, a: int):
    decoTable = ['Summary!M4:Q19', 'Summary!H13:K18', 'Summary!H21:K28', 'Summary!H31:K38', 'Summary!H41:K52']
    if a != 0:
        title = "**Items needed to make a lvl {0} Kunlun Deco.**".format(a)
    else:
        title = "**Items needed to make a lvl {0} Kunlun Deco from all the materials.**".format(a)
    table, note = kunlun_deco(decoTable[a])
    if a == 4 or a == 0:
        await ctx.send(f"{title}\n```\n{table}\n{note}```")
    else:
        await ctx.send(f"{title}\n```\n{table}\n```")

@bot.command()
async def slap(ctx, *, reason: Slapper):
    await ctx.send(reason)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="9Dragons Bot", description="The list of services, commands and their uses:", color=0xeee657)
    embed.add_field(name="SERVICES:",value="All the services", inline=False)
    embed.add_field(name="Newsfeed", value="This service will check for news updates on the Redfox Forum and send "
                                           "them to the <#Newsfeed> channel.", inline=False)


    embed.add_field(name="COMMANDS:",value="All the commands", inline=False)
    embed.add_field(name="!!help", value="Gives this message", inline=False)
    embed.add_field(name="!!LovePotion <argument>", value="<argument> can be [%, Total]. It shows the progress for "
                                                          "the Love epithet.", inline=False)
    embed.add_field(name="!!KunlunDeco <argument>", value="<argument> can be between 0 and 4. Where 0 is the total "
                                                          "cost to make a level 4 deco.")


    await ctx.send(embed=embed)


async def newsFeed_background_task():
    await bot.wait_until_ready()

    while not bot.is_closed():
        NewsFeed = feedparser.parse("http://forums.playredfox.com/index.php?forums/announcements.11/index.rss")
        channel = bot.get_channel(cfg.bot["NewsFeed Channel ID"])
        h = html2text.HTML2Text()
        h.ignore_links = False

        for entry in reversed(NewsFeed.entries[0:5]):
            file_obj = open("StoredNews", "r")

            # TESTING
            file_obj_1 = open("RSS-feed", "a")
            file_obj_1.write(f"{entry.keys()} \n"
                             f"{entry.title} \n"
                             f"{entry.link} \n")
            file_obj_1.close()



            # END OF TESTING
            time_1 = datetime.fromtimestamp(time.mktime(entry.published_parsed[:8] + (-1,)))
            print(time_1, entry.title)
            # TODO: write timestamp to file and check if is newer.
            date_from_file = file_obj.readline()
            file_obj.close()
            file_obj = open("StoredNews", "w")

            print("DF:", date_from_file)

            # If no date print news ...
            if date_from_file == "":
                file_obj.write(str(time_1))
            else:
                d1 = datetime.strptime(date_from_file, "%Y-%m-%d %H:%M:%S")
                if datetime.fromtimestamp(time.mktime(entry.published_parsed[:8] + (-1,))) > d1:
                    file_obj.write(str(time_1))
                    if "summary" in entry.keys():
                        text = h.handle(re.sub(r'<a href(.+?)</a>', "", entry.summary.split("<br />", 1)[1]))
                        await channel.send(f"{entry.link}\n\n")
                else:
                    file_obj.write(str(d1))
            file_obj.close()
        await asyncio.sleep(3600)

bot.loop.create_task(newsFeed_background_task())
bot.run(cfg.bot["Token"])