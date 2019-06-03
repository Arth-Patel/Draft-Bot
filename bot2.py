import discord
import asyncio
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
import time
import pprint

teams = ["Cardinals", "49ers", "Jets", "Raiders", "Buccaneers", "Giants", "Jaguars", "Lions", "Bills", "Broncos", "Bengals", "Packers", "Dolphins", "Falcons", "Redskins", "Panthers", "Browns", "Vikings", "Titans", "Steelers", "Seahawks", "Ravens", "Texans", "Bears", "Eagles", "Colts", "Cowboys", "Chargers", "Chiefs", "Saints", "Rams", "Patriots"]

#teampicks = ["Raiders","49ers","Panthers","Cardinals","Buccaneers","Giants","Jaguars","Lions","Bills","Broncos","Bengals","Packers","Dolphins","Falcons","Redskins","Jets","Giants","Vikings","Titans","Steelers","Seahawks","Ravens","Texans","Raiders","Eagles","Colts","Cardinals","Chargers","Chiefs","Packers","Rams","Patriots","Raiders","Colts","Cardinals","49ers","Giants","Jaguars","Buccaneers","Bills","Broncos","Bengals","Lions","Packers","Falcons","Redskins","Jets","Dolphins","Browns","Vikings","Titans","Steelers","Eagles","Texans","Texans","Patriots","Eagles","Cowboys","Colts","Chargers","Chiefs","Saints","Chiefs","Patriots","Raiders","Steelers","49ers","Jets","Jaguars","Buccaneers","Broncos","Bengals","Patriots","Bills","Packers","Redskins","Panthers","Dolphins","Falcons","Browns","Vikings","Titans","Steelers","Seahawks","Ravens","Texans","Bears","Lions","Colts","Cowboys","Chargers","Chiefs","Jets","Rams","Giants","Redskins","Patriots","Jaguars","Rams","Panthers","Patriots","Ravens","Cardinals","49ers","Jets","Raiders","Buccaneers","Giants","Jaguars","Bengals","Lions","Bills","Ravens","Packers","Jets","Dolphins","Falcons","Packers","Browns","Vikings","Titans","Steelers","Ravens","Seahawks","Broncos","Bears","Eagles","Cowboys","Colts","Chargers","Bills","Giants","Rams","Patriots","Colts","Cowboys","Falcons","Eagles","Cardinals","Raiders","Steelers","Giants","Giants","Browns","Buccaneers","Lions","Bills","Broncos","Bengals","Packers","Dolphins","Falcons","Redskins","Panthers","Browns","Broncos","Titans","Bills","Seahawks","Ravens","Texans","Bears","Eagles","Colts","Cowboys","Chargers","Chiefs","Saints","Rams","Browns","Giants","Falcons","Redskins","Cardinals","Steelers","49ers","Saints","Jaguars","Cardinals","Giants","Bills","Broncos","Bengals","Lions","Packers","Falcons","Panthers","Titans","Browns","Vikings","Ravens","Steelers","Ravens","Packers","Texans","Jets","Eagles","Bengals","Colts","Chargers","Chiefs","Saints","Rams","Lions","Patriots","Redskins","Steelers","Buccaneers","Vikings","Bengals","Bengals","49ers","Bengals","Chiefs","Buccaneers","Chiefs","Jets","Raiders","Steelers","Texans","Browns","Bears","Bengals","Lions","Bills","Packers","Redskins","Bills","Lions","Falcons","Saints","Giants","Dolphins","Dolphins","Raiders","Jaguars","Broncos","Bears","Patriots","Colts","Cowboys","Chargers","Patriots","Saints","Giants","Patriots","Vikings","Cardinals","Cardinals","Vikings","Rams","Patriots","Redskins","Cardinals"]
teampicks = ["Cardinals","49ers","Jets","Raiders","Buccaneers","Giants","Jaguars","Lions","Bills","Broncos","Bengals","Packers","Dolphins","Falcons","Redskins","Panthers","Giants","Vikings","Titans","Steelers","Seahawks","Ravens","Texans","Raiders","Eagles","Colts","Raiders","Chargers","Chiefs","Packers","Rams","Patriots","Cardinals","Colts","Raiders","49ers","Giants","Jaguars","Buccaneers","Bills","Broncos","Bengals","Lions","Packers","Falcons","Redskins","Panthers","Dolphins","Browns","Vikings","Titans","Steelers","Eagles","Texans","Texans","Patriots","Eagles","Cowboys","Colts","Chargers","Chiefs","Saints","Chiefs","Patriots","Cardinals","Steelers","49ers","Jets","Jaguars","Buccaneers","Broncos","Bengals","Patriots","Bills","Packers","Redskins","Panthers","Dolphins","Falcons","Browns","Vikings","Titans","Steelers","Seahawks","Ravens","Texans","Bears","Lions","Colts","Cowboys","Chargers","Chiefs","Jets","Rams","Giants","Redskins","Patriots","Jaguars","Rams","Panthers","Patriots","Ravens","Cardinals","49ers","Jets","Raiders","Buccaneers","Giants","Jaguars","Bengals","Lions","Bills","Ravens","Packers","Panthers","Dolphins","Falcons","Packers","Browns","Vikings","Titans","Steelers","Ravens","Seahawks","Broncos","Bears","Eagles","Cowboys","Colts","Chargers","Bills","Giants","Rams","Patriots","Colts","Cowboys","Falcons","Eagles","Cardinals","Raiders","Steelers","Giants","Giants","Browns","Buccaneers","Lions","Bills","Broncos","Bengals","Packers","Dolphins","Falcons","Redskins","Panthers","Browns","Broncos","Titans","Bills","Seahawks","Ravens","Texans","Bears","Eagles","Colts","Cowboys","Chargers","Chiefs","Saints","Rams","Browns","Giants","Falcons","Redskins","Cardinals","Steelers","49ers","Saints","Jaguars","Cardinals","Giants","Bills","Broncos","Bengals","Lions","Packers","Falcons","Panthers","Titans","Browns","Vikings","Ravens","Steelers","Ravens","Packers","Texans","Jets","Eagles","Bengals","Colts","Chargers","Chiefs","Saints","Rams","Lions","Patriots","Redskins","Steelers","Buccaneers","Vikings","Bengals","Bengals","49ers","Bengals","Chiefs","Buccaneers","Chiefs","Jets","Raiders","Steelers","Texans","Browns","Bears","Bengals","Lions","Bills","Packers","Redskins","Bills","Lions","Falcons","Saints","Giants","Dolphins","Dolphins","Raiders","Jaguars","Broncos","Bears","Patriots","Colts","Cowboys","Chargers","Patriots","Saints","Giants","Patriots","Vikings","Cardinals","Cardinals","Vikings","Rams","Patriots","Redskins","Cardinals"]

