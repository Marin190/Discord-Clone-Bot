# Made by Marin#9044
import json, os
import discord
from discord.ext import commands


jeton = "" # <--- Put your bot token here


bot = commands.Bot(command_prefix="!", help_command=None)

@bot.event
async def on_ready():
    print("  Bot start successfully !")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("By Marin#9044"))

@bot.command()
async def help(ctx):
    file = "\nBot Prefix : !\n\nCommands:\n   !clean | delet all channel of server\n   !load {name of save} | use it to load a save server.\n   !save {name of new save} | use it to save current server.\n   !allSave | use it to show all your save.\n   !content {name of save} | use it to shows content of specifique save.\n   !delete {name of save} | use it to delete a save"
    embed = discord.Embed(title="Help menu", description=file, color=0x82c73d)
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(manage_channels=True)
async def load(ctx, args):
    try:
        with open(f"save/{args}.json", "r") as f: x = json.loads(f.read())
        embed = discord.Embed(title="Clone Bot", description="The cloning start successfully.", color=0x82c73d)
        await ctx.send(embed=embed)
        for i in x:
            category = await ctx.guild.create_category(i)
            for a in x[i]:
                if x[i][a] == "txt": await category.create_text_channel(a)
                elif x[i][a] == "voc": await category.create_voice_channel(a)
    except Exception as e:
        embed = discord.Embed(title="Error", description=f"Save {args} don't exist.\nType !allSave to show your save.", color=0x82c73d)
        await ctx.send(embed=embed)

@bot.command()
async def allSave(ctx):
    files = os.listdir("save/")
    file = ""
    for i in files: file = f"{file}\n{i.replace(r'.json', '', 1)}"
    embed = discord.Embed(title="All save :", description=file, color=0x82c73d)
    await ctx.send(embed=embed)

@bot.command()
async def clean(ctx):
    await ctx.message.guild.edit(name=f"CLEAN")
    await ctx.message.delete()
    for channel in ctx.message.guild.voice_channels: await channel.delete()
    for channel in ctx.message.guild.text_channels: await channel.delete()
    for category in ctx.message.guild.categories: await category.delete()
    await ctx.message.guild.create_text_channel(f"Clean")

@bot.command()
async def content(ctx, args):
    try:
        with open(f"save/{args}.json", "r") as f: x = json.loads(f.read())
        mess = f"- = voice channel\n+ = text channel\n| = categories"
        for i in x:
            mess = f"{mess}\n\n|{i}"
            for a in x[i]:
                if x[i][a] == "txt": mess = f"{mess}\n      + {a}"
                elif x[i][a] == "voc": mess = f"{mess}\n      - {a}"
        embed = discord.Embed(title=f"content of {args}", description=mess, color=0x82c73d)
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(title="Error", description=f"Save {args} don't exist.\nType !allSave to show your save.", color=0x82c73d)
        await ctx.send(embed=embed)

@bot.command()
async def delete(ctx, args):
    if os.path.exists(f"save/{args}.json"):
        os.remove(f"save/{args}.json")
        embed = discord.Embed(title="delete", description=f"Save {args} delet successfully.", color=0x82c73d)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Error", description=f"Save {args} don't exist.\nType !allSave to show your save.", color=0x82c73d)
        await ctx.send(embed=embed)

@bot.command()
async def save(ctx, args):
    categorys = {}
    for category in ctx.message.guild.categories:
        categorys[category.name] = {}
        for voice_channel in category.voice_channels:
            categorys[category.name][voice_channel.name] = "voc"
        for text_channel in category.text_channels:
            categorys[category.name][text_channel.name] = "txt"
    try:
        with open(f"save/{args}.json", "r") as f: pass
        embed = discord.Embed(title="Save", description=f"The name '{args}' is already use.\nUse another.", color=0x82c73d)
        await ctx.send(embed=embed)
    except:
        final = json.dumps(categorys)
        with open(f"save/{args}.json", "w+") as f: f.write(final)
        embed = discord.Embed(title="Save", description=f"Server save successfully as : {args}", color=0x82c73d)
        await ctx.send(embed=embed)

print("\n  Clone Bot by Marin#9044\n\n  Bot is starting . . .")
bot.run(jeton)
