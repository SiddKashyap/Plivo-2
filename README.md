# InspireWorks "Down Memory Lane" Bot 

## Overview
This project is a Forward Deployed Engineering prototype for **InspireWorks**. It is an AI-powered Slack bot designed to generate imaginative childhood photos for storytelling and memory sharing.

The solution integrates **Slack's Socket Mode** for secure, real-time communication with **Replicate's Flux LoRA** models to generate high-fidelity, identity-consistent images based on user prompts.

## Features
- **Slack Integration**: Uses Slack Bolt SDK with Socket Mode (no firewall changes required).
- **Generative AI**: Utilizes the Flux Dev model with Low-Rank Adaptation (LoRA) for facial consistency.
- **Thread-Aware**: Maintains context by replying directly in message threads.
- **Secure Handling**: Ephemeral image processing; images are uploaded directly to Slack's file servers.

## Architecture
1. **User Input**: User mentions `@InspireBot` in Slack (e.g., "Me as a 5-year-old pilot").
2. **Event Processing**: Slack Bolt receives the event via WebSocket.
3. **Prompt Engineering**: The application injects a trained `TRIGGER_WORD` into the prompt to ensure the generated image matches the trained subject.
4. **Inference**: Request sent to Replicate API (Flux LoRA).
5. **Delivery**: Image is downloaded to memory and uploaded back to the specific Slack thread.

## Prerequisites
- Python 3.8+
- A generic Flux LoRA model trained on Replicate (or use `ostris/flux-dev-lora-trainer`).
- A Slack App with `app_mentions:read`, `chat:write`, and `files:write` permissions.

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/inspire-works-bot.git
   cd inspire-works-bot

   python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env

python bot.py

@InspireBot me as a 10 year old astronaut in a garden

---

### 2. `.gitignore`
*Create a file named `.gitignore`. This is CRITICAL. It ensures you do not accidentally upload your API keys to GitHub.*

```text
# Python
__pycache__/
*.py[cod]
*$py.class
venv/
env/

# Environment Variables (NEVER COMMIT THESE)
.env