perround = [32, 32, 38, 36, 35, 41, 40]
players = []
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

positions = [o.position for o in players]
positions = list(dict.fromkeys(positions))
client = commands.Bot(command_prefix='$')

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
googleclient = gspread.authorize(creds)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    if False:
        await setup()
    global start
    start = False
    global pause
    pause = False


def setup():
    # actual = googleclient.open('4 Round bot mock draft').add_worksheet("Round 1", 33, 7)
    y = 1

    for i, v in enumerate(perround):
        actual = googleclient.open('4 Round bot mock draft').add_worksheet("Round " + str(i + 1), v + 1, 7)
        time.sleep(20)
        actual.update_cell(1, 1, "Round Number")
        actual.update_cell(1, 2, "Pick Number")
        actual.update_cell(1, 3, "NFL Team")
        actual.update_cell(1, 4, "Player Name")
        actual.update_cell(1, 5, "Position")
        actual.update_cell(1, 6, "School")
        actual.update_cell(1, 7, "Notes")

        for j in range(0, v):
            time.sleep(10)
            actual.update_cell(j+2, 1, str(i+1))
            actual.update_cell(j+2, 2, str(y))
            actual.update_cell(j+2, 3, teampicks[y-1])
            y += 1
    #
    actual = googleclient.open('4 Round bot mock draft').add_worksheet("Players", 1000, 1000)
    for i, v in enumerate(positions):
        actual.update_cell(1, i+1, v)
        playersinposition = [index for index, value in enumerate(players) if value.position == v]
        for j, u in enumerate(playersinposition):
            time.sleep(1.5)

            actual.update_cell(j+2, i+1, players[u].name)
    actual = googleclient.open('4 Round bot mock draft').add_worksheet("Trades", 1000, 1000)
    actual.update_cell(1, 1, "Team A")
    actual.update_cell(1, 2, "Gives up")
    actual.update_cell(1, 3, "Team B")
    actual.update_cell(1, 5, "Gives up")


