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
        self._files = set()   # paths relatius dels PNG actuals
        self._added = []      # afegits des de l'última crida a reload_fs()
        self._removed = []    # eliminats des de l'última crida a reload_fs()
        self._last_path = None

    def reload_fs(self, path: str = None) -> None:
        if path is not None:
            self._last_path = path
        elif self._last_path is None:
            self._last_path = cfg.ROOT_DIR

        scan_dir = self._last_path
        new_files = set()

        if os.path.exists(scan_dir):
            for r, dirs, files in os.walk(scan_dir): # recorre recursivament tots els subdirectoris a partir del path especificat
                for file in files:
                    if file.lower().endswith(".png"): # només considerem arxius amb extensió .png 
                        full_path = os.path.join(r, file) # obtenim el path complet de l'arxiu
                        # Si escanejem un directori extern (ex: temporal), relatiu a scan_dir; si no, relatiu a cfg.ROOT_DIR
                        if path is not None and path != cfg.ROOT_DIR:
                            rel_path = os.path.relpath(full_path, scan_dir)
                        else:
                            rel_path = os.path.relpath(full_path, cfg.ROOT_DIR)
                        rel_path = rel_path.replace("\\", "/") # convertim els separadors de path a "/" per compatibilitat amb JSON
                        new_files.add(rel_path) # afegim la ruta relativa a la llista de nous arxius

        self._added = sorted(list(new_files - self._files)) # llista dels arxius afegits
        self._removed = sorted(list(self._files - new_files)) # llista dels arxius eliminats
        self._files = new_files # actualitzem la llista d'arxius amb els nous arxiusmj

    def files_added(self) -> list:
        return list(self._added)

    def files_removed(self) -> list:
        return list(self._removed)

    def __len__(self) -> int:
        return len(self._files)

    def __str__(self) -> str:
        return f"ImageFiles(afegits={len(self._added)}, eliminats={len(self._removed)}, total={len(self._files)})"