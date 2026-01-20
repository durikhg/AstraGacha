# 🌌 AstraGacha

AstraGacha is a **generic Discord gacha bot**, built in **Python** using `discord.py`. It allows players to roll characters, collect items, sell characters for coins, and have all progress automatically saved per user.

The project is designed to be **simple, expandable, and easy to customize**, serving as a solid base for any gacha system (anime, games, original characters, cards, etc).

---

## ✨ Features

- 🎲 **Gacha system** (random rolls)
- ⭐ Characters with **different rarities**
- 📊 **Configurable chances** per rarity
- 🎒 **Per-player inventory**
- 💰 **Coin system**
- 🛒 **Character selling system**
- 💾 **Automatic JSON data saving**
- 🖼️ Embeds with **character images**
- 🔘 Interactive Discord **buttons (UI)**

---

## ⭐ Rarity System

Each character has a rarity that defines its chance of appearing in the gacha:

| Rarity | Chance |
|-------|--------|
| Common | 40% |
| Rare | 35% |
| Epic | 20% |
| Legendary | 5% |

Embed colors change automatically based on character rarity.

---

## 🎮 Commands

### 🎲 `!roll`
Rolls the gacha and grants a random character.

- Adds the character to the inventory
- Grants coins to the player
- Displays the character image
- Shows a button to view coins

---

### 🎒 `!inventory`
Displays all characters owned by the player.

- Clean and simple list
- Shows the total number of characters

---

### 🛒 `!sell <name>`
Sells a specific character from the inventory.

- Removes the character
- Grants coins (25% of the original value)

---

### 💰 `!coins`
Displays the player's current coin balance.

---

## 🔘 Interactive Buttons

- **💰 View Coins** → Shows your coins privately (ephemeral message)
- **Sell Character** → Automatically sells the last obtained character

Buttons are **protected**, meaning only the owner can use them.

---

## 📁 Project Structure

```
AstraGacha/
│
├── main.py            # Main bot code
├── data.json          # User data (auto-generated)
├── .env               # Discord bot token
└── images/
    └── johnny.png     # Character images
```

---

## 🧩 Adding Characters

To add new characters, simply insert them into the `characters` list:

- Name
- Rarity
- Price
- Image path

Examples:
- Johnny (common)
- Hero X (epic)
- Astra Lord (legendary)

The system automatically includes new characters in the gacha pool.

---

## ⚙️ Installation

1. Clone the repository
2. Install dependencies:
   - discord.py
   - python-dotenv
3. Create a `.env` file:
   ```
   DISCORD_TOKEN=YOUR_TOKEN_HERE
   ```
4. Run the bot

---

## 💾 Data Storage

- Each user has:
  - Coins
  - Inventory
- All data is saved automatically in `data.json`
- No progress is lost when restarting the bot

---

## 🚀 Expansion Ideas

- 📦 Special packs
- 🎁 Daily rewards system
- 🧬 Character evolution
- 🏆 Global ranking
- 🔁 Player trading
- 🎨 Skins or character variants

---

## 📜 License

Free to use, study, and modify.

If you use this project as a base, credit is always appreciated 💙

---

## 🌠 AstraGacha

> *A simple gacha bot, infinite possibilities.*

