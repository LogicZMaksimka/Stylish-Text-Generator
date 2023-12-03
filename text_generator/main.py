from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

checkpoint_path = "../src/checkpoints/rugpt3large_volk_epochs-3"
device = "cpu"
generator = pipeline("text-generation", model=checkpoint_path)
contrastive_search_generation_config = {
    "do_sample": True,
    "top_k": 4,
    "penalty_alpha": 0.6
}


@app.route("/", methods=["GET", "POST"])
def simple_response():
    return "Text Generator"

@app.route("/generate", methods=["GET", "POST"])
def generate():
    prompts = request.get_json()["prompts"]
    output = generator(prompts, **contrastive_search_generation_config)
    return jsonify(output)

if __name__ == "__main__":
    app.run()