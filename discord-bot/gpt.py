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
askgroup = bot.create_group("ask", "ask different OpenAI models a question")
accessgroup = bot.create_group("member", "access related commands")
imagegroup = bot.create_group("image", "image generation related commands")

# CLASSES
'''
class GptButtons(discord.ui.View):
    def __init__(self, ctx, question, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeout = None

        self.ctx = ctx
        self.question = question
        self.model = model

    @discord.ui.button(label="Regenerate", emoji="♻️", style=discord.ButtonStyle.green)
    async def rbutton_callback(self, _, interaction):
        if self.ctx.author.id == interaction.user.id:
            await interaction.response.defer()
            computation_start = ttime()
            response = openai.Completion.create(
                engine=self.model,
                prompt=self.question,
                temperature=0.6,
                max_tokens=1024,
                top_p=0.1,
                frequency_penalty=0.1,
                presence_penalty=0.1
            )
            elapsedtime = int(round(ttime() - computation_start))
            embed = discord.Embed(title="Ответ:", description=response["choices"][0]["text"], color=0xff0000)
            embed.add_field(name="Вопрос:", value=question, inline=False)
            embed.set_footer(text=f"обработка заняла {str(datetime.timedelta(seconds=elapsedtime))}")
            ogres = await interaction.original_response()
            await interaction.followup.edit_message(message_id=ogres.id, view=None, embed=embed)
        else:
            await interaction.response.send_message("Вы не можете заново сгенерировать ответ на не ваш вопрос", ephemeral=True)
'''

# EVENTS
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('https://github.com/Sheudz/Python-Discord-OpenAi-BOT'))
    print("BOT IS UP")

@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        return await ctx.respond(embed=discord.Embed(
            title="Error",
            description=f"Спробуйте через {round(error.retry_after, 2)} секунд",
            color=0xff0000), ephemeral=True)
    elif isinstance(error, commands.MissingPermissions):
        return await ctx.respond(embed=discord.Embed(
            title="Error",
            description="У тебе бракує прав",
            color=0xff0000), ephemeral=True)

# ACCESS
@accessgroup.command(name="block",description="block AI-BOT for the member")
async def member_block(ctx, member: discord.Member):
        author = ctx.user
        roles = [role.id for role in author.roles]
        if role_admin in roles:
            await member.add_roles(ctx.guild.get_role(role_ban))
            await ctx.respond(f"{member.mention}/{member.name} заблокований", ephemeral=True)
        else:
            await ctx.respond("у тебе недостатньо прав, щоб блокувати GPT для користувачів", ephemeral=True)

@accessgroup.command(name="unblock",description="unblock AI-BOT for the member")
async def member_unblock(ctx, member: discord.Member):
        author = ctx.user
        roles = [role.id for role in author.roles]
        if role_admin in roles:
            try:
                await member.remove_roles(ctx.guild.get_role(role_ban))
                await ctx.respond(f"{member.mention}/{member.name} разблокований", ephemeral=True)
            except:
                await ctx.respond(f"{member.mention}/{member.name} не був заблокований", ephemeral=True)
        else:
            await ctx.respond("у тебе недостатньо прав, щоб розблокувати AI-BOT для користувачів", ephemeral=True)

@bot.user_command(name="Block")
async def member_block(ctx, member: discord.Member):
        author = ctx.user
        roles = [role.id for role in author.roles]
        if role_admin in roles:
            await member.add_roles(ctx.guild.get_role(role_ban))
            await ctx.respond(f"{member.mention}/{member.name} заблокований", ephemeral=True)
        else:
            await ctx.respond("у тебе недостатньо прав, щоб блокувати AI-BOT для користувачів", ephemeral=True)

@bot.user_command(name="Unblock")
async def member_unblock(ctx, member: discord.Member):
        roles = [role.id for role in ctx.author.roles]
        if role_admin in roles:
            try:
                await member.remove_roles(ctx.guild.get_role(role_ban))
                await ctx.respond(f"{member.mention}/{member.name} разблокований", ephemeral=True)
            except:
                await ctx.respond(f"{member.mention}/{member.name} не був заблокований", ephemeral=True)
        else:
            await ctx.respond("у тебе недостатньо прав, щоб розблокувати GPT для користувачів", ephemeral=True)

