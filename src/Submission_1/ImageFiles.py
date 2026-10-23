# -*- coding: utf-8 -*-
"""
ImageFiles.py : ** REQUIRED ** El vostre codi de la classe ImageFiles.

Aquesta classe s'encarrega de gestionar el llistat d'arxius PNG dins la col·lecció d'imatges.

Funcionalitat:
- Recórrer el filesystem a partir de ROOT_DIR per trobar tots els arxius PNG
- Mantenir una representació en memòria dels arxius presents
- Detectar quins arxius s'han afegit o eliminat des de l'última lectura

Mètodes a implementar:
- reload_fs(path: str) -> None
        Recorre el directori especificat i actualitza la llista d'arxius PNG.
        Detecta els arxius nous i els que s'han eliminat.

- files_added() -> list
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han afegit des de l'última crida a reload_fs().

- files_removed() -> list
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han eliminat des de l'última crida a reload_fs().

Notes:
- Els paths han de ser sempre relatius a ROOT_DIR
- Només considereu arxius amb extensió .png (case-insensitive)
- Heu de recórrer tots els subdirectoris recursivament
"""
import os
import cfg

class ImageFiles:

    def __init__(self):
        self._files = set() # conjunt per emmagatzemar els paths relatius dels arxius PNG trobats
        self._added = [] # llista buida per emmagtzemar rutes dels fitxers que sacaben d'afegir
        self._removed = [] # llista buida per emmagatzemar rutes dels fitxers que s'han eliminat
        self._path = None

    def reload_fs(self, path: str = None) -> None:
        if path is not None: # comprova si han passat el path com a parametre, sino fa servir ROOT_DIR
            self._path = path
        elif self._path is None:
            self._path = cfg.ROOT_DIR

        base_dir = self._path
        new_files = set()

        if os.path.exists(base_dir):
            for r, dirs, files in os.walk(base_dir): # recorre tots els directoris
                for file in files:
                    if file.lower().endswith(".png"): # comprova si es .png
                        full_path = os.path.join(r, file)
                        rel_path = os.path.relpath(full_path, cfg.ROOT_DIR) # obtenim el path relatiu a ROOT_DIR
                        rel_path = rel_path.replace("\\", "/") # normalitzem els separadors
                        new_files.add(rel_path) # afegim la ruta relativa

        self._added = sorted(list(new_files - self._files)) # llista dels arxius afegits
        self._removed = sorted(list(self._files - new_files)) # llista dels arxius eliminats
        self._files = new_files # actualitzem la llista d'arxius

    def files_added(self) -> list:
        return list(self._added) # retorna els arxius afegits des de l'ultima crida

    def files_removed(self) -> list:
        return list(self._removed) # retorna els arxius eliminats des de l'ultima crida

    def __len__(self) -> int:
        return len(self._files) # retorna el nombre total d'arxius PNG

    def __str__(self) -> str:
        return f"ImageFiles(afegits={len(self._added)}, eliminats={len(self._removed)}, total={len(self._files)})"
