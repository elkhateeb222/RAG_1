from zai import ZaiClient
from settings import get_settings
from ..prompts.system_prompt import SYSTEM_PROMPT
from ..BaseProvider import BaseProvider


class GLMProvider(BaseProvider):
    def __init__(self,api_key:str,model_id:str):
        self.settings=get_settings()
        self.prompt = SYSTEM_PROMPT
        self.api_key= api_key
        self.model_id=model_id

    def generate_text(self,retrieved_chunk:str,user_query:str):
        

        
        client = ZaiClient(api_key=self.api_key)

        # Create chat completion request
        response = client.chat.completions.create(
            model=self.model_id,
            messages=[
                {
                    "role": "system",
                    "content": self.prompt
                },
                {
                    "role": "user",
                    "content": self.construct_prompt(retrieved_chunk=retrieved_chunk,user_query=user_query)
                }
            ]
        )

        # Get response
        print(response.choices[0].message.content)
                




