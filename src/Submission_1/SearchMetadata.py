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
class SearchMetadata:

    def __init__(self, image_data=None):
        self._image_data = image_data

    def _cercar(self, funcio_getter, sub: str) -> list:
        llista_uuids = []
        if self._image_data is None:
            return llista_uuids
        for uuid in self._image_data._images:
            valor = funcio_getter(uuid)
            if valor is not None and str(valor).find(sub) != -1:
                llista_uuids.append(uuid)
        return llista_uuids

    def prompt(self, sub: str) -> list:
        return self._cercar(self._image_data.get_prompt, sub)

    def model(self, sub: str) -> list:
        return self._cercar(self._image_data.get_model, sub)

    def seed(self, sub: str) -> list:
        return self._cercar(self._image_data.get_seed, sub)

    def cfg_scale(self, sub: str) -> list:
        return self._cercar(self._image_data.get_cfg_scale, sub)

    def steps(self, sub: str) -> list:
        return self._cercar(self._image_data.get_steps, sub)

    def sampler(self, sub: str) -> list:
        return self._cercar(self._image_data.get_sampler, sub)

    def date(self, sub: str) -> list:
        return self._cercar(self._image_data.get_created_date, sub)

    def generated(self, sub: str) -> list:
        if self._image_data is None:
            return []
        return self._cercar(self._image_data.get_generated, sub)

    def dimensions(self, width: int, height: int) -> list:
        llista_uuids = []
        if self._image_data is None:
            return llista_uuids
        for uuid in self._image_data._images:
            dims = self._image_data.get_dimensions(uuid)
            if dims is not None and tuple(dims) == (width, height):
                llista_uuids.append(uuid)
        return llista_uuids

    def and_operator(self, list1: list, list2: list) -> list:
        return list(set(list1) & set(list2))

    def or_operator(self, list1: list, list2: list) -> list:
        return list(set(list1) | set(list2))

    def __str__(self) -> str:
        total = len(self._image_data) if self._image_data else 0
        return f"SearchMetadata(imatges={total})"