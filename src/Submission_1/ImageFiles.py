
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
    """Gestiona els fitxers PNG del directori d'imatges."""

    def __init__(self):
        """Inicialitza les estructures per controlar els fitxers."""
        self._files = set()  # Conjunt de rutes dels fitxers PNG trobats.
        self._added = []  # Llista de fitxers afegits.
        self._removed = []  # Llista de fitxers eliminats.
        self._path = None  # Directori que es vol explorar.

    def reload_fs(self, path: str = None) -> None:
        """Actualitza el registre de fitxers PNG del sistema."""
        # Estableix el directori que s'ha d'explorar.
        if path is not None:
            self._path = path
        elif self._path is None:
            self._path = cfg.ROOT_DIR

        base_dir = self._path
        new_files = set()

        # Comprova si el directori existeix i recorre les seves subcarpetes.
        if os.path.exists(base_dir):
            for r, dirs, files in os.walk(base_dir):
                for file in files:
                    if file.lower().endswith(".png"):
                        full_path = os.path.join(r, file)

                        # Obté la ruta absoluta i normalitza els separadors.
                        rel_path = os.path.abspath(full_path)
                        rel_path = rel_path.replace("\\", "/")
                        new_files.add(rel_path)

        # Compara els fitxers actuals amb els de l'última actualització.
        self._added = sorted(list(new_files - self._files))
        self._removed = sorted(list(self._files - new_files))
        self._files = new_files

    def files_added(self) -> list:
        """Retorna la llista de fitxers afegits en l'última actualització."""
        return list(self._added)

    def files_removed(self) -> list:
        """Retorna la llista de fitxers eliminats en l'última actualització."""
        return list(self._removed)

    def __len__(self) -> int:
        """Retorna el nombre total de fitxers PNG registrats."""
        return len(self._files)

    def __str__(self) -> str:
        """Retorna un resum textual de l'estat dels fitxers."""
        return f"ImageFiles(afegits={len(self._added)}, eliminats={len(self._removed)}, total={len(self._files)})"