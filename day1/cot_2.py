from openai import OpenAI
client = OpenAI()

system_prompt = """Solve the following logic puzzle step-by-step.

Three friends, Alice, Bob, and Carol, have different favorite colors: red, blue, and green. We know that:
1. Alice does not like red.
2. Bob does not like blue.
3. Carol likes green.

Determine the favorite color of each friend.
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
