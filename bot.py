import discord
from discord.ext import commands
import time
import asyncio

token_file = "token.txt"
tkn = open(token_file, "r")
TOKEN = tkn.readline()
tkn.close
bot_idd = open("bot_id.txt", "r")
bot_id = bot_idd.readline()
bot_idd.close
spam_active=False
bot = commands.Bot(command_prefix=".")
bot.remove_command('help')


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("Do .info retard"))
    print("Bot ready")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        await ctx.send("Insufficient Permissions, Kek")

#A .op command i have used before, now the operators system has been replaced with a permission check
"""
@bot.command()
async def op(ctx, new_operator:int):
    global operators
    if ctx.author.id in operators:
        operators.append(new_operator)
        await ctx.send("Successfully added a new operator")
    else:
        await ctx.send("Insufficient Permissions")
"""

#The .clear command

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount:int):
    await ctx.channel.purge(limit=amount)
    await asyncio.sleep(2)
    await ctx.send("Succesfully cleared {} messages {}.".format(amount, ctx.author))


#The .spam and .stopspam command

@bot.command()
@commands.has_permissions(administrator=True)
async def spam(ctx, *, spamcontent):
    global spam_active
    spam_active=True
    amount = 500
    await asyncio.sleep(2)
    print("Spamming started")
    for i in range(amount):
        await ctx.send(spamcontent)
        await asyncio.sleep(0.5)
        if spam_active==False:
            break
        else:
            continue



@bot.command()
@commands.has_permissions(administrator=True)
async def stopspam(ctx):
    global spam_active
    spam_active=False
    await ctx.send("Stopped spamming. **sry**")




#Customisable .invite command

@bot.command()
async def invite(ctx):
    inv = open("invite_link.txt", "r")
    link = inv.readline()
    inv.close
    await ctx.send("To invite me to other servers please use this link: {}".format(link))


#The .fucker command
#Deletes all messages in the channel and then proceeds to spam the defined spam content 500 times


@bot.command()
@commands.has_permissions(administrator=True)
async def fucker(ctx):
    await ctx.send("Welcome {}, the server will be fucked".format(ctx.author))
    await asyncio.sleep(2)
    fuckedchannel = ctx.channel.id
    print("Fucker started")
    await ctx.channel.purge(limit=999999999999)
    amount = 500
    for i in range(amount):
        await ctx.send("Get Fucked by Toxilus")
        """@bot.event
        async def on_message(message):
            if message.channel.id == fuckedchannel:
                if message.author.id != bot_id:
                    await message.delete()"""
            

#The .info command

@bot.command()
async def info(ctx):
    embed=discord.Embed(
        title = "Info",
        description = "Here are all the available commands this Bot can perform. Kek",
        colour=discord.Colour.from_rgb(162, 0, 255)
    )
    embed.set_footer(text="**tntBot made by Purple#4706**", icon_url="https://profilepicturesdp.com/wp-content/uploads/2018/06/best-discord-profile-picture-1.gif")
    embed.add_field(name="User Commands", value=".invite | Get the invite link for this Bot")
    embed.add_field(name="Admin Commands", value=".spam *SPAMCONTENT*  | Spams the *SPAMCONTENT*  in the channel until an admin executes .stopspam (If .stopspam doesn't get executed, the bot will stop spamming after 500 messages.\n.fucker | Fucks the channel (**VERY** dangerous) \n.clear *AMOUNT*  | Deletes *AMOUNT*  messages in the channel")
    await ctx.send(embed=embed)



bot.run(TOKEN)