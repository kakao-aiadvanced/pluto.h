from openai import OpenAI
client = OpenAI()

system_prompt = """English to Korean Translation:

#### Instructions:
- Translate each English word or phrase into Korean.
- Provide the English word followed by its Korean translation.
- Ensure the translations are accurate and commonly used in Korean.

#### Examples:
1. Hello - 안녕하세요
2. Goodbye - 안녕히 가세요
3. Thank you - 감사합니다
4. Car - 자동차
5. Apple - 사과
"""

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {
            "role": "user", 
            "content": "dog"
        }
    ]
)

response = completion.choices[0].message.content
print(response)
