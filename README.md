# 🦆 Discord AI Selfbot - Rug Duckz Edition

A Discord selfbot featuring **Darkwing**, an ex-con lead developer with a toxic gamer personality. Built for the Rug Duckz NFT racing game project on Solana.

## ⚠️ Disclaimer

**This project is for educational purposes only.** Using selfbots is against Discord's Terms of Service and can result in account termination. Use at your own risk.

## ✨ Features

-   **AI-Powered Characters**: Default Darkwing setup, easily customizable to any Rug Duckz character
-   **Multiple AI Providers**: Supports Groq, OpenAI, and Anthropic Claude (optimized for Claude)
-   **Human-Like Responses**: Varies between short quips, medium responses, and long rants
-   **Anti-Detection**: No markdown formatting, realistic typing, randomized timing
-   **Project Integration**: Built-in knowledge of Rug Duckz NFT racing game
-   **Smart Triggers**: Responds to: darkwing, mint, solana, woke, trump, dev, code, coding
-   **Owner Commands**: Full control via separate owner account

## 🎮 Default Character: Darkwing

**Current Setup**: Ex-con lead developer of Rug Duckz, toxic anti-woke gamer, satirically over-the-top but self-aware

**Response Style**:
- 60% SHORT responses ("quack", "based", "skill issue")
- 30% MEDIUM responses (1-2 sentences)
- 10% LONG rants (when triggered)
- Says "quack" frequently, acts busy coding

**Easily Customizable**: Can be changed to any Rug Duckz character (Speedwing, Techquack, Rugmaster, etc.) - see customization section below!

## 🚀 Quick Start

### Prerequisites

-   Python 3.8 or higher
-   Discord account for selfbot
-   Separate Discord account for owner commands
-   API key (Anthropic Claude recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/cybernetix3d/Discord-AI-Selfbot.git
   cd Discord-AI-Selfbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run setup and configure**
   ```bash
   python main.py
   ```

4. **Important Setup Notes**:
   - Set your **main account ID** as owner (NOT the selfbot account)
   - Use trigger words: `darkwing, mint, solana, woke, trump, dev, code, coding`
   - Choose Anthropic Claude for best results

## 📋 Owner Commands

Use these from your **main account** to control the selfbot:

-   `~toggleactive [channelID]` - Activate bot in current/specified channel
-   `~pause` - Pause/unpause AI responses
-   `~reload` - Reload personality and settings
-   `~ping` - Check bot latency
-   `~wipe` - Clear conversation memory
-   `~prompt [text/clear]` - View/change AI instructions
-   `~restart` - Restart the bot
-   `~shutdown` - Shut down the bot

## 🎯 Usage

1. **Activate in channel**: `~toggleactive` (from your main account)
2. **Trigger responses**: Use words like "mint", "darkwing", "woke", etc.
3. **Natural conversation**: Bot maintains context and responds in character

**Example Triggers**:
- "wen mint?" → Darkwing responds about Rug Duckz project
- "darkwing" → Bot responds as the character
- "woke nonsense" → Anti-woke rant (satirical)

## 🦆 Rug Duckz Project Integration

Darkwing knows about:
- Degenerate NFT racing game on Solana
- 3,000 Genesis Duckz NFTs
- Sabotage mechanics and $RUGZ token
- Website: rugduckz.com
- Discord: discord.gg/bsNGahmNBz
- Current status: Building, mint TBA

## 🛡️ Anti-Detection Features

-   **No Bot Formatting**: No *actions* or **bold text**
-   **Human Response Patterns**: Varies length and energy
-   **Realistic Timing**: Random delays and typing simulation
-   **Production Mode**: Reduced logging and detection risks
-   **Natural Language**: Texts like a real person, not a screenplay

## 🔧 Configuration

### Getting Discord IDs

**Enable Developer Mode:**
1. Discord Settings → Advanced → Enable Developer Mode

**Get Your User ID:**
1. Right-click on your profile → Copy User ID
2. Use this as `owner_id` (your main account, NOT the selfbot account)

**Get Channel IDs:**
1. Right-click on any channel → Copy Channel ID
2. Use with `~toggleactive [channelID]` command

**Get Server IDs:**
1. Right-click on server name → Copy Server ID
2. Add to `allowed_servers` in config to limit bot to specific servers

### Getting Your Discord Token

1. Open Discord in your browser
2. Press F12 to open Developer Tools
3. Go to the Network tab
4. Send a message in any channel
5. Look for a request to `/api/v*/messages`
6. In the request headers, find `Authorization` - this is your token

### Key Settings (config.yaml)

```yaml
bot:
  owner_id: YOUR_MAIN_ACCOUNT_ID  # Your main Discord account ID (NOT selfbot ID)
  trigger: "darkwing, mint, solana, woke, trump, dev, code, coding"
  allowed_servers: [1234567890123456789]  # Optional: limit to specific servers
  realistic_typing: true
  production_mode: true
  randomize_timing: true
  claude_model: "claude-3-5-sonnet-20241022"
```

### Getting API Keys

**Anthropic Claude (Recommended):**
- Visit: https://console.anthropic.com/
- Create account and get API key
- Best for personality consistency

**Groq (Free Option):**
- Visit: https://console.groq.com/keys
- Free tier available
- Good performance, limited requests

**OpenAI (Paid):**
- Visit: https://platform.openai.com/api-keys
- Paid service only
- High quality responses

### API Keys (.env file)

```env
DISCORD_TOKEN=your_selfbot_token
ANTHROPIC_API_KEY=your_claude_api_key
GROQ_API_KEY=your_groq_api_key  # Optional
OPENAI_API_KEY=your_openai_api_key  # Optional
```

## 💡 Tips for Best Results

1. **Use Claude API**: Best personality consistency
2. **Limit to one server**: Set `allowed_servers` in config
3. **Monitor responses**: Adjust if too aggressive/frequent
4. **Owner separation**: Always use separate account for commands
5. **Natural triggers**: Let conversations flow naturally

## 🎭 Creating Custom Duck Characters

### Quick Character Swap

The bot is designed to work with any Rug Duckz character. Here's how to customize: (ive made a few templates to copy paste into the instructions.txt and config.yaml file)

#### 1. Edit Character Identity (`config/instructions.txt`)

#### 2. Update Trigger Words (`config/config.yaml`)

#### 3. Customize Personality Traits

Edit the `PERSONALITY:` section in `instructions.txt`:

#### 4. Character-Specific Responses

**Note**: All characters maintain the same Rug Duckz project knowledge while having unique personality traits and speaking patterns.

## ⚠️ Important Notes

- **Owner ID**: Must be your main account, NOT the selfbot account
- **Detection Risk**: Use production mode and limit activity
- **Content**: Character is satirical, not genuinely hostile
- **Compliance**: Educational use only, violates Discord ToS

## 📄 License

MIT License - Educational purposes only. Users responsible for compliance with Discord ToS and applicable laws.
