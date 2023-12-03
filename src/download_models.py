from pathlib import Path

from transformers import AutoModelForCausalLM, AutoTokenizer

if __name__ == "__main__":
    save_dir = Path("checkpoints")
    for model_name in ["logiczmaksimka/rugpt3large_volk_epochs-3"]:
        model = AutoModelForCausalLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        save_path = save_dir / model_name.split("/")[-1]
        model.save_pretrained(save_path)
        tokenizer.save_pretrained(save_path)