# -*- coding: utf-8 -*-
"""
ImageData.py : ** REQUIRED ** El vostre codi de la classe ImageData.

Aquesta classe s'encarrega d'emmagatzemar i gestionar les metadades de les
imatges generades per IA.

Funcionalitat:
    - Afegir i eliminar imatges de la col·lecció
    - Llegir les metadades embegudes dins els arxius PNG
    - Proporcionar accés a totes les metadades d'una imatge

Mètodes a implementar:
    - add_image(uuid: str, file: str) -> None
        Crea una entrada per a la imatge amb l'UUID i el path especificats.
        Inicialment les metadades estan buides (no llegides del disc).

    - remove_image(uuid: str) -> None
        Elimina la imatge i totes les seves metadades de la col·lecció.

    - load_metadata(uuid: str) -> None
        Llegeix les metadades embegudes en l'arxiu PNG i les emmagatzema.
        Aquest mètode es pot cridar múltiples vegades (p.ex. si l'arxiu canvia).

    - get_prompt(uuid: str) -> str
        Retorna el prompt utilitzat per generar la imatge.

    - get_model(uuid: str) -> str
        Retorna el model d'IA utilitzat (p.ex. "SD2", "DALL-E", "Midjourney").

    - get_seed(uuid: str) -> str
        Retorna la llavor aleatòria utilitzada en la generació.

    - get_cfg_scale(uuid: str) -> str
        Retorna el CFG Scale (guidance scale) utilitzat.

    - get_steps(uuid: str) -> str
        Retorna el nombre de passos d'iteració del model.

    - get_sampler(uuid: str) -> str
        Retorna l'algorisme de mostreig utilitzat.

    - get_generated(uuid: str) -> str
        Retorna "true" si la imatge està marcada com a generada.

    - get_created_date(uuid: str) -> str
        Retorna la data de creació en format YYYY-MM-DD.

    - get_dimensions(uuid: str) -> tuple
        Retorna una tupla (width, height) amb les dimensions de la imatge.

Notes:
    - Utilitzeu la llibreria PIL/Pillow per llegir metadades:
      img = Image.open(file)
      metadata = img.text
    - Si un camp no existeix, retorneu "None" (string)
    - Les dimensions es llegeixen amb img.width i img.height
    - Tots els camps de metadades es guarden com a strings
"""

from PIL import Image
import cfg


class ImageData:

    def __init__(self):
        self._images = {}  # Diccionari principal: clau UUID -> diccionari de dades
        self._image_id = image_id

    def add_image(self, uuid: str, file: str) -> None:
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
            "dimensions": (0, 0)
        }

    def remove_image(self, uuid: str) -> None:
        if uuid in self._images:
            del self._images[uuid]

    def load_metadata(self, uuid: str) -> None:
        if uuid not in self._images:
            return

        ruta_fitxer = self._images[uuid]["file"]

        try:
            with Image.open(ruta_fitxer) as img:
                self._images[uuid]["dimensions"] = (img.width, img.height)
                # Backup de metadades si cfg no les proporciona
                raw_text = getattr(img, "text", {}) or {}
        except Exception:
            self._images[uuid]["dimensions"] = (0, 0)
            raw_text = {}

        try:
            metadades = cfg.read_png_metadata(ruta_fitxer) or {}
        except Exception:
            metadades = {}

        self._images[uuid]["prompt"] = str(metadades.get("prompt", "None"))
        self._images[uuid]["model"] = str(metadades.get("model", "None"))
        self._images[uuid]["seed"] = str(metadades.get("seed", "None"))
        self._images[uuid]["cfg_scale"] = str(metadades.get("cfg_scale", "None"))
        self._images[uuid]["steps"] = str(metadades.get("steps", "None"))
        self._images[uuid]["sampler"] = str(metadades.get("sampler", "None"))
        self._images[uuid]["generated"] = str(metadades.get("generated", "None"))
        self._images[uuid]["created_date"] = str(metadades.get("created_date", "None"))

    def get_filename(self, uuid: str) -> str:
        if uuid in self._images:
            return self._images[uuid].get("file", "None")
        return "None"

    def get_prompt(self, uuid: str) -> str:
        if uuid in self._images:
            return self._images[uuid].get("prompt", "None")
        return "None"

    def get_model(self, uuid: str) -> str:
        if uuid in self._images:
            return self._images[uuid].get("model", "None")
        return "None"

    def get_seed(self, uuid: str) -> str:
        if uuid in self._images:
            return self._images[uuid].get("seed", "None")
        return "None"

    def get_cfg_scale(self, uuid: str) -> str:
        if uuid in self._images:
            return self._images[uuid].get("cfg_scale", "None")
        return "None"

    def get_steps(self, uuid: str) -> str:
        if uuid in self._images:
            return self._images[uuid].get("steps", "None")
        return "None"

    def get_sampler(self, uuid: str) -> str:
        if uuid in self._images:
            return self._images[uuid].get("sampler", "None")
        return "None"

    def get_generated(self, uuid: str) -> str:
        if uuid in self._images:
            return self._images[uuid].get("generated", "None")
        return "None"

    def get_created_date(self, uuid: str) -> str:
        if uuid in self._images:
            return self._images[uuid].get("created_date", "None")
        return "None"

    def get_dimensions(self, uuid: str) -> tuple:
        if uuid in self._images:
            return self._images[uuid].get("dimensions", (0, 0))
        return (0, 0)

    def __len__(self) -> int:
        return len(self._images)

    def __str__(self) -> str:
        return f"ImageData(imatges={len(self._images)})"