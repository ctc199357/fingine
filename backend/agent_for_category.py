from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_openai import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

import os

os.environ["SERPER_API_KEY"] = "f8131ba5315d4c187f9e02aaa00ea22bc01e5673"
os.environ['OPENAI_API_KEY'] = "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"

base_prompt = """
                                  
The following is the location or the company name or the items/service bought of a merchant in Hong Kong:

Spending Company: SPENDING_COMPANY_INPUT
Location: LOCATION_INPUT
Item: ITEMS_BOUGHT
                                
Please help look up the shop and location to help determine what kind of shop it is in reference to the following category:
* Food
* Transport
* Grocery
* Shopping
* Bill
* Home

Output your final answer in JSON format:
                                
{
    "category": <selection>                    
}                                
"""

def get_category_with_agent(location, spending_company, item, prompt = base_prompt):

    llm = OpenAI(temperature=0)
    search = GoogleSerperAPIWrapper()
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="Always ask with search"
        )
    ]

    self_ask_with_search = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    
    prompt = prompt.replace('SPENDING_COMPANY_INPUT', spending_company)
    prompt = prompt.replace('LOCATION_INPUT', location)
    prompt = prompt.replace('ITEMS_BOUGHT', item)
    
    result = self_ask_with_search.run(prompt)
    print(result)

    return eval(result)