import discord
from discord.ext import commands, tasks
import os
import openai
import datetime


os.system('clear')
openai.api_key = "апи ключ от опен аи"


bot = discord.Bot(intents=discord.Intents.all())
@bot.event
async def on_ready():
	print("BOT STARTED!!!")

@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        return await ctx.respond(embed=discord.Embed(
            title="Error",
            description=f"{error}",
            color=0x14F803), ephemeral=True)

@bot.command(name="block_user",description="block gpt for user")
async def block_user(ctx, user: discord.Member):
        role_id = 1054002956493664268
        author = ctx.user

        if role_id in [role.id for role in author.roles]:
            role_idiot = 1054109349628358817
            await user.add_roles(ctx.guild.get_role(role_idiot))
            await ctx.respond(f"{user.mention}/{user.name} заблокирован")
        else:
            await ctx.respond("у тебя недостаточно прав чтоб блокировать GPT для юзеров")

@bot.command(name="unblock_user",description="unblock gpt for user")
async def unblock_user(ctx, user: discord.Member):
        role_id = 1054002956493664268
        author = ctx.user
        if role_id in [role.id for role in author.roles]:
            role_idiot = 1054109349628358817
            try:
                await user.remove_roles(ctx.guild.get_role(role_idiot))
                await ctx.respond(f"{user.mention}/{user.name} разаблокирован")
            except:
                await ctx.respond(f"{user.mention}/{user.name} не был заблокирован")
        else:
            await ctx.respond("у тебя недостаточно прав чтоб блокировать GPT для юзеров")

@bot.command(name="ask",description="ask a question for gpt")
@commands.cooldown(1, 30, commands.BucketType.user)
async def ask(ctx, ask: str):
        role_id = 1054109349628358817
        author = ctx.author

        if role_id in [role.id for role in author.roles]:
            await ctx.respond("GPT заблокирован для тебя!")
        elif ctx.channel.id != 1054106565663264809:
            await ctx.respond("Я могу отвечать на ваши вопросы только в канале #gpt-chat")
        else:
            await ctx.defer()
            a = datetime.datetime.now()
            response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=ask,
            temperature=0.4,
            max_tokens=1024,
            top_p=0.1,
            frequency_penalty=0.1,
            presence_penalty=0.1
            )
            b = datetime.datetime.now()
            moment1 = datetime.datetime(9999, 9, 9, a.hour, a.minute, a.second)
            moment2 = datetime.datetime(9999, 9, 9, b.hour, b.minute, b.second)
            delta = moment2 - moment1
            embed = discord.Embed(description=f"**GPT3**", color=0xff0000)
            embed.add_field(name=f"**{ctx.author} задал вопрос GPT:**", value=ask)
            embed.add_field(name="**Ответ GPT:**", value=response["choices"][0]["text"])
            embed.set_footer(text=f"обработка запроса заняла {delta.total_seconds()} секунд(ы)")
            await ctx.followup.send(embed=embed)

bot.run("токен бота.")
