import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot) :
        self.bot = bot 
    

    @commands.slash_command(description="help command")
    async def help(self,ctx):
        
        await ctx.respond(content="Processing your request...", ephemeral=True)

        message = (
            "/sell - you can use this command to see how much USD you'll get for selling Qubic. Simple type ask and enter the qubic quantity\n\n"
            "/buy - you can use this command to see how much qubic you'll get for your USD. simply type /bid and enter the usd you want to buy with.\n\n"
            "/price - use this command to view the price of qubic\n\n"
            "/rate -  to view the current rate per billion and top bids/asks\n\n"
            "/help to view all commands\n"
        )
        
        await ctx.followup.send(content=message, ephemeral=True)

        
def setup(bot):
    bot.add_cog(Help(bot))
        
