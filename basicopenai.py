from openai import OpenAI

secret_key = 

prompt = "What is the capital of the United States?"

client = OpenAI(
    api_key=secret_key,
)

completion = client.completions.create(
    model="gpt-4o",
    prompt=prompt,
    max_tokens=100,
    temperature=0.5
)

print(completion)