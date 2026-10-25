# -*- coding: utf-8 -*-
"""
SearchMetadata.py : ** REQUIRED ** El vostre codi de la classe SearchMetadata.

Aquesta classe s'encarrega de cercar imatges segons criteris basats en metadades.

Funcionalitat:
- Cercar imatges que continguin una subcadena en les seves metadades
- Combinar resultats de cerques amb operadors lògics (AND, OR)

Mètodes a implementar:
- prompt(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Prompt.

- model(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Model.

- seed(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Seed.

- cfg_scale(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp CFG_Scale.

- steps(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Steps.

- sampler(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Sampler.

- date(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Created_Date.

- and_operator(list1: list, list2: list) -> list
        Retorna una llista amb els UUID que apareixen en AMBDUES llistes.
        (Intersecció de conjunts)

- or_operator(list1: list, list2: list) -> list
        Retorna una llista amb els UUID que apareixen en QUALSEVOL de
        les dues llistes, sense duplicats.
        (Unió de conjunts)

Notes:
- Les cerques són case-sensitive (distingeixen majúscules/minúscules)
- Utilitzeu str.find() per cercar subcadenes
- Les llistes retornades poden estar buides
- Els operadors lògics NO modifiquen les llistes originals
- Aquests mètodes NO retornen objectes Gallery, sinó llistes simples
"""
import cfg


class SearchMetadata:
    """Gestiona les cerques de metadades de les imatges."""

    def __init__(self, image_data=None):
        """Inicialitza el cercador amb una referència a ImageData."""
        self._image_data = image_data  # Instància de ImageData per accedir a les metadades.

    def _cercar(self, nom_getter: str, sub) -> list:
        """Busca una subcadena en un camp de metadades i retorna els UUID coincidents."""
        llista_uuids = []

        # Comprova que ImageData i el terme de cerca estiguin disponibles.
        if self._image_data is None or sub is None:
            return llista_uuids

        sub_str = str(sub)
        getter = getattr(self._image_data, nom_getter, None)

        if getter is None:
            return llista_uuids

        # Recorre les imatges registrades i consulta el valor del camp indicat.
        for uuid in getattr(self._image_data, "_images", {}):
            valor = getter(uuid)
            if valor is not None and valor != "None":
                if str(valor).find(sub_str) != -1:
                    llista_uuids.append(uuid)

        return llista_uuids

    def prompt(self, sub: str) -> list:
        """Busca imatges que contenen la subcadena indicada al prompt."""
        return self._cercar("get_prompt", sub)

    def model(self, sub: str) -> list:
        """Busca imatges segons el model d'IA utilitzat."""
        return self._cercar("get_model", sub)

    def seed(self, sub: str) -> list:
        """Busca imatges segons la llavor aleatòria utilitzada."""
        return self._cercar("get_seed", sub)

    def cfg_scale(self, sub: str) -> list:
        """Busca imatges segons el valor de CFG Scale."""
        return self._cercar("get_cfg_scale", sub)

    def steps(self, sub: str) -> list:
        """Busca imatges segons el nombre de passos de generació."""
        return self._cercar("get_steps", sub)

    def sampler(self, sub: str) -> list:
        """Busca imatges segons l'algorisme de mostreig utilitzat."""
        return self._cercar("get_sampler", sub)

    def date(self, sub: str) -> list:
        """Busca imatges segons la data de creació."""
        return self._cercar("get_created_date", sub)

    def generated(self, sub: str) -> list:
        """Busca imatges segons el valor del camp Generated."""
        return self._cercar("get_generated", sub)

    def dimensions(self, width, height) -> list:
        """Busca imatges que tenen les dimensions indicades."""
        llista_uuids = []

        # Comprova que les dimensions i ImageData estiguin disponibles.
        if self._image_data is None or width is None or height is None:
            return llista_uuids

        # Converteix les dimensions a nombres enters.
        try:
            w_val, h_val = int(width), int(height)
        except (TypeError, ValueError):
            return llista_uuids

        # Compara les dimensions de cada imatge amb les dimensions indicades.
        for uuid in getattr(self._image_data, "_images", {}):
            dims = self._image_data.get_dimensions(uuid)
            if dims is not None and tuple(dims) == (w_val, h_val):
                llista_uuids.append(uuid)

        return llista_uuids

    def and_operator(self, list1: list, list2: list) -> list:
        """Retorna la intersecció de dues llistes d'UUID."""
        if list1 is None or list2 is None:
            return []

        # Conserva els elements comuns sense repetir-los.
        en_list2 = set(list2)
        vistos = set()
        resultat = []

        for u in list1:
            if u in en_list2 and u not in vistos:
                vistos.add(u)
                resultat.append(u)

        return resultat

    def or_operator(self, list1: list, list2: list) -> list:
        """Retorna la unió de dues llistes d'UUID sense duplicats."""
        if list1 is None and list2 is None:
            return []

        l1 = list1 if list1 is not None else []
        l2 = list2 if list2 is not None else []

        # Combina les dues llistes i elimina els elements repetits.
        vistos = set()
        resultat = []

        for u in l1 + l2:
            if u not in vistos:
                vistos.add(u)
                resultat.append(u)

        return resultat

    def __str__(self) -> str:
        """Retorna una representació textual del cercador."""
        total = len(self._image_data) if self._image_data else 0
        return f"SearchMetadata(imatges={total})"