import azure.functions as func
import logging
from openai import OpenAI

secret_key =

client = OpenAI(
    api_key=secret_key,
)

image_bp = func.Blueprint()

@image_bp.route(route="generate_image", auth_level=func.AuthLevel.ANONYMOUS)
def generate_image(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON body",
            status_code=400
        )

    prompt = req_body.get('prompt')
    n = req_body.get('n', 1)
    size = req_body.get('size', '1024x1024')

    if not prompt:
        return func.HttpResponse(
            "Please pass a prompt in the request body",
            status_code=400
        )

    try:
        response = client.images.create(
            prompt=prompt,
            n=n,
            size=size
        )
    except Exception as e:
        return func.HttpResponse(
            f"Error generating image: {str(e)}",
            status_code=500
        )

    image_urls = [data['url'] for data in response['data']]
    return func.HttpResponse(f"Generated Image URLs: {image_urls}")
