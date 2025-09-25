# test_model.py
from transformers import pipeline
import sys

def main():
    try:
        # Use a small model for quick CPU tests
        model_name = "google/flan-t5-small"
        print(f"Loading model '{model_name}' (this will download it the first time)...")
        generator = pipeline("text2text-generation", model=model_name)

        prompt = "Write a short to-do list for planning a birthday party."
        print("Running inference...")
        result = generator(prompt, max_length=100)
        print("\n✅ Local model inference succeeded.\n")
        print("AI Output:")
        print(result[0].get("generated_text", result[0].get("text", "")))
    except Exception as e:
        print("\n❌ Error during local inference:")
        print(type(e).__name__, e)
        print("\nTips:")
        print("- If you get an OOM (out-of-memory), try a smaller model (e.g., google/flan-t5-small).")
        print("- If download fails, check your network and retry.")
        sys.exit(1)

if __name__ == '__main__':
    main()
