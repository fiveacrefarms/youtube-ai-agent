from transformers import pipeline

def generate_script():
    """
    Generate a vlog script using Hugging Face's GPT-Neo.
    """
    print("[INFO] Loading GPT-Neo model...")
    generator = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")

    prompt = (
        "Write a 5-8 minute inspiring vlog script. "
        "Use short, impactful sentences suitable for voiceovers. "
        "Divide the script into 10-20 second segments."
    )

    print("[INFO] Generating script...")
    response = generator(prompt, max_length=500, num_return_sequences=1)
    script = response[0]['generated_text']

    with open("script.txt", "w") as f:
        f.write(script)

    print("[INFO] Script generated and saved to script.txt")
    return script

if __name__ == "__main__":
    generate_script()
