import json
from pathlib import Path

from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

checkpoint_path = Path("./checkpoints/rugpt3large_volk_epochs-20")
device = "cpu"
generator = pipeline("text-generation", model=checkpoint_path)

with open(checkpoint_path / "custom_generation_config.json", "r") as file:
    custom_generation_config = json.load(file)

@app.route("/", methods=["GET", "POST"])
def simple_response():
    return "Text Generator"

@app.route("/generate", methods=["GET", "POST"])
def generate():
    prompts = request.get_json()["prompts"]
    output = generator(prompts, **custom_generation_config)
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)