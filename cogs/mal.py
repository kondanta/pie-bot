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
MAL_API_MANGA = "https://" + credentials + "@myanimelist.net/api/manga/search.xml?q="
ANIME_LINK = 'https://myanimelist.net/anime/'
MANGA_LINK = 'https://myanimelist.net/manga/'


class Mal:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def mal(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('https://myanimelist.net/profile/kondanta')

    @mal.command(pass_context=True, description="Shows mal profile", usage=".mal profile profilename")
    async def profile(self, ctx, arg: str):
        conn = PROFILE_URL + arg
        anime_manga_info = []  # collecting anime manga, first 6 elements
        user_img = []
        means = []
        spend_days = []
        anime_manga_status = []

        r = requests.get(conn)

        soup = bs(r.content, "html.parser")
        try:
            for i in soup.find_all('div', attrs={'class': 'data'}, limit=6):
                x = i.findNext('a').text
                anime_manga_info.append(x)
            for i in soup.find_all('div', attrs={'class': 'user-image mb8'}):
                img = i.find('img')['src']
                user_img.append(img)
            for i in soup.find_all('div', attrs={'class': 'di-tc ar pr8 fs12 fw-b'}):
                x = i.text
                means.append(x)
            for i in soup.find_all('div', attrs={'class': 'di-tc al pl8 fs12 fw-b'}):
                x = i.text
                spend_days.append(x)
            for i in soup.find_all('div', attrs={'class': 'fn-grey2'}, limit=6):
                x = i.text
                anime_manga_status.append(x)

            # 2 basic function for handling the array.
            def splitter(s):  # makes array ['xy', 'yz']
                return ' '.join(s.split())

            def listintolist(s):  # makes array [[x][y],[y][z]]
                return s.split(" ")

            means = [listintolist(i) for i in means]
            spend_days = [listintolist(i) for i in spend_days]

            test_list = [splitter(i) for i in anime_manga_status]
            anime_manga_status = [listintolist(i) for i in test_list]

            # That means, user has lack of anime, or manga updates.
            if len(anime_manga_status) < 6:
                raise IndexError

            anime_msg = '{}:  {},  {}.  {} : {}\n' \
                        '{}:  {},  {}.  {} : {}\n' \
                        '{}:  {},  {}.  {} : {}\n'.format(anime_manga_info[0], anime_manga_status[0][0],
                                                          anime_manga_status[0][1], anime_manga_status[0][3],
                                                          anime_manga_status[0][4], anime_manga_info[1],
                                                          anime_manga_status[1][0], anime_manga_status[1][1],
                                                          anime_manga_status[1][3], anime_manga_status[1][4],
                                                          anime_manga_info[2], anime_manga_status[2][0],
                                                          anime_manga_status[2][1], anime_manga_status[2][3],
                                                          anime_manga_status[2][4])

            manga_msg = '{}:  {},  {}.  {} : {}\n' \
                        '{}:  {},  {}.  {} : {}\n' \
                        '{}:  {},  {}.  {} : {}\n'.format(anime_manga_info[3], anime_manga_status[3][0],
                                                          anime_manga_status[3][1], anime_manga_status[3][3],
                                                          anime_manga_status[3][4], anime_manga_info[4],
                                                          anime_manga_status[4][0], anime_manga_status[4][1],
                                                          anime_manga_status[4][3], anime_manga_status[4][4],
                                                          anime_manga_info[5], anime_manga_status[5][0],
                                                          anime_manga_status[5][1], anime_manga_status[5][3],
                                                          anime_manga_status[5][4])

            embed = discord.Embed(title="", description="Additional information", color=0x0000ff,
                                  timestamp=ctx.message.timestamp)
            embed.set_author(name=arg, url=conn,
                             icon_url='https://myanimelist.cdn-dena.com/img/sp/icon/apple-touch-icon-256.png')
            embed.set_thumbnail(url=user_img[0])
            embed.add_field(name="Days spent on Anime", value=spend_days[0][1])
            embed.add_field(name="Days spent on Manga", value=spend_days[1][1])
            embed.add_field(name="Mean Anime Score", value=means[0][2])
            embed.add_field(name="Mean Manga Score", value=means[1][2])
            embed.add_field(name="**Latest Anime Updates**", value=anime_msg, inline=False)
            embed.add_field(name="**Latest Manga Updates**", value=manga_msg, inline=False)
            embed.add_field(name="Link", value=conn, inline=False)
            embed.set_footer(text='Provided by Pie Kek')
            await self.bot.say(embed=embed)
        except TypeError:
            await self.bot.say("Skipping")
        except IndexError:
            msg = "This user has not got enough information to show." \
                  "Please check the profile page directly." \
                  "{}".format(conn)
            await self.bot.say(msg)

    @mal.command(pass_context=True, usage=".mal anime manga-name")
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

        # loops for gathering related information
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

        if len(title_list) >= 10:
            table_to_ten = [i for i in title_list[:10]]
        else:
            table_to_ten = title_list

        # message that printed with the list
        msg = "**Please chose one, by its number..**\n"
        msg += "\n ".join(['{} - {}'.format(n + 1, table_to_ten[n]) for n in range(0, len(table_to_ten))])

        try:
            # printing the list itself
            await self.bot.say(msg)
            # it waits for the response after printing the table
            resp = await self.bot.wait_for_message(author=ctx.message.author, timeout=5)
            # resp returns with message object, so I'm changing it's type to string
            # and final part is, converting it to int, -1 for the numbering order
            entry = int(resp.content) - 1
            text = synop_list[0].replace('<br />', ' ').replace('&#039;', "'").replace('[i]', '*').replace('[/i]',
                                                                                                           '*').replace(
                '&mdash;', '—').replace('&quot;', '"').replace('[size=90]', '').replace('[/size]', '').replace('[b]',
                                                                                                               '**').replace(
                '[/b]', '**')

            embed = discord.Embed(title=' ', description=text, color=0x0000ff, timestamp=ctx.message.timestamp)
            embed.set_author(name=title_list[entry], icon_url=images[entry])
            embed.add_field(name="*Type*", value=tur[entry])
            embed.add_field(name="*Episodes*", value=ep[entry])
            embed.add_field(name="*Status*", value=status[entry])
            embed.add_field(name="*Score*", value=score[entry])
            embed.add_field(name="*Link*", value=anime_id[entry])
            embed.set_thumbnail(url=images[entry])

            if end_date[entry] == '0000-00-00':
                footer_msg = 'It is Currently Airing '
            else:
                footer_msg = 'Aired on ' + start_date[entry] + ' to ' + end_date[entry]

            embed.set_footer(text=footer_msg)
            await self.bot.say(embed=embed)
        except IndexError:
            await self.bot.say("Index Error!!")
        except ValueError:
            await self.bot.say("Please enter a number")
        except UnboundLocalError:
            await self.bot.say("Please enter a number")
        except AttributeError:
            await self.bot.say("**Time is up! Please try again... :cry:**")
        except discord.HTTPException:
            await self.bot.say("Connection Error")

    @mal.command(pass_context=True)
    async def manga(self, ctx, *args):
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
            conn = MAL_API_MANGA + x
        elif len(args) < 1:
            await self.bot.say("Please enter an anime name")
            return -1
        else:
            list(args)
            x = args[0]
            conn = MAL_API_MANGA + x

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
            msg = MANGA_LINK + i.text
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

        if len(title_list) >= 10:
            table_to_ten = [i for i in title_list[:10]]
        else:
            table_to_ten = title_list

        # message that printed with the list
        msg = "**Please chose one, by its number..**\n"
        msg += "\n ".join(['{} - {}'.format(n + 1, table_to_ten[n]) for n in range(0, len(table_to_ten))])

        try:
            # printing the list itself
            await self.bot.say(msg)
            # it waits for the response after printing the table
            resp = await self.bot.wait_for_message(author=ctx.message.author, timeout=5)
            # resp returns with message object, so I'm changing it's type to string
            # and final part is, converting it to int, -1 for the numbering order
            entry = int(resp.content) - 1
            text = synop_list[0].replace('<br />', ' ').replace('&#039;', "'").replace('[i]', '*').replace('[/i]',
                                                                                                           '*').replace(
                '&mdash;', '—').replace('&quot;', '"').replace('[size=90]', '').replace('[/size]', '').replace('[b]',
                                                                                                               '**').replace(
                '[/b]', '**')
            embed = discord.Embed(title=' ', description=text, color=0x0000ff, timestamp=ctx.message.timestamp)
            embed.set_author(name=title_list[entry], icon_url=images[entry])
            embed.add_field(name="*Type*", value=tur[entry])
            embed.add_field(name="*Episodes*", value=ep[entry])
            embed.add_field(name="*Status*", value=status[entry])
            embed.add_field(name="*Score*", value=score[entry])
            embed.add_field(name="*Link*", value=anime_id[entry])
            embed.set_thumbnail(url=images[entry])

            if end_date[entry] == '0000-00-00':
                footer_msg = 'It is Currently Publishing '
            else:
                footer_msg = 'Aired on ' + start_date[entry] + ' to ' + end_date[entry]

            embed.set_footer(text=footer_msg)
            await self.bot.say(embed=embed)
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

            
def setup(bot):
    bot.add_cog(Mal(bot))
