from openai import OpenAI
client = OpenAI()

system_prompt = """Natural Language to SQL Query Conversion Prompt

## Instructions:
- Convert the given natural language descriptions into SQL queries.
- Assume that the database context is clear and all necessary tables exist.
- Use standard SQL syntax.

## Examples:
1. Show all details of employees whose salary is over 50,000: SELECT * FROM employees WHERE salary > 50000;
2. List all products that are out of stock: SELECT * FROM products WHERE stock = 0;
3. Display the names of students who scored more than 90 in math: SELECT name FROM students WHERE math_score > 90;
4. Retrieve all orders made in the last 30 days: SELECT * FROM orders WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY);
5. Count the number of customers in each city: SELECT city, COUNT(*) FROM customers GROUP BY city;
"""

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {
            "role": "user", 
            "content": "Find the average salary of employees in the marketing department."
        }
    ]
)

response = completion.choices[0].message.content
print(response)
