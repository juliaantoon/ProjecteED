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
    """Gestiona les galeries d'imatges i les seves operacions."""

    def __init__(self, image_id=None, image_viewer=None):
        """Inicialitza una galeria amb les seves dependències."""
        self._gallery_name = ""  # Nom de la galeria.
        self._description = ""  # Descripció del contingut de la galeria.
        self._created_date = ""  # Data de creació de la galeria.
        self._images = deque()  # UUID de les imatges de la galeria.
        self._viewer = image_viewer  # Visualitzador d'imatges.
        self._image_id = image_id  # Gestor d'UUID de les imatges.

    def set_viewer(self, image_viewer) -> None:
        """Assigna o actualitza el visualitzador d'imatges."""
        self._viewer = image_viewer

    def set_image_id(self, image_id) -> None:
        """Assigna o actualitza el gestor d'UUID."""
        self._image_id = image_id

    def _find_uuid(self, img_path: str):
        """Busca l'UUID d'una imatge a partir de la seva ruta."""
        if self._image_id is None:
            return None

        # Normalitza la ruta per compatibilitat entre sistemes operatius.
        norm_p = img_path.replace("\\", "/")
        root_dir_name = os.path.basename(
            os.path.normpath(cfg.ROOT_DIR)
        )  # Nom del directori arrel de les imatges.

        # Prepara diferents formats de ruta per buscar l'UUID.
        candidats = [norm_p]
        if norm_p.startswith(root_dir_name + "/"):
            candidats.append(norm_p[len(root_dir_name) + 1:])
        else:
            candidats.append(f"{root_dir_name}/{norm_p}")
        candidats.append(os.path.basename(norm_p))

        for c in candidats:
            uid = self._image_id.get_uuid(c)
            if uid is not None and uid != "None":
                return uid

        return None

    def load_file(self, file: str) -> None:
        """Carrega les dades d'una galeria des d'un fitxer JSON."""
        self._gallery_name = ""
        self._description = ""
        self._created_date = ""
        self._images = deque()

        if not file:
            return

        # Comprova primer la ruta indicada i després el directori arrel.
        full_path = file
        if not os.path.isfile(full_path):
            full_path = os.path.join(cfg.ROOT_DIR, file)

        if not os.path.isfile(full_path):
            raise FileNotFoundError(f"Galeria '{file}' no trobada.")

        try:
            # Obre el fitxer i carrega les dades del JSON.
            with open(full_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self._gallery_name = str(data.get("gallery_name", ""))
            self._description = str(data.get("description", ""))
            self._created_date = str(data.get("created_date", ""))

            raw_images = data.get("images", [])

            # Obté els UUID de les imatges i els afegeix a la galeria.
            for img_path in raw_images:
                if self._image_id is not None:
                    uuid = self._find_uuid(img_path)
                    if uuid:
                        self._images.append(uuid)
                else:
                    self._images.append(img_path)

        except Exception:
            # Reinicialitza la galeria si es produeix un error.
            self._gallery_name = ""
            self._description = ""
            self._created_date = ""
            self._images = deque()

    def show(self) -> None:
        """Mostra totes les imatges de la galeria."""
        if self._viewer is None:
            print("Error: No s'ha configurat cap ImageViewer. No es poden mostrar les imatges.")
            return

        print(f"Galeria: {self._gallery_name}")
        print(f"Descripció: {self._description}")
        print(f"Total d'imatges: {len(self._images)}")

        # Mostra cada imatge mitjançant el visualitzador.
        for uuid in list(self._images):
            self._viewer.show_image(uuid)

    def add_image_at_end(self, uuid: str) -> None:
        """Afegeix una imatge al final de la galeria."""
        self._images.append(uuid)

    def remove_first_image(self) -> None:
        """Elimina la primera imatge de la galeria."""
        if len(self._images) > 0:
            self._images.popleft()

    def remove_last_image(self) -> None:
        """Elimina l'última imatge de la galeria."""
        if len(self._images) > 0:
            self._images.pop()

    def __len__(self) -> int:
        """Retorna el nombre d'imatges de la galeria."""
        return len(self._images)

    def __str__(self) -> str:
        """Retorna una representació textual de la galeria."""
        return f"Gallery('{self._gallery_name}', imatges={len(self._images)})"