# -*- coding: utf-8 -*-
"""
Gallery.py : ** REQUIRED ** El vostre codi de la classe Gallery.

Aquesta classe s'encarrega de gestionar galeries d'imatges en format JSON.

Funcionalitat:
- Llegir galeries des d'arxius JSON
- Visualitzar totes les imatges d'una galeria
- Afegir i eliminar imatges de la galeria

Format JSON d'una galeria:
{
  "gallery_name": "Cyberpunk Cities",
  "description": "Collection of futuristic urban landscapes",
  "created_date": "2025-09-30",
  "images": [
    "generated_images/city_001.png",
    "generated_images/city_neon_12.png",
    "generated_images/urban_street_45.png"
  ]
}

Notes:
- Utilitzeu la llibreria json per llegir els arxius
- Els paths dins el JSON són relatius a ROOT_DIR
- Cada galeria és un objecte independent (instància de Gallery)
- Podeu tenir múltiples galeries actives simultàniament
- Les operacions d'afegir/eliminar són ràpides (no busquen a la llista)
"""

import os
import json
import cfg
from collections import deque


class Gallery:
    def __init__(self, image_id=None, image_viewer=None):
        self._gallery_name = ""
        self._description = ""
        self._created_date = ""
        self._images = deque()
        self._viewer = image_viewer
        self._image_id = image_id

    def set_viewer(self, image_viewer) -> None:
        self._viewer = image_viewer

    def set_image_id(self, image_id) -> None:
        self._image_id = image_id

    def _resolve_image_path(self, img_path):
        norm_path = str(img_path).replace("\\", "/")
        root_dir_name = os.path.basename(os.path.normpath(cfg.ROOT_DIR))

        # Evita repetir el nom de ROOT_DIR si ja apareix al path.
        if norm_path.startswith(root_dir_name + "/"):
            norm_path = norm_path[len(root_dir_name) + 1:]

        full_path = os.path.join(cfg.ROOT_DIR, norm_path)

        if os.path.isfile(full_path):
            return full_path

        # També comprova si el path ja és vàlid des del directori actual.
        if os.path.isfile(img_path):
            return os.path.abspath(img_path)

        return None

    def _find_uuid(self, img_path: str):
        if self._image_id is None:
            return None

        norm_p = str(img_path).replace("\\", "/")
        root_dir_name = os.path.basename(os.path.normpath(cfg.ROOT_DIR))

        candidats = [norm_p]

        if norm_p.startswith(root_dir_name + "/"):
            candidats.append(norm_p[len(root_dir_name) + 1:])
        else:
            candidats.append(f"{root_dir_name}/{norm_p}")

        # Busca també utilitzant la ruta absoluta de la imatge.
        full_path = self._resolve_image_path(img_path)

        if full_path is not None:
            candidats.append(full_path)

        candidats.append(os.path.basename(norm_p))

        for c in candidats:
            uid = self._image_id.get_uuid(c)

            if uid is not None and uid != "None":
                return uid

        return None

    def load_file(self, file: str) -> None:
        self._gallery_name = ""
        self._description = ""
        self._created_date = ""
        self._images = deque()

        if not file:
            return

        full_path = file

        if not os.path.isfile(full_path):
            full_path = os.path.join(cfg.ROOT_DIR, file)

        if not os.path.isfile(full_path):
            raise FileNotFoundError(f"Galeria '{file}' no trobada.")

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self._gallery_name = str(data.get("gallery_name", ""))
            self._description = str(data.get("description", ""))
            self._created_date = str(data.get("created_date", ""))

            raw_images = data.get("images", [])

            for img_path in raw_images:
                if self._image_id is not None:
                    # Comprova que la imatge existeix.
                    resolved_path = self._resolve_image_path(img_path)

                    if resolved_path is None:
                        continue

                    # Obté el UUID de la imatge.
                    uuid = self._find_uuid(img_path)

                    if uuid:
                        self._images.append(uuid)

                else:
                    self._images.append(img_path)

        except Exception:
            self._gallery_name = ""
            self._description = ""
            self._created_date = ""
            self._images = deque()

    def show(self) -> None:
        if self._viewer is None:
            print("Error: No s'ha configurat cap ImageViewer. No es poden mostrar les imatges.")
            return

        print(f"Galeria: {self._gallery_name}")
        print(f"Descripció: {self._description}")
        print(f"Total d'imatges: {len(self._images)}")

        for uuid in list(self._images):
            self._viewer.show_image(uuid)

    def add_image_at_end(self, uuid: str) -> None:
        self._images.append(uuid)

    def remove_first_image(self) -> None:
        if len(self._images) > 0:
            self._images.popleft()

    def remove_last_image(self) -> None:
        if len(self._images) > 0:
            self._images.pop()

    def __len__(self) -> int:
        return len(self._images)

    def __str__(self) -> str:
        return f"Gallery('{self._gallery_name}', imatges={len(self._images)})"