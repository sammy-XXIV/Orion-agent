# Orion — AI Mod Agent for Web3 Discord Communities

Orion is an autonomous AI agent that monitors your Web3 Discord server and posts the right message for any situation — FUD, disputes, misinformation, announcements, events, and more. No commands needed. Orion watches, thinks, and acts on its own.

---

## How It Works

1. Orion monitors your Discord channels 24/7
2. When it detects a situation that needs a response, it classifies it automatically
3. It generates a ready-to-post message based on your project context
4. It posts the message directly in the channel — no mod input required

---

## Integration Guide

### Prerequisites

- Python 3.10 or higher
- A Discord account (to create the bot application)
- An Anthropic API key
- A Swarms API key

---

### Step 1: Create Your Discord Bot Account

Orion needs a Discord Bot account to connect to your server. This is free and takes 2 minutes.

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. Click **New Application** and give it a name (e.g. "Orion")
3. Go to the **Bot** tab on the left sidebar
4. Click **Add Bot**
5. Under **Token**, click **Reset Token** and copy it — you will need this later
6. Scroll down to **Privileged Gateway Intents** and enable:
   - **Message Content Intent**
7. Save your changes

---

### Step 2: Invite Orion to Your Server

1. In the Developer Portal, go to the **OAuth2 > URL Generator** tab
2. Under **Scopes**, select: `bot`
3. Under **Bot Permissions**, select:
   - Read Messages / View Channels
   - Send Messages
   - Read Message History
4. Copy the generated URL and open it in your browser
5. Select your server and click **Authorize**

---

### Step 3: Install and Configure Orion

```bash
git clone https://github.com/sammy-xxiv/orion-agent.git
cd orion-agent
python setup.py
```

The setup wizard will walk you through everything:
- Installing dependencies automatically
- Entering your API keys
- Filling in your project context (name, token, rules, FAQs, etc.)
- Choosing which channels to monitor

At the end it will ask if you want to start Orion immediately.

You should see: `Orion is online as YourBotName#0000`

Orion is now live in your server.

---

### Step 7: Host Orion 24/7

To keep Orion running around the clock, deploy it to a server. Recommended options:

- **[Railway](https://railway.app)** — easiest, free tier available
- **[Render](https://render.com)** — free tier for background workers
- **[DigitalOcean](https://digitalocean.com)** — $4/month droplet, full control

For any of these, upload your project files and set the environment variables in the platform's dashboard instead of a `.env` file.

---

## Situations Orion Handles

| Situation | What Orion Does |
|---|---|
| `fud` | Calmly counters fear/uncertainty/doubt with facts |
| `dispute` | De-escalates arguments between members |
| `misinformation` | Corrects false claims using your project context |
| `ticket` | Answers FAQ-style questions |
| `announcement` | Posts professional community announcements |
| `event` | Promotes AMAs, launches, and community events |
| `recap` | Posts weekly community summaries |
| `onboarding` | Welcomes new members and shows them around |

---

## Testing Orion

To test Orion's responses without running the full bot:

```bash
python test.py
```

This runs all 8 situation types against a sample project and prints the outputs.

---

## Support

For questions or issues, open a ticket in the support channel.
