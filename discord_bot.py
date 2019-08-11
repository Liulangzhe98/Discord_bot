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
from Discord_Bot.helper import *

bot = commands.Bot(command_prefix=cfg.bot["Prefix"], description=cfg.bot["Description"])
client = discord.Client()


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def love_potion(ctx, a: str):
    if a == "%":
        title, table = icy_epi_test()
        await ctx.send(f"{title}")
    elif a == "Total":
        title, table = icy_epi_test()
        await ctx.send(f"{title}\n```\n{table}```")


@bot.command()
async def kunlun_deco(ctx, a: int):
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
async def book_request(ctx, *, args):
    # Textual day, month and year
    date = datetime.today().strftime("%d %B, %Y")

    name = args.split(" ")[0]
    clan = args.split(" ")[1]
    group = args.split(" ")[2]
    cheng = args[-3:]
    book = " ".join(args.split(" ")[3:][:len(cheng) + 1])

    # Check if filled in correctly
    if clan in ["Wu-Tang", "Beggar", "Shaolin"]:
        if group in ["Warrior", "Healer", "Hybrid", "CK"]:
            if len(book) != 0:
                if "C1" in cheng:
                    request_list = [date, name, clan, group, book, cheng]
                    book_request_func(request_list)
                    await ctx.send("Your book request has been added from the request list.")
                else:
                    print("WRONG LEVEL")
            else:
                print("YOU FORGOT YOUR BOOK")
        else:
            print("Use the right version of the classes")
    else:
        print("WRONG CLAN") \
 \
 \
@bot.command()
async def book_viewer(ctx):
    book_table = book_list_viewer()
    await ctx.send(f"```\n{book_table}```")


@bot.command()
async def book_remover(ctx, *, args):
    index = list(map(int, args.split(" ")))
    print(index)
    book = book_remover_func(index)
    if len(index) != 1:
        plural = "entries have "
    else:
        plural = "entry has"
    await ctx.send(f"The book {plural} been deleted from the request list.\n"
                   f"```\n{book}```")


@bot.command()
async def refine(ctx):
    await ctx.send(f"```Refine:\n"
                   "!!refine_rates <options> | Will show the refinement rates with the given options.\n"
                   "    Options: [<Mastery>, <Deco>, <Epithet>, <Tender Stone>, <Band>]\n "
                   "            Deco           = [0,15] \n"
                   "            Epithet        = [0,15,30,50]\n"
                   "            Mastery        = [0,1,3,5] \n"
                   "            Tender Stone   = [0,30,100,200]\n"
                   "            Band attribute = [0,10,20,30,40,50]\n"
                   "    Example: !!Refine_rates [5,15,15,0,50]\n"
                   "    Disclaimer: Rates are not tested, so refine can still fail even if the bot says it's 100%```")


@bot.command()
async def refine_rates(ctx, input_opt: str):
    print(input_opt, len(input_opt))
    rates = input_opt[1:-1]
    print(rates)
    rates_list = rates.split(",")
    rates_list = list(map(int, rates_list))

    if (len(rates_list) != 5):
        await ctx.send("You didn't specify the right amount of options. Please check the example with !!Refine")
    else:
        await ctx.send(f"```With the give options the rates will be like this:\n{refine_rate(rates_list)}```")



bot.remove_command('help')


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="9Dragons Bot", description="The list of services, commands and their uses:",
                          color=0xeee657)
    embed.add_field(name="SERVICES:", value="\u200b", inline=False)

    embed.add_field(name="Newsfeed", value="This service will check for news updates on the Redfox Forum and send "
                                           "them to the <#Newsfeed> channel.\u200b")
    embed.add_field(name="COMMANDS:", value="--------------------", inline=False)
    embed.add_field(name="help", value="Gives this message", inline=False)
    embed.add_field(name="LovePotion <argument>", value="<argument> can be [%, Total]. It shows the progress for "
                                                        "the Love epithet.", inline=False)
    embed.add_field(name="KunlunDeco <argument>", value="<argument> can be between 0 and 4. Where 0 is the total "
                                                        "cost to make a level 4 deco.")

    # Library commands
    embed.add_field(name="book_viewer", value="This command will show all the requested books.")
    embed.add_field(name="book_remover", value="TEMP")

    space = ""

    # Code block style
    code_block = "```\nSERVICES\n"
    code_block += "NewsFeed | This service will check for news updates on the Redfox Forum and send them to the \n" \
                  "           <#Newsfeed> channel.\n\n"
    code_block += "COMMANDS\n"
    code_block += "\t ------- General -------\n"
    code_block += "refine                 | For more information about the refining command.. \n"
    code_block += "love_potion <argument> | <argument> can be [%, Total]. \n" \
                  "                       | It shows the progress for the Love epithet.\n"
    code_block += "kunlun_deco <argument> | <argument> can be [0, 1, 2, 3, 4].\n" \
                  "                       | It will show the cost to make a Kunlun deco.\n" \
                  "                       | Choosing 0 will give the total cost to make a level 4 deco.\n"
    code_block += "\t ------- Library -------\n"
    code_block += "book_request <name> <clan> <class> <book> <cheng> | This will add a request to the list.\n" \
                  "book_request | <clan> has to be one of [Wu-Tang, Beggar, Shaolin].\n" \
                  "             | <class> has to be one of [Warrior, Healer, Hybrid, CK].\n" \
                  "             | <cheng> can be [C11, C12].\n"
    code_block += "book_viewer  | This will give a table of all the requested skill books.\n"
    code_block += "book_remover <index> | This will remove the given index from the list.\n" \
                  "                     | Multiple indices at the same time and only by the Librarians."

    code_block += "```"

    await ctx.send(code_block)
    # await ctx.send(embed=embed)


# async def newsFeed_background_task():
#     await bot.wait_until_ready()
#
#     while not bot.is_closed():
#         news_feed = feedparser.parse("http://forums.playredfox.com/index.php?forums/announcements.11/index.rss")
#         channel = bot.get_channel(int(cfg.bot["NewsFeed Channel ID"]))
#         h = html2text.HTML2Text()
#         h.ignore_links = False
#
#         for entry in reversed(news_feed.entries[0:5]):
#             file_obj = open("StoredNews", "r")
#
#             time_1 = datetime.fromtimestamp(time.mktime(entry.published_parsed[:8] + (-1,)))
#             date_from_file = file_obj.readline()
#             file_obj.close()
#             file_obj = open("StoredNews", "w")
#             if date_from_file == "":
#                 file_obj.write(str(time_1))
#                 text = f"News from : {time_1}"
#                 await channel.send(f"{text}\n{entry.link}\n")
#             else:
#                 d1 = datetime.strptime(date_from_file, "%Y-%m-%d %H:%M:%S")
#                 if datetime.fromtimestamp(time.mktime(entry.published_parsed[:8] + (-1,))) > d1:
#                     file_obj.write(str(time_1))
#                     text = f"News from : {time_1}"
#                     await channel.send(f"{text}\n{entry.link}\n")
#                 else:
#                     file_obj.write(str(d1))
#             file_obj.close()
#         await asyncio.sleep(3600)

# bot.loop.create_task(newsFeed_background_task())
bot.run(cfg.bot["Token"])
