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
        self._images = {}  # dic principal on cada clau és un UUID i el valor és un diccionari amb les dades
        self._image_id = image_id # guarda una referencia 

    def add_image(self, uuid: str, file: str) -> None: # registra una imatge pero sense llegir el disc encara
        u = str(uuid) # convertim l'UUID a string per assegurar que coincideixi sempre com a clau
        self._images[u] = {
            "file": str(file),
            "prompt": None,
            "model": None,
            "seed": None,
            "cfg_scale": None,
            "steps": None,
            "sampler": None,
            "generated": None,
            "created_date": None,
            "dimensions": None  # CANVI: tot a None (de Python) fins que es carreguin les metadades
        }

    def remove_image(self, uuid: str) -> None:
        u = str(uuid) # convertim l'UUID a string
        if u in self._images: # comprovem si l'uuid existeix abans d'eliminar-lo
            del self._images[u] 

    def load_metadata(self, uuid: str) -> None:
        u = str(uuid) # convertim l'UUID a string per poder consultar-lo

        if u not in self._images: # comprovem si la imatge està registrada
            if u: # si l'UUID no és buit, indiquem que no existeix
                raise FileNotFoundError(f"UUID '{u}' desconegut.")
            return # si és buit, acabem sense carregar res

        file_path = self._images[u]["file"] # obtenim el path de la imatge guardat

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
                self._images[u]["dimensions"] = (img.width, img.height) # guardem dimensions com a tupla (width, height)

                raw_text = cfg.read_png_metadata(full_path) # llegim les metadades guardades al PNG amb la funció de cfg
                if raw_text is None: # si no trobem metadades, utilitzem diccionari buit
                    raw_text = {}

                text_meta = {str(k).lower(): str(v) for k, v in raw_text.items()} # convertim claus a minúscules i valors a string
                created_date = text_meta.get("created_date", "None") # obtenim la data de creació o None

                self._images[u]["prompt"] = text_meta.get("prompt", "None") # guardem el prompt
                self._images[u]["model"] = text_meta.get("model", "None") # guardem el model
                self._images[u]["seed"] = text_meta.get("seed", "None") # guardem la seed
                self._images[u]["cfg_scale"] = text_meta.get("cfg_scale", text_meta.get("cfg", "None")) # comprovem cfg_scale o cfg
                self._images[u]["steps"] = text_meta.get("steps", "None") # guardem steps
                self._images[u]["sampler"] = text_meta.get("sampler", "None") # guardem sampler
                self._images[u]["generated"] = text_meta.get("generated", "None") # guardem generated
                self._images[u]["created_date"] = created_date # guardem created_date

        except FileNotFoundError:
            raise # tornem a llançar l'error si el fitxer no existeix

        except Exception as e:
            print(f"Error carregant metadades de {file_path}: {type(e).__name__}: {e}") # mostrem quin tipus d'error ha passat
            self._images[u]["dimensions"] = None # reiniciem dimensions
            self._images[u]["prompt"] = None # deixem prompt per defecte
            self._images[u]["model"] = None # deixem model per defecte
            self._images[u]["seed"] = None # deixem seed per defecte
            self._images[u]["cfg_scale"] = None # deixem cfg_scale per defecte
            self._images[u]["steps"] = None # deixem steps per defecte
            self._images[u]["sampler"] = None # deixem sampler per defecte
            self._images[u]["generated"] = None # deixem generated per defecte
            self._images[u]["created_date"] = None # deixem created_date per defecte

    def _valor(self, u: str, clau: str):
        # CANVI: si la metadada encara no s'ha carregat (o ha fallat) retornem None de Python;
        # si s'ha carregat, retornem el valor com a string (i "None" si el PNG no el tenia)
        v = self._images[u].get(clau)
        return None if v is None else str(v)

    def get_filename(self, uuid: str): # retorna la ruta original de l'arxiu guardat
        u = str(uuid)
        if u not in self._images:
            return None
        return str(self._images[u].get("file", "None"))

    def get_prompt(self, uuid: str):  # Retorna el prompt utilitzat per generar la imatge
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "prompt")

    def get_model(self, uuid: str):  # Retorna el model d'IA utilitzat 
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "model")

    def get_seed(self, uuid: str):  # Retorna la llavor aleatòria utilitzada en la generació
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "seed")

    def get_cfg_scale(self, uuid: str):  # Retorna el guidance scale utilitzat
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "cfg_scale")

    def get_steps(self, uuid: str):  # Retorna el nombre de passos d'iteració del model
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "steps")

    def get_sampler(self, uuid: str):  # Retorna l'algorisme de mostreig utilitzat
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "sampler")

    def get_generated(self, uuid: str):  # Retorna "true" si la imatge està marcada com a generada
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "generated")

    def get_created_date(self, uuid: str):  # Retorna la data de creació en format YYYY-MM-DD
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "created_date")

    def get_dimensions(self, uuid: str):  # Retorna una tupla (width, height) amb les dimensions de la imatge
        u = str(uuid)
        if u not in self._images:
            return None
        return self._images[u].get("dimensions")

    def __len__(self) -> int:
        return len(self._images)

    def __str__(self) -> str:
        return f"ImageData(imatges={len(self._images)})"