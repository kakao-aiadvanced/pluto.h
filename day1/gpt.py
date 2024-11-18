from openai import OpenAI
client = OpenAI()

system_prompt = """
You are an AI that informs you of the security testing of the target entered by the user. Please make the results step by step.
"""

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {
            "role": "user", 
            "content": "RF Devices"
        }
    ]
)

response = completion.choices[0].message.content
print(response)