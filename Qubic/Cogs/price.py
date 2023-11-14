import discord
from discord.ext import commands
import json
import requests
from requests.exceptions import RequestException, ConnectTimeout

# def get_price():
#     url = "https://api.livecoinwatch.com/coins/single"
#     payload = json.dumps({
#         "currency": "USD",
#         "code": "QUBIC",
#         "meta": True
#     })

#     headers = {
#         'content-type': 'application/json',
#         'x-api-key': '045cd7e4-a5a4-4a12-9473-cb4ec60ce97a'
#     }

#     try:
#         response = requests.request("POST", url, headers=headers, data=payload, timeout=30)
#         response.raise_for_status()  # Raises stored HTTPError, if one occurred.
#         data = json.loads(response.text)
#         price = data['rate']
#         return price
#     except KeyError:
#         return None
#     except RequestException as e:
#         print(f"An error occurred while making the API request: {e}")
#         return None
#     except ConnectTimeout as e:
#         print(f"Connection to the API timed out: {e}")
#         return None

def get_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=qubic-network&vs_currencies=usd"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.
        data = json.loads(response.text)
        price = data['qubic-network']['usd']
        return price
    except KeyError:
        return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the API request: {e}")
        return None
    except requests.exceptions.ConnectTimeout as e:
        print(f"Connection to the API timed out: {e}")
        return None

class Price(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="view qubic price")
    async def price(self, ctx):
        try:
            await ctx.respond(content="Processing your request...", ephemeral=True)

            qubic_price = get_price()
            if qubic_price is not None:
                formatted_price = "{:.8f}".format(qubic_price)
                # await ctx.send(f"$ {formatted_price}")
                await ctx.followup.send(f"${formatted_price}", ephemeral=True)
            else:
                # await ctx.send(content="Failed to get the price. Pls try again")
                message = f"Failed to get the price. Pls try again"
                await ctx.followup.send(content=message, ephemeral=True)
        except Exception as e:
            # If an error occurs, send an error message
            
            # await ctx.send(f"")
            message = f"An error occured, pls try again in a minute"
            await ctx.followup.send(content=message, ephemeral=True)

def setup(bot):
    bot.add_cog(Price(bot))
