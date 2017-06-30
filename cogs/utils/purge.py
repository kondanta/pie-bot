from discord.ext import commands
from cogs.utils import check


class Deletion:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @check.mod_or_permissions(manage_messages=True)
    async def purge(self, ctx, arg: int):
        msg = ctx.message
        deleted = await (self.bot.purge_from(msg.channel, limit=arg))
        await self.bot.send_message(msg.channel, 'Deleted {} message(s)'.format(len(deleted)))


def setup(bot):
    bot.add_cog(Deletion(bot))
