import discord
import asyncio
from discord.ext import commands
import csv

teams = ["Cardinals", "49ers", "Jets", "Raiders", "Buccaneers", "Giants", "Jaguars", "Lions", "Bills", "Broncos", "Bengals", "Packers", "Dolphins", "Falcons", "Redskins", "Panthers", "Browns", "Vikings", "Titans", "Steelers", "Seahawks", "Ravens", "Texans", "Bears", "Eagles", "Colts", "Cowboys", "Chargers", "Chiefs", "Saints", "Rams", "Patriots"]

teampicksbefore = ["Cardinals", "49ers", "Jets", "Raiders", "Buccaneers", "Giants", "Jaguars", "Lions", "Bills", "Broncos",
         "Bengals", "Packers", "Dolphins", "Falcons", "Redskins", "Panthers", "Giants", "Vikings", "Titans",
         "Steelers", "Seahawks", "Ravens", "Texans", "Raiders", "Eagles", "Colts", "Raiders", "Chargers", "Chiefs",
         "Packers", "Rams", "Patriots", "Cardinals", "Colts", "Raiders", "49ers", "Giants", "Jaguars", "Buccaneers",
         "Bills", "Broncos", "Bengals", "Lions", "Packers", "Falcons", "Redskins", "Panthers", "Dolphins", "Browns",
         "Vikings", "Titans", "Steelers", "Eagles", "Texans", "Texans", "Patriots", "Eagles", "Cowboys", "Colts",
         "Chargers", "Chiefs", "Saints", "Chiefs", "Patriots", "Cardinals", "Steelers", "49ers", "Jets", "Jaguars",
         "Buccaneers", "Broncos", "Bengals", "Patriots", "Bills", "Packers", "Redskins", "Panthers", "Dolphins",
         "Falcons", "Browns", "Vikings", "Titans", "Steelers", "Seahawks", "Ravens", "Texans", "Bears", "Lions",
         "Colts", "Cowboys", "Chargers", "Chiefs", "Jets", "Rams", "Giants", "Redskins", "Patriots", "Jaguars",
         "Rams", "Panthers", "Patriots", "Ravens", "Cardinals", "49ers", "Jets", "Raiders", "Buccaneers", "Giants",
         "Jaguars", "Bengals", "Lions", "Bills", "Ravens", "Packers", "Panthers", "Dolphins", "Falcons", "Packers",
         "Browns", "Vikings", "Titans", "Steelers", "Ravens", "Seahawks", "Broncos", "Bears", "Eagles", "Cowboys",
         "Colts", "Chargers", "Bills", "Giants", "Rams", "Patriots", "Colts", "Cowboys", "Falcons", "Eagles",
         "Cardinals", "Jets", "Steelers", "Giants", "Giants", "Browns", "Buccaneers", "Lions", "Bills", "Broncos",
         "Bengals", "Packers", "Dolphins", "Falcons", "Redskins", "Panthers", "Browns", "Broncos", "Titans",
         "Bills", "Seahawks", "Ravens", "Texans", "Bears", "Eagles", "Colts", "Cowboys", "Chargers", "Chiefs",
         "Saints", "Rams", "Browns", "Giants", "Falcons", "Redskins", "Cardinals", "Steelers", "49ers", "Saints",
         "Jaguars", "Cardinals", "Giants", "Bills", "Broncos", "Bengals", "Lions", "Packers", "Falcons", "Panthers",
         "Titans", "Browns", "Vikings", "Ravens", "Steelers", "Ravens", "Packers", "Texans", "Raiders", "Eagles",
         "Bengals", "Colts", "Chargers", "Chiefs", "Saints", "Rams", "Lions", "Patriots", "Redskins", "Cardinals",
         "Eagles", "Vikings", "Bengals", "Bengals", "49ers", "Bengals", "Chiefs", "Buccaneers", "Chiefs", "Jets",
         "Raiders", "Steelers", "Texans", "Browns", "Bears", "Bengals", "Lions", "Bills", "Packers", "Redskins",
         "Bills", "Lions", "Falcons", "Saints", "Giants", "Dolphins", "Dolphins", "Raiders", "Jaguars", "Broncos",
         "Bears", "Patriots", "Colts", "Cowboys", "Chargers", "Patriots", "Saints", "Giants", "Patriots", "Vikings",
         "Cardinals", "Cardinals", "Vikings", "Rams", "Patriots", "Redskins", "Cardinals"]

