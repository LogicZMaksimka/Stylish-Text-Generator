import os
from pathlib import Path

from huggingface_hub import snapshot_download

if __name__ == "__main__":
    save_dir = Path("./checkpoints")
    for model_name in ["logiczmaksimka/rugpt3large_volk_epochs-20", "logiczmaksimka/rugpt3large_pushkin_epochs-30"]:
        save_path = save_dir / model_name.split("/")[-1]
        if not os.path.exists(save_path / "pytorch_model.bin"):
            snapshot_download(repo_id=model_name, local_dir=save_path, local_dir_use_symlinks=False)