def googletrade(teamA, givingA, teamB, givingB):
    googleclient.login()
    for x in givingA:
        roundnum = 0
        for y in perround:
            roundnum += 1
            if x <= y:
                break
            x -= y
        state = googleclient.open('4 Round bot mock draft').worksheet("Round " + str(roundnum))
        state.update_cell(x + 1, 3, teamB)
    for x in givingB:
        roundnum = 0
        for y in perround:
            roundnum += 1
            if x <= y:
                break
            x -= y
        state = googleclient.open('4 Round bot mock draft').worksheet("Round " + str(roundnum))
        state.update_cell(x + 1, 3, teamA)



def googlepick(num, playerd):
    googleclient.login()
    roundnum = 0
    for y in perround:
        roundnum += 1
        if num <= y:
            break
        num -= y
    state = googleclient.open('4 Round bot mock draft').worksheet("Round " + str(roundnum))
    state.update_cell(num + 1, 4, playerd.name)
    state.update_cell(num + 1, 5, playerd.position)
    state.update_cell(num + 1, 6, playerd.school)
    state = googleclient.open('4 Round bot mock draft').worksheet("Players")
    posList = [index for index, value in enumerate(players) if value.position == playerd.position]
    location = posList.index(players.index(playerd))
    y = state.cell(location +2, positions.index(playerd.position) + 1).value
    if y == playerd.name:
        state.update_cell(location + 2, positions.index(playerd.position) + 1, strike(y))
        return
    #eventually add an else to look for people who decide to use their own position


def googleuseold():
    replace = 0
    # for z, x in enumerate(perround):
    #     state = googleclient.open('4 Round bot mock draft').worksheet("Round " + str(z+1))
    #     for y in range(0, x):
    #         fake = state.cell(y + 2, 4).value
    #         new_list = [index for index, value in enumerate(players) if value.name == fake]
    #         time.sleep(4)
    #         if len(new_list) == 0:
    #             return
    #         elif len(new_list) == 1:
    #             players[new_list[0]].draftnum = replace
    #         elif players[new_list[0]].position == state.cell(y+2, 5).value:
    #             players[new_list[0]].draftnum = replace
    #         elif players[new_list[1]].position == state.cell(y+2, 5).value:
    #             players[new_list[1]].draftnum = replace
    #         replace += 1

    state = googleclient.open('4 Round bot mock draft').worksheet("Signup Sheet")
    teamsinspread = state.col_values(1)
    gmsinspread = state.col_values(3)
    for y in range(1, 33):
        if gmsinspread[y] != "":
            GMs.append(GM(teamsinspread[y], int(gmsinspread[y])))
       #eventually add a check if its a different player


