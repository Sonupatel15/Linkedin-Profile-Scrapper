import os
import logging
import ollama

# === Logging Setup ===
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def summarize_profile(profile_data: dict) -> str:
    """
    Summarize a LinkedIn-style profile using a local LLaMA3 model via Ollama.

    Args:
        profile_data (dict): A dictionary of profile fields (name, company, skills, etc.)

    Returns:
        str: A natural language summary of the profile, or an error message.
    """
    if not profile_data:
        logger.warning("No profile data provided for summarization.")
        return "No profile data available to summarize."

    # Convert the dict to a human-readable text block
    text_parts = []
    for key, value in profile_data.items():
        if value:
            text_parts.append(f"{key.replace('_', ' ').title()}: {value}")

    full_text = "\n".join(text_parts)

    try:
        # Call the local Ollama model
        response = ollama.chat(
            model="llama3",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes LinkedIn profiles."
                },
                {
                    "role": "user",
                    "content": f"Summarize this LinkedIn profile:\n\n{full_text}"
                }
            ]
        )

        summary = response["message"]["content"].strip()
        logger.info("Profile summarized successfully.")
        return summary

    except Exception as e:
        logger.exception(f"Failed to summarize profile: {e}")
        return f"⚠️ Summarization failed: {e}"
