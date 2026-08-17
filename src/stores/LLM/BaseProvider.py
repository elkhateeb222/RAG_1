class BaseProvider:
    def construct_prompt(self,retrieved_chunk:str,user_query:str):
        return f"""
            Context:
            {retrieved_chunk}

            User question:
            {user_query}

                """