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
import ImageData
class ImageViewer:
    def print_image(self, uuid: str, image_data: object ) -> None:
        
        metadata = {
            "Dimensions": image_data.get_dimensions(uuid),
            "Prompt": image_data.get_prompt(uuid),
            "Model": image_data.get_model(uuid),
            "Seed": image_data.get_seed(uuid),
            "CFG Scale": image_data.get_cfg_scale(uuid),
            "Steps": image_data.get_steps(uuid),
            "Sampler": image_data.get_sampler(uuid),
            "Generated": image_data.get_generated(uuid),
            "Created Date": image_data.get_created_date(uuid),
            "UUID": uuid,
            "Path": self.cfg.get_file_path(uuid)  
        }

        # Imprimim les metadades de manera llegible
        print("Metadades de la imatge:")
        for key, value in metadata.items():
            if key == "Prompt" and value is not None and len(value) > 50:
                value = value[:50] + "..."  # Truncar el prompt si és molt llarg
            print(f"{key}: {value}")

    def show_file(self, file: str) -> None:
        try:
            img = Image.open(file)
            img.show()
        except Exception as e:
            print(f"Error en mostrar la imatge: {e}")

    def show_image(self, uuid: str, mode: int) -> None:
        file_path = #nose com trobar el path de l'uuid
        if mode == 0:
            self.print_image(uuid)
        elif mode == 1:
            self.print_image(uuid)
            cfg.DISPLAY_MODE = 1
            input("Premeu Enter per continuar...")
        elif mode == 2:
            self.show_file(file_path)
            input("Premeu Enter per continuar...")
        else:
            print(f"Mode desconegut: {mode}. Utilitzeu 0, 1 o 2.")