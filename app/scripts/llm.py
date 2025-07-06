
from llama_cpp import Llama
from scripts.utils import download_file_if_not_exists

import os


class llama_models:


        

    def prompt(self, prompt):



        
        response = self.LLM(prompt,
                                max_tokens=100,
                                temperature= 0.7,
                                top_p= 1.0,

                                stop=None)


        return response['choices'][0]['text']
    
    
    def generator_model_chooser(self):
        

        model_name = "Llama-3.2-1B-Instruct-Q5_K_S.gguf"
        model_url = "https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF/resolve/main/Llama-3.2-1B-Instruct-Q5_K_S.gguf?download=true"

        path = os.path.join(os.getcwd(), "llama_models", 'llm', model_name)
        

        download_file_if_not_exists(model_url, path)

        print(path)
        self.LLM = Llama(model_path=path)
        
        


        
