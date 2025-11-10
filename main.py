import discord
from discord.ext import commands
from config import token
from logic import Pokemon, Wizard, Fighter

# Setting up intents for the bot
intents = discord.Intents.default()  # Getting the default settings
intents.messages = True              # Allowing the bot to process messages
intents.message_content = True       # Allowing the bot to read message content
intents.guilds = True                # Allowing the bot to work with servers (guilds)

# Creating a bot with a defined command prefix and activated intents
bot = commands.Bot(command_prefix='!', intents=intents)

# An event that is triggered when the bot is ready to run
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')  # Outputs the bot's name to the console

# The '!go' command
@bot.command()
async def go(ctx):
    author = ctx.author.name  # Getting the name of the message's author
    # Check whether the user already has a Pokémon. If not, then...
    if author not in Pokemon.pokemons.keys():
        pokemon = Pokemon(author)  # Creating a new Pokémon
        await ctx.send(await pokemon.info())  # Sending information about the Pokémon
        image_url = await pokemon.show_img()  # Getting the URL of the Pokémon image
        if image_url:
            embed = discord.Embed()  # Creating an embed message
            embed.set_image(url=image_url)  # Setting up the Pokémon's image
            await ctx.send(embed=embed)  # Sending an embedded message with an image
        else:
            await ctx.send("Failed to upload an image of the pokémon.")
    else:
        await ctx.send("You've already created your own Pokémon.")  # A message that is printed whether a Pokémon has already been created

@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None  # Mendapatkan pengguna yang disebutkan dalam pesan
    if target:  # Memeriksa apakah ada pengguna yang disebutkan
        # Memeriksa apakah yang diserang dan yang bertahan memiliki Pokémon 
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]  # Mendapatkan Pokémon pemain bertahan
            attacker = Pokemon.pokemons[ctx.author.name]  # Mendapatkan Pokémon penyerang 
            result = await attacker.attack(enemy)  # Melakukan serangan dan mendapatkan hasilnya
            await ctx.send(result)  # Mengirimkan hasil serangan
        else:
            await ctx.send("Kedua player harus memiliki Pokémon untuk memulai pertempuran!")  # Mengumumkan bahwa setidaknya salah satu petarung tidak memiliki Pokémon 
    else:
        await ctx.send("Tentukan pengguna yang ingin Kalian serang dengan menyebut mereka.")  # Meminta untuk menyebutkan pengguna untuk menyerang

@bot.command()
async def info(ctx):
    author = ctx.author.name  # Getting the name of the message's author
    # Check whether the user already has a Pokémon. If not, then...
    if author in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[author]  # Creating a new Pokémon
        await ctx.send(await pokemon.info())  # Sending information about the Pokémon
        image_url = await pokemon.show_img()  # Getting the URL of the Pokémon image
        if image_url:
            embed = discord.Embed()  # Creating an embed message
            embed.set_image(url=image_url)  # Setting up the Pokémon's image
            await ctx.send(embed=embed)  # Sending an embedded message with an image
        else:
            await ctx.send("Failed to upload an image of the pokémon.")
    else:
        await ctx.send("You haven't made your own Pokémon.")  # A message that is printed whether a Pokémon has already been created


# Running the bot
bot.run(token)
