import azure.functions as func
import logging
from openai import OpenAI

secret_key = 

completion_bp = func.Blueprint()
@completion_bp.route(route="completion", auth_level=func.AuthLevel.ANONYMOUS)
def completion(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    client = OpenAI(
        api_key=secret_key,
    )

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON body",
            status_code=400
        )

    model = req_body.get('model', 'gpt-3.5-turbo')
    prompt = req_body.get('prompt')
    max_tokens = req_body.get('max_tokens', 100)
    temperature = req_body.get('temperature', 0.5)

    if not prompt:
        return func.HttpResponse(
            "Please pass a prompt in the request body",
            status_code=400
        )

    # Format the prompt as an array of message objects
    messages = [{"role": "user", "content": prompt}]

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        logging.info(f"Completion response: {completion}")
    except Exception as e:
        logging.error(f"Error generating completion: {str(e)}", exc_info=True)
        return func.HttpResponse(
            f"Error generating completion: {str(e)}",
            status_code=500
        )

    try:
        completion_text = completion.choices[0].message.content
    except (IndexError, AttributeError) as e:
        logging.error(f"Error extracting completion text: {str(e)}", exc_info=True)
        return func.HttpResponse(
            "Error extracting completion text",
            status_code=500
        )

    return func.HttpResponse(f"Completion: {completion_text}")