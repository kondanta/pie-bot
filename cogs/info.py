from discord.ext import commands
import discord
import copy
from collections import Counter
import inspect



class Info:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, no_pm=True)
    async def info(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid use of command')

        # channel = ctx.message.channel


    # TODO Gerekli gorursem info serveri tekrar implement ederim

    @info.command(pass_context=True, no_pm=True)
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
        embed.add_field(name='Joined the Server at', value=userjoindate)
        embed.add_field(name='Account Created at', value=usercreatedate)
        embed.add_field(name='Role', value=usertoprole)
        embed.add_field(name='isAdmin', value=testable)
        embed.set_footer(text='Provided by Pie Bot', icon_url='http://www.stickaz.com/4371-5256-square/cute-bot.png')
        embed.set_thumbnail(url=user.avatar_url)
        await self.bot.say(embed=embed)
        await self.bot.say('👌')

    @info.command(name='server', pass_context=True, no_pm=True)
    async def server_info(self, ctx):
        server = ctx.message.server
        roles = [role.name.replace('@', '@\u200b') for role in server.roles]  # gathers sw roles

        secret_member = copy.copy(server.me)
        secret_member.id = '0'
        secret_member.roles = [server.default_role]

        # checking secret channels
        secret_channels = 0
        secret_voice = 0
        text_channels = 0
        for channel in server.channels:
            perms = channel.permissions_for(secret_member)
            is_text = channel.type == discord.ChannelType.text
            text_channels += is_text
            if is_text and not perms.read_messages:
                secret_channels += 1
            elif not is_text and (not perms.connect or not perms.speak):
                secret_voice += 1

        voice_channels = len(server.channels) - text_channels
        member_by_status = Counter(str(m.status) for m in server.members)
        e = discord.Embed()
        e.title = 'Info for ' + server.name
        e.add_field(name='ID', value=server.id)
        e.add_field(name='Owner', value=server.owner)
        if server.icon:
            e.set_thumbnail(url=server.icon_url)
        if server.splash:
            e.set_image(url=server.splash_url)
        e.add_field(name='Partnered?', value='Yes' if len(server.features) >= 3 else 'No')
        fmt = 'Text %s (%s secret)\nVoice %s (%s locked)'
        e.add_field(name='Channels', value=fmt % (text_channels, secret_channels, voice_channels, secret_voice))
        fmt = 'Total: {0}\nOnline: {1[online]}' \
              ', Offline: {1[offline]}' \
              '\nDnD: {1[dnd]}' \
              ', Idle: {1[idle]}'
        e.add_field(name='Members', value=fmt.format(server.member_count, member_by_status))
        e.add_field(name='Roles', value=', '.join(roles) if len(roles) < 10 else '%s roles' % len(roles))
        e.set_footer(text='Provided by Pie Kek').timestamp = server.created_at
        await self.bot.say(embed=e)



def setup(bot):
    bot.add_cog(Info(bot))