# VG Module:
# Functions using the VG API. Functions using Discord libraries will be marked by, "!!!DISCORD!!!", in their description.

# IMPORTS
import gamelocker
import datetime
import discord
from discord.ext import commands
import TOOL_module as tools

# VG Variables--
keyVG = ""  # VG_API_TOKEN_HERE
apiVG = gamelocker.Gamelocker(keyVG).Vainglory()  # API OBJECT


# Will CHECK if NAME is VALID. Will RETURNS True or False if TYPE = 0, if TYPE = 1 returns ID or False.
def getIDVG(name, type=0):
    name = str(name)  # Convert NAME to STRING to prevent errors

    # ADD when FETCHING from VG API!!! example: {"filter[createdAt-start]": daterange, "filter[createdAt-end]": datenow, etc...}
    datenow = datetime.datetime.today()
    daterange = str(datenow - datetime.timedelta(days=7)) + "T00:00:00Z"  # Get the DATE RANGE to SEARCH from
    datenow = str(datetime.datetime.today()) + "T00:00:00Z"  # CURRENT DATE

    try:
        matches = apiVG.matches({"filter[createdAt-start]": "2017-02-16T12:00:00Z", "page[limit]": 2, "filter[playerNames]": name})
        for r in matches[0].rosters:
            for p in r.participants:
                if p.player.name == name:
                    if type == 0:  # Returns TRUE when name is FOUND
                        return True
                    elif type == 1:  # Returns ID when name is FOUND
                        return p.player.id

    except:  # Returns FALSE whenever an ERROR occurs
        return False

# Will get VG GAME MATCHES according to NAME.
def getGameMatchesVG(name):
    name = str(name)  # Converts NAME to STRING to prevent errors

    # ADD when FETCHING from VG API!!! example: {"filter[createdAt-start]": daterange, "filter[createdAt-end]": datenow, etc...}
    datenow = datetime.datetime.today()
    daterange = str(datenow - datetime.timedelta(days=7)) + "T00:00:00Z"  # Get the DATE RANGE to SEARCH from
    datenow = str(datetime.datetime.today()) + "T00:00:00Z"  # CURRENT DATE

    try:  # Tries to FIND PLAYER matches in NA servers
        mathes = apiVG.matches({"filter[createdAt-start]": daterange, "page[limit]" : 50, "sort" : "createAt", "filter[playerNames]" : name})
    except:
        try:  # Tries to FIND PLAYER matches in EU servers
            matches = apiVG.matches({"filter[createdAt-start]": daterange, "page[limit]" : 50, "sort" : "createAt", "filter[playerNames]" : name})
        except:
            print("!!!SOMETHING WENT HORRIBLY WRONG WHILE TRYING TO FETCH VG MATCHES FOR " + name + "!!!")

# GETS a PLAYERS LIFE time INFORMATION with ID. ID = ID or NAME for player, givenname = If True then ID is actually a NAME, server = Server to work with
def getPlayerInfoVG(ID, givenname=False, server="na"):
    ID = str(ID)  # Convert ID to a STRING to prevent errors

    if givenname == True:  # Checks to see if ID is actually a NAME if so then TURN it into a ID
        ID = str(getIDVG(ID, type=1))

    info = apiVG.player(ID)
    return info

