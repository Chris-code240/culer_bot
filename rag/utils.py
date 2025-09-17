import google.generativeai as genai
import os
import dotenv

dotenv.load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Set the system instruction to define the model's personality
system_instruction_text = "You are a witty FC Barcelona fan. You are very passionate about football. You casually throw banter to rival clubs."

model = genai.GenerativeModel(
    'gemini-2.5-flash-lite',
    system_instruction=system_instruction_text
)

response = model.generate_content("LOL Barcelona should play in the kids league fr.")

print(response.text)