import discord
import json
import re
import os
import time
from swarms import Agent
from dotenv import load_dotenv
from agent import ORION_SYSTEM_PROMPT

load_dotenv()

with open("config.json") as f:
    config = json.load(f)

CLASSIFIER_PROMPT = """You are a Discord message analyzer for Web3 communities.

Analyze the incoming Discord message and determine if it requires a response from a moderation AI agent.

Return ONLY a raw JSON object with no markdown, no code blocks, no extra text:
{"needs_response": true/false, "situation_type": "fud|dispute|misinformation|ticket|announcement|event|recap|onboarding|null", "details": "brief description of what is happening"}

Flag messages for response when:
- Someone is spreading FUD or calling the project a scam (fud)
- Members are arguing aggressively or personally attacking each other (dispute)
- Someone is sharing incorrect information about the project (misinformation)
- Someone is asking a question answerable from project FAQs (ticket)
- A mod is sharing major news or a milestone (announcement)
- An event needs to be promoted to the community (event)
- A weekly summary of activity is needed (recap)
- A new member just joined or introduced themselves (onboarding)

Return needs_response: false for normal conversation, price speculation, memes, or off-topic messages that do not require moderation."""


def build_project_context():
    return f"""PROJECT CONTEXT:
- Name: {config["project_name"]}
- What it does: {config["description"]}
- Token: {config["token_info"]}
- Rules: {config["rules"]}
- FAQs: {config["faqs"]}
- Team/Contacts: {config["team_contacts"]}"""


classifier = Agent(
    agent_name="Classifier",
    system_prompt=CLASSIFIER_PROMPT,
    model_name="claude-haiku-4-5-20251001",
    max_loops=1,
)

orion = Agent(
    agent_name="Orion",
    agent_description="Web3 Discord mod agent that drafts perfect responses for any community situation",
    system_prompt=ORION_SYSTEM_PROMPT,
    model_name="claude-haiku-4-5-20251001",
    max_loops=1,
)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

channel_last_response = {}


@client.event
async def on_ready():
    print(f"Orion is online as {client.user}")


@client.event
async def on_message(message):
    if message.author.bot:
        return

    monitored = config.get("monitored_channels", [])
    if monitored and message.channel.id not in monitored:
        return

    cooldown = config.get("response_cooldown_seconds", 60)
    now = time.time()
    if now - channel_last_response.get(message.channel.id, 0) < cooldown:
        return

    classification_raw = classifier.run(message.content)

    try:
        match = re.search(r"\{.*\}", classification_raw, re.DOTALL)
        if not match:
            return
        classification = json.loads(match.group())
    except (json.JSONDecodeError, AttributeError):
        return

    if not classification.get("needs_response"):
        return

    situation_type = classification.get("situation_type")
    details = classification.get("details")

    if not situation_type or situation_type == "null":
        return

    prompt = f"""{build_project_context()}

SITUATION TYPE: {situation_type}

DETAILS: {details}"""

    response = orion.run(prompt)

    await message.channel.send(response)
    channel_last_response[message.channel.id] = time.time()


client.run(os.getenv("DISCORD_BOT_TOKEN"))
