# -*- coding: utf-8 -*-
"""
ImageID.py : ** REQUIRED ** El vostre codi de la classe ImageID.

Aquesta classe s'encarrega de generar i gestionar identificadors únics (UUID)
per a cada imatge de la col·lecció.

Funcionalitat:
    - Generar un UUID únic a partir del path canònic d'un arxiu
    - Mantenir un registre dels UUID generats per evitar col·lisions
    - Permetre consultar i eliminar UUID

Mètodes a implementar:
    - generate_uuid(file: str) -> str
        Genera un UUID únic per a l'arxiu especificat.
        Ha de comprovar que el UUID no estigui ja en ús.
        Si hi ha col·lisió (cas extremadament improbable), retorna None i
        mostra un missatge d'error.

    - get_uuid(file: str) -> str
        Retorna el UUID associat a l'arxiu, si ja ha estat generat.
        Si no existeix, retorna None.

    - remove_uuid(uuid: str) -> None
        Elimina el UUID del registre d'identificadors actius.
        Després d'eliminar-lo, aquest UUID es podrà tornar a utilitzar.

Notes:
    - Els UUID han de seguir el format estàndard (128 bits)
    - Podeu utilitzar la funció cfg.get_uuid() com a base
    - Els UUID s'emmagatzemen com a strings
    - Un UUID només es pot generar una vegada (fins que s'elimini)
"""
import os
import cfg

class ImageID:
    def __init__(self):
        self._file_to_uuid = {}        # diccionari per saber quin uuid té cada fitxer
        self._active_uuids = set()     # conjunt per saber quins uuid estan actius
        self._uuid_to_file = {}        # diccionari per saber quin fitxer té cada uuid

    def generate_uuid(self, file: str) -> str:
        if not isinstance(file, str) or not file:
            return None

        canonical_file = cfg.get_canonical_pathfile(file) # obtenim el path canònic del fitxer
        canonical_file = canonical_file.replace("\\", "/") # normalitzem els separadors

        new_uuid = str(cfg.get_uuid(canonical_file)) # generem el UUID a partir del path canònic

        if new_uuid in self._active_uuids: # comprovem si ja existeix
            print(f"Error: UUID {new_uuid} ja existeix per a un altre fitxer.")
            return None

        self._active_uuids.add(new_uuid) # afegim el nou uuid al conjunt d'uuids actius
        self._file_to_uuid[canonical_file] = new_uuid # associem el fitxer amb el uuid
        self._uuid_to_file[new_uuid] = canonical_file # associem el uuid amb el fitxer
        return new_uuid # retornem el uuid generat

    def get_uuid(self, file: str) -> str:
        if not isinstance(file, str):
            return None

        canonical_file = cfg.get_canonical_pathfile(file) # obtenim el path canònic
        canonical_file = canonical_file.replace("\\", "/") # normalitzem els separadors
        return self._file_to_uuid.get(canonical_file) # retornem el uuid o None si no existeix

    def remove_uuid(self, uuid: str) -> None:
        if uuid in self._active_uuids: # comprovem si l'uuid està actiu
            self._active_uuids.remove(uuid) # eliminem l'uuid del conjunt
            file = self._uuid_to_file.pop(uuid, None) # obtenim i eliminem el fitxer associat
            if file is not None:
                self._file_to_uuid.pop(file, None) # eliminem també la relació inversa

    def __len__(self) -> int:
        return len(self._file_to_uuid)

    def __str__(self) -> str:
        return f"ImageID(identificadors={len(self._file_to_uuid)})"
