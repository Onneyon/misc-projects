import discord
from discord.ext import commands
import random

description = "Anonymously assign people for secret santa online without needing a third party"

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='s!', description=description, intents=intents)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(name="assign",
    help = "Assign a group of people to buy for each other by listing their @s and having the bot DM them",
    brief = "Assign a group by listing @s",
    usage = "@[person 1] @[person 2] @[person 3] ...")

async def assign(ctx, *args: discord.User):

    gifters = []
    recipients = []
    
    for gifter in args:
        if gifter not in gifters:
            gifters.append(gifter)
            recipients.append(gifter)

    if len(gifters) < 3:
        await ctx.send("You need at least 3 people to play")
        return

    assignments = []

    for gifter in gifters:
        while True:
            recipient = recipients[random.randint(0, len(recipients) - 1)]
            if recipient != gifter:
                break

        assignments.append([gifter, recipient])
        recipients.remove(recipient)
    
    for assignment in assignments:
        await assignment[0].send(f"You are buying for {assignment[1]}")


token = False

try:
    with open("token.txt", "r") as f:
        token = f.readline()

except FileNotFoundError:
    print("Error - no file named [token.txt] found")

if token:
    bot.run(token)