
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
        self._images = {}
        self._image_id = image_id

    def add_image(self, uuid: str, file: str) -> None:
        if uuid is None or file is None:
            return

        if not isinstance(uuid, str) or not isinstance(file, str):
            return

        if not uuid or not file:
            return

        if uuid in self._images:
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
        if uuid in self._images:
            del self._images[uuid]

    def _get_full_path(self, file_path):
        # Si ja tenim una ruta absoluta, la utilitzem.
        if os.path.isabs(file_path):
            if os.path.isfile(file_path):
                return file_path
            return None

        root = cfg.ROOT_DIR

        # Provem diferents representacions de la ruta.
        candidates = [
            os.path.join(root, file_path),
            os.path.join(root, file_path.replace("../", "")),
            os.path.abspath(file_path)
        ]

        # Eliminem els ../ inicials sense perdre els subdirectoris.
        cleaned = os.path.normpath(file_path)

        while cleaned == ".." or cleaned.startswith(".." + os.sep):
            if cleaned == "..":
                cleaned = ""
            else:
                cleaned = cleaned[3:]

        candidates.append(os.path.join(root, cleaned))

        for candidate in candidates:
            if os.path.isfile(candidate):
                return candidate

        return None

    def load_metadata(self, uuid: str) -> None:
        if uuid is None:
            return

        if uuid not in self._images:
            raise FileNotFoundError(f"UUID '{uuid}' desconegut.")

        file_path = self._images[uuid]["file"]
        full_path = self._get_full_path(file_path)

        if full_path is None:
            raise FileNotFoundError(f"Fitxer '{file_path}' no trobat.")

        try:
            # Llegim les dimensions de la imatge.
            with Image.open(full_path) as img:
                self._images[uuid]["dimensions"] = (
                    img.width,
                    img.height
                )

            # Llegim les metadades del PNG.
            raw_text = cfg.read_png_metadata(full_path)

            if raw_text is None:
                raw_text = {}

            text_meta = {
                str(k).lower(): str(v)
                for k, v in raw_text.items()
            }

            self._images[uuid]["prompt"] = text_meta.get("prompt", "None")
            self._images[uuid]["model"] = text_meta.get("model", "None")
            self._images[uuid]["seed"] = text_meta.get("seed", "None")
            self._images[uuid]["cfg_scale"] = text_meta.get(
                "cfg_scale", text_meta.get("cfg", "None")
            )
            self._images[uuid]["steps"] = text_meta.get("steps", "None")
            self._images[uuid]["sampler"] = text_meta.get("sampler", "None")
            self._images[uuid]["generated"] = text_meta.get("generated", "None")
            self._images[uuid]["created_date"] = text_meta.get(
                "created_date", "None"
            )

        except Exception as e:
            print(f"Error carregant metadades de {file_path}: {e}")

            self._images[uuid]["dimensions"] = None
            self._images[uuid]["prompt"] = "None"
            self._images[uuid]["model"] = "None"
            self._images[uuid]["seed"] = "None"
            self._images[uuid]["cfg_scale"] = "None"
            self._images[uuid]["steps"] = "None"
            self._images[uuid]["sampler"] = "None"
            self._images[uuid]["generated"] = "None"
            self._images[uuid]["created_date"] = "None"

    def _valor(self, uuid: str, clau: str):
        return str(self._images[uuid].get(clau, "None"))

    def get_filename(self, uuid: str):
        if uuid not in self._images:
            return None
        return str(self._images[uuid].get("file", "None"))

    def get_prompt(self, uuid: str):
        if uuid not in self._images:
            return None
        return self._valor(uuid, "prompt")

    def get_model(self, uuid: str):
        if uuid not in self._images:
            return None
        return self._valor(uuid, "model")

    def get_seed(self, uuid: str):
        if uuid not in self._images:
            return None
        return self._valor(uuid, "seed")

    def get_cfg_scale(self, uuid: str):
        if uuid not in self._images:
            return None
        return self._valor(uuid, "cfg_scale")

    def get_steps(self, uuid: str):
        if uuid not in self._images:
            return None
        return self._valor(uuid, "steps")

    def get_sampler(self, uuid: str):
        if uuid not in self._images:
            return None
        return self._valor(uuid, "sampler")

    def get_generated(self, uuid: str):
        if uuid not in self._images:
            return None
        return self._valor(uuid, "generated")

    def get_created_date(self, uuid: str):
        if uuid not in self._images:
            return None
        return self._valor(uuid, "created_date")

    def get_dimensions(self, uuid: str):
        if uuid not in self._images:
            return None
        return self._images[uuid].get("dimensions")

    def __len__(self) -> int:
        return len(self._images)

    def __str__(self) -> str:
        return f"ImageData(imatges={len(self._images)})"
