
# -*- coding: utf-8 -*-
"""
ImageData.py : ** REQUIRED ** El vostre codi de la classe ImageData.

Aquesta classe s'encarrega d'emmagatzemar i gestionar les metadades de les
imatges generades per IA.

Notes:
- Utilitzeu la llibreria PIL/Pillow per llegir metadades
- Si un camp no existeix, retorneu "None" (string)
- Les dimensions es llegeixen amb img.width i img.height
- Tots els camps de metadades es guarden com a strings
"""
import os
from PIL import Image
import cfg


class ImageData:

    def __init__(self, image_id=None):
        self._images = {}  # diccionari principal amb les dades de cada imatge
        self._image_id = image_id  # guarda una referencia a ImageID

    def add_image(self, uuid: str, file: str) -> None:
        if uuid is None or file is None:  # comprovem que no faltin arguments
            return
        if not isinstance(uuid, str) or not isinstance(file, str):
            return
        if not uuid or not file:
            return

        if uuid in self._images:  # si ja existeix no la tornem a afegir
            return

        self._images[uuid] = {
            "file": file,
            "prompt": "None",
            "model": "None",
            "seed": "None",
            "cfg_scale": "None",
            "steps": "None",
            "sampler": "None",
            "generated": "None",
            "created_date": "None",
            "dimensions": None
        }

    def remove_image(self, uuid: str) -> None:
        u = str(uuid)
        if u in self._images:
            del self._images[u]

    def load_metadata(self, uuid: str) -> None:
        if uuid is None:
            return

        u = str(uuid)

        if u not in self._images:  # comprovem si la imatge està registrada
            raise FileNotFoundError(f"UUID '{u}' desconegut.")

        file_path = self._images[u]["file"]  # obtenim el path de la imatge

        if os.path.isabs(file_path):
            full_path = file_path
        else:
            full_path = os.path.join(cfg.ROOT_DIR, file_path)

            if not os.path.isfile(full_path):  # provem també el path sense ../
                alt_name = file_path.replace("../", "")
                alternative = os.path.join(cfg.ROOT_DIR, alt_name)
                if os.path.isfile(alternative):
                    full_path = alternative

        try:
            with Image.open(full_path) as img:  # obrim la imatge amb Pillow
                self._images[u]["dimensions"] = (img.width, img.height)

            raw_text = cfg.read_png_metadata(full_path)  # llegim les metadades del PNG

            if raw_text is None:
                raw_text = {}

            text_meta = {
                str(k).lower(): str(v)
                for k, v in raw_text.items()
            }  # normalitzem les claus i els valors

            self._images[u]["prompt"] = text_meta.get("prompt", "None")
            self._images[u]["model"] = text_meta.get("model", "None")
            self._images[u]["seed"] = text_meta.get("seed", "None")
            self._images[u]["cfg_scale"] = text_meta.get(
                "cfg_scale", text_meta.get("cfg", "None")
            )
            self._images[u]["steps"] = text_meta.get("steps", "None")
            self._images[u]["sampler"] = text_meta.get("sampler", "None")
            self._images[u]["generated"] = text_meta.get("generated", "None")
            self._images[u]["created_date"] = text_meta.get("created_date", "None")

        except FileNotFoundError:
            raise

        except Exception as e:
            print(f"Error carregant metadades de {file_path}: {type(e).__name__}: {e}")

            self._images[u]["dimensions"] = None
            self._images[u]["prompt"] = "None"
            self._images[u]["model"] = "None"
            self._images[u]["seed"] = "None"
            self._images[u]["cfg_scale"] = "None"
            self._images[u]["steps"] = "None"
            self._images[u]["sampler"] = "None"
            self._images[u]["generated"] = "None"
            self._images[u]["created_date"] = "None"

    def _valor(self, u: str, clau: str):
        return str(self._images[u].get(clau, "None"))

    def get_filename(self, uuid: str):
        u = str(uuid)
        if u not in self._images:
            return None
        return str(self._images[u].get("file", "None"))

    def get_prompt(self, uuid: str):
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "prompt")

    def get_model(self, uuid: str):
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "model")

    def get_seed(self, uuid: str):
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "seed")

    def get_cfg_scale(self, uuid: str):
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "cfg_scale")

    def get_steps(self, uuid: str):
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "steps")

    def get_sampler(self, uuid: str):
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "sampler")

    def get_generated(self, uuid: str):
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "generated")

    def get_created_date(self, uuid: str):
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "created_date")

    def get_dimensions(self, uuid: str):
        u = str(uuid)
        if u not in self._images:
            return None
        return self._images[u].get("dimensions")

    def __len__(self) -> int:
        return len(self._images)

    def __str__(self) -> str:
        return f"ImageData(imatges={len(self._images)})"
