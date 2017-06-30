from discord.ext import commands
import json
import logging
import traceback
import sys

# TODO command.on.error eklenecek.

extension = [
            'cogs.counter',
            'cogs.echo',
            'cogs.utils.modfuncs',
            'cogs.react',
            'cogs.utils.purge',
            'cogs.info',
            'cogs.mal'
]

discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='Pie.log', encoding='utf-8', mode='w')
log.addHandler(handler)


bot = commands.Bot(command_prefix='.', description='Pie Bot', pm_help=None)


@bot.event
async def on_ready():
    print('Logged in')
    print(bot.user.name)
    print(bot.user.id)


@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.NoPrivateMessage):
        await bot.send_message(ctx.message.author, 'This command cannot be used in private messages.')
    elif isinstance(error, commands.DisabledCommand):
        await bot.send_message(ctx.message.author, 'Sorry. This command is disabled and cannot be used.')
    elif isinstance(error, commands.CommandInvokeError):
        print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
        traceback.print_tb(error.original.__traceback__)
        print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)


@bot.event
async def on_member_join(member):
    server = member.server
    fmt = 'Welcome {0.mention} to {1.name}!'
    await bot.send_message(server, fmt.format(member, server))


@bot.event
async def on_member_leave(member):
    server = member.server
    fmt = '{0.mention} bye bye'
    await bot.send_message(server, fmt.format(member))


@bot.command()
async def load(extension_name : str):
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))


@bot.command()
async def unload(extension_name : str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))

f = open('info.json')
data = json.load(f)
token = data['token']


if __name__ == "__main__":
    for extension in extension:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run(token)
handlers = log.handlers[:]
for hdlr in handlers:
    hdlr.close()
    log.removeHandler(hdlr)
