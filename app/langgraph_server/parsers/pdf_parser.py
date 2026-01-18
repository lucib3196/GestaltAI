from .image_encoder import ImageEncoder
from pathlib import Path
from typing import List, Optional, Type

import fitz  # PyMuPDF
from pydantic import BaseModel

from langchain_core.language_models.chat_models import BaseChatModel


class BaseOutput(BaseModel):
    data: str


class PDFMultiModalLLM:
    def __init__(self):
        self.encoder = ImageEncoder()

    def prepare_payload(self, pdf_path: str | Path, prompt: str):
        pdf_bytes = self.pdf_page_to_image_bytes(pdf_path)

        encoded_images = self.encoder.prepare_llm_payload(pdf_bytes)
        message = {
            "role": "user",
            "content": [{"type": "text", "text": prompt}, *encoded_images],
        }
        return message

    def invoke(
        self,
        prompt: str,
        llm: BaseChatModel,
        pdf_path: str | Path,
        output_model: Optional[Type[BaseModel]] = BaseOutput,
    ):
        message = self.prepare_payload(pdf_path, prompt)
        if output_model:
            chain = llm.with_structured_output(schema=output_model)
            return chain.invoke([message])
        else:
            return llm.invoke([message])

    def pdf_page_to_image_bytes(self, pdf_path: str | Path, zoom: float = 2.0):
        doc = fitz.open(pdf_path)
        image_bytes: List[bytes] = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            matrix = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=matrix)  # type: ignore
            image_bytes.append(pix.tobytes("png"))
        doc.close()
        return image_bytes

    def ainvoke(
        self,
        prompt: str,
        llm: BaseChatModel,
        pdf_path: str | Path,
        output_model: Optional[Type[BaseModel]] = BaseOutput,
    ):
        message = self.prepare_payload(pdf_path, prompt)
        if output_model:
            chain = llm.with_structured_output(schema=output_model)
            return chain.ainvoke([message])
        else:
            return llm.ainvoke([message])
