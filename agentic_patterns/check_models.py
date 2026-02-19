from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq()

print("Available Groq Models:")
print("=" * 80)
models = client.models.list()
for model in models.data:
    print(f"- {model.id}")
