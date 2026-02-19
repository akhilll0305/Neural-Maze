"""
Learning the Reflection Pattern - Step by Step

This script demonstrates how the reflection pattern works by building it manually.
We'll ask the LLM to write a poem, then have it critique and improve itself.
"""

import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables (your GROQ_API_KEY)
load_dotenv()

# Initialize the Groq client
client = Groq()


# ============================================================================
# STEP 1: UNDERSTANDING THE GENERATION AGENT
# ============================================================================
# The generator creates content based on user requests
# It maintains its own conversation history

print("=" * 80)
print("STEP 1: Setting up the GENERATOR")
print("=" * 80)

# This is the conversation history for the GENERATOR
# Think of it as a separate chat thread
generation_chat_history = [
    {
        "role": "system",
        "content": (
            "You are a creative poet tasked with writing beautiful poetry. "
            "If the user provides critique, respond with a revised version of your poem."
        )
    }
]

print("\n📝 Generator System Prompt:")
print(generation_chat_history[0]["content"])


# ============================================================================
# STEP 2: THE USER'S REQUEST
# ============================================================================
# What do we want the LLM to generate?

print("\n" + "=" * 80)
print("STEP 2: User makes a request")
print("=" * 80)

user_request = "Write a short poem about artificial intelligence and creativity"

# Add the user's request to the generator's chat history
generation_chat_history.append({
    "role": "user",
    "content": user_request
})

print(f"\n🙋 User Request: {user_request}")


# ============================================================================
# STEP 3: FIRST GENERATION
# ============================================================================
# The generator creates the first draft

print("\n" + "=" * 80)
print("STEP 3: Generator creates FIRST DRAFT")
print("=" * 80)

# Call the LLM to generate the first version
response = client.chat.completions.create(
    messages=generation_chat_history,
    model="llama-3.3-70b-versatile"  # Fast and powerful model from Groq
)

# Extract the generated content
first_draft = response.choices[0].message.content

# Add this to the chat history (so the generator remembers what it created)
generation_chat_history.append({
    "role": "assistant",
    "content": first_draft
})

print("\n🎨 First Draft (Generated):")
print("-" * 80)
print(first_draft)
print("-" * 80)


# ============================================================================
# STEP 4: SETTING UP THE REFLECTION AGENT (CRITIC)
# ============================================================================
# This is a SEPARATE conversation thread!
# The critic's job is to review and suggest improvements

print("\n" + "=" * 80)
print("STEP 4: Setting up the CRITIC (Reflection Agent)")
print("=" * 80)

# This is a DIFFERENT conversation history for the CRITIC
reflection_chat_history = [
    {
        "role": "system",
        "content": (
            "You are a poetry critic and expert literary analyst. "
            "Your task is to provide constructive criticism on poems. "
            "Focus on: imagery, rhythm, emotional impact, word choice, and creativity. "
            "Be specific and actionable in your feedback."
        )
    }
]

print("\n🧐 Critic System Prompt:")
print(reflection_chat_history[0]["content"])


# ============================================================================
# STEP 5: CRITIC REVIEWS THE FIRST DRAFT
# ============================================================================
# We send the generated poem to the critic

print("\n" + "=" * 80)
print("STEP 5: Critic reviews the first draft")
print("=" * 80)

# Add the generated poem as a user message to the CRITIC's chat
reflection_chat_history.append({
    "role": "user",
    "content": first_draft
})

# Get the critique from the LLM (playing the critic role)
critique_response = client.chat.completions.create(
    messages=reflection_chat_history,
    model="llama-3.3-70b-versatile"
)

critique = critique_response.choices[0].message.content

print("\n📋 Critic's Feedback:")
print("-" * 80)
print(critique)
print("-" * 80)


# ============================================================================
# STEP 6: SEND CRITIQUE BACK TO GENERATOR
# ============================================================================
# The generator receives the critique and revises

print("\n" + "=" * 80)
print("STEP 6: Generator receives critique and REVISES")
print("=" * 80)

# Add the critique to the GENERATOR's chat history (as if the user sent it)
generation_chat_history.append({
    "role": "user",
    "content": critique
})

# Generator creates a revised version
revised_response = client.chat.completions.create(
    messages=generation_chat_history,
    model="llama-3.3-70b-versatile"
)

revised_draft = revised_response.choices[0].message.content

# Add to generator's history
generation_chat_history.append({
    "role": "assistant",
    "content": revised_draft
})

print("\n✨ Revised Draft (After Reflection):")
print("-" * 80)
print(revised_draft)
print("-" * 80)


# ============================================================================
# STEP 7: THE LOOP CONTINUES...
# ============================================================================
# We can repeat steps 5-6 multiple times for iterative improvement

print("\n" + "=" * 80)
print("STEP 7: Second round of reflection")
print("=" * 80)

# Send revised draft to critic
reflection_chat_history.append({
    "role": "assistant",
    "content": critique  # Previous critique
})
reflection_chat_history.append({
    "role": "user",
    "content": revised_draft  # New draft to review
})

# Get second critique
second_critique_response = client.chat.completions.create(
    messages=reflection_chat_history,
    model="llama-3.3-70b-versatile"
)

second_critique = second_critique_response.choices[0].message.content

print("\n📋 Critic's Second Feedback:")
print("-" * 80)
print(second_critique)
print("-" * 80)

# Generator revises again
generation_chat_history.append({
    "role": "user",
    "content": second_critique
})

final_response = client.chat.completions.create(
    messages=generation_chat_history,
    model="llama-3.3-70b-versatile"
)

final_draft = final_response.choices[0].message.content

print("\n🎯 FINAL DRAFT (After 2 reflection rounds):")
print("=" * 80)
print(final_draft)
print("=" * 80)


# ============================================================================
# KEY TAKEAWAYS
# ============================================================================
print("\n" + "=" * 80)
print("🎓 KEY LEARNINGS")
print("=" * 80)
print("""
1. TWO SEPARATE CONVERSATIONS:
   - Generator has its own chat history
   - Critic has its own chat history
   
2. THE LOOP:
   - Generator creates → Critic reviews → Generator improves → Repeat
   
3. CHAT HISTORY MANAGEMENT:
   - Generator remembers: user request + all its drafts + all critiques
   - Critic remembers: all drafts it reviewed + all critiques it gave
   
4. WHY IT WORKS:
   - Different system prompts create different "mindsets"
   - Iterative refinement improves quality
   - LLM can be better at critiquing than creating on first try

5. NEXT STEP:
   - We'll wrap this logic into a reusable class!
""")
