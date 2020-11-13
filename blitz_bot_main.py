import discord
import itertools
from discord.ext import commands
import discord.utils
import val_game_stats
import val_player_stats

bot = commands.Bot(command_prefix='-')

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Made by Shep and Peter!'))
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')

#E7103D

bot.add_cog(val_game_stats.ValGameStats(bot))
bot.add_cog(val_player_stats.ValGameStats(bot))
with open('blitz_bot_token.txt', 'r') as f:
    bot.run(f.read().strip())

