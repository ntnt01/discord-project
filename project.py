import os
import discord
import ec2_metadata as md
from dotenv import load_dotenv


#print(md.region)
#print(md.instance_id)

load_dotenv()
client = discord.Client()
token = str(os.getenv('TOKEN'))


csm_commands = {
        'help': 'this will output the current list of commands available to you',
        'hello world': 'bot responds with hello, you can use this as a test command',
        'tell me about my server': 'this will output metadata about your ec2 instance, such as address,region,zone etc',
        'downtime': 'this will output when the next expected downtime will be',
        'downtime log': 'this will output a log of the downtimes in the past'
            }

async def outputMessage(message):
    await message.channel.send(message) 
    

async def outputCommands(commandsDict):
    for command in commandsDict:
        await outputMessage(f"{command} - {commandsDict[command]}")

@client.event
async def on_ready():
    try:
        print("Logged in as a bot {0.user}".format(client))
    except Exception as e:
        print("Something went wrong. Please try again later.")


@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    userMessage = str(message.content)


    if message.author == client.user:
        return

    print(f'{username}: {userMessage} in channel: #{channel}')

    if channel == "server-updates":
        if userMessage == "help":
            await outputCommands("Here are the available commands:\n"+csm_commands)
        elif userMessage == "hello world":
            await outputMessage('hello')
        elif userMessage == "tell me about my server":
            await outputMessage(f"""your ec2 server data:
                          region: {md.region}
                          public ipv4 address: {md.public_ipv4}
                          availability zone:{md.availability_zone}
                          server instance: {md.instance_type}
                          """)
        else:
             await outputMessage(f"I'm sorry, the command '{userMessage}' is not a valid command.\ntry 'help' for a list of available commands.")


client.run(token)
