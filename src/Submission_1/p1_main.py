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

files = ImageFiles()
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
print(g)