import requests
# import discord
# from discord.ext import commands


url = "https://safe.trade/api/v2/peatio/public/markets/qubicusdt/depth"
custom_user_agent = 'MyCustomUserAgent/1.0'

headers = {
    'User-Agent': custom_user_agent
}

response = requests.get(url, headers=headers)

# Check the response
if response.status_code == 200:
    print('Request was successful')

    try:
        data = response.json()

        # Extract the top 20 asks and bids
        top_asks = data['asks'][:20]
        top_bids = data['bids'][:20]

        print('Top 20 Asks:')
        for ask in top_asks:
            price, quantity = ask
            print(f'Price: {price}, Quantity: {quantity}')

        print('Top 20 Bids:')
        for bid in top_bids:
            price, quantity = bid
            print(f'Price: {price}, Quantity: {quantity}')

    except ValueError:
        print('Invalid JSON response')
else:
    print(f'Request failed with status code {response.status_code}')

    
    




# class Depth(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
        
        


# def setup(bot):
#     bot.add_cog(Depth(bot))