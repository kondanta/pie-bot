from discord.ext import commands
from bs4 import BeautifulSoup as bs
import requests
import discord
import json

f = open('info.json')
data = json.load(f)
credentials = data['user'] + ":" + data['pass']

PROFILE_URL = "https://myanimelist.net/profile/"
MAL_API_ANIME = "https://" + credentials + "@myanimelist.net/api/anime/search.xml?q="
ANIME_LINK = 'https://myanimelist.net/anime/'


class Mal:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def mal(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('https://myanimelist.net/profile/kondanta')

    @mal.command(pass_context=True)
    async def lastanime(self, ctx, arg: str):
        # base definitions.
        conn = PROFILE_URL + arg
        titles = []
        links = []
        img_list = []
        episode_infos_dump = []

        r = requests.get(conn)
        soup = bs(r.content, "html.parser")

        data = soup.find_all('div', attrs={'class': 'updates anime'})  # need to specify for the image loop

        # takes the anime's name with it's mal link
        # for link in data:
        try:
            for item in soup.find_all('div', attrs={'class': 'data'}, limit=3):
                x = item.findNext('a').text
                y = item.findNext('a')['href']
                links.append(y)
                titles.append(x)
        except TypeError:
            await self.bot.say("Skip")

        # takes the rest of the info such as status, how many episodes watched.
        # for value in data:
        try:
            for item in soup.find_all('div', attrs={'class': 'fn-grey2'}, limit=3):
                x = item.text
                episode_infos_dump.append(x)
        except TypeError:
            await self.bot.say("skip")

        # takes the anime's image. later printed in thumbnail
        for images in data:
            try:
                for item in images.find_all('img'):
                    x = item.get('src')
                    img_list.append(x)
            except TypeError:
                await self.bot.say('skip')

        # 2 basic function for handling the array.
        def splitter(s):  # makes array ['xy', 'yz']
            return ' '.join(s.split())

        def listintolist(s):  # makes array [[x][y],[y][z]]
            return s.split(" ")

        # TODO try to get rid of these 2 list below

        ep_inf = [splitter(i) for i in episode_infos_dump]
        episode_info = [listintolist(i) for i in ep_inf]

        # first embed for the first anine
        embed = discord.Embed(title=' ', description="Details", color=0x0000ff, timestamp=ctx.message.timestamp)
        embed.set_author(name=titles[0], url=links[0],
                         icon_url='https://myanimelist.cdn-dena.com/img/sp/icon/apple-touch-icon-256.png')
        embed.add_field(name='Status', value=episode_info[0][0])
        embed.add_field(name='Score', value=episode_info[0][4])
        embed.set_thumbnail(url=img_list[0])
        embed.set_footer(text="Provided by Pie Kek")

        # second embed for the second anime
        embed2 = discord.Embed(title=' ', description="Details", color=0x0000ff, timestamp=ctx.message.timestamp)
        embed2.set_author(name=titles[1], url=links[1],
                          icon_url='https://myanimelist.cdn-dena.com/img/sp/icon/apple-touch-icon-256.png')
        embed2.add_field(name='Status', value=episode_info[1][0])
        embed2.add_field(name='Score', value=episode_info[1][4])
        embed2.set_thumbnail(url=img_list[1])
        embed2.set_footer(text="Provided by Pie Kek")

        # third embed for the third anime
        embed3 = discord.Embed(title=' ', description="Details", color=0x0000ff, timestamp=ctx.message.timestamp)
        embed3.set_author(name=titles[2], url=links[2],
                          icon_url='https://myanimelist.cdn-dena.com/img/sp/icon/apple-touch-icon-256.png')
        embed3.add_field(name='Status', value=episode_info[2][0])
        embed3.add_field(name='Score', value=episode_info[2][4])
        embed3.set_thumbnail(url=img_list[2])
        embed3.set_footer(text="Provided by Pie Kek")

        await self.bot.say(embed=embed)
        await self.bot.say(embed=embed2)
        await self.bot.say(embed=embed3)

    @mal.command(pass_context=True,)
    async def anime(self, ctx, *args):
        # typedefs
        title_list = []
        synop_list = []
        status = []
        score = []
        images = []
        tur = []
        ep = []
        start_date = []
        end_date = []
        anime_id = []

        # checks if the argument is one , or multiple
        if len(args) >= 2:
            list(args)
            x = '+'.join(args)
            conn = MAL_API_ANIME + x
        elif len(args) < 1:
            await self.bot.say("Please enter an anime name")
            return -1
        else:
            list(args)
            x = args[0]
            conn = MAL_API_ANIME + x

        r = requests.get(conn)
        soup = bs(r.content, 'lxml')

        # loops for gathering related informations
        for i in soup.find_all('title'):
            title_list.append(i.text)

        for y in soup.find_all('synopsis'):
            synop_list.append(y.text)

        for i in soup.find_all('image'):
            images.append(i.text)

        for i in soup.find_all('id'):
            msg = ANIME_LINK + i.text
            anime_id.append(msg)
        for i in soup.find_all('type'):
            tur.append(i.text)
        for i in soup.find_all('score'):
            score.append(i.text)
        for i in soup.find_all('status'):
            status.append(i.text)
        for i in soup.find_all('status'):
            ep.append(i.text)
        for i in soup.find_all('start_date'):
            start_date.append(i.text)
        for i in soup.find_all('end_date'):
            end_date.append(i.text)
        try:
            text = synop_list[0].replace('<br />', ' ').replace('&#039;', "'").replace('[i]', '*').replace('[/i]', '*').replace('&mdash;', '—').replace('&quot;', '"')
            embed = discord.Embed(title=' ', description=text, color=0x0000ff, timestamp=ctx.message.timestamp)
            embed.set_author(name=title_list[0], icon_url=images[0])
            embed.add_field(name="*Type*", value=tur[0])
            embed.add_field(name="*Episodes*", value=ep[0])
            embed.add_field(name="*Status*", value=status[0])
            embed.add_field(name="*Score*", value=score[0])
            embed.add_field(name="*Link*", value=anime_id[0])
            embed.set_thumbnail(url=images[0])

            msg ='Aired on ' + start_date[0] + ' to ' + end_date[0]
            embed.set_footer(text=msg)
            await self.bot.say(embed=embed)
        except IndexError:
            await self.bot.say("Index Error!!")


def setup(bot):
    bot.add_cog(Mal(bot))
