# -*- coding: utf-8 -*-
"""
ImageViewer.py : ** REQUIRED ** El vostre codi de la classe ImageViewer.

Aquesta classe s'encarrega de visualitzar imatges i mostrar les seves metadades.

Funcionalitat:
- Imprimir per pantalla les metadades d'una imatge
- Mostrar la imatge en pantalla
- Combinar ambdues accions segons la configuració

Mètodes a implementar:
- print_image(uuid: str) -> None
        Imprimeix per pantalla totes les metadades de la imatge identificada
        per l'UUID. Ha de mostrar:
- Dimensions (width x height)
- Prompt (truncat si és molt llarg)
- Model
- Seed
- CFG Scale
- Steps
- Sampler
- Generated
- Created Date
- UUID
- Path de l'arxiu

- show_file(file: str) -> None
        Mostra la imatge especificada utilitzant PIL.
        Aquesta funció NO espera que la imatge es tanqui (asíncrona).

- show_image(uuid: str, mode: int) -> None
        Combina print_image() i show_file() segons el mode especificat:
- mode 0: només metadades
- mode 1: metadades + imatge
- mode 2: només imatge

        Aquesta funció ha d'esperar que l'usuari tanqui la imatge abans
        de retornar (síncrona). Podeu utilitzar input() per fer una pausa.

Notes:
- Utilitzeu cfg.DISPLAY_MODE per determinar el comportament per defecte
- Per mostrar imatges: img.show() de PIL
- Gestioneu les excepcions si la imatge no es pot mostrar
- El format de sortida ha de ser llegible i ben organitzat
"""
import cfg, os
from PIL import Image

class ImageViewer:
    def __init__(self, image_data=None):
        self._image_data = image_data

    def set_image_data(self, image_data: object) -> None:   # ens permet actualitzar l'objecte ImageData si cal
        self._image_data = image_data

    def print_image(self, uuid: str) -> None:
        if self._image_data is None:
            print("Error: No s'ha configurat cap instància d'ImageData a ImageViewer.")
            return
        
        file_path = self._image_data.get_filename(uuid)
        prompt_val = self._image_data.get_prompt(uuid)
        if prompt_val and prompt_val != "None" and len(prompt_val) > 50:
            prompt_val = prompt_val[:50] + "..."  # Truncar el prompt si és molt llarg

        dims = self._image_data.get_dimensions(uuid)
        if dims and isinstance(dims, (tuple, list)) and len(dims) >= 2:
            dims_txt = f"{dims[0]} x {dims[1]}"
        else:
            dims_txt = "0 x 0"

        metadata = {
            "Dimensions": dims_txt,
            "Prompt": prompt_val if prompt_val is not None else "None",
            "Model": self._image_data.get_model(uuid) or "None",
            "Seed": self._image_data.get_seed(uuid) or "None",
            "CFG Scale": self._image_data.get_cfg_scale(uuid) or "None",
            "Steps": self._image_data.get_steps(uuid) or "None",
            "Sampler": self._image_data.get_sampler(uuid) or "None",
            "Generated": self._image_data.get_generated(uuid) or "None",
            "Created Date": self._image_data.get_created_date(uuid) or "None",
            "UUID": uuid if uuid is not None else "",
            "Path": file_path if file_path is not None else "None"
        }

        # Imprimim les metadades de manera llegible
        print("Metadades de la imatge:")
        for key, value in metadata.items():
            print(f"{key}: {value}")

    def show_file(self, file: str) -> None: # Mostra la imatge especificada utilitzant PIL 
        if not file or file == "None":
            return
        if not os.path.isfile(file):
            file = os.path.join(cfg.ROOT_DIR, file)
        try:
            with Image.open(file) as img:  # Obrim la imatge amb Pillow
                img.show()  # Obre el visor d'imatges del sistema operatiu
        except Exception as e:
            print(f"Error en mostrar el fitxer '{file}': {e}")  # Gestió d'errors si la imatge no existeix 

    def show_image(self, uuid: str, mode: int = None) -> None:
        if mode is None:
            mode = cfg.DISPLAY_MODE  # obte el mode per defecte

        if self._image_data is None:
            print("Error: No s'ha configurat cap instància d'ImageData a ImageViewer.")
            return

        file_path = self._image_data.get_filename(uuid)

        if mode == 0:
            self.print_image(uuid)

        elif mode == 1:
            self.print_image(uuid)
            if file_path and file_path != "None":  # comprovem que el fitxer sigui valid
                self.show_file(file_path)

        elif mode == 2:
            if file_path and file_path != "None":  # comprovem que el fitxer sigui valid
                self.show_file(file_path)
        else:
            print(f"Mode desconegut: {mode}. Utilitzeu 0, 1 o 2.")

    def __str__(self) -> str:
        estat = "connectat" if self._image_data is not None else "desconnectat"
        return f"ImageViewer(estat='{estat}')"