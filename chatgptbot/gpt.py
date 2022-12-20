import discord
from discord.ext import commands
import os
from sys import exit
import openai
import datetime
from time import time as ttime

openai.api_key = os.getenv("OPENAI_API_KEY")

bot = discord.Bot(intents=discord.Intents.all())
start_time = ttime()
askgroup = bot.create_group("ask", "gpt related commands")
accessgroup = bot.create_group("member", "member access related commands")

# EVENTS
@bot.event
async def on_ready():
    print("BOT IS READY")

@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        return await ctx.respond(embed=discord.Embed(
            title="Error",
            description=f"{error}",
            color=0xff0000), ephemeral=True)

# ACCESS
@accessgroup.command(name="block",description="block gpt for the member")
async def member_block(ctx, member: discord.Member):
        role_id = 1054002956493664268
        author = ctx.user

        if role_id in [role.id for role in author.roles]:
            role_ban = 1054109349628358817
            await member.add_roles(ctx.guild.get_role(role_ban))
            await ctx.respond(f"{member.mention}/{member.name} заблокирован", ephemeral=True)
        else:
            await ctx.respond("у тебя недостаточно прав чтоб блокировать GPT для пользователей", ephemeral=True)

@accessgroup.command(name="unblock",description="unblock gpt for the member")
async def member_unblock(ctx, member: discord.Member):
        role_id = 1054002956493664268
        author = ctx.user
        if role_id in [role.id for role in author.roles]:
            role_ban = 1054109349628358817
            try:
                await member.remove_roles(ctx.guild.get_role(role_ban))
                await ctx.respond(f"{member.mention}/{member.name} разаблокирован", ephemeral=True)
            except:
                await ctx.respond(f"{member.mention}/{member.name} не был заблокирован", ephemeral=True)
        else:
            await ctx.respond("у тебя недостаточно прав чтоб разблокировать GPT для пользователей", ephemeral=True)

@bot.user_command(name="Block")
async def member_block(ctx, member: discord.Member):
        role_id = 1054002956493664268
        author = ctx.user

        if role_id in [role.id for role in author.roles]:
            role_ban = 1054109349628358817
            await member.add_roles(ctx.guild.get_role(role_ban))
            await ctx.respond(f"{member.mention}/{member.name} заблокирован", ephemeral=True)
        else:
            await ctx.respond("у тебя недостаточно прав чтоб блокировать GPT для пользователей", ephemeral=True)

@bot.user_command(name="Unblock")
async def member_unblock(ctx, member: discord.Member):
        role_id = 1054002956493664268
        author = ctx.user
        if role_id in [role.id for role in author.roles]:
            role_ban = 1054109349628358817
            try:
                await member.remove_roles(ctx.guild.get_role(role_ban))
                await ctx.respond(f"{member.mention}/{member.name} разаблокирован", ephemeral=True)
            except:
                await ctx.respond(f"{member.mention}/{member.name} не был заблокирован", ephemeral=True)
        else:
            await ctx.respond("у тебя недостаточно прав чтоб разблокировать GPT для пользователей", ephemeral=True)

# GPT
@askgroup.command(name="davinci", description="ask davinci model a question")
@commands.cooldown(1, 30, commands.BucketType.user)
async def ask(ctx, question: discord.Option(str)):
        role_id = 1054109349628358817
        author = ctx.author
        if role_id in [role.id for role in author.roles]:
            await ctx.respond("тебе не доступен GPT", ephemeral=True)
        elif ctx.channel.id != 1054106565663264809:
            await ctx.respond("Я могу отвечать на ваши вопросы только в канале #gpt-chat", ephemeral=True)
        else:
            await ctx.defer()
            computation_start = ttime()
            response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=question,
            temperature=0.4,
            max_tokens=1024,
            top_p=0.1,
            frequency_penalty=0.1,
            presence_penalty=0.1
            )
            computation_finish = ttime()
            elapsedtime = int(round(computation_finish - computation_start))
            embed = discord.Embed(description=f"**GPT3**", color=0xff0000)
            embed.add_field(name=f"**{ctx.author} задал вопрос GPT:**", value=question)
            embed.add_field(name="**Ответ GPT:**", value=response["choices"][0]["text"])
            embed.set_footer(text=f"обработка запроса заняла {str(datetime.timedelta(seconds=elapsedtime))}")
            await ctx.followup.send(embed=embed)

# MISC
@bot.command(name="ping", description="measures latency")
@commands.cooldown(1, 15, commands.BucketType.user)
async def ping(ctx):
    return await ctx.respond(embed=discord.Embed(
        title="Ping",
        description=f"Pong:  {round(bot.latency * 1000)}ms",
        color=0xff0000), ephemeral=True)

@bot.command(name="uptime", description="shows bot uptime")
@commands.cooldown(1, 15, commands.BucketType.user)
async def uptime(ctx):
    current_time = ttime()
    difference = int(round(current_time - start_time))
    text = str(datetime.timedelta(seconds=difference))
    embed = discord.Embed(color=0xff0000)
    embed.add_field(name="Uptime", value=text)
    await ctx.respond(embed=embed, ephemeral=True)

try:
    bot.run(os.getenv("BOT_TOKEN"))
except Exception as err:
    print('Discord bot token error')
    print(err)
    exit()