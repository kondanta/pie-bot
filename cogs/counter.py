from discord.ext import commands


class MsgCounter:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True,)
    async def count(self, ctx):
        try:
            if not ctx.message.mentions:
                user = ctx.message.author
            else:
                user = ctx.message.mentions[0]
            counter = 0
            tmp = await (self.bot.send_message(ctx.message.channel, 'Calculating messages...'))
            async for log in self.bot.logs_from(ctx.message.channel, limit=100):
                if log.author == user:
                    counter += 1

            await self.bot.edit_message(tmp, '{} has {} messages.'.format(user.mention, counter))
            await self.bot.add_reaction(tmp, '👍')
        except IndexError:
            await self.bot.send_message(ctx.message.channel, 'Please mention someone.')


def setup(bot):
    bot.add_cog(MsgCounter(bot))