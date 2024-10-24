import azure.functions as func
import logging
from openai import OpenAI
from PIL import Image
import io
import base64

secret_key = "

image_bp = func.Blueprint()

@image_bp.route(route="generate_image", auth_level=func.AuthLevel.ANONYMOUS)
def image(req: func.HttpRequest) -> func.HttpResponse:
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

    prompt = req_body.get('prompt')
    if not prompt:
        return func.HttpResponse(
            "Please pass a text prompt in the request body",
            status_code=400
        )

    try:
        # Generate an image based on the text prompt using the OpenAI API
        response = client.images.generate(
            model="dall-e-3",
            prompt= prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        

        # Download the image from the URL
        image_url = response.data[0].url

        logging.info("Image generated successfully")
    except Exception as e:
        logging.error(f"Error generating image: {str(e)}", exc_info=True)
        return func.HttpResponse(
            f"Error generating image: {str(e)}",
            status_code=500
        )

    return func.HttpResponse(image_url, status_code=200)