# GPT
@askgroup.command(name="babbage", description="ask babbage model a question")
@commands.cooldown(1, 30, commands.BucketType.user)
async def ask_babbage(ctx, question: discord.Option(str)):
        if role_ban in [role.id for role in ctx.author.roles]:
            await ctx.respond("Тобі не доступний GPT-BOT", ephemeral=True)
        elif ctx.channel.id != channel_gpt:
            await ctx.respond("Я можу відповідати на ваші запитання лише у каналі #gpt-chat", ephemeral=True)
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
            elapsedtime = int(round(ttime() - computation_start))
            embed = discord.Embed(title="Відповідь:", description=response["choices"][0]["text"], color=0xff0000)
            embed.add_field(name="Питання:", value=question, inline=False)
            embed.set_footer(text=f"обробка зайняла {str(datetime.timedelta(seconds=elapsedtime))}")
            await ctx.followup.send(embed=embed)

@askgroup.command(name="curie", description="ask curie model a question")
@commands.cooldown(1, 30, commands.BucketType.user)
async def ask_curie(ctx, question: discord.Option(str)):
        roles = [role.id for role in ctx.author.roles]
        if role_ban in roles:
            await ctx.respond("Тобі не доступний GPT-BOT", ephemeral=True)
        elif role_newbie not in roles and role_constant not in roles and role_old not in roles and role_eternalold not in roles and role_pseudoowner not in roles:
            await ctx.respond("Тобі не доступна ця модель через занадто низький рівень", ephemeral=True)
        elif ctx.channel.id != channel_gpt:
            await ctx.respond("Я можу відповідати на ваші запитання лише у каналі #gpt-chat", ephemeral=True)
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
            elapsedtime = int(round(ttime() - computation_start))
            embed = discord.Embed(title="Відповідь:", description=response["choices"][0]["text"], color=0xff0000)
            embed.add_field(name="Питання:", value=question, inline=False)
            embed.set_footer(text=f"обробка зайняла {str(datetime.timedelta(seconds=elapsedtime))}")
            await ctx.followup.send(embed=embed)

@askgroup.command(name="davinci", description="ask davinci model a question")
@commands.cooldown(1, 30, commands.BucketType.user)
async def ask_davinci(ctx, question: discord.Option(str)):
        roles = [role.id for role in ctx.author.roles]
        if role_ban in roles:
            await ctx.respond("Тобі не доступний GPT-BOT", ephemeral=True)
        elif role_constant not in roles and role_old not in roles and role_eternalold not in roles and role_pseudoowner not in roles:
            await ctx.respond("Тобі не доступна ця модель через занадто низький рівень", ephemeral=True)
        elif ctx.channel.id != channel_gpt:
            await ctx.respond("Я можу відповідати на ваші запитання лише у каналі #gpt-chat", ephemeral=True)
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
            elapsedtime = int(round(ttime() - computation_start))
            embed = discord.Embed(title="Відповідь:", description=response["choices"][0]["text"], color=0xff0000)
            embed.add_field(name="Питання:", value=question, inline=False)
            embed.set_footer(text=f"обробка зайняла {str(datetime.timedelta(seconds=elapsedtime))}")
            await ctx.followup.send(embed=embed)

@imagegroup.command(name="generate", description="generate image")
@commands.cooldown(1, 70, commands.BucketType.user)
async def image_generate(ctx, prompt):
    roles = [role.id for role in ctx.author.roles]
    if role_ban in roles:
        await ctx.respond("Тобі не доступний GPT-BOT", ephemeral=True)
    elif ctx.channel.id != channel_gpt:
        await ctx.respond("Я можу відповідати на ваші запитання лише у каналі #gpt-chat", ephemeral=True)
    else:
        await ctx.defer()
        computation_start = ttime()
        response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
        )
        image_url = response['data'][0]['url']
        elapsedtime = int(round(ttime() - computation_start))
        embed = discord.Embed(title="Згенероване зображення: " + prompt, color=0xff0000)
        embed.set_image(url=image_url)
        embed.set_footer(text=f"обробка зайняла {str(datetime.timedelta(seconds=elapsedtime))}")
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
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))
except Exception as err:
    print('Discord bot token error')
    print(err)
    exit()
