import disnake
from disnake.ext import commands

from datetime import timedelta
from time import time


class Misc(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
        self.start_time = time()

    @commands.slash_command(name="uptime", description="shows bot uptime")
    async def uptime(
        self,
        inter: disnake.interactions.application_command.ApplicationCommandInteraction,
    ) -> None:
        current_time = time()
        difference = int(round(current_time - self.start_time))
        text = str(timedelta(seconds=difference))
        embed = disnake.Embed(color=0x14F803)
        embed.add_field(name="Uptime", value=text)
        await inter.response.send_message(embed=embed, ephemeral=True)

    @commands.slash_command(name="ping", description="measures latency")
    async def ping(
        self,
        inter: disnake.interactions.application_command.ApplicationCommandInteraction,
    ) -> None:
        await inter.response.send_message(
            embed=disnake.Embed(
                title="Ping",
                description=f"Pong:  {round(self.bot.latency * 1000)}ms",
                color=0x14F803,
            ),
            ephemeral=True,
        )


def setup(bot: commands.InteractionBot) -> None:
    bot.add_cog(Misc(bot))
