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
        self._images = {}  # dic principal on cada clau és un UUID i el valor és un diccionari amb les dades[cite: 3, 8]
        self._image_id = image_id # guarda una referencia[cite: 3, 8]

    def add_image(self, uuid: str, file: str) -> None: # registra una imatge pero sense llegir el disc encara[cite: 3, 8]
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
        if uuid in self._images: # comprovem si l'uuid existeix abans d'eliminar-lo[cite: 3, 8]
            del self._images[uuid] 

    def load_metadata(self, uuid: str) -> None:
        uuid = str(uuid) # convertim l'UUID a string per poder consultar-lo

        if uuid not in self._images: # comprovem si la imatge està registrada
            if uuid: # si l'UUID no és buit, indiquem que no existeix
                raise FileNotFoundError(f"UUID '{uuid}' desconegut.")
            return # si és buit, acabem sense carregar res

        file_path = self._images[uuid]["file"] # obtenim el path de la imatge guardat

        if os.path.isabs(file_path): # comprovem si el path ja és una ruta absoluta
            full_path = file_path # si és absoluta, la podem utilitzar directament
        else:
            root_dir = getattr(cfg, "ROOT_DIR", "") # obtenim el directori arrel
            full_path = os.path.join(root_dir, file_path) # si és relativa, la unim amb la carpeta ROOT_DIR

            if not os.path.isfile(full_path): # si no trobem el fitxer, provem alternativa
                alt_name = file_path.removeprefix("../") if hasattr(file_path, "removeprefix") else file_path.replace("../", "") # traiem el prefix ../
                alternative = os.path.join(root_dir, alt_name) # unim amb ROOT_DIR
                if os.path.isfile(alternative): # si el fitxer existeix amb la ruta alternativa
                    full_path = alternative # utilitzem aquesta ruta per carregar-lo

        try:
            with Image.open(full_path) as img: # intentem obrir la imatge amb Pillow
                self._images[uuid]["dimensions"] = (img.width, img.height) # guardem dimensions com a tupla (width, height)

                raw_text = cfg.read_png_metadata(full_path) # llegim les metadades guardades al PNG amb la funció de cfg
                if raw_text is None: # si no trobem metadades, utilitzem diccionari buit
                    raw_text = {}

                text_meta = {str(k).lower(): str(v) for k, v in raw_text.items()} # convertim claus a minúscules i valors a string
                created_date = text_meta.get("created_date", "None") # obtenim la data de creació o None

                self._images[uuid]["prompt"] = text_meta.get("prompt", "None") # guardem el prompt[cite: 3, 8]
                self._images[uuid]["model"] = text_meta.get("model", "None") # guardem el model[cite: 3, 8]
                self._images[uuid]["seed"] = text_meta.get("seed", "None") # guardem la seed[cite: 3, 8]
                self._images[uuid]["cfg_scale"] = text_meta.get("cfg_scale", text_meta.get("cfg", "None")) # comprovem cfg_scale o cfg
                self._images[uuid]["steps"] = text_meta.get("steps", "None") # guardem steps[cite: 3, 8]
                self._images[uuid]["sampler"] = text_meta.get("sampler", "None") # guardem sampler[cite: 3, 8]
                self._images[uuid]["generated"] = text_meta.get("generated", "None") # guardem generated[cite: 3, 8]
                self._images[uuid]["created_date"] = created_date # guardem created_date

        except FileNotFoundError:
            raise # tornem a llançar l'error si el fitxer no existeix

        except Exception as e:
            print(f"Error carregant metadades de {file_path}: {type(e).__name__}: {e}") # mostrem quin tipus d'error ha passat
            self._images[uuid]["dimensions"] = (0, 0) # reiniciem dimensions a 0x0
            self._images[uuid]["prompt"] = "None" # deixem prompt per defecte
            self._images[uuid]["model"] = "None" # deixem model per defecte
            self._images[uuid]["seed"] = "None" # deixem seed per defecte
            self._images[uuid]["cfg_scale"] = "None" # deixem cfg_scale per defecte
            self._images[uuid]["steps"] = "None" # deixem steps per defecte
            self._images[uuid]["sampler"] = "None" # deixem sampler per defecte
            self._images[uuid]["generated"] = "None" # deixem generated per defecte
            self._images[uuid]["created_date"] = "None" # deixem created_date per defecte

    def get_filename(self, uuid: str): # retorna la ruta original de l'arxiu guardat[cite: 3, 8]
        if uuid not in self._images:
            return None
        return str(self._images[uuid].get("file", "None"))

    def get_prompt(self, uuid: str):  # Retorna el prompt utilitzat per generar la imatge[cite: 3, 8]
        if uuid not in self._images:
            return None
        return str(self._images[uuid].get("prompt", "None"))

    def get_model(self, uuid: str):  # Retorna el model d'IA utilitzat[cite: 3, 8]
        if uuid not in self._images:
            return None
        return str(self._images[uuid].get("model", "None"))

    def get_seed(self, uuid: str):  # Retorna la llavor aleatòria utilitzada en la generació[cite: 3, 8]
        if uuid not in self._images:
            return None
        return str(self._images[uuid].get("seed", "None"))

    def get_cfg_scale(self, uuid: str):  # Retorna el guidance scale utilitzat[cite: 3, 8]
        if uuid not in self._images:
            return None
        return str(self._images[uuid].get("cfg_scale", "None"))

    def get_steps(self, uuid: str):  # Retorna el nombre de passos d'iteració del model[cite: 3, 8]
        if uuid not in self._images:
            return None
        return str(self._images[uuid].get("steps", "None"))

    def get_sampler(self, uuid: str):  # Retorna l'algorisme de mostreig utilitzat[cite: 3, 8]
        if uuid not in self._images:
            return None
        return str(self._images[uuid].get("sampler", "None"))

    def get_generated(self, uuid: str):  # Retorna "true" si la imatge està marcada com a generada[cite: 3, 8]
        if uuid not in self._images:
            return None
        return str(self._images[uuid].get("generated", "None"))

    def get_created_date(self, uuid: str):  # Retorna la data de creació en format YYYY-MM-DD[cite: 3, 8]
        if uuid not in self._images:
            return None
        return str(self._images[uuid].get("created_date", "None"))

    def get_dimensions(self, uuid: str):  # Retorna una tupla (width, height) amb les dimensions de la imatge[cite: 3, 8]
        if uuid not in self._images:
            return None
        return self._images[uuid].get("dimensions", (0, 0))

    def __len__(self) -> int:
        return len(self._images)

    def __str__(self) -> str:
        return f"ImageData(imatges={len(self._images)})"