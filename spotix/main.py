import discord
from flask import Flask, jsonify
import aiosqlite
import requests
import random
import asyncio
import os
from threading import Thread
from discord.ext import commands, tasks
import ccxt


# LISTNERS / IMPORTS

from events.guild_events import on_guild_join
from events.join_events import on_member_join

# client.add_listener(on_guild_join)
# client.add_listener(on_member_join)
# Flask Webserver Setup
app = Flask(__name__)

# Virtuelle Spielerprofile
players = {}
active_trades = {}

exchange = ccxt.bybit()

intents = discord.Intents.all()
client = commands.Bot(command_prefix = '!', intents = intents)


@client.event
async def on_ready():
    print('=================================================')
    print(f'Botname: {client.user} • Botid: {client.user.id}')

    # -- LOADER
    for filename in os.listdir('./cogs/essential'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.essential.{filename[:-3]}')
    
    for filename in os.listdir('./cogs/currency'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.currency.{filename[:-3]}')
    
    for filename in os.listdir('./cogs/safeguard'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.safeguard.{filename[:-3]}')
		

		



client.add_listener(on_guild_join)
client.add_listener(on_member_join)

# -- USER-PROFIL COMMANDS


#APPS

@app.route('/')
def index():
    return jsonify({"message": "SPOTIX"})

@app.route('/profile/<int:user_id>', methods=['GET'])
def profile(user_id):
    player = get_player_profile(user_id)
    return jsonify(player)



# -- USER COMMANDS

@client.command(name='adde')
async def add_emoji(ctx):
    emoji_path = ""  # put your desired file path to get the emoji from
    with open(emoji_path, "rb") as f:
        await ctx.guild.create_custom_emoji(name="emoji_name", image=f.read())

@client.command(name='markets')
async def market_command(ctx):
    try:
        exchange = ccxt.binance()

        # Abrufen aller Markt-Ticker
        tickers = exchange.fetch_tickers()

        # Liste zur Speicherung von Gewinnern, Verlierern und Coins mit höchstem Volumen
        gainers = []
        losers = []
        top_volume = []

        for symbol, ticker in tickers.items():
            percentage_change = ticker.get('percentage', None)
            volume = ticker.get('quoteVolume', None)
            market_data = {
                'symbol': symbol,
                'percentage': percentage_change if percentage_change is not None else 0,
                'volume': volume if volume is not None else 0
            }

            if percentage_change is not None:
                if percentage_change > 0:
                    gainers.append(market_data)
                elif percentage_change < 0:
                    losers.append(market_data)
            top_volume.append(market_data)

        # Sortieren der Listen
        gainers = sorted(gainers, key=lambda x: x['percentage'], reverse=True)[:5]
        losers = sorted(losers, key=lambda x: x['percentage'])[:5]
        top_volume = sorted(top_volume, key=lambda x: x['volume'], reverse=True)[:5]

        # Erstellen und Senden der Nachricht
        embed = discord.Embed(title="📈 Marktübersicht", color=0x1ABC9C)
        
        # Top-Gewinner
        embed.add_field(name="Top Gewinner", value="\n".join([f"{g['symbol']}: {g['percentage']}%" for g in gainers]), inline=False)
        
        # Top-Verlierer
        embed.add_field(name="Top Verlierer", value="\n".join([f"{l['symbol']}: {l['percentage']}%" for l in losers]), inline=False)
        
        # Top Volumen
        embed.add_field(name="Top Volumen", value="\n".join([f"{v['symbol']}: {v['volume']}" for v in top_volume]), inline=False)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"Fehler beim Abrufen der Marktdaten: {str(e)}")


token = ('')

async def start_discord_bot():
    await client.start(token)

def start_flask():
    app.run(port=5000)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    
    # Starte den Flask-Server in einem separaten Thread
    flask_thread = loop.run_in_executor(None, start_flask)
    
    # Starte den Discord-Bot im Event-Loop
    loop.run_until_complete(start_discord_bot())
