import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
# from llama_index.multi_modal_llms.gemini import GeminiMultiModal
import os
from dotenv import load_dotenv
# from llama_index.core import SimpleDirectoryReader


load_dotenv()

os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

base_prompt = """

The provided is a generic expense day-to-day receipt, please extract the fields listed and respond in JSON format:

Write "" into the unrecognizable field if necessary

Reponse Format:
{
  "date_of_spending": <extraction>,
  "location_of_spending": <extraction>,
  "spending_company": <extraction>,
  "dollar_spent": <extraction>
  "items_or_service_bought": <extraction>

}

"""

# gemini_pro = GeminiMultiModal(model_name="models/gemini-pro-vision")

def generate(image_data, file_type, prompt = base_prompt):
  # reader = SimpleDirectoryReader(
  #   input_files = [file_path]
  #   # input_dir="/Users/Caius.Chun/BOC_Competition/vertex_ai_gemini/sample/3BQ8250CF74DCEE80C7565lv.jpg"
  #   )
  # documents = reader.load_data()
  vertexai.init(project="instant-form-426202-b1", location="us-central1")
  model = GenerativeModel(
    "gemini-1.5-flash-001",
  )
  image1 = Part.from_data(
    mime_type= file_type,
    data=image_data)

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
  # complete_response = gemini_pro.complete(

  #   prompt=prompt,
    
  #   image_documents=[documents[0]],

  # )
  # return complete_response
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

