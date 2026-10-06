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
import json, ImageID,cfg,ImageViewer

class Gallery:
    def __init__(self, gestor_ids:ImageID,gestor_imatges=ImageViewer):
        self.gestor_ids = gestor_ids
        self.gestor_imatges=gestor_imatges
        self.image_uuids = []
        self.gallery_name = ""
        self.description = ""
        self.created_date = ""


    def load_file(self,file: str) -> None:
        """
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
            - load_file(file: str) -> None
            Llegeix un arxiu JSON amb la definició de la galeria.
            Ha de validar que cada imatge referenciada existeix a la col·lecció.
            Si una imatge no existeix, l'ignora i continua processant.
            Emmagatzema internament els UUID de les imatges vàlides.
        
        """

        with open(file, 'r', encoding='utf-8') as f:
            dades = json.load(f)
        self.gallery_name = dades.get("gallery_name","")
        self.description = dades.get("description","")
        self.created_date= dades.get("created_date","")
        images = dades.get("images",[])
        self.image_uuids=[]
        for im in images:
            ruta_neta=cfg.get_canonical_pathfile(im)
            uuid= self.gestor_ids.get_uuid(ruta_neta)

            if uuid is not None:
                self.image_uuids.append(uuid)

    def show (self):
        for image in self.image_uuids:
            self.gestor_imatges.show_image(image)

    def add_image_at_end(self,uuid:str):
        self.image_uuids.append(uuid)

    def remove_first_image(self) -> None:
        if self.image_uuids:
            self.image_uuids.pop(0)

    def remove_last_image(self) -> None:
        if self.image_uuids:
            self.image_uuids.pop()