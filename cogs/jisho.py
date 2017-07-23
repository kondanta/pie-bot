# -*- coding: utf8 -*-

from discord.ext import commands
import discord
from urllib import request
import json


BASE_URL = 'http://jisho.org/api/v1/search/words?keyword='
BASE_LINK = 'http://jisho.org/search'

# logic -> something =  urllib.request.urlopen('customized url'),
# json -> something = json.load(something)
# for item in data['data']: print(item['japanese'])


class Jisho:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def jisho(self, ctx, arg: str):
        """Quick Look up from Jisho.org"""
        japanese_words = []
        readings = []
        meanings = []
        part_of_speech = []
        conn = BASE_URL + arg
        word_link = BASE_LINK + '/' + arg
        http = request.urlopen(conn)

        json_data = json.load(http)
        if not json_data['data']:
            await self.bot.say("I cannot find the word.")
            return -1
        # Starting to load values.
        for item in json_data['data']:
            try:
                try:
                    value2 = item['japanese'][0]['reading']
                    value1 = item['japanese'][0]['word']
                    value3 = item['senses'][0]['english_definitions']
                    value4 = item['senses'][0]['parts_of_speech']
                except KeyError:  # Kinda fucked up way to edit if there is no kanji case.
                    value1 = item['japanese'][0]['reading']
                    value3 = item['senses'][0]['english_definitions']
                    value4 = item['senses'][0]['parts_of_speech']
                readings.append(value2)
                japanese_words.append(value1)
                meanings.append(value3)
                part_of_speech.append(value4)
            except:
                await self.bot.say("Uh....")

        if len(japanese_words) >= 10:
            table_to_ten = [i for i in japanese_words[:10]]
        else:
            table_to_ten = japanese_words

        # message that printed with the list
        msg = "**Please chose one, by its number..**\n"
        msg += "\n ".join(['{} - {}'.format(n + 1, table_to_ten[n]) for n in range(0, len(table_to_ten))])

        try:
            # printing the list itself
            await self.bot.say(msg)
            # it waits for the response after printing the table
            resp = await self.bot.wait_for_message(author=ctx.message.author, timeout=7)
            # resp returns with message object, so I'm changing it's type to string
            # and final part is, converting it to int, -1 for the numbering order
            entry = int(resp.content) - 1

            e = discord.Embed(title='', description=readings[entry], timestamp=ctx.message.timestamp,
                              color=0xff0000)
            e.set_author(name=japanese_words[entry], url=word_link,
                         icon_url="https://qph.ec.quoracdn.net/main-qimg-4e8f332134d4ae07214bbce9e77759a6",
                         )
            e.add_field(name="Meaning", value=meanings[entry], inline=False)
            e.add_field(name="Part of Speech", value=part_of_speech[entry])
            e.add_field(name="Link", value=word_link)
            e.set_footer(text='Provided by Pie Kek')

            await self.bot.say(embed=e)
        except UnicodeEncodeError:
            await self.bot.say("I cannot read kanji -for now-")
        except IndexError:
            await self.bot.say("Index Error!!")
        except ValueError:
            await self.bot.say("Please enter a number")
        except UnboundLocalError:
            await self.bot.say("Please enter a number that shown on the list")
        except AttributeError:
            await self.bot.say("**Time is up! Please try again... :cry:**")
        except discord.HTTPException:
            await self.bot.say("Connection Error")
        except TypeError:
            await self.bot.say("Something went wrong, please try again.!.")


def setup(bot):
    bot.add_cog(Jisho(bot))