def strike(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result


@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return

    if not message.guild:
        await message.channel.send("Don't private message me")
        if message.content.startswith("$checkpicks"):
            await client.process_commands(message)
        print(message.content)
        print(message.author.name)
        return
    if message.channel.name == "flair_requests":
        for x in teams:
            if x.lower() in message.content.lower():
                role = discord.utils.get(message.guild.roles, name=x)
                await message.author.add_roles(role)
                return
        await message.channel.send("Post the full NFL teamname you want your flair to be.")
        return
    await client.process_commands(message)


@client.command(brief="Shows which GM spots are still open")
async def gmspotsopen(ctx):
    if len(GMs) == 32:
        await ctx.send("All teams are filled :sweat_smile: ")
        return
    await ctx.send("The " + str(len(list(set(teams) - set(o.team for o in GMs)))) + " Teams that don't have a gm are" + str(list(set(teams) - set(o.team for o in GMs))))


@client.command()
async def setup(ctx):
    if "MODS" not in [o.name for o in ctx.author.roles] and "COMMISH" not in [o.name for o in ctx.author.roles]:
        await ctx.send('You do not have permissions for that')
        return
    await setup()


@client.command(brief="Can check whos the gm of a certain Team")
async def gmcheck(ctx, team: str):
    team = team[0].upper() + team[1:].lower()
    if team not in teams:
        await ctx.send('Not Valid Team Name')
        return
    if team in [o.team for o in GMs]:
        x = [o.team for o in GMs].index(team)
        guild = ctx.author.guild
        #print(GMs[x].gmID)
        await ctx.send('The GM of the ' + GMs[x].team + " is " + guild.get_member(GMs[x].gmID).mention)
    else:
        await ctx.send('No one is GMing the ' + team)


@client.command(brief="MODONLY!     Opens GM Signups")
async def opensignups(ctx):
    if "MODS" not in [o.name for o in ctx.author.roles] and "COMMISH" not in [o.name for o in ctx.author.roles]:
        await ctx.send('You do not have permissions for that')
    else:
        await ctx.send('SignUps are Open')
        GMs.clear()
        global signin
        signin = True


@client.command(brief="Signin To GM a team, $gmsignin TeamName")
async def gmsignin(ctx, team: str):
    team = team[0].upper() + team[1:].lower()
    if signin:
        if ctx.author.id in [o.gmID for o in GMs] and "MODS" not in [o.name for o in ctx.author.roles] and "COMMISH" not in [o.name for o in ctx.author.roles]:
            await ctx.send('You have already signed up for a team. If you are GMing more than one team talk to the commish')
        elif team not in teams:
            await ctx.send('Not Valid Team Name')
        elif team in [o.team for o in GMs]:
            x = [o.team for o in GMs].index(team)
            guild = ctx.author.guild
            await ctx.send(guild.get_member(GMs[x].gmID).name + ' is already GMing the ' + team)
        else:
            GMs.append(GM(team, ctx.author.id))
            googleclient.login()
            sheet = googleclient.open('4 Round bot mock draft').worksheet("Signup Sheet")
            sheet.update_cell(sheet.col_values(1).index(team)+1, 3, str(ctx.author.id))
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
    team = team[0].upper() + team[1:].lower()
    googleclient.login()
    if "MODS" not in [o.name for o in ctx.author.roles] and "COMMISH" not in [o.name for o in ctx.author.roles]:
        await ctx.send('You do not have permissions for that')
    elif team not in teams:
        await ctx.send('Not Valid Team Name')
    elif team in [o.team for o in GMs]:
        x = [o.team for o in GMs].index(team)
        GMs[x].gmID = castro.id
        await ctx.send('The GM of the ' + team + " is  now " + castro.mention)
        sheet = googleclient.open('4 Round bot mock draft').worksheet("Signup Sheet")
        sheet.update_cell(sheet.col_values(1).index(team)+1, 3, str(castro.id))

    else:
        GMs.append(GM(team, castro.id))
        await ctx.send(castro.mention + ' is now GMing the ' + team)
        sheet = googleclient.open('4 Round bot mock draft').worksheet("Signup Sheet")
        sheet.update_cell(sheet.col_values(1).index(team)+1, 3, str(castro.id))



@client.command(brief="Pick a player, $pick FirstName LastName")
async def pick(ctx):
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
                y = [o.team for o in GMs].index(b)
                if GMs[y].gmID == message.author.id:
                    print(GMs[y].team)
                    x = y
                    break
            except ValueError:
                pass
        else:
            task = asyncio.ensure_future(message.channel.send(message.author.name + ', wait your turn'))
            return False
        print(GMs[x].team)
        print(GMs[y].team)
        pickname = args[1] + ' ' + args[2]
        pickposition = ""
        pickschool = ""
        if len(args) == 4:
            if args[3] in positions:
                pickposition = args[3]
            else:
                pickschool = args[3]
        elif len(args) == 5:
            pickschool = args[4]
            pickposition = args[3]
        roundnum = 0
        juv = peoplewhocandraft[freshlist.index(GMs[x].team)] + 1
        for y in perround:
            roundnum += 1
            if juv <= y:
                 break
            juv -= y
        explanation = "Did you mean " + pickname + ","
        z = 0
        if pickname.lower() in [o.name.lower() for o in players]:
            indices = [i for i, y in enumerate([o.name.lower() for o in players]) if y == pickname.lower()]
            if len(indices) > 1:
                while z < len(indices):

                    explanation += players[indices[z]].position+", from " + players[indices[z]].school + " or the "
                    if pickschool == players[indices[z]].school or players[indices[z]].position == pickposition:
                        if players[indices[z]].draftnum != -1:
                            task = asyncio.ensure_future(message.channel.send(message.author.name + ', that guy was drafted'))
                            return False
                        else:
                            task = asyncio.ensure_future(message.guild.text_channels[[o.name for o in message.guild.text_channels].index("mock-draft-room")].send("The " + GMs[x].team + " pick is in!"))
                            task = asyncio.ensure_future(message.guild.text_channels[[o.name for o in message.guild.text_channels].index("pickannouncement")].send(str(roundnum) + "." + str(peoplewhocandraft[freshlist.index(GMs[x].team)] + 1) + '.  The ' + GMs[x].team + ' take ' + players[indices[0]].name + ", " + players[indices[z]].position + ', ' + players[indices[z]].school))
                            task = asyncio.ensure_future(message.channel.send("Confirmed pick"))
                            players[indices[z]].draftnum = peoplewhocandraft[freshlist.index(GMs[x].team)]
                            store = peoplewhocandraft[freshlist.index(GMs[x].team)]
                            peoplewhocandraft.pop(freshlist.index(GMs[x].team))
                            googlepick(store + 1, players[indices[z]])
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
            task = asyncio.ensure_future(message.guild.text_channels[[o.name for o in message.guild.text_channels].index("mock-draft-room")].send("The " + GMs[x].team + " pick is in!"))

            task = asyncio.ensure_future(message.guild.text_channels[[o.name for o in message.guild.text_channels].index("pickannouncement")].send(str(roundnum) + "." + str(peoplewhocandraft[freshlist.index(GMs[x].team)]+1) + '  The ' + GMs[x].team + ' take ' + players[indices[0]].name + ", " + pickposition + ', ' + players[indices[0]].school))
            task = asyncio.ensure_future(message.channel.send("Confirmed pick"))
            players[indices[0]].draftnum = peoplewhocandraft[freshlist.index(GMs[x].team)]
            store = peoplewhocandraft[freshlist.index(GMs[x].team)]
            peoplewhocandraft.pop(freshlist.index(GMs[x].team))
            googlepick(store + 1, players[indices[0]])
            return True
        else:
            task = asyncio.ensure_future(message.channel.send(message.author.name + ', Double check your spelling, cause that is not a player'))
            return False


@client.command()
async def useold(ctx):
    if "MODS" not in [o.name for o in ctx.author.roles] and "COMMISH" not in [o.name for o in ctx.author.roles]:
        await ctx.send('You do not have permissions for that')
        return
    googleuseold()
    await ctx.send("Finished Setting up Old")



@client.command(brief="MODONLY! Starts Draft, $start RoundAmount ")
async def start(ctx, roundnum: int = 2):
    global start
    start = True
    if "MODS" not in [o.name for o in ctx.author.roles] and "COMMISH" not in [o.name for o in ctx.author.roles]:
        await ctx.send('You do not have permissions for that')
        return
    if len(GMs) != 32:
        await ctx.send('We are ' + str(32-len(GMs)) + ' GMs short from everyone having a GM')
    val = 0
    timelimit = [120, 90, 90, 90, 60, 60, 60]
    storage = ""
    global peoplewhocandraft
    global pause
    pause = False
    useless = [o.draftnum for o in players]
    lastpick = max(useless)
    startup = lastpick+1
    while start:
        for x, end in enumerate(perround):
            if x == roundnum:
                break
            val += end
            await ctx.send(str(timelimit[x]) + " seconds per round")
            for y in range(startup, val):
                # if teampicks[y] in [o.name for o in ctx.guild.roles]:
                #     await ctx.send(ctx.guild.roles[[o.name for o in ctx.guild.roles].index(teampicks[y])].mention + ' are on the clock')
                # else:
                #
                await ctx.send(teampicks[y] + ' are on the clock ')
                try:
                    await ctx.guild.text_channels[([idx for idx, s in enumerate([o.name.lower() for o in ctx.guild.text_channels]) if teampicks[y].lower() in s][0])].send(teampicks[y] + " are on the clock")
                    await ctx.guild.text_channels[([idx for idx, s in enumerate([o.name.lower() for o in ctx.guild.text_channels]) if teampicks[y+1].lower() in s][0])].send("You guys are up next")
                except IndexError:
                    print(teampicks[y] + " Doesnt have  a channel")

                timer = 0
                peoplewhocandraft.append(y)
                storage = teampicks[y]

                #print(peoplewhocandraft[0])
                while timer < timelimit[x] and start:
                    while pause:
                        await asyncio.sleep(1)
                    if storage != teampicks[y]:
                        storage = teampicks[y]
                        try:
                            await ctx.guild.text_channels[([idx for idx, s in enumerate([o.name.lower() for o in ctx.guild.text_channels]) if teampicks[y].lower() in s][0])].send(teampicks[y] + ' are now on the clock and have ' + str(timelimit[x] - timer) + ' seconds left ')
                        except IndexError:
                            print(teampicks[y].lower() + " Doesnt have  a channel")
                        timer -= 30
                        await ctx.send(teampicks[y] + ' are now on the clock and have ' + str(timelimit[x] - timer) + ' seconds left ')
                    try:
                        switch = True
                        if timer % 30 == 0:
                            await ctx.send(teampicks[y] + ' have ' + str(timelimit[x]-timer) + ' seconds left')
                            try:
                                await ctx.guild.text_channels[([idx for idx, s in enumerate([o.name.lower() for o in ctx.guild.text_channels]) if teampicks[y].lower() in s][0])].send(teampicks[y] + ' have ' + str(timelimit[x] - timer) + ' seconds left ')
                            except IndexError:
                                print(teampicks[y].lower() + " Doesnt have  a channel")
                        await client.wait_for('message', check=is_correct, timeout=1)
                    except asyncio.TimeoutError:
                        switch = False
                        timer += 1
                    #print("Why " + str(switch) + " " + str(y))
                    if switch and y not in peoplewhocandraft:
                        break
                if not start:
                    break
            if not start:
                break
            await ctx.guild.text_channels[[o.name for o in ctx.guild.text_channels].index("pickannouncement")].send("End of Round:" + str(x + 1))
            await ctx.send("End of Round:" + str(x + 1))
            jumanji=0
            await ctx.send("Two Minute break til next round. Pause if you want a longer one")
            while jumanji < 120 or pause:
                jumanji += 1
                await asyncio.sleep(1)
            startup += end


@client.command(brief="MODONLY! Stops Draft")
async def stop(ctx):
    if "MODS" not in [o.name for o in ctx.author.roles] and "COMMISH" not in [o.name for o in ctx.author.roles]:
        await ctx.send('You do not have permissions for that')
        return
    global start
    start = False
    await ctx.send("The draft has stopped buddy")


@client.command(brief="MODONLY! Pauses Draft")
async def pause(ctx):
    if "MODS" not in [o.name for o in ctx.author.roles] and "COMMISH" not in [o.name for o in ctx.author.roles]:
        await ctx.send('You do not have permissions for that')
        return
    global pause
    pause = True
    await ctx.send("The draft has paused matey")


@client.command(brief="MODONLY! Unpauses Draft")
async def unpause(ctx):
    if "MODS" not in [o.name for o in ctx.author.roles] and "COMMISH" not in [o.name for o in ctx.author.roles]:
        await ctx.send('You do not have permissions for that')
        return
    global pause
    pause = False
    global start
    start = True
    await ctx.send("The draft has been unpaused guy")


@client.command(brief="Check picks")
async def checkpicks(ctx, team: str = None):
    if not team:
        if ctx.author.id in [o.gmID for o in GMs]:
            team = GMs[[o.gmID for o in GMs].index(ctx.author.id)].team
        else:
            for x in [o.name for o in ctx.author.roles]:
                if x in teams:
                    team = x
                    break
        if not team:
            await ctx.send('I cant tell what team you are. Use $checkpicks teamname')
            return
    if team not in teams:
        await ctx.send('Invalid team name')
        return
    last_list = []
    new_list = [index for index, value in enumerate(teampicks) if value.lower() == team.lower()]
    for x in new_list:
        if len([value.name for value in players if value.draftnum == x]) == 0:
            last_list.append(str(x+1))
        else:
            last_list.append(str(x+1) + ": " + [value for value in players if value.draftnum == x][0].name)
    await ctx.send(team + ": " + str(last_list))


@client.command(brief="Check positions")
async def checkpositions(ctx):
    await ctx.send(positions)


def is_correct2(message):
    if message.content.startswith('$trade accept') or message.content.startswith('$trade deny'):
        args = message.content.split(" ")
        if len(args) < 3:
            task = asyncio.ensure_future(message.channel.send(message.author.name + ', Use $trade accept TeamName or $trade deny TeamName'))
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
                    message.content += str(x)
                    return True
                z += 1
            x += 1
            z = 0
        task = asyncio.ensure_future(message.channel.send(message.author.name + ', no valid offers from that team'))
        return False
    return False

@client.command(brief='Trade assets, $trade opposingteam GivingUp(Split by , and surrounded by quotes for stuff like "2020 1st,Teddy BridgeWater,1,33") GettingBack(Split the same as before) ')
async def trade(ctx, team: str = None, offer: str = None, recv: str = None, sendingteam: str = None):
    if team == "accept" or team == "deny":
        return
    if not recv:
        await ctx.send('$trade opposingteam GivingUp(Split by , and surrounded by quotes for stuff like "2020 1st,Teddy BridgeWater,1,33") GettingBack(Split the same as before)')
        return
    print(ctx.message.content)
    print(ctx.channel.name)
    offerargs = offer.split(",")
    recvargs = recv.split(",")
    offerpicks = []
    recvpicks = []
    x = 0
    global teampicks
    #await ctx.send(start)
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
    tradeoffers.append(Trade(sendingteam, team))
    await ctx.send("Offer sent")
    try:
        await ctx.guild.text_channels[([idx for idx, s in enumerate([o.name.lower() for o in ctx.guild.text_channels]) if team.lower() in s][0])].send(team + ", Trade attempt here. The " + sendingteam + " want to trade you " + offer + " for " + recv)
        await ctx.guild.text_channels[([idx for idx, s in enumerate([o.name.lower() for o in ctx.guild.text_channels]) if team.lower() in s][0])].send("Accept with $trade accept " + sendingteam)
    except IndexError:
            print(team + " Doesnt have  a channel")
        #await ctx.send(guild.get_member(opposingGM).mention + ", Trade attempt here. The " + sendingteam + " want to trade you " + offer + " for " + recv)
    timedout = True
    for x in range(0, 60):
        try:
            george = await client.wait_for('message', check=is_correct2, timeout=1)
            args = george.content.split(" ")
            if args[2] == sendingteam and GMs[[o for o in GM.gmID].index(george.author)].team == team:
                timedout = False
                break
        except asyncio.TimeoutError:
            pass
    x = 0
    tradeoffers = [item for item in tradeoffers if item.sendteam != sendingteam and item.recvteam != team]
    if george.content.startswith('$trade deny'):
        await ctx.send("Trade offer was denied")
        return
    if timedout:
        await ctx.send("Offer Timed out")
        try:
            await ctx.guild.text_channels[([idx for idx, s in enumerate([o.name.lower() for o in ctx.guild.text_channels]) if team.lower() in s][0])].send(team + ", Trade timed out")
        except IndexError:
            print(team + " Doesnt have  a channel")
            await ctx.send("Trade attempt timed out, " + ctx.author.mention)
        return
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

    await ctx.guild.text_channels[[o.name for o in ctx.guild.text_channels].index("mock-draft-room")].send("Trade Alert!!! :rotating_light: :rotating_light: :rotating_light: ")
    await ctx.send("Trade confirmed")
    await ctx.guild.text_channels[[o.name for o in ctx.guild.text_channels].index("tradeannouncement")].send("Trade Alert: The "+sendingteam + " sends " + offer + " to the " + team + " for " + recv)
    googleclient.login()
    actual = googleclient.open('4 Round bot mock draft').worksheet("Trades")
    actual.update_cell(len(actual.col_values(1)) + 1, 1, sendingteam)
    actual.update_cell(len(actual.col_values(2)) + 1, 2, str(offerargs))
    actual.update_cell(len(actual.col_values(3)) + 1, 3, team)
    actual.update_cell(len(actual.col_values(4)) + 1, 4, str(recvargs))
    googletrade(sendingteam, offerpicks, team, recvpicks)

client.run('NTU1ODI0NzYzNTQ1NzE0NzQ4.D2wz1Q.naMLxdEsOn1ur67nKT39E6NKCeY')
