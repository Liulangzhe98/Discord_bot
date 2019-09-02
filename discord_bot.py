import discord
from discord.ext import commands
from itertools import zip_longest
from datetime import datetime

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
    print(bot.guilds)
    print('------')
    prefix = cfg.bot["Prefix"]
    game = discord.Game(f"Version 1.0 | Use {prefix}help")
    await bot.change_presence(activity=game)


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
    table, note = kunlun_deco_gs(deco_table[a])
    if a == 4 or a == 0:
        await ctx.send(f"{title}\n```\n{table}\n{note}```")
    else:
        await ctx.send(f"{title}\n```\n{table}\n```")


@bot.command()
async def book_request(ctx, *, args):
    # Textual day, month and year
    date = datetime.today().strftime("%d %B, %Y")
    re_use_str = args.split("|")[0].strip()
    book = args.split("|")[1]
    print(book)
    book = book.strip().lower()
    name = re_use_str.split(",")[0].strip()
    clan = re_use_str.split(",")[1].strip().capitalize()
    group = re_use_str.split(",")[2].strip().capitalize()
    cheng = book[book.find("c1"):]
    book = book.split(cheng)[0]
    cheng = cheng.capitalize()
    print(book)
    print(name, clan, group, cheng)
    # Check if filled in correctly
    if clan in ["Wu-tang", "Beggar", "Shaolin"]:
        if group in ["Warrior", "Healer", "Hybrid", "Ck"]:
            request_list = [date, name, clan, group, book, cheng]
            book_request_func(request_list)
            await ctx.send("Your book request have been added to the request list.")
        else:
            print("Use the right version of the classes")
    else:
        print("WRONG CLAN")


@bot.command()
async def book_requests(ctx, *, args):
    # Textual day, month and year
    date = datetime.today().strftime("%d %B, %Y")
    role_id = ""
    for guild in bot.guilds:
        if guild.name == "Enlightened" or guild.name == "Test_Server":
            for role in guild.roles:
                if role.name == "Library":
                    role_id = role

    if "library" in [y.name.lower() for y in ctx.author.roles]:
        re_use_str = args.split("|")[0].strip()
        books = args.split("|")[1]
        print(books)
        length = len(books.split(","))
        for book in books.split(","):
            book = book.strip().lower()
            name = re_use_str.split(",")[0].strip()
            clan = re_use_str.split(",")[1].strip().capitalize()
            group = re_use_str.split(",")[2].strip().capitalize()
            cheng = book[book.find("c1"):]
            book = book.split(cheng)[0]
            cheng = cheng.capitalize()
            print(book)
            print(name, clan, group, cheng)
            # Check if filled in correctly
            if clan in ["Wu-tang", "Beggar", "Shaolin"]:
                if group in ["Warrior", "Healer", "Hybrid", "Ck"]:
                    request_list = [date, name, clan, group, book, cheng]
                    book_request_func(request_list)
                    length -= 1
                else:
                    print("Use the right version of the classes")
            else:
                print("WRONG CLAN")
        if length == 0:
            await ctx.send("Your book requests have been added to the request list.")
    else:
        await ctx.send(f"You are not allowed to use this command. Ask {role_id.mention}")


@bot.command()
async def book_viewer(ctx):
    book_table = book_list_viewer()
    if len(book_table) > 2000:
        for item in zip_longest(*[iter(book_table.split("\n"))] * 10, fillvalue=''):
            lines = "\n".join(item).strip()
            await ctx.send(f"```\n{lines}```")
    else:
        await ctx.send(f"```\n{book_table}```")


@bot.command()
async def book_remover(ctx, *, args):
    role_id = ""
    for guild in bot.guilds:
        if guild.name == "Enlightened" or guild.name == "Test_Server":
            for role in guild.roles:
                if role.name == "Library":
                    role_id = role

    if "library" in [y.name.lower() for y in ctx.author.roles]:
        index = list(map(int, args.split(" ")))
        book = book_remover_func(index)
        if len(index) != 1:
            plural = "entries have "
        else:
            plural = "entry has"
        await ctx.send(f"The book {plural} been deleted from the request list.\n"
                       f"```\n{book}```")
    else:
        await ctx.send(f"You are not allowed to use this command. Ask {role_id.mention}")


@bot.command()
async def refine(ctx):
    await ctx.send(f"```Refine:\n"
                   "refine_rates <options> | Will show the refinement rates with the given options.\n"
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
    rates = input_opt[1:-1]
    rates_list = rates.split(",")
    rates_list = list(map(int, rates_list))
    if len(rates_list) != 5:
        await ctx.send("You didn't specify the right amount of options. Please check the example with !!Refine")
    else:
        await ctx.send(f"```With the give options the rates will be like this:\n{refine_rate(rates_list)}```")

bot.remove_command('help')


@bot.command()
async def help(ctx):
    # Code block style
    prefix = cfg.bot["Prefix"]
    code_block = "```" \
                f"Use {prefix} in combination with these commands\n"\
                 "COMMANDS\n"
    code_block += "\t ------- General -------\n"
    code_block += "refine                 | For more information about the refining command.\n"
    code_block += "love_potion <argument> | <argument> can be [%, Total]. \n" \
                  "                       | It shows the progress for the Love epithet.\n"
    code_block += "kunlun_deco <argument> | <argument> can be [0, 1, 2, 3, 4].\n" \
                  "                       | It will show the cost to make a Kunlun deco.\n" \
                  "                       | Choosing 0 will give the total cost to make a level 4 deco.\n"
    code_block += "\t ------- Library -------\n"
    code_block += "book_request | This will add a request to the list.\n" \
                  "book_request <name>, <clan>, <class> | <book name> <cheng>\n"\
                  "book_request | <clan> has to be one of [Wu-Tang, Beggar, Shaolin].\n" \
                  "             | <class> has to be one of [Warrior, Healer, Hybrid, CK].\n" \
                  "             | <cheng> can to be one of [c11, c12, c11 \ c12].\n"
    code_block += "book_viewer  | This will give a table of all the requested skill books.\n"
    code_block += "```"

    await ctx.send(code_block)

bot.run(cfg.bot["Token"])
