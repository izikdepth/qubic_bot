import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot) :
        self.bot = bot 
    

    @commands.slash_command(description="help command")
    async def help(self,ctx):
        message = (
            "/ask - you can use this command to see how much USD you'll get for selling Qubic. Simple type ask and enter the qubic quantity\n"
            "/bid - you can use this command to see how much qubic you'll get for your USD. simply type /bid and enter the usd you want to buy with.\n"
            "/price - use this command to view the price of qubic\n"
            "/help to view all commands"
        )
        
        await ctx.send(message)
        
def setup(bot):
    bot.add_cog(Help(bot))
        