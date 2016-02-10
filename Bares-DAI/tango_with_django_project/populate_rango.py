#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Bares, Tapas


def populate():
    venecia_bar = add_bar('Bar Venecia', address='Calle Carretera 32, Pinos del Valle', views=128, likes=64)

    add_tapas(bar=venecia_bar,
        title="Patatas fritas",
        url="http://www.cosasdesalud.es/images/patatasfritas.jpg", views=20)

    add_tapas(bar=venecia_bar,
        title="Albóndigas en salsa",
        url="https://macrecetas.files.wordpress.com/2013/10/image8.jpg", views=60)

    add_tapas(bar=venecia_bar,
        title="Gulas con jamón",
        url="http://2.bp.blogspot.com/-elHxAV7xj6Q/TpIooEHZgNI/AAAAAAAAARs/b5V5WDg35uw/s640/finde+9.10.11+026.jpg", views=48)

    cateto_bar = add_bar("Bar el cateto", address='Calle Real 3, Alhendín', views=64, likes=32)

    add_tapas(bar=cateto_bar,
        title="Jamón",
        url="http://www.eladerezo.com/wp-content/uploads/2008/09/tapa-de-jamon-iberico-3.jpg", views=18)

    add_tapas(bar=cateto_bar,
        title="Sándwich vegetal",
        url="http://1.bp.blogspot.com/-hCxAkfOewtQ/VGsaHel2cmI/AAAAAAAAh8k/oNBfbyE7TMk/s1600/20141117_203051.jpg", views=29)

    add_tapas(bar=cateto_bar,
        title="Chipirón a la parrilla",
        url="http://www.afuegolento.com/img_db/recetas/9288_ppal_Chipiron_Pimientos_D.jpg", views=16)

    juego_bar = add_bar("Bar fuera de juego", address='Calle Arrayanes 6, Dúcal', views=32, likes=16)

    add_tapas(bar=juego_bar,
        title="Setas variadas con huevo de codorniz",
        url="http://3.bp.blogspot.com/-2lIgnzaKMTA/UgUSmKx_kmI/AAAAAAAACDc/9MBKRSq6Bc8/s640/P2080095.JPG", views=23)

    add_tapas(bar=juego_bar,
        title="Pulpo",
        url="http://estaticos.elmundo.es/elmundo/imagenes/2013/06/03/valencia/1370244305_0.jpg", views=12)

    # Print out what we have added to the user.
    for b in Bares.objects.all():
        for t in Tapas.objects.filter(bares=b):
            print "- {0} - {1}".format(str(b), str(t))

def add_tapas(bar, title, url, views=0):
    t = Tapas.objects.get_or_create(bares=bar, title=title)[0]
    t.url=url
    t.views=views
    t.save()
    return t

def add_bar(name, address='NULL', views=0, likes=0):
    b = Bares.objects.get_or_create(name=name)[0]
    b.address=address
    b.views=views
    b.likes=likes
    b.save()
    return b

# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()