# Get a PLAYERS performance from RANGE of DAYS with the players NAME
def getPlayerPerformanceVG(name, days=7, type=0,region="na"):
    name = str(name)  # Convert NAME to STRING to prevent errors
    days = int(days)  # Convert DAYS to INT to prevent errors

    # ADD when FETCHING from VG API!!! example: {"filter[createdAt-start]": daterange, "filter[createdAt-end]": datenow, etc...}
    datenow = datetime.date.today()
    daterange = str(datenow - datetime.timedelta(days=days)) + "T00:00:00Z"  # Get the DATE RANGE to SEARCH from
    datenow = str(datetime.date.today()) + "T00:00:00Z"  # CURRENT DATE

    try:
        matches = apiVG.matches({"filter[createdAt-start]": daterange, "page[limit]": 50, "filter[playerNames]": name},region=region)  # GET MATCHES

    except:
        return "Couldn't get any matches for **" + name + "** from the past " + str(days) + " days!"  # RETURN if player MATCHES AREN'T FOUND

    # Get DATA out of the MATCH OBJECTS
    playerdata = []
    for match in matches:
        for roaster in match.rosters:
            for participant in roaster.participants:
                if participant.player.name == name:
                    playerdata.append(participant.to_dict())  # If DATA belongs to PLAYER then KEEP

    # DATA VARIABLES
    size = int(len(playerdata)) - 1  # Get the SIZE of the PLAYERSDATA

    # PROFILE VARIABLES ~ most of this will be USED for MEAN and MODE
    actor = []
    assists = []
    crystalMineCaptures = []
    deaths = []
    farm = []
    goldMineCaptures = []
    itemslist = []
    karmaLevel = []
    kills = []
    krakenCaptures = []
    level = 0
    minionKills = []
    skillTier = []
    skinKey = []
    turretCaptures = []
    wentAfk = []
    winner = []

    num = 0
    # Go though PLAYERDATA getting DATA needed and building a PROFILE
    for data in playerdata:
        attributes = data["attributes"]
        stats = attributes["stats"]
        items = stats["items"]

        actor.append(attributes["actor"])
        assists.append(stats["assists"])
        crystalMineCaptures.append(stats["crystalMineCaptures"])
        deaths.append(stats["deaths"])
        farm.append(stats["farm"])
        goldMineCaptures.append(stats["goldMineCaptures"])
        # itemslist.append(stats["items"])

        for item in stats["items"]:
            itemslist.append(item)

        karmaLevel.append(stats["karmaLevel"])
        kills.append(stats["kills"])
        krakenCaptures.append(stats["krakenCaptures"])
        minionKills.append(stats["minionKills"])
        skillTier.append(stats["skillTier"])
        skinKey.append(stats["skinKey"])
        turretCaptures.append(stats["turretCaptures"])
        wentAfk.append(stats["wentAfk"])
        winner.append(stats["winner"])

        if num == size:
            level = stats["level"]
        num += 1

    print(itemslist)

    msg = "```"

    # Adding the TOP ACTORS used in the past X days to MSG
    actors = tools.giveListInOrderTOOL(actor)
    num = 0
    while num < 5:
        num += 1
        msg += "**" + str(num) + "** ~ *" + str(giveHeroNameVG(actors[num])) + "*\n"

    # Adding KILLS MEAN from the past X days to MSG
    msg += "\n**Kills per Game:** *" + str(tools.giveMeanOfList(kills)) + "*"

    # Adding ASSISTS MEAN from the past X days to MSG
    msg += "\n**Assists per Game:** *" + str(tools.giveMeanOfList(assists)) + "*"

    # Adding DEATHS MEAN from the past X days to MSG
    msg += "\n**Deaths per Game:** *" + str(tools.giveMeanOfList(deaths)) + "*"

    # Adding FARM MEAN from the past X days to MSG
    msg += "\n**Farm per Game:** *" + str(tools.giveMeanOfList(farm)) + "*"

    # # Adding  MEAN from the past X days to MSG
    # msg += "\n**:** *" + str(tools.giveMeanOfList()) + "*"
    #
    # # Adding  MEAN from the past X days to MSG
    # msg += "\n**:** *" + str(tools.giveMeanOfList()) + "*"
    #
    # # Adding  MEAN from the past X days to MSG
    # msg += "\n**:** *" + str(tools.giveMeanOfList()) + "*"
    #
    # # Adding  MEAN from the past X days to MSG
    # msg += "\n**:** *" + str(tools.giveMeanOfList()) + "*"
    #
    # # Adding  MEAN from the past X days to MSG
    # msg += "\n**:** *" + str(tools.giveMeanOfList()) + "*"
    #
    # # Adding  MEAN from the past X days to MSG
    # msg += "\n**:** *" + str(tools.giveMeanOfList()) + "*"
    #
    # # Adding  MEAN from the past X days to MSG
    # msg += "\n**:** *" + str(tools.giveMeanOfList()) + "*"
    #
    # # Adding  MEAN from the past X days to MSG
    # msg += "\n**:** *" + str(tools.giveMeanOfList()) + "*"

    msg += "\n```"
    return msg

