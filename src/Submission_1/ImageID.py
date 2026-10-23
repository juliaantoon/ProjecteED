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
        self._file_to_uuid = {}
        self._active_uuids = set()
        self._uuid_to_file = {}

    def _canonical_file(self, file):
        if not isinstance(file, str) or not file:
            return None

        root = os.path.abspath(cfg.ROOT_DIR)

        # Si el path és absolut, el convertim a relatiu a ROOT_DIR.
        if os.path.isabs(file):
            canonical_file = os.path.relpath(file, root)

        else:
            canonical_file = file.replace("\\", "/")

            # Si ja inclou el nom de ROOT_DIR, l'eliminem.
            root_name = os.path.basename(os.path.normpath(root))

            if canonical_file.startswith(root_name + "/"):
                canonical_file = canonical_file[len(root_name) + 1:]

        canonical_file = os.path.normpath(canonical_file)
        return canonical_file.replace("\\", "/")

    def generate_uuid(self, file: str) -> str:
        canonical_file = self._canonical_file(file)

        if canonical_file is None:
            return None

        new_uuid = str(cfg.get_uuid(canonical_file))

        # Comprovem que l'UUID no estigui actiu.
        if new_uuid in self._active_uuids:
            print(f"Error: UUID {new_uuid} ja existeix per a un altre fitxer.")
            return None

        self._active_uuids.add(new_uuid)
        self._file_to_uuid[canonical_file] = new_uuid
        self._uuid_to_file[new_uuid] = canonical_file

        return new_uuid

    def get_uuid(self, file: str) -> str:
        canonical_file = self._canonical_file(file)

        if canonical_file is None:
            return None

        return self._file_to_uuid.get(canonical_file)

    def remove_uuid(self, uuid: str) -> None:
        if uuid in self._active_uuids:
            self._active_uuids.remove(uuid)

            file = self._uuid_to_file.pop(uuid, None)

            if file is not None:
                self._file_to_uuid.pop(file, None)

    def __len__(self) -> int:
        return len(self._active_uuids)

    def __str__(self) -> str:
        return f"ImageID(identificadors={len(self._active_uuids)})"