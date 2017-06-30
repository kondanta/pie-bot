from discord.ext import commands
import discord


class Info:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, no_pm=True)
    async def info(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid use of command')

    # TODO Gerekli gorursem info serveri tekrar implement ederim

    @info.command(pass_context=True)
    async def user(self, ctx):
        if not ctx.message.mentions:
            user = ctx.message.author
        else:
            user = ctx.message.mentions[0]

        userjoindate = str(user.joined_at).split('.', 1)[0]
        usercreatedate = str(user.created_at).split('.', 1)[0]
        usertoprole = user.top_role
        isadmin = user.server_permissions.administrator
        iconurl = 'https://cdn.discordapp.com/avatars/322892878311587851/ac5a96cec668a4293682be1c237a1086.png?size=2048'

        if isadmin is True:
            x = str(user).split('#', 1)[0]
            testable = 'Yes, {} is an admin.'.format(x)
        elif isadmin is False:
            x = str(user).split('#', 1)[0]
            testable = 'No, {} is not an admin'.format(x)

        embed = discord.Embed(title='Username', description=user.name, color=51, timestamp=ctx.message.timestamp)
        embed.set_author(name='{}'.format(self.bot.user), icon_url=iconurl)
        embed.add_field(name='Discriminator', value=user.discriminator)
        embed.add_field(name='User ID', value=user.id)
        embed.add_field(name='Joined the Server at',value=userjoindate,)
        embed.add_field(name='Account Created at', value=usercreatedate)
        embed.add_field(name='Role', value=usertoprole)
        embed.add_field(name='isAdmin', value=testable)
        embed.set_footer(text='Provided by Pie Bot',icon_url='http://www.stickaz.com/4371-5256-square/cute-bot.png',)
        embed.set_thumbnail(url=user.avatar_url)
        await self.bot.say(embed=embed)
        await self.bot.say('👌')


def setup(bot):
    bot.add_cog(Info(bot))