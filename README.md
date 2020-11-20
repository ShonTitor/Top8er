# Top 8 Graphic Generator

This is a Django app that generates top 8 result graphics for many different fighting games tournaments using Pillow. These graphics include a picture of the player's main character as well as their nicknames and tournament placing. The graphic template parts used were made by [EDM](https://twitter.com/Elenriqu3). Character portraits are not included in this repository. You can see the app working [here](https://www.top8er.com/).

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/E1E4K0N2)  
[support the designer on paypal](https://www.paypal.com/paypalme/Elenriqu3)

![alt text](https://i.imgur.com/iXjo0pU.png "Top 8 Graphic Generator")

## Features

- Boxes under each player's name for their twitter handle.
- Bottom Left, Top Left and Top Right texts to insert details regarding tournaments or other related information.
- Custom layout and font colors, custom backgrounds.
- Custom Palettes (only Eternal Fighter Zero)
- Support for japanese and european characters (by changing the font).
- Option to import data from a smash.gg or challonge link.

## Usage

- Install pillow https://pypi.org/project/Pillow/
- Install colorful https://pypi.org/project/django-colorful/
- Install fonttools https://github.com/fonttools/fonttools
- Put this app on your Django project and add it to the installed app on your `settings.py` file.
- Create text files named `smashgg.apikey` and `challonge.apikey` on the `generar` directory containing valid [smash.gg ](https://smash.gg/) and [challonge](https://challonge.com) api keys.
- Create an `assets` directory in the `generar`. Folder structure is as follows:
```
assets/
        game/
             bg.png
             portraits/
                      Character/
                                0.png
                                1.png
                                ...
                                n.png
                      ...
                      OtherCharacter/
                                0.png
                                1.png
                                ...
                                n.png
             icons/
                      Character/
                                0.png
                                1.png
                                ...
                                n.png
                      ...
                      OtherCharacter/
                                0.png
                                1.png
                                ...
                                n.png
```
- If you would rather use the command line, check the `generar/perro.py` script.
