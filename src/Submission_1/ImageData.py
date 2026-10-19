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
import os
from PIL import Image
import cfg


class ImageData:

    def __init__(self, image_id=None):
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
        if uuid in self._images: # comprovem si l'uuid existeix abans d'eliminar-lo
            del self._images[uuid]

    def _trobar_ruta_real(self, file_path: str) -> str:
        if not file_path or file_path == "None":
            return ""
        candidats = [
            file_path,
            os.path.join(cfg.ROOT_DIR, file_path),
            os.path.normpath(os.path.join(cfg.ROOT_DIR, file_path)),
            os.path.abspath(file_path),
            os.path.abspath(os.path.join(cfg.ROOT_DIR, file_path))
        ]
        for c in candidats:
            if os.path.isfile(c):
                return c
        return file_path

    def load_metadata(self, uuid: str) -> None:
        if uuid not in self._images:
            return

        ruta_raw = self._images[uuid]["file"]
        ruta_fitxer = self._trobar_ruta_real(ruta_raw)

        raw_text = {}
        try:
            with Image.open(ruta_fitxer) as img: # obrim la imatge amb pillow
                self._images[uuid]["dimensions"] = (img.width, img.height) # guardem les mides de la imatge com a tupla (width, height)
                raw_text = getattr(img, "text", {}) or {}
        except Exception:
            self._images[uuid]["dimensions"] = (0, 0)
            raw_text = {}

        metadades = {}
        # Provem amb cfg.read_png_metadata tant a la ruta resolta com a l'original
        if hasattr(cfg, "read_png_metadata"):
            try:
                metadades = cfg.read_png_metadata(ruta_fitxer) or {}
            except Exception:
                try:
                    metadades = cfg.read_png_metadata(ruta_raw) or {}
                except Exception:
                    metadades = {}

        # Si cfg no ha donat res o està buit, fem servir el que ha llegit Pillow
        combinat = {}
        if isinstance(raw_text, dict):
            for k, v in raw_text.items():
                combinat[str(k).lower()] = str(v)
        if isinstance(metadades, dict):
            for k, v in metadades.items():
                if v is not None and str(v).strip() != "":
                    combinat[str(k).lower()] = str(v)

        def _obtenir(camp):
            v = combinat.get(camp)
            if v is None or str(v).strip() == "" or str(v) == "None":
                return "None"
            return str(v)

        self._images[uuid]["prompt"] = _obtenir("prompt")
        self._images[uuid]["model"] = _obtenir("model")
        self._images[uuid]["seed"] = _obtenir("seed")
        self._images[uuid]["cfg_scale"] = _obtenir("cfg_scale")
        self._images[uuid]["steps"] = _obtenir("steps")
        self._images[uuid]["sampler"] = _obtenir("sampler")
        self._images[uuid]["generated"] = _obtenir("generated")
        self._images[uuid]["created_date"] = _obtenir("created_date")

    def get_filename(self, uuid: str) -> str:
        if uuid in self._images:
            return str(self._images[uuid].get("file", "None"))
        return "None"

    def get_prompt(self, uuid: str) -> str:  # Retorna el prompt utilitzat per generar la imatge
        if uuid in self._images:
            return str(self._images[uuid].get("prompt", "None"))
        return "None"

    def get_model(self, uuid: str) -> str:  # Retorna el model d'IA utilitzat 
        if uuid in self._images:
            return str(self._images[uuid].get("model", "None"))
        return "None"

    def get_seed(self, uuid: str) -> str:  # Retorna la llavor aleatòria utilitzada en la generació
        if uuid in self._images:
            return str(self._images[uuid].get("seed", "None"))
        return "None"

    def get_cfg_scale(self, uuid: str) -> str:  # Retorna el guidance scale utilitzat
        if uuid in self._images:
            return str(self._images[uuid].get("cfg_scale", "None"))
        return "None"

    def get_steps(self, uuid: str) -> str:  # Retorna el nombre de passos d'iteració del model
        if uuid in self._images:
            return str(self._images[uuid].get("steps", "None"))
        return "None"

    def get_sampler(self, uuid: str) -> str:  # Retorna l'algorisme de mostreig utilitzat
        if uuid in self._images:
            return str(self._images[uuid].get("sampler", "None"))
        return "None"

    def get_generated(self, uuid: str) -> str:  # Retorna "true" si la imatge està marcada com a generada
        if uuid in self._images:
            return str(self._images[uuid].get("generated", "None"))
        return "None"

    def get_created_date(self, uuid: str) -> str:  # Retorna la data de creació en format YYYY-MM-DD
        if uuid in self._images:
            return str(self._images[uuid].get("created_date", "None"))
        return "None"

    def get_dimensions(self, uuid: str) -> tuple:  # Retorna una tupla (width, height) amb les dimensions de la imatge
        if uuid in self._images:
            return self._images[uuid].get("dimensions", (0, 0))
        return (0, 0)

    def __len__(self) -> int:
        return len(self._images)

    def __str__(self) -> str:
        return f"ImageData(imatges={len(self._images)})"