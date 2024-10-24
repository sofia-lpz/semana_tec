import azure.functions as func
import logging
from openai import OpenAI

secret_key =

client = OpenAI(
    api_key=secret_key,
)

completion_bp = func.Blueprint()

@completion_bp.route(route="completion", auth_level=func.AuthLevel.ANONYMOUS)
def completion(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON body",
            status_code=400
        )

    model = req_body.get('model', 'gpt-4o')
    prompt = req_body.get('prompt')
    max_tokens = req_body.get('max_tokens', 100)
    temperature = req_body.get('temperature', 0.5)

    if not prompt:
        return func.HttpResponse(
            "Please pass a prompt in the request body",
            status_code=400
        )

    try:
        completion = client.completions.create(
            model=model,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
    except Exception as e:
        return func.HttpResponse(
            f"Error generating completion: {str(e)}",
            status_code=500
        )

    return func.HttpResponse(f"Completion: {completion.choices[0].text}")
