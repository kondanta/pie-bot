from discord.ext import commands
import json

# TODO command.on.error eklenecek.

extension = [
            'cogs.counter',
]

bot = commands.Bot(command_prefix='.', description='Pie Bot')


@bot.event
async def on_ready():
    print('Logged in')
    print(bot.user.name)
    print(bot.user.id)


@bot.commands()
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


if __name__ == "__main__":
    for extension in extension:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run(token)