import asyncio
import discord
from discord.ext import commands
import random
import feedparser
import html2text
import re
from datetime import datetime
import time

import Discord_Bot.discord_config as cfg
from Discord_Bot.google_sheets import *

bot = commands.Bot(command_prefix=cfg.bot["Prefix"], description=cfg.bot["Description"])
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
    news_feed = feedparser.parse("http://forums.playredfox.com/index.php?forums/announcements.11/index.rss")
    h = html2text.HTML2Text()
    h.ignore_links = False
    for entry in news_feed.entries[0:5]:
        if "summary" in entry.keys():
            text = h.handle(re.sub(r'<a href(.+?)</a>', "", entry.summary.split("<br />", 1)[1]))
            await ctx.send(f"{entry.title}\n```{text}\n```")


@bot.command()
async def KunlunDeco(ctx, a: int):
    deco_table = ['Summary!M4:Q19', 'Summary!H13:K18', 'Summary!H21:K28', 'Summary!H31:K38', 'Summary!H41:K52']
    if a != 0:
        title = "**Items needed to make a lvl {0} Kunlun Deco.**".format(a)
    else:
        title = "**Items needed to make a lvl {0} Kunlun Deco from all the materials.**".format(a)
    table, note = kunlun_deco(deco_table[a])
    if a == 4 or a == 0:
        await ctx.send(f"{title}\n```\n{table}\n{note}```")
    else:
        await ctx.send(f"{title}\n```\n{table}\n```")

@bot.command()
async def Book_Request(ctx, *, args):
    # Textual day, month and year
    date = datetime.today().strftime("%d %B, %Y")

    name = args.split(" ")[0]
    clan = args.split(" ")[1]
    group = args.split(" ")[2]
    cheng = args[-3:]
    book = " ".join(args.split(" ")[3:][:len(cheng)+1])

    #Check if filled in correctly
    if clan in ["Wu-Tang", "Beggar", "Shaolin"]:
        if group in ["Warrior", "Healer", "Hybrid", "CK"]:
            if len(book) != 0:
                if "C1" in cheng:
                    request_list = [date, name, clan, group, book, cheng]
                    book_request(request_list)
                    print(f"{request_list}")
                else:
                    print("WRONG LEVEL")
            else:
                print("YOU FORGOT YOUR BOOK")
        else:
            print("Use the right version of the classes")
    else:
        print("WRONG CLAN")\

@bot.command()
async def book_viewer(ctx):
    book_table = book_list_viewer()
    await ctx.send(f"```\n{book_table}```")

@bot.command()
async def book_remover(ctx, index: int):
    book_remover_func(index)
    await ctx.send("Your book request has been deleted from the request list.")

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
        news_feed = feedparser.parse("http://forums.playredfox.com/index.php?forums/announcements.11/index.rss")
        channel = bot.get_channel(int(cfg.bot["NewsFeed Channel ID"]))
        h = html2text.HTML2Text()
        h.ignore_links = False

        for entry in reversed(news_feed.entries[0:5]):
            file_obj = open("StoredNews", "r")

            time_1 = datetime.fromtimestamp(time.mktime(entry.published_parsed[:8] + (-1,)))
            date_from_file = file_obj.readline()
            file_obj.close()
            file_obj = open("StoredNews", "w")
            if date_from_file == "":
                file_obj.write(str(time_1))
                text = f"News from : {time_1}"
                await channel.send(f"{text}\n{entry.link}\n")
            else:
                d1 = datetime.strptime(date_from_file, "%Y-%m-%d %H:%M:%S")
                if datetime.fromtimestamp(time.mktime(entry.published_parsed[:8] + (-1,))) > d1:
                    file_obj.write(str(time_1))
                    text = f"News from : {time_1}"
                    await channel.send(f"{text}\n{entry.link}\n")
                else:
                    file_obj.write(str(d1))
            file_obj.close()
        await asyncio.sleep(3600)

bot.loop.create_task(newsFeed_background_task())
bot.run(cfg.bot["Token"])
