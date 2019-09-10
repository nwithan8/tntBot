import discord
from discord.ext import commands
import time
import asyncio
from cryptography.fernet import Fernet
from collections.abc import Sequence


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



def make_sequence(seq):
    if seq is None:
        return ()
    if isinstance(seq, Sequence) and not isinstance(seq, str):
        return seq
    else:
        return (seq,)

#A function for getting a messages content.
def message_check(channel=None, author=None, content=None, ignore_bot=True, lower=True):
    channel = make_sequence(channel)
    author = make_sequence(author)
    content = make_sequence(content)
    if lower:
        content = tuple(c.lower() for c in content)
    def check(message):
        if ignore_bot and message.author.bot:
            return False
        if channel and message.channel not in channel:
            return False
        if author and message.author not in author:
            return False
        actual_content = message.content.lower() if lower else message.content
        if content and actual_content not in content:
            return False
        return True
    return check

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("Do .info"))
    print("Bot ready")

# .encrypt command to encrypt a message (AES-128-CBC + HMAC-SHA-256)

@bot.command()
async def encrypt(ctx):
    user = ctx.author
    await user.send("Please enter the message to decrypt.")
    response = await bot.wait_for('message', check=message_check(channel=ctx.author.dm_channel))
    message = response.content
    encoded = message.encode()
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted = f.encrypt(encoded)
    embed=discord.Embed(
        title = "Copy",
        colour=discord.Colour.from_rgb(162, 0, 255)
    )
    embed.set_footer(text="**tntBot made by Purple#4706**", icon_url="https://profilepicturesdp.com/wp-content/uploads/2018/06/best-discord-profile-picture-1.gif")
    embed.add_field(name="Encrypted message", value=encrypted.decode())
    embed.add_field(name="Decryption key", value=key.decode())
    await user.send(embed=embed)


# .decrypt command to decrypt a encrypted message from the .encrypt command

@bot.command()
async def decrypt(ctx):
    user = ctx.author
    await user.send("Please enter the encrypted message.")
    response = await bot.wait_for('message', check=message_check(channel=ctx.author.dm_channel))
    encrypted = response.content.encode()
    await asyncio.sleep(1)
    await user.send("Please enter the decryption key:")
    response = await bot.wait_for('message', check=message_check(channel=ctx.author.dm_channel))
    key = response.content.encode()
    f = Fernet(key)
    decrypted = f.decrypt(encrypted)
    decoded = decrypted.decode()
    await user.send("Encrypted: {}".format(decoded))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        await ctx.send("Insufficient Permissions.")

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
        await ctx.send("F")
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
        description = "Here are all the available commands this Bot can perform.",
        colour=discord.Colour.from_rgb(162, 0, 255)
    )
    embed.set_footer(text="**tntBot made by Purple#4706**", icon_url="https://profilepicturesdp.com/wp-content/uploads/2018/06/best-discord-profile-picture-1.gif")
    embed.add_field(name="User Commands", value=".invite | Get the invite link for this bot.\n.encrypt | Lets you encrypt a message in your DM's which another person can decrypt using the bot.\n.decrypt | Lets you decrypt an encrypted message.")
    embed.add_field(name="Admin Commands", value=".spam *SPAMCONTENT*  | Spams the *SPAMCONTENT*  in the channel until an admin executes .stopspam (If .stopspam doesn't get executed, the bot will stop spamming after 500 messages.\n.fucker | Fucks the channel (**VERY** dangerous) \n.clear *AMOUNT*  | Deletes *AMOUNT*  messages in the channel")
    await ctx.send(embed=embed)



bot.run(TOKEN)