import os
import json
import subprocess
import sys


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def ask(prompt, required=True, default=None):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        if not required:
            return default
        print("  This field is required.\n")


def ask_int(prompt, default):
    value = ask(prompt, required=False, default=None)
    if value and value.isdigit():
        return int(value)
    return default


def divider():
    print("-" * 56)


def header(step, title):
    print()
    print(f"  Step {step}: {title}")
    divider()


def main():
    clear()
    print()
    print("=" * 56)
    print("          Welcome to Orion Setup")
    print("  Configure Orion for your Web3 Discord server.")
    print("=" * 56)

    # Step 1: Install dependencies
    header(1, "Installing dependencies")
    print("  Installing required packages...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"]
    )
    print("  Done.\n")

    # Step 2: API Keys
    header(2, "API Keys")
    print("  You need 3 keys to run Orion:\n")
    print("  - Discord Bot Token  →  discord.com/developers/applications")
    print("  - Anthropic API Key  →  console.anthropic.com")
    print("  - Swarms API Key     →  swarms.world\n")

    discord_token = ask("  Discord Bot Token: ")
    anthropic_key = ask("  Anthropic API Key: ")
    swarms_key = ask("  Swarms API Key: ")

    with open(".env", "w") as f:
        f.write(f"DISCORD_BOT_TOKEN={discord_token}\n")
        f.write(f"ANTHROPIC_API_KEY={anthropic_key}\n")
        f.write(f"SWARMS_API_KEY={swarms_key}\n")

    print("\n  Keys saved to .env\n")

    # Step 3: Project context
    header(3, "Your Project Context")
    print("  Orion uses this to generate accurate, on-brand responses.\n")

    project_name = ask("  Project name: ")
    description = ask("  What does your project do? (1-2 sentences): ")
    token_info = ask("  Token name and details (e.g. NOVA — governance and fee sharing): ")
    rules = ask("  Server rules (e.g. No FUD, no spam, English only): ")
    faqs = ask("  FAQs (e.g. TGE date, where to buy, how to get support): ")
    team_contacts = ask("  Team/contact info (e.g. open a ticket in #support): ")

    print("\n  Project context saved.\n")

    # Step 4: Channel settings
    header(4, "Channel Settings")
    print("  Leave blank to monitor ALL channels.")
    print("  To monitor specific channels, enter their IDs separated by commas.")
    print("  (Right-click a channel in Discord > Copy Channel ID)\n")

    channels_input = ask("  Channel IDs to monitor (or leave blank for all): ", required=False, default="")
    monitored = []
    if channels_input:
        monitored = [
            int(c.strip())
            for c in channels_input.split(",")
            if c.strip().isdigit()
        ]

    cooldown = ask_int(
        "  Cooldown between responses per channel in seconds (default 60): ",
        default=60,
    )

    config = {
        "project_name": project_name,
        "description": description,
        "token_info": token_info,
        "rules": rules,
        "faqs": faqs,
        "team_contacts": team_contacts,
        "monitored_channels": monitored,
        "response_cooldown_seconds": cooldown,
    }

    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)

    # Done
    print()
    print("=" * 56)
    print("  Orion is ready!")
    print("=" * 56)
    print()
    print("  To start Orion anytime, run:")
    print("    python bot.py")
    print()

    start_now = ask("  Start Orion now? (yes/no): ", required=False, default="no")
    if start_now.lower() in ("yes", "y"):
        print("\n  Starting Orion...\n")
        os.execv(sys.executable, [sys.executable, "bot.py"])
    else:
        print("\n  Setup complete. Run 'python bot.py' whenever you're ready.\n")


if __name__ == "__main__":
    main()
