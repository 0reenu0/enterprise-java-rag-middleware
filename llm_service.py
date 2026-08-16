import os
from dotenv import load_dotenv
from openai import OpenAI
from schemas import TextAnalysisResponse

load_dotenv()

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPEAI_API_KEY"))

    def parse_unstructured_text(self, text: str) -> TextAnalysisResponse:
        """
        Sends raw text to OpenAI and forces the response into a 
        validated TextAnalysisResponse Pydantic instance.
        """
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an enterprise data extractor. Analyze input text and extract structured metrics."
                },
                {"role": "user", "content": text},
            ],
            response_format=TextAnalysisResponse, # Constrained decoding enforcer
        )
        return completion.choices[0].message.parsed