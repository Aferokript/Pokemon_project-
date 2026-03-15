import folium
import json
from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import PokemonEntity, Pokemon, PokemonElementType
from django.utils import timezone
from django.utils.timezone import localtime

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def build_absolute_url(request, image_url):
    return request.build_absolute_uri(image_url)


def count_time():
    now = timezone.now()
    entities = PokemonEntity.objects.filter(
        disappeared_at__gte=now,
        appeared_at__lte=now
    )
    return entities


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
        pokemons = json.load(database)['pokemons']

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        for pokemon_entity in pokemon['entities']:
            add_pokemon(
                folium_map,
                pokemon_entity['lat'],
                pokemon_entity['lon'],
                pokemon['img_url']
            )

    pokemons_on_page = []
    for entity in count_time():
        pokemon = entity.pokemon
        if pokemon.image:
            absolute_url = build_absolute_url(request, pokemon.image.url)
        else:
            absolute_url = None
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'title_ru': pokemon.title_ru,
            'img_url': absolute_url,
            'lat': entity.lat,
            'lon': entity.lon,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon = Pokemon.objects.get(id=pokemon_id)
    entities = PokemonEntity.objects.filter(pokemon_id=pokemon_id)
    elements = pokemon.element_type.all()

    previous_evolution = None
    next_evolution = None

    if pokemon.previous_evolution:
        previous_evolution = {
            'pokemon_id': pokemon.previous_evolution.id,
            'title_ru': pokemon.previous_evolution.title_ru,
            'img_url': build_absolute_url(request, pokemon.previous_evolution.image.url),
        }
    if pokemon.next_evolution.exists():
        evolution = pokemon.next_evolution.first()
        next_evolution = {
            'pokemon_id': evolution.id,
            'title_ru': evolution.title_ru,
            'img_url': build_absolute_url(request, evolution.image.url),
        }

    element_type = []
    for element in elements:
        element_type.append({
            'title': element.title,
            'img': build_absolute_url(request, element.image.url)
        })

    pokemon_data = {}
    for entity in entities:
        if entity.image:
            entity_image_url = build_absolute_url(request, entity.image.url)
            pokemon_data['pokemon_id'] = entity.id
            pokemon_data['title_ru'] = pokemon.title_ru
            pokemon_data['img_url'] = entity_image_url
            pokemon_data['lat'] = entity.lat
            pokemon_data['lon'] = entity.lon
            pokemon_data['title_en'] = pokemon.title_en
            pokemon_data['title_jp'] = pokemon.title_jp
            pokemon_data['description'] = pokemon.description
            pokemon_data['previous_evolution'] = previous_evolution
            pokemon_data['next_evolution'] = next_evolution
            pokemon_data['element_type'] = element_type

            add_pokemon(
                folium_map,
                pokemon_data['lat'],
                pokemon_data['lon'],
                pokemon_data['img_url'],
            )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_data
    })