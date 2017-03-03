# Body Module:
# Things that give a bot meaning!

# IMPORTS
# import discord
from discord.ext import commands
import asyncio
import TOOL_module as tools

# CLASS containing ALL COMMANDS for THIS MODULE
class Bot():
    """All the commands in relation to Vainglory.

            Made using the Vainglory api, python - gamelocker.

    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def catch(self, msg):
        """Gives your number of messages in this channel."""

        author = msg.message.author  # Get the AUTHOR of the MESSAGE
        channel = msg.message.channel  # Get the CHANNEL of the MESSAGE
        msgs = 0  # NUMBER of MESSAGES
        msg = await self.bot.send_message(channel, "Calculating messages...")
        async for log in self.bot.logs_from(channel, limit=100):  # LOOKS THROUGH the CHANNELS LOG
                if log.author == author:
                    msgs += 1  # Add 1 to MSGS whenever a MSG is found in CHANNEL belonging to the AUTHOR

        if msgs == 100:  # BOT SAYS that you have over 100 MESSAGES
            await self.bot.edit_message(msg, "You have over 100 messages!")

        else:  # BOT SAYS number of MESSAGES you HAVE
            await self.bot.edit_message(msg, "You have " + str(msgs) + " messages!")

    @commands.command()
    async def sleep(self, seconds="3"):
        """Give the bot a rest.

                >sleep (seconds)
            seconds   ~   number of seconds bot should sleep for

        """

        if tools.isIntTOOL(seconds) == False:
            await self.bot.say(str(seconds) + " isn't a valid number!")

        else:
            seconds = int(seconds)  # CONVERT to INT to PREVENT ERRORS

            if seconds > 3600:
                seconds = 3600
            elif seconds <= 0:
                seconds = 1

            await self.bot.say("Going to sleep for " + str(seconds) + " seconds good night... :sleeping:")
            await asyncio.sleep(seconds)
            await self.bot.say("Done sleeping! :raised_hands:")

def setup(bot):
    bot.add_cog(Bot(bot))
