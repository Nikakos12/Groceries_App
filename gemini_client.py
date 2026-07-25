from google import genai
import streamlit as st
from google.genai import types
from tools import TOOLS


client = genai.Client(
    api_key=st.secrets["gemini"]["api_key"]
)



def convert_parameters(parameters):

    properties = {}

    for name, parameter in parameters.items():

        properties[name] = parameter

    return {
        "type": "object",
        "properties": properties,
        "required": list(properties.keys())
    }




def build_gemini_tools():
    
    declarations = []
    
    for tool_name, tool in TOOLS.items():
        declarations.append(
            types.FunctionDeclaration(
                name = tool_name,
                description = tool['description'],
                parameters = convert_parameters(tool['parameters'])
            )
        )
    
    gemini_tool = types.Tool(
        function_declarations=declarations
    )
    
    return [gemini_tool]





def ask_gemini_with_context(question, context):

    prompt = f"""
You are a helpful grocery and nutrition assistant.

Use the following user information to answer the question.

User context:
{context}

User question:
{question}

Answer clearly and concisely.
"""

    response = client.models.generate_content(
        model=st.secrets["gemini"]["model"],
        contents=prompt
    )

    return response.text





def ask_gemini(contents):

    response = client.models.generate_content(
    model=st.secrets["gemini"]["model"],
    contents=contents,
    config=types.GenerateContentConfig(
    tools = build_gemini_tools()
)
)

    return response


