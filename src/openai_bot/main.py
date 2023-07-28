from typing import Union

from disnake.ext import commands
import disnake

from os import getenv


bot = commands.InteractionBot(intents=disnake.Intents.all())
cogs: list[str] = ["misc", "ai_bot"]
for cog in cogs:
    bot.load_extension(f"cogs.{cog}")
    print(f"Loaded {cog}")


@bot.event
async def on_ready() -> None:
    await bot.change_presence(
        status=disnake.Status.online,
        activity=disnake.Game("https://github.com/Sheudz/OpenAI-BOT"),
    )
    print("BOT IS UP")


@bot.event
async def on_slash_command_error(
    inter: disnake.ApplicationCommandInteraction,
    error: Union[
        commands.CommandOnCooldown, commands.MissingPermissions, commands.MissingRole
    ],
) -> None:
    if isinstance(error, commands.CommandOnCooldown):
        await inter.response.send_message(
            embed=disnake.Embed(
                title="Error",
                description=f"Спробуйте через {round(error.retry_after, 2)} секунд",
                color=0xFF0000,
            ),
            ephemeral=True,
        )
    elif isinstance(error, commands.MissingPermissions):
        await inter.response.send_message(
            embed=disnake.Embed(
                title="Error",
                description="У тебе невистачає таких прав:\n"
                + "\n".join(error.missing_permissions),
                color=0xFF0000,
            ),
            ephemeral=True,
        )
    elif isinstance(error, commands.MissingRole):
        if isinstance(inter.guild, disnake.Guild):
            role = inter.guild.get_role(int(error.missing_role))
            if isinstance(role, disnake.Role):
                await inter.response.send_message(
                    embed=disnake.Embed(
                        title="Error",
                        description=f"У тебе невистачає цієї ролі: {role.mention}",
                        color=0xFF0000,
                    ),
                    ephemeral=True,
                )
    elif isinstance(error, commands.CommandError):
        await inter.response.send_message(
            embed=disnake.Embed(
                title="Error", description=f"{error.args[0]}", color=0xFF0000
            ),
            ephemeral=True,
        )
    else:
        raise error


@bot.event
async def on_user_command_error(
    inter: disnake.ApplicationCommandInteraction,
    error: Union[
        commands.CommandError,
        commands.CommandOnCooldown,
        commands.MissingPermissions,
        commands.MissingRole,
    ],
) -> None:
    if isinstance(error, commands.CommandOnCooldown):
        await inter.response.send_message(
            embed=disnake.Embed(
                title="Error",
                description=f"Спробуйте через {round(error.retry_after, 2)} секунд",
                color=0xFF0000,
            ),
            ephemeral=True,
        )
    elif isinstance(error, commands.MissingPermissions):
        await inter.response.send_message(
            embed=disnake.Embed(
                title="Error",
                description="У тебе невистачає таких прав:\n"
                + "\n".join(error.missing_permissions),
                color=0xFF0000,
            ),
            ephemeral=True,
        )
    elif isinstance(error, commands.MissingRole):
        if isinstance(inter.guild, disnake.Guild):
            role = inter.guild.get_role(int(error.missing_role))
            if isinstance(role, disnake.Role):
                await inter.response.send_message(
                    embed=disnake.Embed(
                        title="Error",
                        description=f"У тебе невистачає цієї ролі: {role.mention}",
                        color=0xFF0000,
                    ),
                    ephemeral=True,
                )
    elif isinstance(error, commands.CommandError):
        await inter.response.send_message(
            embed=disnake.Embed(
                title="Error", description=f"{error.args[0]}", color=0xFF0000
            ),
            ephemeral=True,
        )
    else:
        raise error


if __name__ == "__main__":
    bot.run(getenv("DISCORD_BOT_TOKEN"))
