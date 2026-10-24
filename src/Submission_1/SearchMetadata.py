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
 
    def __init__(self, image_data=None):
        self._image_data = image_data  # instància de la classe ImageData per accedir a les metadades
 
    def _cercar(self, nom_getter: str, sub) -> list:  # rep el nom del getter
        llista_uuids = []
        if self._image_data is None or sub is None:
            return llista_uuids
        sub_str = str(sub)
        getter = getattr(self._image_data, nom_getter, None)
        if getter is None:
            return llista_uuids
        for uuid in getattr(self._image_data, "_images", {}):
            valor = getter(uuid)
            if valor is not None and valor != "None":
                if str(valor).find(sub_str) != -1:
                    llista_uuids.append(uuid)
        return llista_uuids
 
    def prompt(self, sub: str) -> list: 
        return self._cercar("get_prompt", sub)                          # busca la subcadena en el camp Prompt de les metadades de les imatges
 
    def model(self, sub: str) -> list:
        return self._cercar("get_model", sub)                           # busca la subcadena en el camp Model de les metadades de les imatges
 
    def seed(self, sub: str) -> list:
        return self._cercar("get_seed", sub)                            # busca la subcadena en el camp Seed de les metadades de les imatges
 
    def cfg_scale(self, sub: str) -> list:
        return self._cercar("get_cfg_scale", sub)                       # busca la subcadena en el camp CFG_Scale de les metadades de les imatges
 
    def steps(self, sub: str) -> list:
        return self._cercar("get_steps", sub)                           # busca la subcadena en el camp Steps de les metadades de les imatges
 
    def sampler(self, sub: str) -> list:
        return self._cercar("get_sampler", sub)                         # busca la subcadena en el camp Sampler de les metadades de les imatges
 
    def date(self, sub: str) -> list:
        return self._cercar("get_created_date", sub)                    # busca la subcadena en el camp Created_Date de les metadades de les imatges
 
    def generated(self, sub: str) -> list:
        return self._cercar("get_generated", sub) 
 
    def dimensions(self, width, height) -> list:
        llista_uuids = []
        if self._image_data is None or width is None or height is None:
            return llista_uuids
        try:                                          
            w_val, h_val = int(width), int(height)
        except (TypeError, ValueError):
            return llista_uuids
        for uuid in getattr(self._image_data, "_images", {}):
            dims = self._image_data.get_dimensions(uuid)
            if dims is not None and tuple(dims) == (w_val, h_val):
                llista_uuids.append(uuid)
        return llista_uuids
 
    def and_operator(self, list1: list, list2: list) -> list: # intersecció de conjunts
        if list1 is None or list2 is None:
            return []
        en_list2 = set(list2)
        vistos = set()
        resultat = []
        for u in list1:
            if u in en_list2 and u not in vistos:
                vistos.add(u)
                resultat.append(u)
        return resultat
 
    def or_operator(self, list1: list, list2: list) -> list: # unió de conjunts
        if list1 is None and list2 is None:
            return []
        l1 = list1 if list1 is not None else []
        l2 = list2 if list2 is not None else []
        vistos = set()
        resultat = []
        for u in l1 + l2:
            if u not in vistos:
                vistos.add(u)
                resultat.append(u)
        return resultat
 
    def __str__(self) -> str:
        total = len(self._image_data) if self._image_data else 0
        return f"SearchMetadata(imatges={total})"