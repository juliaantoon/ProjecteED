# -*- coding: utf-8 -*-
"""
p1_main.py : ** OPTIONAL ** Si heu fet un main vostre, poseu aquí el codi.
                            Aquest arxiu no s'avalua automàticament.

Aquí podeu posar el vostre codi de proves per testejar les funcionalitats
implementades.

Exemples d'ús:
    - Carregar la col·lecció d'imatges
    - Generar UUID per a totes les imatges
    - Llegir metadades d'algunes imatges
    - Visualitzar imatges
    - Carregar i mostrar galeries
    - Fer cerques i crear galeries a partir dels resultats
"""
import cfg
from ImageFiles import ImageFiles
from ImageID import ImageID
from ImageData import ImageData
from ImageViewer import ImageViewer
from Gallery import Gallery
from SearchMetadata import SearchMetadata

'''files = ImageFiles()
ids = ImageID()
data = ImageData(ids)

files.reload_fs(cfg.ROOT_DIR)
print(files)

for f in files.files_added():
    u = ids.generate_uuid(f)
    data.add_image(u, f)
    data.load_metadata(u)

print(ids, data)

# Visualitzador i galeria
viewer = ImageViewer(data)
g = Gallery(ids, viewer)

# Cerca -> galeria (Func7)
cerca = SearchMetadata(data)
trobats = cerca.prompt("robots")
print("Trobats:", len(trobats))
for u in trobats:
    g.add_image_at_end(u)
print(g)
g.show()

g.remove_first_image()
g.remove_last_image()
print(g)'''

    # 2. Crear els objectes
files=ImageFiles()
ids=ImageID()

# 3. Connectar-los
data = ImageData(ids)
viewer = ImageViewer(data)
gallery = Gallery(ids, viewer)
search = SearchMetadata(data)
files.reload_fs()                     
print(files)                          


    # 4. Carregar les imatges
for f in files.files_added():
    u = ids.generate_uuid(f)
    if u:
        data.add_image(u, f)
        data.load_metadata(u)
        
    # 5. Carregar una galeria
    # 6. Fer cerques
def buscar_valor(uuids, getter):
    """Retorna el primer valor real (no None ni "None") que trobi."""
    for u in uuids:
        v = getter(u)
        if v is not None and v != "None":
            return u, v
    return None, None


def mostrar_resultat(descripcio, resultat):
    print(f"\n{descripcio}")
    print(f"  Imatges trobades: {len(resultat)}")
    for u in resultat[:3]:                       # només les 3 primeres
        print(f"  - {data.get_filename(u)}")


uuids = list(data._images)       # tots els UUID registrats a ImageData

models = set()
steps = set()
for u in uuids:
    m = data.get_model(u)
    s = data.get_steps(u)
    if m is not None and m != "None":
        models.add(m)
    if s is not None and s != "None":
        steps.add(s)
print(steps)
print(models)
models = list(models)

# PROVA 1: cerca per model
'''nom_model = "Dalle2"        # posa-hi el model que vulguis (o fes servir input())
# nom_model = input("Model a cercar: ")

resultat = search.model(nom_model)
print(f"Imatges amb el model '{nom_model}': {len(resultat)}")

if resultat:
    viewer.show_image(resultat[0], 1)     # mostra la primera: metadades + imatge
else:
    print("Cap imatge té aquest model")'''


# PROVA 2: cerca per data (any i mes, p. ex. "2026-10")
'''data = "2022-08"        
# nom_model = input("Model a cercar: ")

resultat = search.date(data)
print(f"Imatges amb el model '{data}': {len(resultat)}")

if resultat:
    viewer.show_image(resultat[0], 1)     # mostra la primera: metadades + imatge
else:
    print("Cap imatge té aquest model")'''

# PROVA 3: cerca combinada amb AND (model i steps)
nom_model = "SD2"        # posa-hi el model que vulguis
nom_steps = "50"        # posa-hi els steps que vulguis
# nom_model = input("Model: ")
# nom_steps = input("Steps: ")

res_model = search.model(nom_model)
res_steps = search.steps(nom_steps)
resultat = search.and_operator(res_model, res_steps)

print(f"Model '{nom_model}': {len(res_model)} imatges")
print(f"Steps '{nom_steps}': {len(res_steps)} imatges")
print(f"Les dues condicions (AND): {len(resultat)} imatges")

if resultat:
    viewer.show_image(resultat[0], 1)     # metadades + imatge
else:
    print("Cap imatge compleix les dues condicions")

              



nova = Gallery(ids, viewer)
for u in resultat:
    nova.add_image_at_end(u)

print("2. Imatges a la galeria:", len(nova))
print("3.", nova)
