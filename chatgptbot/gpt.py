# LIBRARIES
import discord
from discord.ext import commands
import os
from sys import exit
import openai
import datetime
from time import time as ttime

openai.api_key = os.getenv("OPENAI_API_KEY")

# VALUES
role_ban = 1054109349628358817
role_admin = 1054002956493664268
role_newbie = 973871427788873748
role_constant = 974602932265811988
role_old = 973718824174092288
role_eternalold = 1044959103316918354
role_pseudoowner = 1044959814096269312

channel_gpt = 1054106565663264809

# BOT
bot = discord.Bot(intents=discord.Intents.all())
start_time = ttime()

# GROUPS
askgroup = bot.create_group("ask", "ask different models a question")
accessgroup = bot.create_group("member", "member access related commands")

# CLASSES
class GptButtons(discord.ui.View):
    def __init__(self, question, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeout = None

        self.question = question
        self.model = model

    @discord.ui.button(label="Regenerate", emoji="♻️", style=discord.ButtonStyle.green)
    async def rbutton_callback(self, _, interaction):
        await interaction.response.defer()
        computation_start = ttime()
        response = openai.Completion.create(
            engine=self.model,
            prompt=self.question,
            temperature=0.4,
            max_tokens=1024,
            top_p=0.1,
            frequency_penalty=0.1,
            presence_penalty=0.1
        )
        computation_finish = ttime()
        elapsedtime = int(round(computation_finish - computation_start))
        embed = discord.Embed(color=0xff0000)
        embed.add_field(name="**Ответ GPT:**", value=response["choices"][0]["text"])
        embed.set_footer(text=f"обработка заняла {str(datetime.timedelta(seconds=elapsedtime))}")
        ogres = await interaction.original_response()
        await interaction.followup.edit_message(message_id=ogres.id, view=GptButtons(self.question, self.model), embed=embed)

# EVENTS
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('https://github.com/Sheudz/Python-GPT-BOT'))
    print("BOT IS UP")

@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        return await ctx.respond(embed=discord.Embed(
            title="Error",
            description=f"{error}",
            color=0xff0000), ephemeral=True)
    elif isinstance(error, commands.MissingPermissions):
        return await ctx.respond(embed=discord.Embed(
            title="Error",
            description="У тебя нехватает прав",
            color=0xff0000), ephemeral=True)

# ACCESS
@accessgroup.command(name="block",description="block gpt for the member")
async def member_block(ctx, member: discord.Member):
        author = ctx.user
        roles = [role.id for role in author.roles]
        if role_admin in roles:
            await member.add_roles(ctx.guild.get_role(role_ban))
            await ctx.respond(f"{member.mention}/{member.name} заблокирован", ephemeral=True)
        else:
            await ctx.respond("у тебя недостаточно прав чтоб блокировать GPT для пользователей", ephemeral=True)

@accessgroup.command(name="unblock",description="unblock gpt for the member")
async def member_unblock(ctx, member: discord.Member):
        author = ctx.user
        roles = [role.id for role in author.roles]
        if role_admin in roles:
            try:
                await member.remove_roles(ctx.guild.get_role(role_ban))
                await ctx.respond(f"{member.mention}/{member.name} разаблокирован", ephemeral=True)
            except:
                await ctx.respond(f"{member.mention}/{member.name} не был заблокирован", ephemeral=True)
        else:
            await ctx.respond("у тебя недостаточно прав чтоб разблокировать GPT для пользователей", ephemeral=True)

@bot.user_command(name="Block")
async def member_block(ctx, member: discord.Member):
        author = ctx.user
        roles = [role.id for role in author.roles]
        if role_admin in roles:
            await member.add_roles(ctx.guild.get_role(role_ban))
            await ctx.respond(f"{member.mention}/{member.name} заблокирован", ephemeral=True)
        else:
            await ctx.respond("у тебя недостаточно прав чтоб блокировать GPT для пользователей", ephemeral=True)

