import discord
import random
import feedparser
from discord.ext import commands

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
recommended_movies = []

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

@bot.command()
async def recomenda(ctx):
    url = 'https://cinematecando.com.br/feed/'
    
    feed = feedparser.parse(url)

    if 'entries' not in feed:
        await ctx.send("Não foi possível obter os filmes do feed.")
        return

    entries = feed.entries

    if not entries:
        await ctx.send("Não foram encontrados filmes no feed.")
        return

    titles = [entry.title for entry in entries]
    unrecommended_titles = list(set(titles) - set(recommended_movies))

    if len(unrecommended_titles) < 5:
        await ctx.send("Não há filmes suficientes para recomendar.")
        return

    movie_titles = random.sample(unrecommended_titles, 5)
    recommended_movies.extend(movie_titles)

    message = "Recomendação de notícias de filmes:\n\n"
    for title in movie_titles:
        entry = next(entry for entry in entries if entry.title == title)
        link = entry.link
        message += f"Título: {title}\nLink: {link}\n\n"

    await ctx.send(message)

bot.run('MTExNjQ3NDIxMTQ5ODcyNTQ3NQ.GSjdW1.-VgEQvHWlJeRmGn-7ol0Ua1SgdECHUb4WCH__o')