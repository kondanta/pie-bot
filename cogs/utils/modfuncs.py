from discord.ext import commands
from cogs.utils import check
import discord


class ModFuncs:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pm=True)
    @check.admin_or_permissions(kick_members=True)
    async def kick(self, *, member: discord.Member):
        try:
            await self.bot.kick(member)
        except discord.Forbidden:
            await self.bot.say('I don\'t have the permission to kick this user.')
        except discord.HTTPException:
            await self.bot.say('Failed.')
        else:
            await self.bot.say('👌')

    @commands.command(no_pm=True)
    @check.admin_or_permissions(ban_members=True)
    async def ban(self, *, member: discord.Member):
        try:
            await self.bot.ban(member)
        except discord.Forbidden:
            await self.bot.say('The bot does not have permissions to ban this member.')
        except discord.HTTPException:
            await self.bot.say('Banning failed.')
        else:
            await self.bot.say('👌')

    @commands.command(no_pm=True)
    @check.admin_or_permissions(kick_members=True)
    async def softban(self, *, member: discord.Member):
        """Soft bans a member from the server.
        A softban is basically banning the member from the server but
        then unbanning the member as well. This allows you to essentially
        kick the member while removing their messages.
        To use this command you must have Kick Members permissions or have
        the Bot Admin role. Note that the bot must have the permission as well.
        """
        try:
            await self.bot.ban(member)
            await self.bot.unban(member.server, member)
        except discord.Forbidden:
            await self.bot.say('The bot does not have permissions to ban this member.')
        except discord.HTTPException:
            await self.bot.say('Banning failed.')
        else:
            await self.bot.say('👌')



def setup(bot):
    bot.add_cog(ModFuncs(bot))
