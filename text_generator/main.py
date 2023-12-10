import os
import json
from pathlib import Path

import psycopg2
from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

DEFAULT_MODEL = "VOLK"

POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
database_connection = psycopg2.connect(dbname=POSTGRES_DB,
                                       user=POSTGRES_USER, 
                                       host=POSTGRES_HOST, 
                                       port=POSTGRES_PORT, 
                                       password=POSTGRES_PASSWORD)

def checkpoint2pipeline(checkpoint_path):
    checkpoint_path = Path(checkpoint_path)
    pipe = pipeline("text-generation", model=checkpoint_path)
    with open(checkpoint_path / "custom_generation_config.json", "r") as file:
        custom_generation_config = json.load(file)
    return lambda prompts: pipe(prompts, **custom_generation_config)


model2pipleine = {
    "VOLK": checkpoint2pipeline("./checkpoints/rugpt3large_volk_epochs-20"),
    "PUSHKIN": checkpoint2pipeline("./checkpoints/rugpt3large_pushkin_epochs-30")
}

# model2pipleine = {
#     "VOLK": lambda x: [{"generated_text": "Волк"}],
#     "PUSHKIN": lambda x: [{"generated_text": "Пушкин"}]
# }


def update_user_model(user_id, username, current_model):
    with database_connection.cursor() as curs:
        curs.execute(f"""
            INSERT INTO user_table (user_id, username, current_model) 
            VALUES ({user_id}, '{username}','{current_model}')
            ON CONFLICT (user_id)
            DO UPDATE SET current_model = '{current_model}', username = '{username};'
        """)
        database_connection.commit()

def get_user_model(user_id):
     with database_connection.cursor() as curs:
        curs.execute(f"""SELECT user_id, current_model FROM user_table WHERE (user_id = '{user_id}')""")
        row = curs.fetchone()
        if row:
            return row[-1]
        else:
            return DEFAULT_MODEL


@app.route("/", methods=["GET", "POST"])
def simple_response():
    return "Text Generator"

@app.route("/change_model", methods=["POST"])
def change_model():
    request_data = request.get_json()
    model_name = request_data["bot"]
    user = request_data["user"]
    username = user["username"]
    user_id = user["id"]

    update_user_model(user_id, username, model_name)

    return f"Changed model to {model_name} for user {username} with id {user_id}"

@app.route("/generate", methods=["POST"])
def generate():
    request_data = request.get_json()

    # Choose the last model requested by user
    model_name = get_user_model(request_data["user"]["id"])
    generator_pipeline = model2pipleine[model_name]

    # Run generation pipeline
    output = generator_pipeline(request_data["prompts"])
    return jsonify(output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)