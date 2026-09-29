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
import cfg

class ImageID:
    def __init__(self):
        self._file_to_uuid = {}        # diccionari per saber quin uuid té cada fitxer
        self._active_uuids = set()     # conjunt per saber quins uuid estan actius (evita duplicats)

    def generate_uuid(self, file: str) -> str:
        new_uuid = str(cfg.get_uuid(file))  # generem un nou uuid 

        if new_uuid in self._active_uuids:  # comprovem si ja existeix (col·lisió)
            print(f"Error: UUID {new_uuid} ja existeix per a un altre fitxer.")
            return None
        else:
            self._active_uuids.add(new_uuid)
            self._file_to_uuid[file] = new_uuid
            return new_uuid

    def get_uuid(self, file: str) -> str:
        if file in self._file_to_uuid:
            return self._file_to_uuid[file]
        else:
            return None

    def remove_uuid(self, uuid: str) -> None:
        if uuid in self._active_uuids:       # mirem si el uuid està actiu
            self._active_uuids.remove(uuid)  # si hi és, l'alliberem del conjunt

            for file in list(self._file_to_uuid.keys()):
                if self._file_to_uuid[file] == uuid:
                    del self._file_to_uuid[file]  # esborrem el fitxer del diccionari
                    break


# COMPROVACIÓ 
if __name__ == "__main__":
    gestor_id = ImageID()

    print("--- 1. GENERAR UUID ---")
    foto = "animals/gat.png"
    uuid_generat = gestor_id.generate_uuid(foto)
    print(f"Fitxer: {foto} -> UUID: {uuid_generat}")

    print("\n--- 2. CONSULTAR UUID (get_uuid) ---")
    consulta_existent = gestor_id.get_uuid(foto)
    print(f"Consulta d'arxiu existent ({foto}): {consulta_existent}")

    consulta_inexistent = gestor_id.get_uuid("inexistent.png")
    print(f"Consulta d'arxiu desconegut: {consulta_inexistent}")

    print("\n--- 3. ELIMINAR UUID (remove_uuid) ---")
    print(f"Eliminant UUID: {uuid_generat}...")
    gestor_id.remove_uuid(uuid_generat)

    comprovacio_despres = gestor_id.get_uuid(foto)
    print(f"Consulta de {foto} després d'esborrar: {comprovacio_despres}")
    print(f"Està el UUID encara a la llista d'actius?: {uuid_generat in gestor_id._active_uuids}")
        


