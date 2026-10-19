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

Mètodes a implementar:
- load_file(file: str) -> None
        Llegeix un arxiu JSON amb la definició de la galeria.
        Ha de validar que cada imatge referenciada existeix a la col·lecció.
        Si una imatge no existeix, l'ignora i continua processant.
        Emmagatzema internament els UUID de les imatges vàlides.

- show() -> None
        Visualitza totes les imatges de la galeria en ordre utilitzant
        ImageViewer.show_image().

- add_image_at_end(uuid: str) -> None
        Afegeix una imatge al final de la galeria.

- remove_first_image() -> None
        Elimina la primera imatge de la galeria.

- remove_last_image() -> None
        Elimina l'última imatge de la galeria.

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
        self._gallery_name = ""  # nom de la galeria
        self._description = ""  # descripcio del contingut de la galeria
        self._created_date = ""  # data de creacio de la galeria
        self._images = deque()  # llista d'UUID de les imatges que pertanyen a la galeria
        self._viewer = image_viewer  # instància de la classe ImageViewer per mostrar les imatges
        self._image_id = image_id  # instància de la classe ImageID per obtenir els UUID de les imatges

    def set_viewer(self, image_viewer) -> None:
        self._viewer = image_viewer  # assigna o actualitza el visualitzador d'imatges

    def set_image_id(self, image_id) -> None:
        self._image_id = image_id  # assigna o actualitza el gestor ImageID

    def _find_uuid(self, img_path: str):
        if self._image_id is None or not isinstance(img_path, str):
            return None

        norm_p = img_path.replace("\\", "/")  # normalitza el path per compatibilitat entre sistemes operatius
        root_dir_name = os.path.basename(os.path.normpath(cfg.ROOT_DIR))  # obtenim el nom del directori arrel

        candidats = [norm_p]  # possibles formats del path per buscar l'UUID

        if norm_p.startswith(root_dir_name + "/"):
            candidats.append(norm_p[len(root_dir_name) + 1:])
        else:
            candidats.append(f"{root_dir_name}/{norm_p}")

        candidats.append(os.path.basename(norm_p))  # també provem amb el nom del fitxer

        for c in candidats:
            uid = self._image_id.get_uuid(c)

            if uid is not None and uid != "None":
                return uid

        return None

    def load_file(self, file: str) -> None:
        self._gallery_name = ""  # reiniciem el nom de la galeria
        self._description = ""  # reiniciem la descripció
        self._created_date = ""  # reiniciem la data
        self._images = deque()  # reiniciem la llista d'imatges

        full_path = file

        if not os.path.isfile(full_path):
            full_path = os.path.join(cfg.ROOT_DIR, file)  # provem la ruta relativa a ROOT_DIR

        if not os.path.isfile(full_path):
            return  # si no existeix el JSON, deixem la galeria buida

        try:
            with open(full_path, 'r', encoding='utf-8') as f:  # obrim l'arxiu JSON
                data = json.load(f)  # carreguem les dades del fitxer

            if not isinstance(data, dict):  # comprovem que les dades siguin un diccionari
                return

            self._gallery_name = str(data.get("gallery_name", ""))
            self._description = str(data.get("description", ""))
            self._created_date = str(data.get("created_date", ""))

            raw_images = data.get("images", [])  # obtenim la llista d'imatges del JSON

            if not isinstance(raw_images, list):  # comprovem que sigui una llista
                return

            for img_path in raw_images:
                uuid = self._find_uuid(img_path)  # obtenim l'UUID a partir del path

                if uuid is not None:  # només afegim imatges que existeixen a ImageID
                    self._images.append(uuid)

        except Exception:
            self._gallery_name = ""
            self._description = ""
            self._created_date = ""
            self._images = deque()  # si hi ha un error, deixem la galeria buida

    def show(self) -> None:
        if self._viewer is None:  # comprovem que hi hagi un visualitzador
            print("Error: No s'ha configurat cap ImageViewer. No es poden mostrar les imatges.")
            return

        print(f"Galeria: {self._gallery_name}")
        print(f"Descripció: {self._description}")
        print(f"Total d'imatges: {len(self._images)}")

        for uuid in list(self._images):
            self._viewer.show_image(uuid)  # mostra cada imatge utilitzant el visualitzador

    def add_image_at_end(self, uuid: str) -> None:
        self._images.append(uuid)  # afegeix la imatge al final de la galeria

    def remove_first_image(self) -> None:
        if len(self._images) > 0:  # comprovem que la galeria no estigui buida
            self._images.popleft()  # eliminem la primera imatge

    def remove_last_image(self) -> None:
        if len(self._images) > 0:  # comprovem que la galeria no estigui buida
            self._images.pop()  # eliminem l'última imatge

    def __len__(self) -> int:
        return len(self._images)

    def __str__(self) -> str:
        return f"Gallery('{self._gallery_name}', imatges={len(self._images)})"