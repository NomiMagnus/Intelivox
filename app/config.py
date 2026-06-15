from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RESIDENTS_FILE = DATA_DIR / "residents.json"
AUDIO_DIR = DATA_DIR / "audio"

class Settings:
    def __init__(self):
        self.data_dir = DATA_DIR
        self.residents_file = RESIDENTS_FILE
        self.audio_dir = AUDIO_DIR

    def ensure_data_paths(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.audio_dir.mkdir(parents=True, exist_ok=True)

settings = Settings()
