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
        self._files = set()   # paths relatius a ROOT_DIR dels PNG actuals
        self._added = []      # afegits des de l'última crida a reload_fs()
        self._removed = []    # eliminats des de l'última crida a reload_fs()
 
    def reload_fs(self, path: str = None) -> None:
        # Directori a recórrer: el indicat o, per defecte, el ROOT_DIR actual
        base_dir = path if path is not None else cfg.ROOT_DIR
        root_dir = cfg.ROOT_DIR
 
        new_files = set()
        if os.path.exists(base_dir):
            for r, dirs, files in os.walk(base_dir):
                for file in files:
                    if file.lower().endswith(".png"):
                        full_path = os.path.join(r, file)
                        # IMPORTANT: relatiu a ROOT_DIR (no al directori recorregut)
                        try:
                            rel_path = os.path.relpath(full_path, root_dir)
                        except ValueError:
                            rel_path = full_path
                        new_files.add(rel_path.replace("\\", "/"))
 
        self._added = sorted(new_files - self._files)
        self._removed = sorted(self._files - new_files)
        self._files = new_files
 
    def files_added(self) -> list:
        return list(self._added)
 
    def files_removed(self) -> list:
        return list(self._removed)
 
    def __len__(self) -> int:
        return len(self._files)
 
    def __str__(self) -> str:
        return (f"ImageFiles(afegits={len(self._added)}, "
                f"eliminats={len(self._removed)}, total={len(self._files)})")