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
        self._images = {}  # dic principal on cada clau és un UUID i el valor és un diccionari amb les dades
        self._image_id = image_id  # guarda una referencia

    def add_image(self, uuid: str, file: str) -> None:
        u = str(uuid)  # convertim l'UUID a string per assegurar que coincideixi sempre com a clau

        self._images[u] = {
            "file": str(file),
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
        u = str(uuid)  # convertim l'UUID a string
        if u in self._images:  # comprovem si l'uuid existeix abans d'eliminar-lo
            del self._images[u]

    def load_metadata(self, uuid: str) -> None:
        u = str(uuid)  # convertim l'UUID a string per poder consultar-lo

        if u not in self._images:  # comprovem si la imatge està registrada
            if u:
                raise FileNotFoundError(f"UUID '{u}' desconegut.")
            return

        file_path = self._images[u]["file"]  # obtenim el path de la imatge guardat

        if os.path.isabs(file_path):  # comprovem si el path ja és una ruta absoluta
            full_path = file_path
        else:
            root_dir = getattr(cfg, "ROOT_DIR", "")  # obtenim el directori arrel
            full_path = os.path.join(root_dir, file_path)  # unim la ruta amb ROOT_DIR

            if not os.path.isfile(full_path):  # si no trobem el fitxer, provem una ruta alternativa
                alt_name = file_path.replace("../", "")
                alternative = os.path.join(root_dir, alt_name)

                if os.path.isfile(alternative):
                    full_path = alternative

        if not os.path.isfile(full_path):  # comprovem que el fitxer existeixi
            raise FileNotFoundError(full_path)

        try:
            with Image.open(full_path) as img:  # intentem obrir la imatge amb Pillow
                self._images[u]["dimensions"] = (img.width, img.height)  # guardem les dimensions

            raw_text = cfg.read_png_metadata(full_path)  # llegim les metadades del PNG

            if raw_text is None:  # si no trobem metadades, utilitzem un diccionari buit
                raw_text = {}

            text_meta = {str(k).lower(): str(v) for k, v in raw_text.items()}  # convertim les claus i valors a string

            # Funció auxiliar per obtenir una metadada o retornar "None" si està buida
            def get_value(key, alternative=None):
                value = text_meta.get(key)

                if (value is None or value.strip() == "") and alternative:
                    value = text_meta.get(alternative)

                if value is None or value.strip() == "":
                    return "None"

                return value

            self._images[u]["prompt"] = get_value("prompt")  # guardem el prompt
            self._images[u]["model"] = get_value("model")  # guardem el model
            self._images[u]["seed"] = get_value("seed")  # guardem la seed
            self._images[u]["cfg_scale"] = get_value("cfg_scale", "cfg")  # comprovem cfg_scale o cfg
            self._images[u]["steps"] = get_value("steps")  # guardem steps
            self._images[u]["sampler"] = get_value("sampler")  # guardem sampler
            self._images[u]["generated"] = get_value("generated")  # guardem generated
            self._images[u]["created_date"] = get_value("created_date")  # guardem la data

        except FileNotFoundError:
            raise

        except Exception as e:
            print(f"WARNING with empty metadata elements: {e}")  # avisem si hi ha problemes llegint les metadades

            self._images[u]["dimensions"] = (0, 0)  # reiniciem les dimensions
            self._images[u]["prompt"] = "None"
            self._images[u]["model"] = "None"
            self._images[u]["seed"] = "None"
            self._images[u]["cfg_scale"] = "None"
            self._images[u]["steps"] = "None"
            self._images[u]["sampler"] = "None"
            self._images[u]["generated"] = "None"
            self._images[u]["created_date"] = "None"

    def get_filename(self, uuid: str):
        u = str(uuid)  # convertim l'UUID a string
        if u not in self._images:
            return None
        return str(self._images[u].get("file", "None"))

    def get_prompt(self, uuid: str):
        u = str(uuid)
        if u not in self._images:
            return None
        return str(self._images[u].get("prompt", "None"))

    def get_model(self, uuid: str):
        u = str(uuid)
        if u not in self._images:
            return None
        return str(self._images[u].get("model", "None"))

    def get_seed(self, uuid: str):
        u = str(uuid)
        if u not in self._images:
            return None
        return str(self._images[u].get("seed", "None"))

    def get_cfg_scale(self, uuid: str):
        u = str(uuid)
        if u not in self._images:
            return None
        return str(self._images[u].get("cfg_scale", "None"))

    def get_steps(self, uuid: str):
        u = str(uuid)
        if u not in self._images:
            return None
        return str(self._images[u].get("steps", "None"))

    def get_sampler(self, uuid: str):
        u = str(uuid)
        if u not in self._images:
            return None
        return str(self._images[u].get("sampler", "None"))

    def get_generated(self, uuid: str):
        u = str(uuid)
        if u not in self._images:
            return None
        return str(self._images[u].get("generated", "None"))

    def get_created_date(self, uuid: str):
        u = str(uuid)
        if u not in self._images:
            return None
        return str(self._images[u].get("created_date", "None"))

    def get_dimensions(self, uuid: str):
        u = str(uuid)
        if u not in self._images:
            return None
        return self._images[u].get("dimensions", (0, 0))

    def __len__(self) -> int:
        return len(self._images)

    def __str__(self) -> str:
        return f"ImageData(imatges={len(self._images)})"