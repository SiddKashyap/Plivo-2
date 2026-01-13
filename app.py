import os
import requests
import replicate
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
TRIGGER_WORD = os.environ.get("TRIGGER_WORD", "TOK")
MODEL_VERSION = os.environ.get("MODEL_VERSION")

# Initialize Slack App
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

def generate_image(prompt):
    """
    Calls the Replicate API with the Flux LoRA model.
    """
    # Inject trigger word for identity consistency
    full_prompt = f"A photo of {TRIGGER_WORD} person, {prompt}, realistic, high quality, 4k, film grain"
    
    print(f"Generating: {full_prompt}")
    
    output = replicate.run(
        MODEL_VERSION,
        input={
            "prompt": full_prompt,
            "num_inference_steps": 28,
            "guidance_scale": 3.5,
            "output_quality": 90,
        }
    )
    # Return the first image URL in the list
    return output[0] if isinstance(output, list) else output

@app.event("app_mention")
def handle_mention(event, say, client):
    """
    Event listener for @mentions.
    1. Acknowledge receipt.
    2. Generate Image.
    3. Upload Image to Slack.
    """
    channel_id = event['channel']
    user_id = event['user']
    thread_ts = event.get('thread_ts', event['ts'])
    
    # Clean the prompt (remove the @mention)
    user_prompt = event['text'].replace(f"<@{user_id}>", "").strip()

    if not user_prompt:
        say("Please provide a description! Example: '@InspireBot me as a pilot'", thread_ts=thread_ts)
        return

    # 1. Acknowledge
    say(f" *Traveling down memory lane...* \nGenerating: _{user_prompt}_", thread_ts=thread_ts)

    try:
        # 2. Generate
        image_url = generate_image(user_prompt)
        
        # 3. Download & Upload
        img_data = requests.get(image_url).content
        
        client.files_upload_v2(
            channel=channel_id,
            thread_ts=thread_ts,
            title=user_prompt,
            file=img_data,
            filename=f"memory_{user_id}.png",
            initial_comment=f"Here is your memory: *{user_prompt}* "
        )

    except Exception as e:
        error_msg = f" Failed to generate memory. Error: {str(e)}"
        print(error_msg)
        say(error_msg, thread_ts=thread_ts)

if __name__ == "__main__":
    print(f" InspireBot is running with Trigger Word: '{TRIGGER_WORD}'")
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
