from discord.ext import commands
import asyncio


class Reaction:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True,)
    async def react(self, ctx):
        msg = await (self.bot.send_message(ctx.message.channel, 'Use the emojis :thumbsup: and :thumbsdown:'))
        await self.bot.add_reaction(msg, '👍')
        await self.bot.add_reaction(msg, '👎')

        def checks(reaction, user):
            e = str(reaction.emoji)
            return e.startswith(('👍', '👎'))

        await asyncio.sleep(1)
        res = await (self.bot.wait_for_reaction(message=msg, check=checks,))
        await self.bot.send_message(ctx.message.channel, '{0.user.mention} reacted with {0.reaction.emoji}!'.format(res))


def setup(bot):
    bot.add_cog(Reaction(bot))
