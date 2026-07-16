import streamlit as st
import numpy as np
from openai import OpenAI
import json
from dotenv import load_dotenv
import os
import pickle

load_dotenv()

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

with open("results_model.json", "r", encoding="utf-8") as f:
    results = json.load(f)

def get_model_score():
    return json.dumps(results, ensure_ascii=False)

def get_explanation():
    return json.dumps({
        "dataset": "Breast Cancer Wisconsin",
        "model": results["model"],
        "metric": "Recall Macro",
        "recall": results["recall_cv"],
        "objective": "Auxiliar na classificação de tumores benignos e malignos. Destacar como é feita a previsão, tendo como base os parâmetros concave_points_mean, radius_worst, perimeter_worst, concave_points_worst",
        "classes": {
            "B": "Benigno",
            "M": "Maligno"
        },
        "obs": "O modelo é uma ferramenta de apoio à decisão e não substitui a avaliação médica."
    }, ensure_ascii=False)

def predict_diagnosys(concave_points_mean, radius_worst, perimeter_worst, concave_points_worst):
    model = pickle.load(open("model.pkl", "rb"))

    scaler = pickle.load(open("scaler.pkl", "rb"))

    patient = np.array([[
        concave_points_mean,
        radius_worst,
        perimeter_worst,
        concave_points_worst
    ]])

    patient = scaler.transform(patient)

    prediction = model.predict(patient)[0]

    return f"Diagnóstico previsto: {prediction}"  

funcoes = [
    {
        "type": "function",
        "function": {
            "name": "get_model_score",
            "description": "Retorna as métricas do modelo de classificação de câncer de mama, baseadas no treinamento do modelo.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_explanation",
            "description": "Gera explicações em linguagem natural dos diagnósticos produzidos pelos modelos.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"predict_diagnosys",
            "description":"Realiza uma previsão utilizando o modelo treinado para diagnóstico de câncer de mama. Se o resultado for 'M', é um diagnóstico maligno. Se for 'B', benigno.",
            "parameters":{
                "type":"object",
                "properties":{
                    "concave_points_mean":{"type":"number"},
                    "radius_worst":{"type":"number"},
                    "perimeter_worst":{"type":"number"},
                    "concave_points_worst":{"type":"number"}
                },
                "required":[
                    "concave_points_mean",
                    "radius_worst",
                    "perimeter_worst",
                    "concave_points_worst"
                ]
            }
        }
    }
]

available_functions = {
    "get_model_score" : get_model_score,
    "get_explanation" : get_explanation,
    "predict_diagnosys": predict_diagnosys
}

if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {
            'role' : 'system', 
            'content' : 'Você é um assistente de apoio à decisão médica especializado em interpretação de resultados de modelos de aprendizado de máquina para diagnóstico de câncer de mama. Explique os resultados utilizando linguagem clara, destacando que a decisão final deve sempre ser tomada por um médico.'}
    ]

st.title("Assistente de Diagnóstico")

user_input = st.text_input("Pergunte: ")

if user_input:
    try:
        st.session_state['messages'].append({
            'role' : 'user', 
            'content' : f'{user_input}'})

        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state['messages'],
        tools=funcoes,
        tool_choice='auto'
    )   
        response_message = response.choices[0].message


        if response_message.tool_calls:

            function_name = response_message.tool_calls[0].function.name
            function_args = json.loads(response_message.tool_calls[0].function.arguments)
            tool_call_id =  response_message.tool_calls[0].id

            function_to_call = available_functions[function_name]
            function_response = function_to_call(**function_args)
        
            st.session_state['messages'].append(response_message)
            st.session_state['messages'].append(
                {
                    'role' : 'tool',
                    "tool_call_id":tool_call_id,
                    'name' : function_name,
                    'content' : function_response
                }
            )
            second_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state['messages'],
            )
            st.text(second_response.choices[0].message.content.strip())
            st.session_state['messages'].append(
                {
                    'role' : 'assistant',
                    'content' : f'{second_response.choices[0].message.content.strip()}'
                }
            )
        else:
            st.text(response_message['content'])
            st.session_state['messages'].append(
                    {
                        'role' : 'assistant',
                        'content' : f"{response_message['content']}"
                    }
                )
    except Exception as e:
        print(e)
        st.text(str(e))