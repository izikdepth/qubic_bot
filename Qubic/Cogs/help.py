import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot) :
        self.bot = bot 
    

    @commands.slash_command(description="help command")
    async def help(self,ctx):

        initial_response = await ctx.send(content="Processing your request...")

        message = (
            "/sell - you can use this command to see how much USD you'll get for selling Qubic. Simple type ask and enter the qubic quantity\n"
            "/buy - you can use this command to see how much qubic you'll get for your USD. simply type /bid and enter the usd you want to buy with.\n"
            "/price - use this command to view the price of qubic\n\n"
            "/rate -  to view the current rate per billion and top bids/asks\n\n"
            "/help to view all commands"
        )
        
        await initial_response.edit(content=message)
        
def setup(bot):
    bot.add_cog(Help(bot))
        
