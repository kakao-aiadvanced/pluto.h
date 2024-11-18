from openai import OpenAI
client = OpenAI()

system_prompt = """Solve the following logic puzzle step-by-step:

Four people (A, B, C, D) are sitting in a row. We know that:
1. A is not next to B.
2. B is next to C.
3. C is not next to D.

Determine the possible seating arrangements.
"""

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {
            "role": "user", 
            "content": "What is answer?"
        }
    ]
)

response = completion.choices[0].message.content
print(response)
