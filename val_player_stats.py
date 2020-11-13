import discord
import itertools
from discord.ext import commands
import discord.utils
from discord.utils import get
import asyncio
import json
from blitzAPI import Blitz_API


class ValGameStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.blitz = Blitz_API()

    def create_embed(self, embed_type, data):
        blitz_logo = "https://cdn.discordapp.com/icons/352224176645341184/71dab2675787e63a547d6e8b3b36c768.webp?size=256"
        embed = discord.Embed(title="", description="",
                color=0xe7103d
            )
        embed.title = data["name"]

        all_stats = data["stats"]["all"]["overall"]
        blitz_url = f"https://blitz.gg/valorant/profile/{data['name']}-{data['tag']}"
        
        if embed_type == "player_home":
            player_career = all_stats["career"]
            embed.description = f"Career Stats for **{data['name']}**\n[More Info]({blitz_url})"

            embed.add_field(name="Career Match Stats", value=f'Total Wins: {player_career["wins"]}\nTotal Matches Played: {player_career["matches"]}', inline=True)
            embed.add_field(name="Career Match Impact", value=f'Total Kills: {player_career["kills"]}\nTotal Asists: {player_career["assists"]}\nTotal Bomb Plants: {player_career["plants"]}\nTotal Bomb Defuses: {player_career["defuses"]}', inline=True)   
        
        elif embed_type == "player_map_stats":
            map_stats = all_stats["career"]["mapStats"]
             
            embed.description = f"Map Stats for **{data['name']}**\n[More Info]({blitz_url})"
            
            for map_name, stats in map_stats.items():
                embed.add_field(name=map_name.capitalize(), value=f'Total Matches Played: {stats["matches"]}\nTotals Wins: {stats["wins"]}', inline=True)

        elif embed_type == "player_agent_stats":
            pass
        embed.set_footer(text="Made by Shep and Peter - Powered by blitz.gg", icon_url=blitz_logo)
        return embed
    @commands.command()
    async def val(self, ctx, player_id:str):

        player = self.blitz.get_val_player(player_id)
        

        if player:
            await ctx.send(embed=self.create_embed("player_home", player))
            await ctx.send(embed=self.create_embed("player_map_stats", player))

        else:
            await ctx.send("That player does not exist.")
