# Top 8 Banner Generator

This is a Django app that generates Top 8 result banners for Super Smash Bros Ultimate Tournaments using Pillow. The banner template parts used were made by [EDM](https://twitter.com/Elenriqu3). Character portraits are not included in this repository. You can see the app working [here](https://riokaru.pythonanywhere.com/).

![alt text](https://i.imgur.com/XUnYuR0.png "Top 8")

## Features

- Spots under each player's name for their twitter handle.
- Bottom Left, Top Left and Top Right texts to put information of the tournament or anything really.
- Custom layout colors and custom background.
- Option to generate a banner for a smash.gg tournemant given a link. It looks for top 8's players name, character and twitter handle and the event's name, date, city, number of participants and url.

## Usage

- Install pillow https://pypi.org/project/Pillow/
- Install colorful https://pypi.org/project/django-colorful/
- Put this app on your Django project and add it to the installed app on your `settings.py` file.
- Create a text file named `smashgg.apikey` on the `generar` directory containing a valid [smash.gg ](https://smash.gg/) api key.
- Create a directory named `Fighter Portraits` on the `generar` directory.
- For each character, create a directory under `generar/Fighter Portraits` and place in it 8 portraits in `.png` format. The portraits must be named `0.png`...`7.png`. The app was made with 512x512 portraits in mind but it should work fine as long as they're square (will be stretched otherwise). Additionally, create a `Random` directory and place a single `0.png` portrait in it.
- If you just want to generate pictures without the need of using django check the `generar/perro.py` script.
