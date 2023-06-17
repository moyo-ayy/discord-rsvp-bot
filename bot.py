import discord
from discord.ext import commands
import datetime
import threading
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='.', intents=intents)


@client.event
async def on_ready():
    print('bot ready')


@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    channel_id = payload.channel_id
    channel = client.get_channel(channel_id)
    # await channel.send("Reaction noted")


# @client.event
# async def on_message(message):
#     print(message.author, message.content, message.channel.id)


@client.command()
async def hello(ctx):
    await ctx.channel.send(f'hello there {ctx.author.mention}')

storedEvents = []


@client.command()
async def event(ctx):

    try:
        answers = []
        emojis = ['✔️','❌']
        await ctx.send("What is the title of this event?")
        message = await client.wait_for('message', check=lambda m: m.channel == ctx.channel and m.author == ctx.author,
                                        timeout=30)
        answers.append(message.content)
        await ctx.send("What is the date and time of this event (in the format: 8/21 18:30)")
        message = await client.wait_for('message', check=lambda m: m.channel == ctx.channel and m.author == ctx.author,
                                        timeout=30)
        answers.append(message.content)

        datetime_object = datetime.datetime.strptime(answers[1], '%m/%d %H:%M')
        temp = {"title": answers[0], "time": datetime_object, "channel": ctx.channel.id}

        embed = discord.Embed(title="Event successfully created",
                              description=f'The event "{answers[0]}" was scheduled for {answers[1]}'
                                          f'\n\nWill you be able to attend',
                              color=0x00ff00)

        message = await ctx.send(embed=embed)
        for i in emojis:
            await message.add_reaction(i)

        storedEvents.append(temp)

        def check(reaction, user):
            return str(reaction.emoji) == '✔️'

        await client.wait_for('reaction_add', timeout=120.0, check=check)

    except:
        await ctx.send("Event could not be created")


def checktime():
    threading.Timer(5, checktime).start()
    now = datetime.datetime.now()
    current_time = now.strftime("%m/%d %H:%M")
    current_time = datetime.datetime.strptime(current_time, '%m/%d %H:%M')

    for i in storedEvents:
        if current_time == i["time"]:
            channel = client.get_channel(i["channel"])
            print(f'IT IS TIME FOR {i["title"]}')
            client.loop.create_task(channel.send(f'IT IS TIME FOR \"{i["title"]}\" @here'))
            storedEvents.remove(i)


checktime()


@client.command()
async def test(ctx):
    print(storedEvents)








client.run(token)