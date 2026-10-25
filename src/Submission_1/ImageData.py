
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
    """Gestiona les dades i les metadades de les imatges."""

    def __init__(self, image_id=None):
        """Inicialitza el diccionari d'imatges i la referència a ImageID."""
        self._images = {}  # Diccionari amb les dades de cada imatge, identificada pel seu UUID.
        self._image_id = image_id  # Referència a la classe ImageID.

    def add_image(self, uuid: str, file: str) -> None:
        """Registra una imatge sense llegir encara les seves dades del disc."""
        if uuid is None or file is None:
            return

        # Comprova que els arguments siguin cadenes de text no buides.
        if not isinstance(uuid, str) or not isinstance(file, str):
            return
        if not uuid or not file:
            return

        u = uuid
        if u in self._images:
            return

        # Inicialitza els camps de metadades amb valors per defecte.
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
            "dimensions": None
        }

    def remove_image(self, uuid: str) -> None:
        """Elimina una imatge del registre a partir del seu UUID."""
        u = str(uuid)
        if u in self._images:
            del self._images[u]

    def load_metadata(self, uuid: str) -> None:
        """Carrega les dimensions i les metadades d'una imatge."""
        u = str(uuid)

        # Comprova si l'UUID correspon a una imatge registrada.
        if u not in self._images:
            if u:
                raise FileNotFoundError(f"UUID '{u}' desconegut.")
            return

        file_path = self._images[u]["file"]

        # Determina la ruta completa del fitxer.
        if os.path.isabs(file_path):
            full_path = file_path
        else:
            root_dir = getattr(cfg, "ROOT_DIR", "")
            full_path = os.path.join(root_dir, file_path)

            # Si la ruta no existeix, prova eliminant el prefix ../.
            if not os.path.isfile(full_path):
                alt_name = file_path.removeprefix("../") if hasattr(file_path, "removeprefix") else file_path.replace("../", "")
                alternative = os.path.join(root_dir, alt_name)
                if os.path.isfile(alternative):
                    full_path = alternative

        try:
            # Obre la imatge amb Pillow i obté les seves dimensions.
            with Image.open(full_path) as img:
                self._images[u]["dimensions"] = (img.width, img.height)

                # Llegeix les metadades PNG mitjançant la funció de cfg.
                raw_text = cfg.read_png_metadata(full_path)
                if raw_text is None:
                    raw_text = {}

                # Normalitza les claus i els valors de les metadades.
                text_meta = {str(k).lower(): str(v) for k, v in raw_text.items()}
                created_date = text_meta.get("created_date", "None")

                # Guarda les metadades de generació de la imatge.
                self._images[u]["prompt"] = text_meta.get("prompt", "None")
                self._images[u]["model"] = text_meta.get("model", "None")
                self._images[u]["seed"] = text_meta.get("seed", "None")
                self._images[u]["cfg_scale"] = text_meta.get("cfg_scale", text_meta.get("cfg", "None"))
                self._images[u]["steps"] = text_meta.get("steps", "None")
                self._images[u]["sampler"] = text_meta.get("sampler", "None")
                self._images[u]["generated"] = text_meta.get("generated", "None")
                self._images[u]["created_date"] = created_date

        except FileNotFoundError:
            raise

        except Exception as e:
            # Mostra l'error i reinicialitza les metadades de la imatge.
            print(f"Error carregant metadades de {file_path}: {type(e).__name__}: {e}")
            self._images[u]["dimensions"] = None
            self._images[u]["prompt"] = None
            self._images[u]["model"] = None
            self._images[u]["seed"] = None
            self._images[u]["cfg_scale"] = None
            self._images[u]["steps"] = None
            self._images[u]["sampler"] = None
            self._images[u]["generated"] = None
            self._images[u]["created_date"] = None

    def _valor(self, u: str, clau: str):
        """Retorna el valor d'un camp de metadades com a cadena de text."""
        v = self._images[u].get(clau)
        return None if v is None else str(v)

    def get_filename(self, uuid: str):
        """Retorna la ruta original del fitxer de la imatge."""
        u = str(uuid)
        if u not in self._images:
            return None
        return str(self._images[u].get("file", "None"))

    def get_prompt(self, uuid: str):
        """Retorna el prompt utilitzat per generar la imatge."""
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "prompt")

    def get_model(self, uuid: str):
        """Retorna el model d'IA utilitzat per generar la imatge."""
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "model")

    def get_seed(self, uuid: str):
        """Retorna la llavor aleatòria utilitzada en la generació."""
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "seed")

    def get_cfg_scale(self, uuid: str):
        """Retorna el guidance scale utilitzat durant la generació."""
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "cfg_scale")

    def get_steps(self, uuid: str):
        """Retorna el nombre de passos d'iteració del model."""
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "steps")

    def get_sampler(self, uuid: str):
        """Retorna l'algorisme de mostreig utilitzat."""
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "sampler")

    def get_generated(self, uuid: str):
        """Retorna el valor que indica si la imatge és generada."""
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "generated")

    def get_created_date(self, uuid: str):
        """Retorna la data de creació de la imatge."""
        u = str(uuid)
        if u not in self._images:
            return None
        return self._valor(u, "created_date")

    def get_dimensions(self, uuid: str):
        """Retorna les dimensions de la imatge en una tupla (width, height)."""
        u = str(uuid)
        if u not in self._images:
            return None
        return self._images[u].get("dimensions")

    def __len__(self) -> int:
        """Retorna el nombre d'imatges registrades."""
        return len(self._images)

    def __str__(self) -> str:
        """Retorna una representació textual de les dades d'imatges."""
        return f"ImageData(imatges={len(self._images)})"