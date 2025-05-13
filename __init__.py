import os
import json
import azure.functions as func
from openai import AzureOpenAI

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        user_prompt = req_body.get('user')

        client = AzureOpenAI(
            api_key = os.environ["AZURE_OPENAI_API_KEY"],
            azure_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"],
            api_version = "2024-10-21"
        )

        messages = [
            {"role": "system", "content": "Eres un asistente legal multilingüe experto en contratos. Responde de forma profesional."},
            {"role": "user", "content": user_prompt}
        ]

        response = client.chat.completions.create(
            model=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
            messages=messages
        )

        return func.HttpResponse(
            json.dumps({"assistant_response": response.choices[0].message.content}),
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)


