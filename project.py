#importing the modules I need
import os
import discord
from ec2_metadata import ec2_metadata as md
from dotenv import load_dotenv

#here for debugging, remove later
print(md.region)

load_dotenv()
client = discord.Client()
token = str(os.getenv('TOKEN'))

csm_commands = {
    '`help`': 'this will output the current list of commands available to you',
    '`hello world`': 'bot responds with hello, you can use this as a test command',
    '`server status`': 'you can use this command to determine whether your server is online or offline`',
    '`tell me about my server`': 'this will output metadata about your ec2 instance, such as address, region, zone etc',
    '`downtime`': 'this will output when the next expected downtime will be',
    '`downtime log`': 'this will output a log of the downtimes in the past(work in progress)'
}

dev_commands = {
    '`help`': 'this will output the current list of commands available to you',
    '`set downtime from {start-time} to {downtime}`': 'eg. set downtime from 8pm to 11pm',
    '`server start`': "starts up the server if it's offline",
    '`server stop`': "stops the server if it's online"
}

downtime = "1 septillion years" #change later lol
downtimes = []
downtimeStart = "unknown"
downtimeEnd = "unknown"
serverOnline = True

@client.event
async def on_ready():
    try:
        print("Logged in as a bot {0.user}".format(client))
    except Exception as e:
        print("Something went wrong. Please try again later.")

@client.event
async def on_message(message):
    global serverOnline
    global downtimeStart
    global downtimeEnd
    global downtimes

    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    userMessage = str(message.content)
    print(serverOnline)

    async def outputMessage(msg):
        try:
            await message.channel.send(msg)
        except discord.errors.HTTPException as e:
            print(f"Error sending message: {e}")

    async def outputCommands(commandsDict):
        for command in commandsDict:
            await outputMessage(f"{command} - {commandsDict[command]}")

    if message.author == client.user:
        return

    print(f'{username}: {userMessage} in channel: #{channel}')

    try:
        if channel == "server-updates":
            if userMessage == "help":
                await outputMessage("Here are the available commands:\n")
                await outputCommands(csm_commands)
            elif userMessage == "hello world":
                await outputMessage('hello')
            elif userMessage == "downtime":
                if downtimeStart == "unknown":
                    await outputMessage(f'No expected downtimes in the future currently :)')
                elif serverOnline:
                    await outputMessage(f'Upcoming Downtime is from {downtimeStart} to {downtimeEnd}')
                else:
                    await outputMessage(f'Your server will be up and running after {downtimeEnd}')
            elif userMessage == "tell me about my server":
                await outputMessage(f"""your ec2 server data:
region: {md.region}
public ipv4 address: {md.public_ipv4}
availability zone:{md.availability_zone}
server instance: {md.instance_type}
""")
            elif userMessage == "server status":
                if serverOnline:
                    await outputMessage("Server status: online")
                else:
                    await outputMessage("Server status: offline")
            else:
                await outputMessage(f"I'm sorry, the command '{userMessage}' is not a valid command.\ntry 'help' for a list of available commands.")

        if channel == "engineering-team":
            if userMessage == "help":
                await outputMessage("Here are the available commands:\n")
                await outputCommands(dev_commands)
            elif userMessage.startswith("set downtime from"):
                downtimes = userMessage.split("from")[1].split("to")
                downtimeStart = downtimes[0].strip()
                downtimeEnd = downtimes[1].strip()
                await outputMessage(f"Downtime has been set from {downtimeStart} to {downtimeEnd}.")
            elif userMessage == "server stop":
                serverOnline = False
                await outputMessage(f'the server has been shutdown')
            elif userMessage == "server start":
                serverOnline = True
                await outputMessage(f'The server has been started')
            else:
                await outputMessage(f"I'm sorry, the command '{userMessage}' is not a valid command.\ntry 'help' for a list of available commands.")
    except Exception as e:
        print(f"An error occurred: {e}")

client.run(token)

