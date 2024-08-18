import discord
import ccxt
from discord.ext import commands


exchange = ccxt.bybit()

class Cryptocurrency_0(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name = 'show')
    async def show(self, ctx, symbol: str):
        try:
            ticker = exchange.fetch_ticker(symbol.upper() + '/USDT')
            order_book = exchange.fetch_order_book(symbol.upper() + '/USDT')
            total_volume = ticker["quoteVolume"]
            last_price = ticker["last"]
            market_price = ticker["bid"]
            high_24h = ticker["high"]
            low_24h = ticker["low"]
            open_price = ticker['open']
            ordkauf = order_book['bids'][0][0]
            ordverkauf = order_book['asks'][0][0]
            percent_change = ((last_price - open_price) / open_price) * 100
            embed = discord.Embed(description = 
            f'🟢 **{symbol.upper()}/USDT**\n'
            f'\n'
            f'💵 USD: **L** `${last_price}` ➞ **M** `${market_price}`\n'
            f'📊 Vol: `${total_volume}`\n'
            f'📈 High: `${high_24h}`\n'
            f'📉 Low: `${low_24h}`\n'
            f'\n'
            f'📦 Orders: **K** `${ordkauf}` - **V** `${ordverkauf}`\n'
            f"⬆️ %: `{percent_change:.2f}%`\n"
            f'\n'
            f'[TradingView](https://www.tradingView.com/symbols/{symbol.upper()}) • [Spotix](https://google.com) • [Support](https://discord.gg/fcvyFm37jq)', color = discord.Colour.green())
            embed.set_image(url='https://media.discordapp.net/attachments/1271016541416067082/1273232175700901888/CDB67EF3-183B-4F54-B649-086C9638A68D.PNG?ex=66bddd5e&is=66bc8bde&hm=4c07f3b19e1eddc2a685027c22d176d2f17f304f781d5a6fcd4982d89da2d650&')
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(f'Fehler beim Abrufen des Preises für {symbol}: {str(e)}')


async def setup(client):
    await client.add_cog(Cryptocurrency_0(client))