@bot.user_command(name="Unblock")
async def member_unblock(ctx, member: discord.Member):
        roles = [role.id for role in ctx.author.roles]
        if role_admin in roles:
            try:
                await member.remove_roles(ctx.guild.get_role(role_ban))
                await ctx.respond(f"{member.mention}/{member.name} разаблокирован", ephemeral=True)
            except:
                await ctx.respond(f"{member.mention}/{member.name} не был заблокирован", ephemeral=True)
        else:
            await ctx.respond("у тебя недостаточно прав чтоб разблокировать GPT для пользователей", ephemeral=True)

# GPT
@askgroup.command(name="babbage", description="ask babbage model a question")
@commands.cooldown(1, 30, commands.BucketType.user)
async def ask(ctx, question: discord.Option(str)):
        if role_ban in [role.id for role in ctx.author.roles]:
            await ctx.respond("тебе не доступен GPT", ephemeral=True)
        elif ctx.channel.id != channel_gpt:
            await ctx.respond("Я могу отвечать на ваши вопросы только в канале #gpt-chat", ephemeral=True)
        else:
            await ctx.defer()
            computation_start = ttime()
            response = openai.Completion.create(
            engine="text-babbage-001",
            prompt=question,
            temperature=0.4,
            max_tokens=1024,
            top_p=0.1,
            frequency_penalty=0.1,
            presence_penalty=0.1
            )
            computation_finish = ttime()
            elapsedtime = int(round(computation_finish - computation_start))
            embed = discord.Embed(color=0xff0000)
            embed.add_field(name="**Ответ GPT:**", value=response["choices"][0]["text"])
            embed.set_footer(text=f"обработка заняла {str(datetime.timedelta(seconds=elapsedtime))}")
            await ctx.followup.send(embed=embed, view=GptButtons(question, "text-babbage-001"))

@askgroup.command(name="curie", description="ask curie model a question")
@commands.cooldown(1, 30, commands.BucketType.user)
async def ask(ctx, question: discord.Option(str)):
        roles = [role.id for role in ctx.author.roles]
        if role_ban in roles:
            await ctx.respond("тебе не доступен GPT", ephemeral=True)
        elif role_newbie not in roles and role_constant not in roles and role_old not in roles and role_eternalold not in roles and role_pseudoowner not in roles:
            await ctx.respond("тебе не доступна єта модель из-за слишком низкого уровня", ephemeral=True)
        elif ctx.channel.id != channel_gpt:
            await ctx.respond("Я могу отвечать на ваши вопросы только в канале #gpt-chat", ephemeral=True)
        else:
            await ctx.defer()
            computation_start = ttime()
            response = openai.Completion.create(
            engine="text-curie-001",
            prompt=question,
            temperature=0.4,
            max_tokens=1024,
            top_p=0.1,
            frequency_penalty=0.1,
            presence_penalty=0.1
            )
            computation_finish = ttime()
            elapsedtime = int(round(computation_finish - computation_start))
            embed = discord.Embed(color=0xff0000)
            embed.add_field(name="**Ответ GPT:**", value=response["choices"][0]["text"])
            embed.set_footer(text=f"обработка заняла {str(datetime.timedelta(seconds=elapsedtime))}")
            await ctx.followup.send(embed=embed, view=GptButtons(question, "text-curie-001"))

@askgroup.command(name="davinci", description="ask davinci model a question")
@commands.cooldown(1, 30, commands.BucketType.user)
async def ask(ctx, question: discord.Option(str)):
        roles = [role.id for role in ctx.author.roles]
        if role_ban in roles:
            await ctx.respond("тебе не доступен GPT", ephemeral=True)
        elif role_constant not in roles and role_old not in roles and role_eternalold not in roles and role_pseudoowner not in roles:
            await ctx.respond("тебе не доступна єта модель из-за слишком низкого уровня", ephemeral=True)
        elif ctx.channel.id != channel_gpt:
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
            embed = discord.Embed(color=0xff0000)
            embed.add_field(name="**Ответ GPT:**", value=response["choices"][0]["text"])
            embed.set_footer(text=f"обработка заняла {str(datetime.timedelta(seconds=elapsedtime))}")
            await ctx.followup.send(embed=embed, view=GptButtons(question, "text-davinci-003"))

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