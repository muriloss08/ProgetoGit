import discord
import random
import feedparser
from discord.ext import commands
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém o token do bot da variável de ambiente
TOKEN = os.getenv('BOT_TOKEN')


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
async def filme(ctx):
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
    
    if not unrecommended_titles:
        await ctx.send("Todos os filmes já foram recomendados.")
        return
    
    title = random.choice(unrecommended_titles)
    recommended_movies.append(title)

    entry = next(entry for entry in entries if entry.title == title)
    link = entry.link

    entry = random.choice(entries)
    title = entry.title
    link = entry.link

    message = f"Recomendação de notícia de filmes:\n\nTítulo: {title}\nLink: {link}"
    await ctx.send(message)
    
bot.run(TOKEN)