# Given ACTOR ID give HERO title
def giveHeroNameVG(ID):
    ID = str(ID)  # ID to STRING to PREVENT ERRORS

    if ID == "*Adagio*":
        return "Adagio"

    elif ID == "*Alpha*":
        return "Alpha"

    elif ID == "*Ardan*":
        return "Ardan"

    elif ID == "*Baron*":
        return "Baron"

    elif ID == "*Blackfeather*":
        return "Blackfeather"

    elif ID == "*Catherine":
        return "Catherine"

    elif ID == "*Celeste*":
        return "Celeste"

    elif ID == "*Flicker*":
        return "Flicker"

    elif ID == "*Fortress*":
        return "Fortress"

    elif ID == "*Glaive*":
        return "Glaive"

    elif ID == "*Gwen*":
        return "Gwen"

    elif ID == "*Idris*":
        return "Idris"

    elif ID == "*Joule*":
        return "Joule"

    elif ID == "*Kestrel*":
        return "Kestrel"

    elif ID == "*Koshka*":
        return "Koshka"

    elif ID == "*Hero009*":
        return "Krul"

    elif ID == "*Lance*":
        return "Lance"

    elif ID == "*Lyra*":
        return "Lyra"

    elif ID == "*Ozo*":
        return "Ozo"

    elif ID == "*Petal*":
        return "Petal"

    elif ID == "*Phinn*":
        return "Phinn"

    elif ID == "*Reim*":
        return "Reim"

    elif ID == "*Ringo*":
        return "Ringo"

    elif ID == "*Hero016*":
        return "Rona"

    elif ID == "*Samuel*":
        return "Samuel"

    elif ID == "*SAW*":
        return "SAW"

    elif ID == "*Hero010*":
        return "Skaarf"

    elif ID == "*Skye*":
        return "Skye"

    elif ID == "*Sayoc*":
        return "Taka"

    elif ID == "*Vox*":
        return "Vox"

    else:
        return "Unknown Hero"


# CLASS containing ALL COMMANDS for THIS MODULE
class Vg():
    """All the commands in relation to Vainglory.

            Made with love and some Vainglory api, python - gamelocker.

    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vgperformance(self, player_name="",region="na" ,days=7):
        """Gets a players performance in the past days.

                >vgperformance (player_name) (days)
            player_name   ~   name of player to search for
            days          ~   day range to search from
            region        ~   region of the player

        """

        if player_name == "":  # MESSAGE the USER if NO NAME was GIVEN
            await self.bot.say("You need to give a players name at least...")
            return

        if len(str(player_name)) < 3:  # MESSAGE the USER if NAME GIVEN is TOO SHORT
            await self.bot.say("That isn't a valid name... :sweat_smile:")
            return

        if tools.isIntTOOL(player_name) == True:  # MESSAGE the USER if a NUMBER was GIVEN
            await self.bot.say(str(player_name) + " isn't a valid name... :sweat_smile:")
            return

        notice = "Looking for match results for " + str(player_name) + " from the past " + str(days) + " days... :eyes:"

        if tools.isIntTOOL(days) == True and days != "":  # CHECK DAYS to be a VALID NUMBER
            days = int(days)

            if days > 93:
                notice += "\nDates down from " + str(days) + " to 93 days!"  # ADD to NOTICE that DATE was CHANGED
                days = 93  # MAKE DAYS a VALID RANGE

            elif days <= 0:
                notice += "\nDates up from " + str(days) + " to 1 day!"  # ADD to NOTICE that DATE was CHANGED
                days = 1  # MAKE DAYS a VALID RANGE

        if tools.isIntTOOL(days) == False and days != "":
            await self.bot.say("Sorry but " + str(days) + " isn't a valid number... :sweat_smile:")  # If DAYS is an INVALID number TELL USER
            return

        msg = await self.bot.say(notice)  # NOTICE USER that THEIR COMMAND is being PROCESSED
        await self.bot.edit_message(msg, str(getPlayerPerformanceVG(player_name, days,region = region)))  # RUNS PERFORMANCE FETCH and UPDATES MESSAGE once DONE

    @commands.command()
    async def vgcheckplayer(self, player_name=""):
        """Checks if player exist in vainglory.

                >vgcheckplayer (player_name)
            player_name   ~   name of player to check for

        """

        if player_name == "":
            await self.bot.say("You need to give a players name... :sweat_smile:")
            return

        elif tools.isIntTOOL(player_name) == False:
            player_name = str(player_name)  # Convert PLAYER_NAME to STRING to prevent errors

            notice = "Looking for " + player_name + "... :eyes:"  # DEFAULT NOTICE SENT to USER!

            msg = await self.bot.say(notice)  # NOTICE USER that THEIR COMMAND is being PROCESSED
            await self.bot.edit_message(msg, str(getIDVG(player_name)))  # RUNS ID TEST

        else:
            await self.bot.say("Sorry but " + str(player_name) + " isn't a valid name... :sweat_smile:")
            return


def setup(bot):
    bot.add_cog(Vg(bot))
