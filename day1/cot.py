from openai import OpenAI
client = OpenAI()

system_prompt = """
Solve the following problem step-by-step.
"""

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {
            "role": "user", 
            "content": "345 + 678 - 123"
        }
    ]
)

response = completion.choices[0].message.content
print(response)
