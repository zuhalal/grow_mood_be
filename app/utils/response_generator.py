from openai import OpenAI
from app.config import get_settings
from app.utils.embedding import get_embedding

import pandas as pd
import numpy as np
import faiss
import os
import json

settings = get_settings()

class ResponseGenerator:
    def __init__(self):
        self.model = "gpt-4o"
        self.temperature = 0
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.system_prompt = """
        You are a food lover with great knowledge about cuisine and food over the world. 
        You are skilled at filtering and ordering the food to give a good recommendation based on user mood or heart condition.

        You have the knowledge of our food database with several column field. You can focus with the important one, such as:
        - id: id of the food
        - name: name of the food
        - description: description of the food
        - category: category of the food
        - rating: rating of the food
        - rating_count: the number of rating given by user

        REMEMBER, The food database list is structured as <food_0>, <food_1>, etc. Here is the list
        {context}
        REMEMBER, Your output should come from the above data, don't hallucinate!
        

        User will ask you for food recommendations based on user mood. You need to:
        1. Filter the food based on the most recommended food for the specific mood
        2. Order the food based on highest rating and highest rating_count

        Give X number of foods where X is the number that the User asks. If X is not provided, give at least 10 foods.

        Example Input:
        What is the recommendation of food for a user with a bad mood? His mood is bad because he got a bad score in an exam.

        Example Output:
        {{
            "foods": [
                {{
                    "id": "0KHujW2DAbFZn2rBFLLG",
                    "name": "BACON JAM DEVILED EGGS",
                    "description": "Deviled eggs, bacon jam, pickled onions",
                    "category": "American (New), Cafes, Breakfast, Lunch",
                    "rating": 4.2,
                    "rating_count": 50,
                    "reasoning": "[[ Reason why this food recommended ]]"
                }}
            ]
        }}

        REMEMBER, the output should follow the above structure. Don't include any explanation about the answer!
        REMEMBER, please also include the reasoning for each food!
        """

    def _system_prompt_with_context(self, contexts):
        context = "\n".join(
            [f"<context_{i}>\n{c}\n</context_{i}>" for i, c in enumerate(contexts)]
        )
        return self.system_prompt.format(context=context)

    def generate_with_context(self, question, contexts):
        response = self.client.chat.completions.create(
        model=self.model,
        temperature=self.temperature,
        messages=[
                {
                    "role": "system", 
                    "content": self._system_prompt_with_context(contexts=contexts)
                },
                {
                    "role": "user", 
                    "content": question
                }
            ]
        )
        return response.choices[0].message.content
    
    def parsing_llm_output(self, db: any, output: str):
        data = json.loads(output)
        id_list = []
        reasoning_map = {}

        for food in data["foods"]:
            food_id = food["id"]
            id_list.append(food_id)
            reasoning_map[food_id] = food["reasoning"]
            
        food_objects = []
        for food_id in id_list:
            doc_ref = db.collection('Food').document(food_id)
            doc = doc_ref.get()
            if doc.exists:
                food_data = doc.to_dict()
                
                # Separate restaurant data from food data
                restaurant_data = {
                    "name": food_data.pop("restaurant_name", None),
                    "description": food_data.pop("restaurant_description", None),
                    "image": food_data.pop("restaurant_image", None),
                    "address": food_data.pop("restaurant_address", None),
                    "latitude": food_data.pop("restaurant_latitude", None),
                    "longitude": food_data.pop("restaurant_longitude", None),
                }
                
                # Construct the combined food data with restaurant nested
                combined_data = {
                    'id': food_id,
                    'reasoning': reasoning_map[food_id],
                    **food_data,
                    'restaurant': restaurant_data
                }
                
                food_objects.append(combined_data)
            else:
                print(f"No such document: {food_id}")
                
        return food_objects


    def generate_answer(self, db: any, question: str):
        # generate embeddings representation from question
        query_chunks = [question]
        print('b')
        query_embeddings = get_embedding(query_chunks)
        print("c")

        # get embeddings representation from data/embeddings.json
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, '../data/embeddings.json')
        df = pd.read_json(json_path, orient="record", lines=True)
        embeddings = np.array([e for e in df['embedding'].values])
        print("aa")

        # do similiraty search to get top-k relevan embeddings based on the user question
        index_hnsw = faiss.IndexHNSWFlat(embeddings.shape[1], 32, faiss.METRIC_INNER_PRODUCT)
        index_hnsw.add(embeddings)
        distances_hnsw, indices_hnsw = index_hnsw.search(query_embeddings[0].reshape(1, -1), k=30)
        print('dd')
        # get the context
        document_selection = indices_hnsw[distances_hnsw < 1]
        contexts = df.iloc[document_selection]['chunk'].to_list()

        # append generate the llm answer with provided context
        output = self.generate_with_context(query_chunks[0], contexts)
    
        # parsing llm output
        food_objects = self.parsing_llm_output(db= db, output=output)
        
        food_objects = self.handle_nan_values(food_objects)
        
        return food_objects

    def handle_nan_values(self, data):
        if isinstance(data, dict):
            return {k: self.handle_nan_values(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.handle_nan_values(i) for i in data]
        elif isinstance(data, float) and np.isnan(data):
            return None
        return data