perround = [32, 32, 38, 36, 35, 41, 40]
players = []
teampicks = []
tradeoffers = []
GMs = []
peoplewhocandraft = []
signin = False
start = False
pause = False

class Player:
    def __init__(self, name, position, school):
        self.name = name
        self.position = position
        self.school = school
        self.draftnum = -1


class GM:
    def __init__(self, team, gmid):
        self.team = team
        self.gmID = gmid


class Trade:
    def __init__(self, sendteam, recvteam):
        self.sendteam = sendteam
        self.recvteam = recvteam


with open('PlayerBank.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        players.append(Player(row[0], row[1], row[2]))
        #print(row[0])

positions = [o.position for o in players]
positions = list(dict.fromkeys(positions))
client = commands.Bot(command_prefix='$')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    global start
    start = False

# @client.event
# async def on_message(message):
#     global start
#     if start and message.channel.name == "mock-draft-room":
#         for players ==
#     await client.process_commands(message)


@client.command(brief="Shows which GM spots are still open")
async def gmspotsopen(ctx):
    await ctx.send("Teams that don't have a gm are" + str(list(set(teams) - set(o.team for o in GMs))))


@client.command(brief="Can check whos the gm of a certain Team")
async def gmcheck(ctx, team: str):
    if team not in teams:
        await ctx.send('Not Valid Team Name')
        return
    if team in [o.team for o in GMs]:
        x = [o.team for o in GMs].index(team)
        guild = ctx.author.guild
        await ctx.send('The GM of the ' + GMs[x].team + " is " + guild.get_member(GMs[x].gmID).mention)
    else:
        await ctx.send('No one is GMing the ' + team)


@client.command(brief="MODONLY!     Opens GM Signups")
async def opensignups(ctx):
    if "MODS" not in [o.name for o in ctx.author.roles]:
        await ctx.send('You do not have permissions for that')
    else:
        await ctx.send('SignUps are Open')
        GMs.clear()
        global signin
        signin = True


@client.command(brief="Signin To GM a team, $gmsignin TeamName")
async def gmsignin(ctx, team: str):
    if signin:
        if ctx.author.id in [o.gmID for o in GMs] and "MODS" not in [o.name for o in ctx.author.roles]:
            await ctx.send('You have already signed up for a team. If you are GMing more than one team talk to the commish')
        elif team not in teams:
            await ctx.send('Not Valid Team Name')
        elif team in [o.team for o in GMs]:
            x = [o.team for o in GMs].index(team)
            guild = ctx.author.guild
            await ctx.send(guild.get_member(GMs[x].gmID).name + ' is already GMing the ' + team)
        else:
            GMs.append(GM(team, ctx.author.id))
            await ctx.send(ctx.author.name + ' is now GMing the ' + team)
    else:
        await ctx.send('Gm Signin has not started')


@client.command(brief="Resign from GMing your team.")
async def gmresign(ctx):
    if ctx.author.id in [o.gmID for o in GMs]:
        x = [o.gmID for o in GMs].index(ctx.author.id)
        await ctx.send('You have resigned from being the ' + GMs[x].team + " GM")
        GMs.pop(x)
    else:
        await ctx.send('Cannot resign if you are not a GM')


@client.command(brief="MODONLY! Assign a GM to team, $gmassign TeamName <@bot>")
async def gmassign(ctx, team: str, castro: discord.Member):
    if "MODS" not in [o.name for o in ctx.author.roles]:
        await ctx.send('You do not have permissions for that')
    elif team not in teams:
        await ctx.send('Not Valid Team Name')
    elif team in [o.team for o in GMs]:
        x = [o.team for o in GMs].index(team)
        GMs[x].gmID = castro.id
        await ctx.send('The GM of the ' + team + " is " + castro.mention)
    else:
        GMs.append(GM(team, castro.id))
        await ctx.send(castro.mention + ' is now GMing the ' + team)


@client.command(brief="Pick a player, $pick FirstName LastName")
async def pick(ctx, first: str, last: str):
    if not start:
        await ctx.send('Draft has not started')
    # elif "MODS" not in [o.name for o in ctx.author.roles]:
    #     await ctx.send('You do not have permissions for that')
    # elif team not in teams:
    #     await ctx.send('Not Valid Team Name')
    # elif team in [o.team for o in GMs]:
    #     x = [o.team for o in GMs].index(team)
    #     GMs[x].gmID = castro.id
    #     await ctx.send('The GM of the ' + team + " is " + castro.mention)
    # else:
    #     GMs.append(GM(team, castro.id))
    #     await ctx.send(castro.name + 'is now GMing the ' + team)


def is_correct(message):
    if message.content.startswith('$pick'):
        args = message.content.split(" ")
        freshlist = []
        if len(args) < 3:
            task = asyncio.ensure_future(message.channel.send(message.author.name + ', Use $pick FirstName LastName Position(optional/Use Abbrev) School(optional except if theres multiple and put in quotes'))
            return False
        if message.author.id not in [o.gmID for o in GMs]:
            task = asyncio.ensure_future(message.channel.send(message.author.name + ', you aren\'t a GM why are you trying to pick'))
            return False
        #message.guild.text_channels[[o.name for o in message.guild.text_channels].index("pickannouncement")]
        global peoplewhocandraft
        global players
        for j in peoplewhocandraft:
            freshlist.append(teampicks[j])
        for b in freshlist:
            try:
                x = [o.team for o in GMs].index(b)
                if GMs[x].gmID == message.author.id:
                    break
            except ValueError:
                pass
        else:
            task = asyncio.ensure_future(message.channel.send(message.author.name + ', wait your turn'))
            return False
        pickname = args[1] + ' ' + args[2]
        pickposition=""
        pickschool=""
        if len(args)==4:
            if args[3] in positions:
                pickposition=args[3]
            else:
                pickschool=args[3]
        elif len(args)==5:
            pickschool=args[4]
            pickposition = args[3]

        explanation = "Did you mean " + pickname + ","
        freakout = True
        z=0
        if pickname in [o.name for o in players]:
            indices = [i for i, y in enumerate([o.name for o in players]) if y == pickname]
            if len(indices) > 1:
                print( "Why kyler is unique?")
                while z < len(indices):
                    explanation += players[indices[z]].position+", from " + players[indices[z]].school + " or the "
                    if pickschool == players[indices[z]].school or players[indices[z]].position == pickposition:
                        if players[indices[z]].draftnum != -1:
                            task = asyncio.ensure_future(message.channel.send(message.author.name + ', that guy was drafted'))
                        else:
                            task = asyncio.ensure_future(message.guild.text_channels[[o.name for o in message.guild.text_channels].index("mock-draft-room")].send("The " + GMs[x].team + " pick is in!"))
                            task = asyncio.ensure_future(message.guild.text_channels[[o.name for o in message.guild.text_channels].index("pickannouncement")].send(str(peoplewhocandraft[freshlist.index(GMs[x].team)] + 1) + '.  The ' + GMs[x].team + ' take ' + pickname + ", " + players[indices[z]].position + ', ' + players[indices[z]].school))
                            players[indices[z]].draftnum = peoplewhocandraft[freshlist.index(GMs[x].team)]
                            return True
                    z += 1
                lengthofexplanation = len(explanation)
                explanation = explanation[:-7]
                explanation += ". Only need the position or school. When you submit again"
                asyncio.ensure_future(message.channel.send(message.author.name + ', ' + explanation))
                return False
            if players[indices[0]].draftnum != -1:
                task = asyncio.ensure_future(message.channel.send(message.author.name + ', that guy was drafted'))
                return False
            if pickposition == "":
                pickposition = players[indices[0]].position
            task = asyncio.ensure_future(message.guild.text_channels[[o.name for o in message.guild.text_channels].index("pickannouncement")].send(str(peoplewhocandraft[freshlist.index(GMs[x].team)]+1) + '.  The ' + GMs[x].team + ' take ' + pickname + ", " + pickposition + ', ' + players[indices[0]].school))
            players[z].draftnum = peoplewhocandraft[freshlist.index(GMs[x].team)]
            peoplewhocandraft.pop(freshlist.index(GMs[x].team))

            return True
        else:
            task = asyncio.ensure_future(message.channel.send(message.author.name + ', Double check your spelling, cause that is not a player'))
            return False


@client.command(brief="MODONLY! Starts Draft, $start RoundAmount ")
async def start(ctx, roundnum: int = 2):
    global start
    start = True
    if "MODS" not in [o.name for o in ctx.author.roles]:
        await ctx.send('You do not have permissions for that')
        return
    if len(GMs)!= 32:
        await ctx.send('We are ' + str(32-len(GMs)) + ' GMs short from everyone having a GM')
    global teampicks
    teampicks= teampicksbefore
    startup = 0
    val = 0
    timelimit = 35
    storage = ""
    global peoplewhocandraft
    global pause
    pause = False
    while start:
        for x, end in enumerate(perround):
            if x == roundnum:
                break
            val += end
            for y in range(startup, val):
                if teampicks[y] in [o.name for o in ctx.guild.roles]:
                    await ctx.send(ctx.guild.roles[[o.name for o in ctx.guild.roles].index(teampicks[y])].mention + ' are on the clock')
                else:
                    await ctx.send(teampicks[y] + ' are on the clock ')
                timer = 0
                peoplewhocandraft.append(y)
                storage = teampicks[y]
                #print(peoplewhocandraft[0])
                while timer < timelimit and start:
                    while pause:
                        await asyncio.sleep(1)
                    if storage != teampicks[y]:
                        storage = teampicks[y]
                        if teampicks[y] in [o.name for o in ctx.guild.roles]:
                            await ctx.send(ctx.guild.roles[[o.name for o in ctx.guild.roles].index(teampicks[y])].mention + ' are now on the clock and have ' + str(timelimit - timer) + ' seconds left ')
                        else:
                            await ctx.send(teampicks[y] + ' are now on the clock and have ' + str(timelimit - timer) + ' seconds left ')
                    try:
                        switch = True
                        if timer % 30 == 0:
                            await ctx.send(teampicks[y] + ' have ' + str(timelimit-timer) + ' seconds left')
                        await client.wait_for('message', check=is_correct, timeout=1)
                    except asyncio.TimeoutError:
                        switch = False
                        timer += 1
                    if switch and y not in peoplewhocandraft:
                        break
                if not start:
                    break
            if not start:
                break
            await ctx.send("End of Round:" + str(x + 1))
            startup += end


@client.command(brief="MODONLY! Stops Draft")
async def stop(ctx):
    if "MODS" not in [o.name for o in ctx.author.roles]:
        await ctx.send('You do not have permissions for that')
        return
    global start
    start = False
    await ctx.send("The draft has stopped buddy")


@client.command(brief="MODONLY! Pauses Draft")
async def pause(ctx):
    if "MODS" not in [o.name for o in ctx.author.roles]:
        await ctx.send('You do not have permissions for that')
        return
    global pause
    pause = True
    await ctx.send("The draft has paused matey")


@client.command(brief="MODONLY! Unpauses Draft")
async def unpause(ctx):
    if "MODS" not in [o.name for o in ctx.author.roles]:
        await ctx.send('You do not have permissions for that')
        return
    global pause
    pause = False
    await ctx.send("The draft has been unpaused guy")


@client.command(brief="Check picks")
async def checkpicks(ctx, team: str = None):
    if not team:
        for x in [o.name for o in ctx.author.roles]:
            if x in teams:
                team = x
                break
        else:
            if ctx.author.id in [o.gmID for o in GMs]:
                team = GMs[[o.gmID for o in GMs].index(ctx.author.id)].team
            else:
                await ctx.send('I cant tell what team you are. Use $pick teamname')
                return
    global start
    if start is False:
        new_list = [index for index, value in enumerate(teampicks) if value == team]
    else:
        new_list = [index for index, value in enumerate(teampicksbefore) if value == team]
    new_list = [x + 1 for x in new_list]
    await ctx.send(team + ": " + str(new_list))


@client.command(brief="Check positions")
async def checkpositions(ctx):
    await ctx.send(positions)


def is_correct2(message):
    if message.content.startswith('$trade accept'):
        args = message.content.split(" ")
        if len(args) < 3:
            task = asyncio.ensure_future(message.channel.send(message.author.name + ', Use $trade accept TeamName'))
            #task = asyncio.ensure_future(message.channel.send(message.author.name + ', Use $trade TeamName GivingUp(Split by , and quotes for stuff like "2020 1st","Teddy BridgeWater") GettingBack(Split the same as before)'))
            #task = asyncio.ensure_future(message.channel.send(message.author.name + ', Use $trade TeamName GivingUp(Split by , and quotes for stuff like "2020 1st","Teddy BridgeWater") GettingBack(Split the same as before)'))
            return False
        if message.author.id not in [o.gmID for o in GMs]:
            task = asyncio.ensure_future(message.channel.send(message.author.name + ', you aren\'t a GM why are you trying to accept a trade'))
            return False
        x = 0
        team = args[2]
        indices = [i for i, x in enumerate([o.gmID for o in GMs]) if x == message.author.id]
        #print(indices)
        x = 0
        z = 0
        while x < len(tradeoffers):
            while z < len(indices):
                if team == tradeoffers[x].sendteam and GMs[indices[z]].team == tradeoffers[x].recvteam:
                    return True
                z += 1
            x += 1
            z = 0
        task = asyncio.ensure_future(message.channel.send(message.author.name + ', no valid offers from that team'))
        return False


@client.command(brief='Trade assets, $trade opposingteam GivingUp(Split by , and surrounded by quotes for stuff like "2020 1st,Teddy BridgeWater,1,33") GettingBack(Split the same as before) ')
async def trade(ctx, team: str = None, offer: str = None, recv: str = None, sendingteam: str = None):
    if team == "accept":
        return
    if not recv:
        await ctx.send('$trade opposingteam GivingUp(Split by , and surrounded by quotes for stuff like "2020 1st,Teddy BridgeWater,1,33") GettingBack(Split the same as before)')
        return
    offerargs = offer.split(",")
    recvargs = recv.split(",")
    offerpicks = []
    recvpicks = []
    x = 0
    global teampicks
    #await ctx.send(start)
    if start is False:
        await ctx.send("Can't officially trade until draft starts")
        return
    if ctx.author.id not in [o.gmID for o in GMs]:
        await ctx.send(ctx.author.name + ', you aren\'t a GM why are you trying to trade')
        return
    if team not in teams:
        await ctx.send(ctx.author.name + ', you are trading with an invalid team name')
        return
    if team not in [o.team for o in GMs]:
        await ctx.send(ctx.author.name + ', that team does not have a GM')
        return
    opposingGM = GMs[[o.team for o in GMs].index(team)].gmID
    if ctx.author.id == opposingGM:
        await ctx.send(ctx.author.name + ', you can\'t trade with yourself')
        return
    while x < len(offerargs):
        if len(offerargs[x]) < 4 and offerargs[x][0].isdigit():
            if int(offerargs[x]) < 255:
                offerpicks.append(int(offerargs[x]))
        x += 1
    x = 0
    while x < len(recvargs):
        if len(recvargs[x]) < 4 and recvargs[x][0].isdigit():
            if int(recvargs[x]) < 255:
                recvpicks.append(int(recvargs[x]))
        x += 1
    x = 0
    if len(offerpicks) < 1:
        if [o.gmID for o in GMs].count(ctx.author.id) > 1:
            if not sendingteam:
                await ctx.send("Don't know what team you are. If you aren't sending a pick in this draft. Use $trade ReceivingTeam SendingOffer ReceivingOffer YourTeam")
                return
        else:
            sendingteam = GMs[[o.gmID for o in GMs].index(ctx.author.id)].team
    while x < len(offerpicks):
        if not sendingteam:
            sendingteam = teampicks[offerpicks[x]-1]
        elif sendingteam != teampicks[offerpicks[x]-1]:
            await ctx.send("Trading picks from different teams :thinking:")
            return
        if offerpicks[x]-1 in [o.draftnum for o in players]:
            await ctx.send("Trading picks that you already used to draft. Pulling a fast one eh? :thinking:")
            return
        x += 1
    sendingGM = GMs[[o.team for o in GMs].index(sendingteam)].gmID
    global tradeoffers
    x = 0
    while x < len(tradeoffers):
        if sendingteam == tradeoffers[x].sendteam and team == tradeoffers[x].recvteam:
            await ctx.send("Can't send another trade to the same team with one pending")
            return
        x += 1
    if sendingGM != ctx.author.id:
        await ctx.send("Trading picks from different teams :thinking:")
        return
    x = 0
    while x < len(recvpicks):
        if team != teampicks[recvpicks[x]-1]:
            await ctx.send("The team you are trying to trade with doesnt have those picks :thinking:")
            return
        if recvpicks[x]-1 in [o.draftnum for o in players]:
            await ctx.send("Don't scam yourself they already drafted with that pick :thinking:")
            return
        x += 1

    guild = ctx.author.guild
    try:
        tradeoffers.append(Trade(sendingteam, team))
        await ctx.send(guild.get_member(opposingGM).mention + ", Trade attempt here. The " + sendingteam + " want to trade you " + offer + " for " + recv)
        await client.wait_for('message', check=is_correct2, timeout=60)
    except asyncio.TimeoutError:
        tradeoffers = [item for item in tradeoffers if item.sendteam != sendingteam and item.recvteam != team]
        await ctx.send("Trade attempt timed out, " + ctx.author.mention)
        return
    x = 0
    tradeoffers = [item for item in tradeoffers if item.sendteam != sendingteam and item.recvteam != team]
    while x < len(recvpicks):
        if team != teampicks[recvpicks[x] - 1]:
            await ctx.send("The team you are trying to trade with doesnt have those picks anymore :thinking:")
            return
        if recvpicks[x]-1 in [o.draftnum for o in players]:
            await ctx.send("Don't scam yourself they already drafted with that pick :thinking:")
            return
        x += 1
    x = 0
    while x < len(offerpicks):
        if not sendingteam:
            sendingteam = teampicks[offerpicks[x]-1]
        elif sendingteam != teampicks[offerpicks[x]-1]:
            await ctx.send("Trading picks from different teams :thinking:")
            return
        if offerpicks[x]-1 in [o.draftnum for o in players]:
            await ctx.send("Trading picks that you already used to draft. Pulling a fast one eh? :thinking:")
            return
        x += 1
    x = 0
    while x < len(recvpicks):
        teampicks[recvpicks[x]-1] = sendingteam
        x += 1
    x = 0
    while x < len(offerpicks):
        teampicks[offerpicks[x] - 1] = team
        x += 1
    await ctx.guild.text_channels[[o.name for o in ctx.guild.text_channels].index("mock-draft-room")].send("Trade Alert!!!")
    await ctx.guild.text_channels[[o.name for o in ctx.guild.text_channels].index("tradeannouncement")].send("Trade Alert: The "+sendingteam + " sends " + offer + " to the " + team + " for " + recv)

client.run('token')
