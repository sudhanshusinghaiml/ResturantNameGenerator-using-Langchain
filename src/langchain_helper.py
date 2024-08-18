import os
import openai
from langchain_openai import OpenAI
from langchain_core.runnables.base import RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.chains.sequential import SequentialChain

# Use the below codes to load the passowrd in py or ipynb files
from dotenv import load_dotenv, find_dotenv
# Checking if the .env is loaded or not - Returns True
_ = load_dotenv(find_dotenv())

client = openai.OpenAI()
client.api_key = os.getenv('OPENAI_API_KEY')


def generate_resturant_name_and_items(cuisine_name):
    llm = OpenAI(temperature=0.7)
    # Chain 1:
    prompt_template_name = PromptTemplate(
        input_variables= ["cuisine_name"],
        template= "I want to open a resturant for {cuisine_name} food. Suggest a fancy name for this."
    )

    name_chain = prompt_template_name | llm | StrOutputParser()

    # Chain 2: Generate menu items
    prompt_template_items = PromptTemplate(
        input_variables= ["resturant_name"],
        template= "Suggest some menu items for {resturant_name}. Return it as comma separated field."
    )

    food_items_chain = prompt_template_items | llm | StrOutputParser()

    # Create a sequence of these chains
    # def chain_wrapper(inputs):
    #     # First, run the name chain
    #     restaurant_name = name_chain.invoke({"cuisine_name": inputs["cuisine_name"]})
    #     
    #     # Use the restaurant name as input for the menu items chain
    #     menu_items = food_items_chain.invoke({"restaurant_name": restaurant_name})
    #     
    #     # Return both outputs
    #     return {
    #         "restaurant_name": restaurant_name,
    #         "menu_items": menu_items
    #     }

    # Create a runnable sequence to execute above wrapper
    sequential_chain = RunnableSequence(
        steps=[name_chain, food_items_chain]
    )

    chain_response = sequential_chain.invoke({"cuisine_name": cuisine_name})
    
    return chain_response


if __name__ == "__main__":
    response = generate_resturant_name_and_items("Indian")
    print("Restaurant Name:", response["restaurant_name"])
    print("Menu Items:", response["menu_items"])