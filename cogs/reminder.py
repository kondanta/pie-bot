from discord.ext import commands
import asyncio
import datetime
import re
from cogs.utils import formats


# Note: Entire file with/ formats taken from *https://github.com/Rapptz
class TimeParser:
    def __init__(self, argument):
        compiled = re.compile(r"(?:(?P<hours>[0-9]{1,5})h)?(?:(?P<minutes>[0-9]{1,5})m)?(?:(?P<seconds>[0-9]{1,5})s)?$")
        self.original = argument
        try:
            self.seconds = int(argument)
        except ValueError as e:
            match = compiled.match(argument)
            if match is None or not match.group(0):
                raise commands.BadArgument('Failed to parse time.') from e

            self.seconds = 0
            hours = match.group('hours')
            if hours is not None:
                self.seconds += int(hours) * 3600
            minutes = match.group('minutes')
            if minutes is not None:
                self.seconds += int(minutes) * 60
            seconds = match.group('seconds')
            if seconds is not None:
                self.seconds += int(seconds)

        if self.seconds <= 0:
            raise commands.BadArgument('Bad time provided.')

        if self.seconds > 604800: # 7 days
            raise commands.BadArgument('That\'s a bit too far in the future for me.')


class Reminder:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, usage=".reminder time text")
    async def reminder(self, ctx, time: TimeParser, *, message=''):

        author = ctx.message.author
        reminder = None
        completed = None
        message = message.replace('@everyone', '@\u200beveryone').replace('@here', '@\u200bhere')

        if not message:
            reminder = '{0.mention}, You\'ll be noticed when the time {1} comes.'
            completed = '{0.mention}! You asked to be reminded about something {2}.'
        else:
            reminder = '{0.mention} You\'ll be noticed about "{2}" in {1}.'
            completed = '{0.mention}! You asked to be reminded about "{1}", {2}.'

        human_time = datetime.datetime.utcnow() - datetime.timedelta(seconds=time.seconds)
        human_time = formats.human_timedelta(human_time)

        await self.bot.say(reminder.format(author, human_time.replace('ago', ''), message))
        await asyncio.sleep(time.seconds)
        await self.bot.say(completed.format(author, message, human_time))

    @reminder.error
    async def timer_error(self, error, ctx):
        if isinstance(error, commands.BadArgument):
            await self.bot.say(str(error))


def setup(bot):
    bot.add_cog(Reminder(bot))