
# -*- coding: utf-8 -*-
"""
Gallery.py : ** REQUIRED ** El vostre codi de la classe Gallery.

Aquesta classe s'encarrega de gestionar galeries d'imatges en format JSON.

Funcionalitat:
- Llegir galeries des d'arxius JSON
- Visualitzar totes les imatges d'una galeria
- Afegir i eliminar imatges de la galeria
"""
import os
import json
import cfg
from collections import deque


class Gallery:
    def __init__(self, image_id=None, image_viewer=None):
        self._gallery_name = ""  # nom de la galeria
        self._description = ""  # descripcio del contingut de la galeria
        self._created_date = ""  # data de creacio de la galeria
        self._images = deque()  # llista d'UUID de les imatges que pertanyen a la galeria
        self._viewer = image_viewer  # instància de la classe ImageViewer per mostrar les imatges
        self._image_id = image_id  # instància de la classe ImageID per obtenir els UUID de les imatges

    def set_viewer(self, image_viewer) -> None:  # assigna o actualitza el visualitzador d'imatges
        self._viewer = image_viewer

    def set_image_id(self, image_id) -> None:  # assigna o actualitza el gestor ImageID
        self._image_id = image_id

    def _find_uuid(self, img_path: str):
        if self._image_id is None:
            return None

        norm_p = str(img_path).replace("\\", "/") # normalitza el path per compatibilitat amb JSON i diferents sistemes operatius
        root_dir = cfg.get_root()
        root_dir_name = os.path.basename(os.path.normpath(root_dir))

        candidats = [norm_p] # llista de possibles paths per buscar l'UUID segons diferents formats

        # Si el JSON inclou generated_images/ al principi, traiem aquest directori
        if norm_p.startswith(root_dir_name + "/"):
            candidats.append(norm_p[len(root_dir_name) + 1:])

        # També provem el nom del fitxer sense directoris
        candidats.append(os.path.basename(norm_p))

        # Provem les diferents rutes directament amb ImageID
        for c in candidats:
            uid = self._image_id.get_uuid(c)
            if uid is not None:
                return uid

        # Comparem les rutes absolutes per si ImageID les havia guardat així
        possibles_paths = set()
        for c in candidats:
            if os.path.isabs(c):
                possibles_paths.add(os.path.normcase(os.path.realpath(c)))
            else:
                possibles_paths.add(os.path.normcase(os.path.realpath(os.path.join(root_dir, c))))

        # Revisem els fitxers registrats a ImageID
        for file_path, uid in getattr(self._image_id, "_file_to_uuid", {}).items():
            if os.path.isabs(file_path):
                path_registrat = os.path.normcase(os.path.realpath(file_path))
            else:
                path_registrat = os.path.normcase(os.path.realpath(os.path.join(root_dir, file_path)))

            if path_registrat in possibles_paths:
                return uid

        return None

    def load_file(self, file: str) -> None:
        self._gallery_name = ""
        self._description = ""
        self._created_date = ""
        self._images = deque()

        full_path = file
        if not os.path.isfile(full_path):
            full_path = os.path.join(cfg.get_root(), file)

        if not os.path.isfile(full_path):
            return

        try:
            with open(full_path, 'r', encoding='utf-8') as f:  # obre l'arxiu usant la ruta completa
                data = json.load(f)  # carrega les dades del fitxer JSON a un diccionari

            self._gallery_name = str(data.get("gallery_name", data.get("name", "")))
            self._description = str(data.get("description", ""))
            self._created_date = str(data.get("created_date", data.get("creation_date", "")))

            raw_images = data.get("images", []) # obté la llista d'imatges del JSON

            if not isinstance(raw_images, list):
                return

            for img_path in raw_images:
                if self._image_id is not None:
                    uuid = self._find_uuid(img_path) # obté l'UUID de la imatge a partir del path
                    if uuid is not None: # si l'UUID és vàlid, afegeix-lo a la llista d'imatges
                        self._images.append(uuid)
                else:
                    self._images.append(img_path)

        except (json.JSONDecodeError, OSError, TypeError, AttributeError):
            self._gallery_name = ""
            self._description = ""
            self._created_date = ""
            self._images = deque()

    def show(self) -> None:  # mostra totes les imatges
        if self._viewer is None:
            print("Error: No s'ha configurat cap ImageViewer. No es poden mostrar les imatges.")
            return

        print(f"Galeria: {self._gallery_name}")
        print(f"Descripció: {self._description}")
        print(f"Total d'imatges: {len(self._images)}")

        for uuid in self._images:
            self._viewer.show_image(uuid) # mostra cada imatge utilitzant el visualitzador

    def add_image_at_end(self, uuid: str) -> None:  # afegeix una imatge al final de la galeria
        self._images.append(uuid)

    def remove_first_image(self) -> None:  # elimina la primera imatge de la galeria
        if len(self._images) > 0:
            self._images.popleft()

    def remove_last_image(self) -> None:  # elimina l'última imatge de la galeria
        if len(self._images) > 0:
            self._images.pop()

    def __len__(self) -> int:  # retorna el nombre d'imatges de la galeria
        return len(self._images)

    def __str__(self) -> str:  # representació en text de la galeria
        return f"Gallery('{self._gallery_name}', imatges={len(self._images)})"
