# Main:
# Where all Discord events are handled

# IMPORTS
import discord
from discord.ext import commands
import BOT_module
import VG_module

# BOT Variables--
keyBOT = ""  # DISCORD_BOT_TOKEN_HERE
extensionsForBOT = ["BOT_module", "VG_module"]  # MODULES that EXTEND the BOTS COMMANDS ~ !!!ADD YOUR MODULE TO THIS LIST IF YOU WANT TO EXTEND COMMANDS!!!
descriptionBOT = "Computer is a bot created for Discord to utilize the VG api!"  # DESCRIPTION of the BOT
bot = commands.Bot(command_prefix=">", description=descriptionBOT)  # CREATE the BOT


# Whenever BOT is READY
@bot.event
async def on_ready():
    print('Logged In As: ' + bot.user.name + "  ID:  " + bot.user.id + "\n\n")

# ADDS all the COMMANDS from other MODULES
if __name__ == "__main__":
    for extension in extensionsForBOT:
        try:
            bot.load_extension(extension)
        except Exception:
            print("Failed to load extension:   " + extension)

# RUNS BOT with Discord KEY
bot.run(keyBOT)
