from urllib.parse import urlencode
from discord.ext import commands
from cogs.utils import check


class Echo:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @check.admin_or_permissions(administrator=True)
    async def echo(self, ctx):
        """Git gud"""
        message = ctx.message.content.split(' ', 1)[1]
        await self.bot.send_message(ctx.message.channel, message)

    @commands.command(pass_context=True)
    async def author(self, ctx):
        """Tips... Also you can find me under the nickname kondanta"""
        f = {'q': 'Author'}
        url = 'https://github.com/kondanta'.format(urlencode({'q': ' '.join(f)}))
        await self.bot.send_message(ctx.message.channel, url)

    @commands.command(pass_context=True)
    async def hi(self, ctx):
        msg = 'Hello {0.author.mention}'.format(ctx.message)
        await self.bot.send_message(ctx.message.channel, msg)

    @check.is_owner()
    @commands.command(pass_context=True)
    async def owner(self, ctx):
        """Tells the owner of the bot"""
        msg = 'My owner is {0.author.mention}'.format(ctx.message)
        await self.bot.send_message(ctx.message.channel, msg)

    @commands.command(pass_context=True)
    async def lenny(self):
        """prints the lenny face"""
        msg = '( ͡° ͜ʖ ͡°)'
        await self.bot.say(msg)


def setup(bot):
    bot.add_cog(Echo(bot))
