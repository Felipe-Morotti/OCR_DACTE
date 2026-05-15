#LightOnOCR-2

import torch
from transformers import LightOnOcrForConditionalGeneration, LightOnOcrProcessor
from PIL import Image
from pathlib import Path
import logging

def performOCR(imgs_path: str | Path, logger: logging.Logger) -> dict[str, str]:

    #configuração do hardware e precisão
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.bfloat16

    #carregamento do modelo e processador
    #model = carrega os pesos do LightOnOCR-2-1B
    #processor = tradutor que prepara a imagem e o texto
    model = LightOnOcrForConditionalGeneration.from_pretrained("lightonai/LightOnOCR-2-1B", torch_dtype=dtype).to(device)
    processor = LightOnOcrProcessor.from_pretrained("lightonai/LIghtOnOCR-2-1B")

    results = {}

    for i, img in enumerate(imgs_path.glob("*.png"), 1):
        image = Image.open(img)
        logger.info(f"Imagem {i} carregada. \u2705")

        conversation = [{"role": "user", "content": [
        {"type": "image", "image": image},
        {"type": "text", "text": "Extract all text from this image."}]}]

        prompt = processor.apply_chat_template(
            conversation,
            add_generation_prompt=True,
            tokenize=False,
        )

        inputs = processor(text=prompt, images=image, return_tensors="pt")

        inputs = {k: v.to(device=device, dtype=dtype) if v.is_floating_point() else v.to(device) for k, v in inputs.items()}

        output_ids = model.generate(**inputs, max_new_tokens=2048)
        generated_ids = output_ids[0, inputs["input_ids"].shape[1]:]

        output_text = processor.decode(generated_ids, skip_special_tokens=True)

        
        logger.info(f"OCR da imagem {i} concluída. \u2705")

        results[img.name] = output_text
    
    return results

