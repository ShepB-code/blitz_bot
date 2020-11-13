import discord
import itertools
from discord.ext import commands
import discord.utils
from discord.utils import get
import asyncio
import json
from blitzAPI import Blitz_API

import requests
from gif import GIF_API
BLITZ_WEAPONS_URL = "https://blitz.gg/valorant/weapons/"

class ValGameStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.blitz = Blitz_API()
        self.gif = GIF_API()

    def get_dict(self, data_type, data, key):

        if data_type == "weapon":
            for category in data.keys():
                for weapon in data[category]:
                    if weapon["key"] == key:
                        return weapon
        elif data_type == "agent":
            for agent in data["list"]:
                if agent["key"] == key:
                    return agent
        return None
    def create_embed(self, embed_type, data):
        blitz_logo = "https://cdn.discordapp.com/icons/352224176645341184/71dab2675787e63a547d6e8b3b36c768.webp?size=256"
        embed = discord.Embed(title="", description="",
                color=0xe7103d
            )

        if embed_type == "weapon":
            primary_kind = data["primary"]["kind"]
            primary_rate = data["primary"]["rate"]
            shooting_test_url = BLITZ_WEAPONS_URL + data["key"] 


            embed.title = data["name"]
            embed.description = f'The **{data["name"]}** is a(n) {data["type"]}\n[Shooting Test]({shooting_test_url})'
            
            embed.add_field(name="Cost", value=f"${data['cost']}", inline=False)
            for item in data['damage']:
                embed.add_field(name=f"Range: {item['range']}", value=f"Head: {item['head']}\nBody: {item['body']}\nLeg: {item['leg']}", inline=True)
            embed.add_field(name="Bullet Penetration", value=data["penetration"], inline=False)
            embed.add_field(name="Weapon Info", value=f"Fire type: {primary_kind}\nRate of fire: {primary_rate}", inline=True)
            
            embed.set_thumbnail(url=data['images']['model'])
        

        elif embed_type == "agent":
            embed.title = f"{str(data['name'])} ({str(data['Class'])})"
            embed.description=f"{data['name']} is a {data['Class']} agent"

            for item in data["abilities"]:
                if item["type"] == "Ultimate":
                    embed.add_field(name=f'{item["type"]}: {item["name"]}', value=f'Cost: {item["cost"]} Ability Points\nKeybind: {item["keybind"]}\nUses: {item["chargesCount"]}', inline=False)
                else:
                    embed.add_field(name=f'{item["type"]}: {item["name"]}', value=f'Cost: ${item["cost"]}\nKeybind: {item["keybind"]}\nUses: {item["chargesCount"]}', inline=False)


            embed.set_thumbnail(url=data['images']['headshot'])
            
        embed.set_footer(text="Made by Shep and Peter - Powered by blitz.gg", icon_url=blitz_logo)
        return embed

    @commands.command()
    async def weapon(self, ctx, weapon_name:str):
        
        get_weapons = self.blitz.get_val_weapons()
        weapon_dict = self.get_dict("weapon", get_weapons, weapon_name.lower())
                
        if weapon_dict:
            await ctx.send(embed=self.create_embed("weapon", weapon_dict))
        else:
            await ctx.send("Weapon not found!")
    
    @commands.command()
    async def agent(self, ctx, agent_name:str):

        get_agents = self.blitz.get_val_agents()

        agent_dict = self.get_dict("agent", get_agents, agent_name.lower())

        if agent_dict:
            await ctx.send(embed=self.create_embed("agent", agent_dict))
        else:
            await ctx.send("Agent not found!")


        

