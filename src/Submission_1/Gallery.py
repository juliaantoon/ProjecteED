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


class Gallery:
    def __init__(self, viewer=None, image_id=None):
        self._gallery_name = ""  # nom de la galeria
        self._description = ""  # descripcio del contingut de la galeria
        self._created_date = ""  # data de creacio de la galeria
        self._images = []  # llista d'UUID de les imatges que pertanyen a la galeria
        self._viewer = viewer  # instància de la classe ImageViewer per mostrar les imatges
        self._image_id = image_id  # instància de la classe ImageID per obtenir els UUID de les imatges

    def set_viewer(self, viewer) -> None:  # assigna o actualitza el visualitzador d'imatges
        self._viewer = viewer

    def set_image_id(self, image_id) -> None:  # assigna o actualitza el gestor ImageID
        self._image_id = image_id

    def load_file(self, file: str) -> None:
        if not os.path.isfile(file) and hasattr(cfg, "ROOT_DIR"):  # comprova si el fitxer és relatiu a ROOT_DIR
            full_path = os.path.join(cfg.ROOT_DIR, file)  # construeix la ruta sencera
        else:
            full_path = file  # usa la ruta directa

        try:
            with open(full_path, 'r', encoding='utf-8') as f:  # obre l'arxiu usant la ruta completa
                data = json.load(f)  # carrega les dades del fitxer JSON a un diccionari
            self._gallery_name = data.get("gallery_name", "")
            self._description = data.get("description", "")
            self._created_date = data.get("created_date", "")
            self._images = []  # reinicia la llista d'imatges

            raw_images = data.get("images", [])  # obté la llista d'imatges del JSON
            for img_path in raw_images:
                if self._image_id is not None:
                    uuid = self._image_id.get_uuid(img_path)  # obté l'UUID de la imatge a partir del path
                    if uuid and uuid != "None":  # si l'UUID és vàlid, afegeix-lo a la llista d'imatges
                        self._images.append(uuid)
                else:
                    self._images.append(img_path)
        except Exception as e:
            print(f"Error carregant la galeria '{file}': {e}")

    def show(self) -> None:  # mostra totes les imatges
        if self._viewer is None:
            print("Error: No s'ha configurat cap ImageViewer. No es poden mostrar les imatges.")
            return
        print(f"Galeria: {self._gallery_name}")
        print(f"Descripció: {self._description}")
        print(f"Total d'imatges: {len(self._images)}")
        for uuid in self._images:
            self._viewer.show_image(uuid)  # mostra cada imatge utilitzant el visualitzador

    def add_image_at_end(self, uuid: str) -> None:  # afegeix una imatge al final de la galeria
        self._images.append(uuid)

    def remove_first_image(self) -> None:  # elimina la primera imatge de la galeria
        if len(self._images) > 0:
            self._images.pop(0)

    def remove_last_image(self) -> None:  # elimina l'última imatge de la galeria
        if len(self._images) > 0:
            self._images.pop()