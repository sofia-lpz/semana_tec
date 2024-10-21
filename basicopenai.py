from openai import OpenAI

secret_key = ""

client = OpenAI(
    api_key=secret_key,
)

completion = client.Completion.create(
    model ="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    max_tokens=100
    temperature=0.5
)

print(completion)