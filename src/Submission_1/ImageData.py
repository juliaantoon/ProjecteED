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
        self._images = {}  # dic principal on cada clau és un UUID i el valor és un diccionari amb les metadades de la imatge
        self._image_id = image_id # guarda una referencia 

    def add_image(self, uuid: str, file: str) -> None: # registra una imatge pero sense llegir el disc encara
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

    def _resolve_file_path(self, file_path: str) -> str:
        if not file_path or file_path == "None": # verifiva si la ruta existeix
            return ""
        if os.path.isfile(file_path):
            return file_path
        joined = os.path.join(cfg.ROOT_DIR, file_path) # si no existeix probem a unirlo amb el directori arrel de l'aplicació
        if os.path.isfile(joined):
            return joined
        normed = os.path.normpath(joined)
        if os.path.isfile(normed):
            return normed
        return file_path # retorna la ruta amb la que es pot obrir l'arxiu

    def load_metadata(self, uuid: str) -> None:
        if uuid not in self._images:
            return # si no existeix l'uuid, sortim netament sense llançar cap excepció

        ruta_original = self._images[uuid]["file"]
        ruta_fitxer = self._resolve_file_path(ruta_original)

        if not os.path.isfile(ruta_fitxer): # si no existeix el fitxer, assignem dimensions 0x0 i sortim
            self._images[uuid]["dimensions"] = (0, 0)
            return

        # Pillow
        try:
            with Image.open(ruta_fitxer) as img: # intenta obrir el archiu amb Pillow
                self._images[uuid]["dimensions"] = (img.width, img.height) # extreu les dimensions reals i les guarda com a tupla
                raw_text = getattr(img, "text", {}) or {} # si no hi ha metadades, retorna un diccionari buit
        except Exception:
            self._images[uuid]["dimensions"] = (0, 0) # si no es pot obrir el fitxer, assignem dimensions 0x0 i sortim
            raw_text = {}

        # Llegeix les metadades embegudes dins l'arxiu PNG i les emmagatzema
        metadades = {}
        try:
            metadades = cfg.read_png_metadata(ruta_fitxer) or {}
        except Exception:
            try:
                metadades = cfg.read_png_metadata(ruta_original) or {}
            except Exception:
                metadades = raw_text

        metadades_lower = {str(k).lower(): v for k, v in metadades.items()} # converteix totes les claus a minúscules per evitar problemes de majúscules/minúscules

        def _get_field(field_name): 
            val = metadades_lower.get(field_name)
            if val is None or str(val).strip() == "" or str(val) == "None":
                return "None"
            return str(val)

        self._images[uuid]["prompt"] = _get_field("prompt")
        self._images[uuid]["model"] = _get_field("model")
        self._images[uuid]["seed"] = _get_field("seed")
        self._images[uuid]["cfg_scale"] = _get_field("cfg_scale")
        self._images[uuid]["steps"] = _get_field("steps")
        self._images[uuid]["sampler"] = _get_field("sampler")
        self._images[uuid]["generated"] = _get_field("generated")
        self._images[uuid]["created_date"] = _get_field("created_date")

    def get_filename(self, uuid: str): # retorna la ruta original de l'archiu guardat
        if uuid not in self._images:
            return None
        return str(self._images[uuid].get("file", "None"))

    def get_prompt(self, uuid: str) -> str:  # Retorna el prompt utilitzat per generar la imatge
        if uuid not in self._images:
            return "None"
        return str(self._images[uuid].get("prompt", "None"))

    def get_model(self, uuid: str) -> str:  # Retorna el model d'IA utilitzat 
        if uuid not in self._images:
            return "None"
        return str(self._images[uuid].get("model", "None"))

    def get_seed(self, uuid: str) -> str:  # Retorna la llavor aleatòria utilitzada en la generació
        if uuid not in self._images:
            return "None"
        return str(self._images[uuid].get("seed", "None"))

    def get_cfg_scale(self, uuid: str) -> str:  # Retorna el guidance scale utilitzat
        if uuid not in self._images:
            return "None"
        return str(self._images[uuid].get("cfg_scale", "None"))

    def get_steps(self, uuid: str) -> str:  # Retorna el nombre de passos d'iteració del model
        if uuid not in self._images:
            return "None"
        return str(self._images[uuid].get("steps", "None"))

    def get_sampler(self, uuid: str) -> str:  # Retorna l'algorisme de mostreig utilitzat
        if uuid not in self._images:
            return "None"
        return str(self._images[uuid].get("sampler", "None"))

    def get_generated(self, uuid: str) -> str:  # Retorna "true" si la imatge està marcada com a generada
        if uuid not in self._images:
            return "None"
        return str(self._images[uuid].get("generated", "None"))

    def get_created_date(self, uuid: str) -> str:  # Retorna la data de creació en format YYYY-MM-DD
        if uuid not in self._images:
            return "None"
        return str(self._images[uuid].get("created_date", "None"))

    def get_dimensions(self, uuid: str) -> tuple:  # Retorna una tupla (width, height) amb les dimensions de la imatge
        if uuid not in self._images:
            return (0, 0)
        return self._images[uuid].get("dimensions", (0, 0))

    def __len__(self) -> int:
        return len(self._images)

    def __str__(self) -> str:
        return f"ImageData(imatges={len(self._images)})"