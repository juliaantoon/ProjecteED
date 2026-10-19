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

    def set_viewer(self, image_viewer) -> None:  # assigna o actualitza el visualitzador d'imatges
        self._viewer = image_viewer

    def set_image_id(self, image_id) -> None:  # assigna o actualitza el gestor ImageID
        self._image_id = image_id

    def _find_uuid(self, img_path: str): 
        if self._image_id is None:
            return None
        norm_p = img_path.replace("\\", "/") # normalitza el path per compatibilitat amb JSON i diferents sistemes operatius
        root_dir_name = os.path.basename(os.path.normpath(cfg.ROOT_DIR)) # obtenim el nom del directori arrel de la col·lecció d'imatges

        candidats = [norm_p] # llista de possibles paths per buscar l'UUID segons diferents formats (relatiu, absolut, només nom de fitxer)
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
        self._gallery_name = ""             
        self._description = ""              
        self._created_date = ""             
        self._images = deque() 

        full_path = file
        if not os.path.isfile(full_path):
            full_path = os.path.join(cfg.ROOT_DIR, file)

        if not os.path.isfile(full_path):
            return

        try:
            with open(full_path, 'r', encoding='utf-8') as f:  # obre l'arxiu usant la ruta completa
                data = json.load(f)  # carrega les dades del fitxer JSON a un diccionari
            self._gallery_name = str(data.get("gallery_name", ""))
            self._description = str(data.get("description", ""))
            self._created_date = str(data.get("created_date", ""))

            raw_images = data.get("images", [])  # obté la llista d'imatges del JSON
            for img_path in raw_images:
                if self._image_id is not None:
                    uuid = self._find_uuid(img_path)  # obté l'UUID de la imatge a partir del path
                    if uuid:  # si l'UUID és vàlid, afegeix-lo a la llista d'imatges
                        self._images.append(uuid)
                else:
                    self._images.append(img_path)
        except Exception:
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
        for uuid in list(self._images):
            self._viewer.show_image(uuid)  # mostra cada imatge utilitzant el visualitzador

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