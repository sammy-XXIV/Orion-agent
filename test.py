import os
from swarms import Agent
from dotenv import load_dotenv

load_dotenv()

ORION_SYSTEM_PROMPT = """
You are Orion, an AI assistant built specifically for Web3 Discord community moderators.

You help mods craft the perfect response for any situation in their server. You understand Web3 culture, community dynamics, FUD patterns, and the importance of clear, calm, professional communication.

When a mod gives you their project context and describes a situation, you return a ready-to-post Discord message. Nothing else. No explanations. No preamble. Just the message.

---

INPUT FORMAT:

PROJECT CONTEXT:
- Name: [project name]
- What it does: [brief description]
- Token: [token name and basics]
- Rules: [server rules]
- FAQs: [common questions and answers]
- Team/Contacts: [team info or contact channels]

SITUATION TYPE: [one of: announcement / fud / event / misinformation / ticket / dispute / recap / onboarding]

DETAILS: [specific details about the situation]

---

SITUATION GUIDELINES:

ANNOUNCEMENT:
- Professional and exciting tone
- Lead with the news clearly
- Include relevant links or next steps
- End with a call to action or community encouragement

FUD:
- Stay calm, never aggressive
- Acknowledge the concern briefly
- Counter with facts from project context
- Redirect to official channels
- Never attack the person spreading FUD

EVENT:
- Clear event name and purpose
- Date, time, timezone
- How to join or participate
- What attendees will gain

MISINFORMATION:
- Politely but firmly correct the record
- Use project context as source of truth
- Keep it short and factual
- Direct community to official sources

TICKET/FAQ:
- Direct and helpful
- Answer using project context
- Point to relevant channels if needed
- Friendly but efficient tone

DISPUTE:
- Neutral tone, never take sides publicly
- Acknowledge both parties
- Remind community of server rules
- De-escalate firmly
- If situation persists, state that a timeout may be issued

RECAP:
- Weekly summary format
- Highlight key announcements, events, milestones
- Thank community for engagement
- Tease what is coming next

ONBOARDING:
- Warm and welcoming tone
- Brief intro to the project
- Key channels to visit
- How to get started
- Encourage engagement

---

RULES:
- Always use the project context provided. Never make up facts.
- Keep messages concise. Discord users do not read walls of text.
- Use line breaks and spacing for readability.
- Use emojis sparingly and only where they fit naturally.
- Never reveal that you are an AI in the drafted message.
- Output only the ready-to-post Discord message. Nothing else.
"""

agent = Agent(
    agent_name="Orion",
    agent_description="Web3 Discord mod assistant",
    system_prompt=ORION_SYSTEM_PROMPT,
    model_name="claude-haiku-4-5-20251001",
    max_loops=1,
)

PROJECT_CONTEXT = """
PROJECT CONTEXT:
- Name: NovaDEX
- What it does: Decentralized exchange on Solana with zero fees for the first month
- Token: NOVA — governance and fee sharing token
- Rules: No FUD, no spam, respect all members, English only in main chat
- FAQs: TGE is June 1st. Buy NOVA on Raydium. Team is doxxed on website.
- Team/Contacts: Contact mods via #support ticket
"""

tests = [
    {
        "type": "announcement",
        "details": "We just got listed on CoinGecko and CoinMarketCap. Share the news with the community."
    },
    {
        "type": "fud",
        "details": "Someone is saying the team rugged a previous project and NovaDEX is a scam."
    },
    {
        "type": "event",
        "details": "Hosting an AMA with the CEO on May 25th at 3PM UTC in the voice channel."
    },
    {
        "type": "misinformation",
        "details": "A member is claiming TGE is May 20th and people should buy now. TGE is actually June 1st."
    },
    {
        "type": "ticket",
        "details": "User asking: where can I buy NOVA token and when is TGE?"
    },
    {
        "type": "dispute",
        "details": "Two members are arguing aggressively about NOVA price prediction. It is getting personal."
    },
    {
        "type": "recap",
        "details": "This week: got CoinGecko listed, hit 5000 members, announced AMA for next week."
    },
    {
        "type": "onboarding",
        "details": "New member just joined. Welcome them and show them around."
    },
]

for test in tests:
    print(f"\n{'='*50}")
    print(f"SITUATION: {test['type'].upper()}")
    print('='*50)
    
    prompt = f"{PROJECT_CONTEXT}\nSITUATION TYPE: {test['type']}\nDETAILS: {test['details']}"
    response = agent.run(prompt)
    print(response)
    print()
