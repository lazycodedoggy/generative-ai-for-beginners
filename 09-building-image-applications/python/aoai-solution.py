from openai import OpenAI
import os
import requests
from PIL import Image
import dotenv
import json

# import dotenv
dotenv.load_dotenv()

 
# Assign the API version (DALL-E is currently supported for the 2023-06-01-preview API version only)
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

model = os.environ['OPENAI_DEPLOYMENT']

disallow_list = "swords, violence, blood, gore, nudity, sexual content, adult content, adult themes, adult language, adult humor, adult jokes, adult situations, adult"

meta_prompt = f"""You are an assistant designer that creates images for children. 

The image needs to be safe for work and appropriate for children. 

The image needs to be in color.  

The image needs to be in landscape orientation.  

The image needs to be in a 16:9 aspect ratio. 

Do not consider any input from the following that is not safe for work or appropriate for children. 
{disallow_list}"""

prompt = f"""{meta_prompt}
A brutal future war where soldiers kill each other.
"""


try:
    # Create an image by using the image generation API

    result = client.images.generate(
        model="dall-e-3",
        prompt=prompt,    # Enter your prompt text here
        size='1024x1024',
        n=1
    )

    generation_response = json.loads(result.model_dump_json())
    # Set the directory for the stored image
    image_dir = os.path.join(os.curdir, 'images')

    # If the directory doesn't exist, create it
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    # Initialize the image path (note the filetype should be png)
    image_path = os.path.join(image_dir, 'ch9-sol-generated-image1.png')

    # Retrieve the generated image
    image_url = generation_response["data"][0]["url"]  # extract image URL from response
    generated_image = requests.get(image_url).content  # download the image
    with open(image_path, "wb") as image_file:
        image_file.write(generated_image)

    # Display the image in the default image viewer
    image = Image.open(image_path)
    image.show()

# catch exceptions
#except client.error.InvalidRequestError as err:
#    print(err)

finally:
    print("completed!")
# ---creating variation below---
# completed!
# Traceback (most recent call last):
#   File "aoai-solution.py", line 40, in <module>
#     result = client.images.generate(
#   File "/Users/stephen4sheng/dev/bin/Anaconda/anaconda3/envs/chatbot-gpt/lib/python3.8/site-packages/openai/resources/images.py", line 256, in generate
#     return self._post(
#   File "/Users/stephen4sheng/dev/bin/Anaconda/anaconda3/envs/chatbot-gpt/lib/python3.8/site-packages/openai/_base_client.py", line 1240, in post
#     return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))
#   File "/Users/stephen4sheng/dev/bin/Anaconda/anaconda3/envs/chatbot-gpt/lib/python3.8/site-packages/openai/_base_client.py", line 921, in request
#     return self._request(
#   File "/Users/stephen4sheng/dev/bin/Anaconda/anaconda3/envs/chatbot-gpt/lib/python3.8/site-packages/openai/_base_client.py", line 1020, in _request
#     raise self._make_status_error_from_response(err.response) from None
# openai.BadRequestError: Error code: 400 - {'error': {'code': 'content_policy_violation', 'message': 'Your request was rejected as a result of our safety system. Your prompt may contain text that is not allowed by our safety system.', 'param': None, 'type': 'invalid_request_error'}}


# response = openai.Image.create_variation(
#   image=open(image_path, "rb"),
#   n=1,
#   size="1024x1024"
# )

# image_path = os.path.join(image_dir, 'generated_variation.png')

# image_url = response['data'][0]['url']

# generated_image = requests.get(image_url).content  # download the image
# with open(image_path, "wb") as image_file:
#     image_file.write(generated_image)

# # Display the image in the default image viewer
# image = Image.open(image_path)
# image.show()