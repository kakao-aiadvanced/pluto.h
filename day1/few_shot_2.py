from openai import OpenAI
client = OpenAI()

system_prompt = """Movie Review Sentiment Analysis Prompt

#### Instructions:
- Determine if the sentiment expressed in the movie review is **positive** or **negative**.
- Base your decision on the overall tone and words used in the review.

#### Examples:
1. **The acting was superb and the plot kept me on the edge of my seat.** - Positive
2. **I found the movie to be a complete waste of time.** - Negative
3. **The visuals were stunning, but the story fell short.** - Mixed (for this example, consider it Negative if you must choose one)
4. **A heartwarming tale that left me in tears.** - Positive
5. **The characters were flat and the direction lacked creativity.** - Negative
"""

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {
            "role": "user", 
            "content": "The storyline was dull and uninspiring."
        }
    ]
)

response = completion.choices[0].message.content
print(response)
