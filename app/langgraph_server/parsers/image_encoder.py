from pathlib import Path
import base64
from .encoder_base import EncoderBase
from typing import Sequence


class ImageEncoder(EncoderBase):
    def encode_base64(self, path: str | Path | bytes) -> str:
        if isinstance(path, (str, Path)):
            path = Path(path).resolve()
            if not path.exists():
                raise ValueError(f"Image path {path} not found")
            data_bytes = path.read_bytes()
        else:
            data_bytes = path
        encoded = base64.b64encode(data_bytes).decode("utf-8")
        return encoded

    def decode_base64(self, encoded_str: str, output_path: str | Path) -> Path:
        output_path = Path(output_path).resolve()
        bytes = base64.b64decode(encoded_str.encode("utf-8"))
        output_path.write_bytes(bytes)
        return output_path

    def prepare_llm_payload(self, paths: Sequence[str | Path | bytes]):
        encoded_payload = [
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{self.encode_base64(p)}"},
            }
            for p in paths
        ]
        return encoded_payload


if __name__ == "__main__":
    image_path = Path(r"langgraph_server/data/Lecture_02_03.pdf").absolute()
    paylod = ImageEncoder().prepare_llm_payload(
        paths=[image_path],
    )
    print(paylod)
