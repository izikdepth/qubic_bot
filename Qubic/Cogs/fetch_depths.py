import aiohttp
import discord
from discord.ext import commands
from Cogs.price import get_price
import requests


def format_quantity(quantity):
    if quantity >= 1_000_000_000_000:
        return f"{quantity / 1_000_000_000_000:.2f} trillion"
    elif quantity >= 1_000_000_000:
        return f"{quantity / 1_000_000_000:.2f} billion"
    elif quantity >= 1_000_000:
        return f"{quantity / 1_000_000:.2f} million"
    else:
        return str(quantity)

class MarketDepthCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="see how much you'll sell  $ for qubic")
    async def ask(self, ctx, quantity: int):
        initial_response = await ctx.send(content="Processing your request...")

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
                        if total_quantity + ask_quantity <= quantity:
                            total_quantity += ask_quantity
                            total_amount += price * ask_quantity
                        else:
                            remaining_quantity = quantity - total_quantity
                            total_quantity += remaining_quantity  # Add the remaining quantity to the total quantity
                            total_amount += price * remaining_quantity
                            break

                    total_amount = int(total_amount)  # Remove decimals from USD result
                    formatted_quantity = format_quantity(total_quantity)
                    formatted_amount = "{:,}".format(total_amount)  # Add commas as thousand separators

                    message = f"With {formatted_quantity} Qubic coins, you can sell for ${formatted_amount}."
                    await initial_response.edit(content=message)
                else:
                    await initial_response.edit(content=f'Request failed with status code {response.status}')


    
    @commands.slash_command(description="see how much you'll buy $ for qubic")
    async def bid(self, ctx, amount: int):
        initial_response = await ctx.send(content="Processing your request...")

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
                        if total_amount + (price * bid_quantity) <= amount:
                            total_quantity += bid_quantity
                            total_amount += price * bid_quantity
                        else:
                            remaining_amount = amount - total_amount
                            remaining_quantity = remaining_amount / price
                            total_quantity += remaining_quantity  # Add the remaining quantity to the total quantity
                            total_amount += price * remaining_quantity
                            break

                    total_amount = int(total_amount)  # Remove decimals from USD result
                    formatted_quantity = format_quantity(total_quantity)
                    formatted_amount = "{:,}".format(total_amount)  # Add commas as thousand separators

                    message = f"With ${formatted_amount}, you can bid for {formatted_quantity} Qubic coins."
                    await initial_response.edit(content=message)
                else:
                    await initial_response.edit(content=f'Request failed with status code {response.status}')



    
    #this function calculates how much  qubic coins are worth per billion. 
    @commands.slash_command(description="view the price of qubic per billion")
    async def rate(self, ctx):
        # Defer the response
        # await ctx.defer()

        initial_response = await ctx.send(content="Processing your request,pls wait...")

        try:
            qubic_price = get_price()
            per_per_billion = qubic_price * 1_000_000_000
            formatted_number = "{:.3f}".format(per_per_billion)
            message = f"Current rate per billion qubic coins is ${formatted_number}/bln"
        except requests.exceptions.RequestException as e:
            # Handle the exception if there's a connection error
            message = "Error: Unable to fetch the rates. Please try again ."

        await initial_response.edit(content=message)

def setup(bot):
    bot.add_cog(MarketDepthCog(bot))
