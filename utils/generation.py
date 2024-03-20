from .constants import DALLE_RESULT_FIELD_NAME, DREAM_SHAPER_MODEL_ID, LEONARDO_RESULT_FIELD_NAME
from .resizer import reduce_size
import os

delay = int(os.environ.get("DELAY", "60"))

def download_image(image_url):
    import requests
    return requests.get(image_url).content

def convert_to_webp(image_bin):
    from io import BytesIO
    from PIL import Image
    with Image.open(BytesIO(image_bin)) as image:
        with BytesIO() as img_bytes:
            # Save the image to the BytesIO object, specifying the format if necessary
            image.save(img_bytes, format='WEBP')  # You can change 'PNG' to your desired format
            return img_bytes.getvalue()

def run_dalle(prompt):
    import os
    import time
    from openai import AzureOpenAI
    
    
    client = AzureOpenAI(
    api_version="2024-02-01",
    azure_endpoint="https://schrodinger-east-us.openai.azure.com/",
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )
    response = client.images.generate(
      model="Dalle3",
      prompt=prompt,
      n=1
    )

    return response.dict()

def run_one_sample(coll, sample_item):
    import base64
    doc = coll.find_one({'prompt': sample_item['prompt']}, {'_id': 0})
    if DALLE_RESULT_FIELD_NAME in doc:
        print("Existing: " + doc['prompt'])
        return
    dalle_result = run_dalle(sample_item['prompt'])
    url = dalle_result['data'][0]['url']
    image_bin = download_image(url)
    image_256 = reduce_size(image_bin, 4)
    result = {
        DALLE_RESULT_FIELD_NAME: dalle_result,
        'image': base64.b64encode(image_bin).decode('utf8'),
        'image256': base64.b64encode(image_256).decode('utf8'),
    }
    coll.update_one({'prompt': doc['prompt']}, {'$set': result})
    return result

def generate_one_sample(prompt):
    import base64
    print("generating image now")
    dalle_result = run_dalle(prompt)
    url = dalle_result['data'][0]['url'] if dalle_result['data'][0]['url'] else "error"
    revised_prompt = dalle_result['data'][0]['revised_prompt'] if dalle_result['data'][0]['revised_prompt'] else "error"
    if url != "error":
        image_bin = download_image(url)
        image_256 = reduce_size(image_bin, 4)
        base64Image = base64.b64encode(image_256).decode('utf8')
    else:
        base64Image = ""
    return base64Image, revised_prompt
