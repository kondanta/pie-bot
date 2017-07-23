from discord.ext import commands
from cogs.utils import check
import discord


class Deletion:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, usage="purge `number`")
    @check.mod_or_permissions(manage_messages=True)
    async def purge(self, ctx, arg: int):
        """Deletes the messages: Limited -> Deletes only messages that are under 14 days old.
        """
        try:
            msg = ctx.message
            deleted = await (self.bot.purge_from(msg.channel, limit=arg))
            await self.bot.send_message(msg.channel, 'Deleted {} message(s)'.format(len(deleted)))
        except discord.HTTPException:
            await self.bot.say("For now, I can only delete messages that are under 14 days old.")


def setup(bot):
    bot.add_cog(Deletion(bot))
