import numpy as np
from pydub import AudioSegment

FREQUENCIES = (
    (4000, 20000),
    (2000, 4000),
    (500, 2000),
    (250, 500),
    (20, 250)
)

def load_file(path: str):
    return AudioSegment.from_file(path)

