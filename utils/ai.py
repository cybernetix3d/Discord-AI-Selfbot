import sys
import re
import random

from groq import AsyncGroq
from openai import AsyncOpenAI as OpenAI
from anthropic import AsyncAnthropic
from os import getenv
from dotenv import load_dotenv

from utils.helpers import get_env_path, load_config
from utils.error_notifications import webhook_log, print_error

client = None
model = None


def get_random_max_tokens(prompt=""):
    """Get randomized max_tokens based on personality distribution and context"""
    # Check for trigger words that might warrant longer responses
    rant_triggers = ["woke", "mainstream", "politics", "explain", "why", "how", "what", "tell me about"]
    prompt_lower = prompt.lower()

    # Increase chance of longer response if rant triggers are present
    rant_boost = any(trigger in prompt_lower for trigger in rant_triggers)

    rand = random.random()

    if rant_boost:
        # Shift distribution toward longer responses when triggered
        if rand < 0.60:  # 60% short (reduced from 80%)
            return random.randint(15, 40)  # Slightly longer short responses
        elif rand < 0.85:  # 25% medium (increased from 15%)
            return random.randint(50, 120)  # Medium responses
        else:  # 15% long rants (increased from 5%)
            return random.randint(150, 400)  # Long rants when really triggered
    else:
        # Normal distribution for casual conversation
        if rand < 0.80:  # 80% short responses
            return random.randint(10, 30)  # Very short (1-5 words)
        elif rand < 0.95:  # 15% medium responses
            return random.randint(40, 80)  # Medium (1-2 sentences)
        else:  # 5% long rants
            return random.randint(150, 300)  # Long responses when triggered


def clean_response(response):
    """Remove markdown formatting and bot-like patterns from responses"""
    if not response:
        return response

    # Remove markdown formatting
    response = re.sub(r'\*\*([^*]+)\*\*', r'\1', response)  # Remove **bold**
    response = re.sub(r'\*([^*]+)\*', r'\1', response)      # Remove *italic*
    response = re.sub(r'_([^_]+)_', r'\1', response)        # Remove _underline_
    response = re.sub(r'`([^`]+)`', r'\1', response)        # Remove `code`
    response = re.sub(r'~~([^~]+)~~', r'\1', response)      # Remove ~~strikethrough~~

    # Remove action-like patterns
    response = re.sub(r'\*[^*]*\*', '', response)           # Remove *actions*
    response = re.sub(r'_[^_]*_', '', response)             # Remove _actions_

    # Clean up extra whitespace
    response = re.sub(r'\s+', ' ', response).strip()

    return response





def init_ai():
    global client, model
    env_path = get_env_path()
    config = load_config()

    load_dotenv(dotenv_path=env_path)

    if getenv("ANTHROPIC_API_KEY"):
        client = AsyncAnthropic(api_key=getenv("ANTHROPIC_API_KEY"))
        model = config["bot"]["claude_model"]
    elif getenv("OPENAI_API_KEY"):
        client = OpenAI(api_key=getenv("OPENAI_API_KEY"))
        model = config["bot"]["openai_model"]
    elif getenv("GROQ_API_KEY"):
        client = AsyncGroq(api_key=getenv("GROQ_API_KEY"))
        model = config["bot"]["groq_model"]
    else:
        print("No API keys found, exiting.")
        sys.exit(1)


async def generate_response(prompt, instructions, history=None):
    if not client:
        init_ai()
    try:
        # Check if using Claude (Anthropic)
        if isinstance(client, AsyncAnthropic):
            messages = []
            if history:
                messages.extend(history)
            messages.append({"role": "user", "content": prompt})

            max_tokens = get_random_max_tokens(prompt)
            response = await client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=instructions,
                messages=messages
            )
            return clean_response(response.content[0].text)
        else:
            # OpenAI/Groq format
            if history:
                response = await client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": instructions},
                        {"role": "user", "content": prompt},
                        *history,
                    ],
                )
            else:
                response = await client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": instructions},
                        {"role": "user", "content": prompt},
                    ],
                )
            return clean_response(response.choices[0].message.content)
    except Exception as e:
        print_error("AI Error", e)
        await webhook_log(None, e)
        return "Sorry, I couldn't generate a response."


async def generate_response_image(prompt, instructions, image_url, history=None):
    if not client:
        init_ai()
    try:
        # Check if using Claude (Anthropic)
        if isinstance(client, AsyncAnthropic):
            # Claude supports vision, so we can send the image directly
            messages = []
            if history:
                messages.extend(history)

            # Add the message with image
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_url  # Note: This would need to be base64 encoded data for Claude
                        }
                    }
                ]
            })

            max_tokens = get_random_max_tokens(prompt)
            response = await client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=instructions + " You can see and analyze images that are sent to you.",
                messages=messages
            )

            if history:
                history.append({"role": "assistant", "content": response.content[0].text})

            return clean_response(response.content[0].text)
        else:
            # OpenAI/Groq format - use existing logic
            image_response = await client.chat.completions.create(
                model="meta-llama/llama-4-maverick-17b-128e-instruct",  # [ ] make sure this works when user is using openai
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Describe / Explain in detail this image sent by a Discord user to an AI who will be responding to the message '{prompt}' based on your output as the AI cannot see the image. So make sure to tell the AI any key details about the image that you think are important to include in the response, especially any text on screen that the AI should be aware of.",
                            },
                            {"type": "image_url", "image_url": {"url": image_url}},
                        ],
                    }
                ],
            )

            prompt_with_image = (
                f"{prompt} [Image of {image_response.choices[0].message.content}]"
            )

            if history:
                history.append({"role": "user", "content": prompt_with_image})

                response = await client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": instructions
                            + " Images will be described to you, with the description wrapped in [|description|], so understand that you are to respond to the description as if it were an image you can see.",
                        },
                        {"role": "user", "content": prompt_with_image},
                        *history,
                    ],
                )
            else:
                history = [{"role": "user", "content": prompt_with_image}]
                response = await client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": instructions},
                        {"role": "user", "content": prompt_with_image},
                    ],
                )
            history.append(
                {"role": "assistant", "content": response.choices[0].message.content}
            )
            return clean_response(response.choices[0].message.content)
    except Exception as e:
        print_error("AI Error", e)
        await webhook_log(None, e)
        return "Sorry, I couldn't generate a response."
