import aiohttp
import discord
from discord.ext import commands
from Cogs.price import get_price
import requests


def format_quantity(quantity):
    if quantity >= 1_000_000_000_000:
        return f"{quantity / 1_000_000_000_000:.2f} Tln"
    elif quantity >= 1_000_000_000:
        return f"{quantity / 1_000_000_000:.2f} Bln"
    elif quantity >= 1_000_000:
        return f"{quantity / 1_000_000:.2f} Mln"
    else:
        return str(quantity)

class MarketDepthCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    
    @commands.slash_command(description="see how much you'll by buying qubic with ur $")
    async def buy(self, ctx, amount: int):
        await ctx.respond(content="Processing your request...", ephemeral=True)

        url = "https://safe.trade/api/v2/peatio/public/markets/qubicusdt/depth"
        custom_user_agent = 'MyCustomUserAgent/1.0'
        headers = {'User-Agent': custom_user_agent}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()

                    asks = data['asks']

                    total_quantity = 0
                    total_amount = 0
                    for price, ask_quantity in asks:
                        price = float(price)
                        ask_quantity = float(ask_quantity)
                        if total_amount + (price * ask_quantity) <= amount:
                            total_quantity += ask_quantity
                            total_amount += price * ask_quantity
                        else:
                            remaining_amount = amount - total_amount
                            remaining_quantity = remaining_amount / price
                            total_quantity += remaining_quantity  # Add the remaining quantity to the total quantity
                            total_amount += price * remaining_quantity
                            break

                    total_amount = int(total_amount)  # Remove decimals from USD result
                    formatted_quantity = format_quantity(total_quantity)
                    formatted_amount = "{:,}".format(total_amount)  # Add commas as thousand separators

                    message = f"With ${formatted_amount} you can buy for {formatted_quantity} Qubic coins."
                    await ctx.followup.send(content=message, ephemeral=True)
                else:
                    await ctx.followup.send(content=f'Request failed with status code {response.status}', ephemeral=True)


    @commands.slash_command(description="see how much you'll get by selling qubic")
    async def sell(self, ctx, quantity: int):
        await ctx.respond(content="Processing your request...", ephemeral=True)

        url = "https://safe.trade/api/v2/peatio/public/markets/qubicusdt/depth"
        custom_user_agent = 'MyCustomUserAgent/1.0'
        headers = {'User-Agent': custom_user_agent}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()

                    bids = data['bids']

                    total_quantity = 0
                    total_amount = 0
                    for price, bid_quantity in bids:
                        price = float(price)
                        bid_quantity = float(bid_quantity)
                        if total_quantity + bid_quantity <= quantity:
                            total_quantity += bid_quantity
                            total_amount += price * bid_quantity
                        else:
                            remaining_quantity = quantity - total_quantity
                            total_quantity += remaining_quantity  # Add the remaining quantity to the total quantity
                            total_amount += price * remaining_quantity
                            break

                    total_amount = int(total_amount)  # Remove decimals from USD result
                    formatted_quantity = format_quantity(total_quantity)
                    formatted_amount = "{:,}".format(total_amount)  # Add commas as thousand separators

                    message = f"With {formatted_quantity} Qubic coins, you can sell for ${formatted_amount}."
                    
                    await ctx.followup.send(content=message, ephemeral=True)
                else:
                    await ctx.followup.send(content=f'Request failed with status code {response.status}', ephemeral=True)



    @commands.slash_command(description="view the rate and top bids/asks")
    async def rate(self, ctx):
        initial_response = await ctx.respond(content="Processing your request...", ephemeral=True)

        url = "https://safe.trade/api/v2/peatio/public/markets/qubicusdt/depth"
        custom_user_agent = 'MyCustomUserAgent/1.0'
        headers = {'User-Agent': custom_user_agent}

        quantities = [10_000_000_000, 50_000_000_000, 100_000_000_000, 200_000_000_000]

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()

                    asks = data['asks']
                    bids = data['bids']

                    ask_message = "Sell on safe.trade:\n\n"
                    for ask, quantity in zip(asks, quantities):
                        price = float(ask[0])
                        total_price = int(price * quantity)
                        price_per_bln = int(price * 1_000_000_000)
                        ask_message += f"{format_quantity(quantity)}: {price_per_bln} usd/bln\n"

                    bid_message = "Buy on safe.trade:\n\n"
                    for bid, quantity in zip(bids, quantities):
                        price = float(bid[0])
                        total_price = int(price * quantity)
                        price_per_bln = int(price * 1_000_000_000)
                        bid_message += f"{format_quantity(quantity)}: {price_per_bln} usd/bln\n"

                    price_per_bln = int(get_price() * 1_000_000_000)
                    message = f"Current rate per billion qubic coins is ${price_per_bln}/bln\n\n" + f"{ask_message}\n" + f"{bid_message}\n"
                    await ctx.followup.send(content=message, ephemeral=True)
                else:
                    await ctx.followup.send(content=f'Request failed with status code {response.status}', ephemeral=True)

    

    
def setup(bot):
    bot.add_cog(MarketDepthCog(bot))
