import json
from pathlib import Path

from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)


def chackpoint2pipeline(checkpoint_path):
    checkpoint_path = Path(checkpoint_path)
    pipe = pipeline("text-generation", model=checkpoint_path)
    with open(checkpoint_path / "custom_generation_config.json", "r") as file:
        custom_generation_config = json.load(file)
    return lambda prompts: pipe(prompts, **custom_generation_config)


model2path = {
    "VOLK": "./checkpoints/rugpt3large_volk_epochs-20",
    "PUSHKIN": "./checkpoints/rugpt3large_pushkin_epochs-30"
}
generator_pipeline = chackpoint2pipeline(model2path["VOLK"])


@app.route("/", methods=["GET", "POST"])
def simple_response():
    return "Text Generator"

@app.route("/change_model", methods=["POST"])
def change_model():
    request_data = request.get_json()
    checkpoint_path = model2path[request_data["bot"]]
    global generator_pipeline
    generator_pipeline = chackpoint2pipeline(checkpoint_path)

@app.route("/generate", methods=["POST"])
def generate():
    request_data = request.get_json()
    output = generator_pipeline(request_data["prompts"])
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)