import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
import os
from dotenv import load_dotenv

load_dotenv()
GDC = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
print(GDC)

base_prompt = """

The provided is a generic expense day-to-day receipt, please extract the fields listed and respond in JSON format:

Write "" into the unrecognizable field if necessary

Reponse Format:
{
  "date_of_spending": <extraction>,
  "location_of_spending": <extraction>,
  "spending_company": <extraction>,
  "dollar_spent": <extraction>

}

"""

def generate(file_path, file_type, prompt = base_prompt):
  vertexai.init(project="instant-form-426202-b1", location="us-central1")
  model = GenerativeModel(
    "gemini-1.5-flash-001",
  )
  image1 = Part.from_data(
    mime_type= f"image/{file_type}",
    data=base64.b64decode(encode_image(file_path)))

  generation_config = {
      "max_output_tokens": 500,
      "top_p": 0.95,
  }


  responses = model.generate_content(
      [image1, prompt],
      generation_config=generation_config,
      # safety_settings=safety_settings,
      stream=False,
  )

  return responses

def encode_image(path):
    with open(path, 'rb') as f:
        image_data = f.read()
    encoded_image = base64.b64encode(image_data)
    return encoded_image


def parse_markdown_json(output_string):
    output_string = output_string.replace("""```json""","")
    output_string = output_string.replace("""```""","")
    return eval(output_string)

