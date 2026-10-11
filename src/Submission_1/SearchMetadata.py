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
import ImageData
class SearchMetadata:

    def __init__(self, uuid):
        self._image_data = image_data  # instància de la classe ImageData per accedir a les metadades

    def prompt(self, sub: str) -> list:

        llista_uuids=[]

        for uuid in self.image_data.get_dicciomari:#sha de ttribar el diccionaride uuids i la seva METADATA

            if sub in self.image_data.get_prompt(uuid):
                llista_uuids.append(uuid)

        return llista_uuids

    def model(self, sub: str) -> list:
        llista_uuids=[]

        for uuid in self.image_data.get_dicciomari:

            if sub in self.image_data.get_model(uuid):
                llista_uuids.append(uuid)

        return llista_uuids

    def seed(self, sub: str) -> list:
        llista_uuids=[]

        for uuid in self.image_data.get_dicciomari:

            if sub in self.image_data.get_seed(uuid):
                llista_uuids.append(uuid)

        return llista_uuids

    def cfg_scale(self, sub: str) -> list:
        llista_uuids=[]

        for uuid in self.image_data.get_dicciomari:

            if sub in self.image_data.get_cfg_scale(uuid):
                llista_uuids.append(uuid)

        return llista_uuids

    def steps(self, sub: str) -> list:
        llista_uuids=[]

        for uuid in self.image_data.get_dicciomari:

            if sub in self.image_data.get_steps(uuid):
                llista_uuids.append(uuid)

        return llista_uuids

    def sampler(self, sub: str) -> list:
        llista_uuids=[]

        for uuid in self.image_data.get_dicciomari:

            if sub in self.image_data.get_sampler(uuid):
                llista_uuids.append(uuid)

        return llista_uuids

    def date(self, sub: str) -> list:
        llista_uuids=[]

        for uuid in self.image_data.get_dicciomari:

            if sub in self.image_data.get_created_date(uuid):
                llista_uuids.append(uuid)

        return llista_uuids

    def and_operator(self, list1: list, list2: list) -> list:
        return list(set(list1) & set(list2))  # Intersecció de conjunts

    def or_operator(self, list1: list, list2: list) -> list:
        return list(set(list1) | set(list2))  # Unió de conjunts


# amb un metode general perl bucle:


class SearchMetadata:
    
    def __init__(self, image_data):
        self._image_data = image_data  # instància de la classe ImageData per accedir a les metadades

    def _cercar (self, funcio_getter, sub:str) -> list:
        llista_uuids=[]
        if self._image_data is None:
            return llista_uuids
        for uuid in self._image_data._images:
            valor = funcio_getter(uuid)
            if valor is not None:
                if str(valor).find(sub) != -1:
                    llista_uuids.append(uuid)
        return llista_uuids

    def prompt(self, sub: str) -> list: 
        return self._cercar(self._image_data.get_prompt, sub) # busca la subcadena en el camp Prompt de les metadades de les imatges

    def model(self, sub: str) -> list:
        return self._cercar(self._image_data.get_model, sub) # busca la subcadena en el camp Model de les metadades de les imatges

    def seed(self, sub: str) -> list:
        return self._cercar(self._image_data.get_seed, sub) # busca la subcadena en el camp Seed de les metadades de les imatges

    def cfg_scale(self, sub: str) -> list:
        return self._cercar(self._image_data.get_cfg_scale, sub) # busca la subcadena en el camp CFG_Scale de les metadades de les imatges

    def steps(self, sub: str) -> list:
        return self._cercar(self._image_data.get_steps, sub) # busca la subcadena en el camp Steps de les metadades de les imatges

    def sampler(self, sub: str) -> list:
        return self._cercar(self._image_data.get_sampler, sub) # busca la subcadena en el camp Sampler de les metadades de les imatges

    def date (self, sub: str) -> list:
        return self._cercar(self._image_data.get_created_date, sub) # busca la subcadena en el camp Created_Date de les metadades de les imatges

    def and_operator(self, list1: list, list2: list) -> list: # intersecció de conjunts
        return list(set(list1) & set(list2))  

    def or_operator(self, list1: list, list2: list) -> list: # unió de conjunts
        return list(set(list1) | set(list2))  