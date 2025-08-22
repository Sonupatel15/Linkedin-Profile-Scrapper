import ollama

def summarize_profile(profile_data: dict) -> str:
    """
    Summarize profile information using local Llama3 (Ollama).
    """
    if not profile_data:
        return "No profile data available to summarize."

    # Convert dict to readable text
    text_parts = []
    for k, v in profile_data.items():
        if v:
            text_parts.append(f"{k.replace('_',' ').title()}: {v}")
    full_text = "\n".join(text_parts)

    try:
        response = ollama.chat(
            model="llama3",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes LinkedIn profiles."},
                {"role": "user", "content": f"Summarize this LinkedIn profile:\n\n{full_text}"}
            ]
        )
        return response["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ Summarization failed: {e}"
