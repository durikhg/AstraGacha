import discord
import random
import json
import os
from discord.ext import commands
from dotenv import load_dotenv

# ================== CONFIG ==================
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

DATA_FILE = "data.json"

# ================== CHARACTERS ==================
characters = [
    {
        "name": "Johnny",
        "rarity": "common",
        "price": 10,
        "image": "images/johnny.png"
    }
]

rarityChances = {
    "common": 40,
    "rare": 35,
    "epic": 20,
    "legendary": 5
}

rarityColors = {
    "common": discord.Color.light_grey(),
    "rare": discord.Color.blue(),
    "epic": discord.Color.purple(),
    "legendary": discord.Color.gold()
}

# ================== DATA ==================
def loadData():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)

    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def saveData(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def ensureUser(user_id):
    data = loadData()
    uid = str(user_id)

    if uid not in data:
        data[uid] = {
            "coins": 0,
            "inventory": []
        }
        saveData(data)

# ================== LOGIC ==================
def rollCharacter():
    rarity = random.choices(
        list(rarityChances.keys()),
        weights=rarityChances.values()
    )[0]

    available = [c for c in characters if c["rarity"] == rarity]
    return random.choice(available)

# ================== BUTTONS ==================
class coinButton(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=30)
        self.user_id = str(user_id)

    @discord.ui.button(label="💰 View Coins", style=discord.ButtonStyle.green)
    async def viewCoins(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = loadData()
        coins = data[self.user_id]["coins"]

        embed = discord.Embed(
            title="💰 Your Coins",
            description=f"You have **{coins} coins**",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

class sellButton(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=30)
        self.user_id = str(user_id)

    @discord.ui.button(label="Sell Character", style=discord.ButtonStyle.red)
    async def sellCharacter(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            return await interaction.response.send_message(
                "❌ This button is not for you.",
                ephemeral=True
            )
        
        data = loadData()
        user = data[self.user_id]

        if not user["inventory"]:
            embed = discord.Embed(
                title="❌ Error",
                description="Your inventory is empty.",
                color=discord.Color.red()
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        character_name = user["inventory"].pop()
        character = next(
            c for c in characters
            if c["name"].lower() == character_name.lower()
        )
        gain = character["price"] // 4
        user["coins"] += gain
        saveData(data)
        embed = discord.Embed(
            title="🛒 Character Sold!",
            description=f"You sold **{character_name}**",
            color=discord.Color.green()
        )
        embed.add_field(name="💰 Earned", value=f"{gain} coins")

        await interaction.response.send_message(embed=embed)

# ================== EVENTS ==================
@bot.event
async def on_ready():
    print(f"{bot.user} is online")

# ================== COMMANDS ==================
@bot.command()
async def roll(ctx):
    ensureUser(ctx.author.id)
    data = loadData()
    uid = str(ctx.author.id)

    character = rollCharacter()
    data[uid]["inventory"].append(character["name"])
    data[uid]["coins"] += 50
    saveData(data)

    file = discord.File(character["image"], filename="character.png")

    embed = discord.Embed(
        title="🎲 Character Obtained!",
        color=rarityColors[character["rarity"]]
    )

    embed.add_field(name="👤 Name", value=character["name"], inline=False)
    embed.add_field(name="⭐ Rarity", value=character["rarity"].capitalize(), inline=True)
    embed.add_field(name="💰 Value", value=f"{character['price']} coins", inline=True)
    embed.set_image(url="attachment://character.png")
    embed.set_footer(text=f"Requested by {ctx.author}")

    await ctx.send(
        embed=embed,
        file=file,
        view=coinButton(ctx.author.id)
    )

@bot.command()
async def inventory(ctx):
    ensureUser(ctx.author.id)
    data = loadData()
    uid = str(ctx.author.id)

    inventory = data[uid]["inventory"]

    if not inventory:
        embed = discord.Embed(
            title="🎒 Inventory",
            description="Your inventory is empty.",
            color=discord.Color.red()
        )
        return await ctx.send(embed=embed)

    items = "\n".join(f"• {item}" for item in inventory)

    embed = discord.Embed(
        title="🎒 Your Inventory",
        description=items,
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"Total: {len(inventory)} characters")

    await ctx.send(embed=embed)

@bot.command()
async def sell(ctx, *, character_name):
    ensureUser(ctx.author.id)
    data = loadData()
    uid = str(ctx.author.id)
    user = data[uid]

    if character_name not in user["inventory"]:
        embed = discord.Embed(
            title="❌ Error",
            description="You don't own this character.",
            color=discord.Color.red()
        )
        return await ctx.send(embed=embed)

    character = next(c for c in characters if c["name"].lower() == character_name.lower())

    user["inventory"].remove(character_name)
    gain = character["price"] // 4
    user["coins"] += gain
    saveData(data)

    embed = discord.Embed(
        title="🛒 Character Sold!",
        description=f"You sold **{character_name}**",
        color=discord.Color.green()
    )
    embed.add_field(name="💰 Earned", value=f"{gain} coins")

    await ctx.send(embed=embed)

@bot.command()
async def coins(ctx):
    ensureUser(ctx.author.id)
    data = loadData()
    uid = str(ctx.author.id)

    embed = discord.Embed(
        title="💰 Your Coins",
        description=f"You have **{data[uid]['coins']} coins**",
        color=discord.Color.gold()
    )
    await ctx.send(embed=embed)

bot.run(TOKEN)
