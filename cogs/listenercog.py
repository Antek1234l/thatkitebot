import discord
from discord.enums import Status
from discord.ext.commands.errors import CommandInvokeError
from bf.util import  errormsg
from discord.ext import commands,tasks
import asyncio
from datetime import datetime,timedelta
import random
from bf.util import colors
class listeners(commands.Cog):
    def __init__(self, bot, dirname,):
        self.dirname=dirname
        self.bot:discord.Client=bot
        self.colors=colors()

    @commands.Cog.listener()
    async def on_command_error(self,ctx:commands.Context,error:CommandInvokeError):
        if isinstance(error,commands.CommandNotFound):
            await errormsg(ctx,f"unknown command | do `{ctx.prefix}help` in order to see what i can do")
        elif isinstance(error,commands.CommandOnCooldown):
            await errormsg(ctx,"Sorry, but this command is on cooldown! Try again in a few seconds.")
        elif isinstance(error,CommandInvokeError) and self.bot.debugmode:
            await errormsg(ctx,str(error))
            await errormsg(ctx,str(error.original))
            raise error
        else:
            raise error

    @tasks.loop(minutes=20.0)
    async def statuschange(self):
        ontime:timedelta=datetime.now() - self.bot.starttime
        times=str(ontime).split(".")

        possible_status=[
            (Status.idle,"nothing"),
            (Status.online,"with code"),
            (Status.online,f"{self.bot.command_prefix}help"),
            (Status.online,f"uptime:    {times[0]}"),
            (Status.dnd,"with trains"),
            (Status.online,"with myself"),
            (Status.online,"games")
            ]
        
        chosen_status,chosen_message=random.choice(possible_status)
        await self.bot.change_presence(status=chosen_status,activity=discord.Game(chosen_message))
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"\nbot successfully started!")  
        await self.bot.change_presence(status=discord.Status.dnd,activity=discord.Game("booting"))
        self.statuschange.start()