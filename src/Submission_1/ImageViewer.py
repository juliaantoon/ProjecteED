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
import cfg
import PIL.Image as Image

class ImageViewer:
    def __init__(self, image_data=None):
        self.image_data = image_data

    def set_image_data(self, image_data: object) -> None:   # ens permet actualitxar el objecte ImageData si cal
        self.image_data = image_data

    def print_image(self, uuid: str, image_data: object ) -> None:
        if self._image_data is None:
            print("Error: No s'ha configurat cap instància d'ImageData a ImageViewer.")
            return
        
        file_path = self._image_data.get_filename(uuid)
        prompt_val = self._image_data.get_prompt(uuid)
        if prompt_val and prompt_val != "None" and len(prompt_val) > 50:
            prompt_val = prompt_val[:50] + "..."
        
        metadata = {
            "Dimensions": self._image_data.get_dimensions(uuid),
            "Prompt": self._image_data.get_prompt(uuid),
            "Model": self._image_data.get_model(uuid),
            "Seed": self._image_data.get_seed(uuid),
            "CFG Scale": self._image_data.get_cfg_scale(uuid),
            "Steps": self._image_data.get_steps(uuid),
            "Sampler": self._image_data.get_sampler(uuid),
            "Generated": self._image_data.get_generated(uuid),
            "Created Date": self._image_data.get_created_date(uuid),
            "UUID": uuid,
            "Path": file_path
        }

        print("Metadades de la imatge:")
        for key, value in metadata.items():
            if key == "Prompt" and value is not None and len(value) > 50:
                value = value[:50] + "..."  # Truncar el prompt si és molt llarg
            print(f"{key}: {value}")

    def show_file(self, file: str) -> None:
        try:
            with Image.open(file) as img:
                img.show()
        except Exception as e:
            print(f"Error en mostrar el fitxer '{file}': {e}")

    def show_image(self, uuid: str, mode: int = None) -> None:
        if mode is None:
            mode = getattr(cfg, "DISPLAY_MODE", 1)  # obte el mode per defecte

        if self._image_data is None:
            print("Error: No s'ha configurat cap instància d'ImageData a ImageViewer.")
            return

        file_path = self._image_data.get_file(uuid)

        if mode == 0:
            self.print_image(uuid)

        elif mode == 1:
            self.print_image(uuid)
            if file_path and file_path != "None":  # comprovem que el fitxer sigui valid
                self.show_file(file_path)
                input("\nPrem [ENTER] per continuar després de tancar la imatge...")

        elif mode == 2:
            if file_path and file_path != "None":  # comprovem que el fitxer sigui valid
                self.show_file(file_path)
                input("\nPrem [ENTER] per continuar després de tancar la imatge...")
        else:
            print(f"Mode desconegut: {mode}. Utilitzeu 0, 1 o 2.")

    def __str__(self) -> str:
        estat = "connectat" if self._image_data  is not None else "desconnectat"
        return f"ImageViewer(estat={estat})"