from django import forms
from colorful.forms import RGBColorField

class GenForm(forms.Form):
    chars = ['Banjo & Kazooie', 'Bayonetta', 'Bowser', 'Bowser Jr', 'Byleth', 'Captain Falcon', 'Chrom', 'Cloud', 'Corrin', 'Daisy', 'Dark Pit', 'Dark Samus', 'Diddy Kong', 'Donkey Kong', 'Dr Mario', 'Duck Hunt', 'Falco', 'Fox', 'Ganondorf', 'Greninja', 'Hero', 'Ice Climbers', 'Ike', 'Incineroar', 'Inkling', 'Isabelle', 'Jigglypuff', 'Joker', 'Ken', 'King Dedede', 'King K Rool', 'Kirby', 'Link', 'Little Mac', 'Lucario', 'Lucas', 'Lucina', 'Luigi', 'Mario', 'Marth', 'Mega Man', 'Meta Knight', 'Mewtwo', 'Mii Brawler', 'Mii Gunner', 'Mii Swordfighter', 'Min Min', 'Mr Game and Watch', 'Ness', 'Olimar', 'Pac-Man', 'Palutena', 'Peach', 'Pichu', 'Pikachu', 'Piranha Plant', 'Pit', 'Pokémon Trainer', 'Richter', 'Ridley', 'ROB', 'Robin', 'Rosalina and Luma', 'Roy', 'Ryu', 'Samus', 'Sheik', 'Shulk', 'Simon', 'Snake', 'Sonic', 'Terry', 'Toon Link', 'Villager', 'Wario', 'Wii Fit Trainer', 'Wolf', 'Yoshi', 'Young Link', 'Zelda', 'Zero Suit Samus']
    chars = tuple([(i, i) for i in chars])
    numeritos = tuple([(str(i), str(i)) for i in range(8)])

    name1 = forms.CharField(label='Player Name', max_length=23)
    twitter1 = forms.CharField(label='Twitter Handle', max_length=15, required=False)
    char1 = forms.ChoiceField(label='Character', choices=chars)
    color1 = forms.ChoiceField(label='Color', choices=numeritos)


    name2 = forms.CharField(label='Player Name', max_length=23)
    twitter2 = forms.CharField(label='Twitter Handle', max_length=15, required=False)
    char2 = forms.ChoiceField(label='Character', choices=chars)
    color2 = forms.ChoiceField(label='Color', choices=numeritos)


    name3 = forms.CharField(label='Player Name', max_length=23)
    twitter3 = forms.CharField(label='Twitter Handle', max_length=15, required=False)
    char3 = forms.ChoiceField(label='Character', choices=chars)
    color3 = forms.ChoiceField(label='Color', choices=numeritos)


    name4 = forms.CharField(label='Player Name', max_length=23)
    twitter4 = forms.CharField(label='Twitter Handle', max_length=15, required=False)
    char4 = forms.ChoiceField(label='Character', choices=chars)
    color4 = forms.ChoiceField(label='Color', choices=numeritos)


    name5 = forms.CharField(label='Player Name', max_length=23)
    twitter5 = forms.CharField(label='Twitter Handle', max_length=15, required=False)
    char5 = forms.ChoiceField(label='Character', choices=chars)
    color5 = forms.ChoiceField(label='Color', choices=numeritos)


    name6 = forms.CharField(label='Player Name', max_length=23)
    twitter6 = forms.CharField(label='Twitter Handle', max_length=15, required=False)
    char6 = forms.ChoiceField(label='Character', choices=chars)
    color6 = forms.ChoiceField(label='Color', choices=numeritos)


    name7 = forms.CharField(label='Player Name', max_length=23)
    twitter7 = forms.CharField(label='Twitter Handle', max_length=15, required=False)
    char7 = forms.ChoiceField(label='Character', choices=chars)
    color7 = forms.ChoiceField(label='Color', choices=numeritos)


    name8 = forms.CharField(label='Player Name', max_length=23)
    twitter8 = forms.CharField(label='Twitter Handle', max_length=15, required=False)
    char8 = forms.ChoiceField(label='Character', choices=chars)
    color8 = forms.ChoiceField(label='Color', choices=numeritos)

    ttext = forms.CharField(label='Top Text', max_length=50, required=False)
    btext = forms.CharField(label='Bottom Text', max_length=70, required=False)
    url = forms.CharField(label='URL', max_length=40, required=False, initial="riokaru.pythonanywhere.com")

    lcolor1 = RGBColorField(label="Main Color", initial="#ff281a")
    lcolor2 = RGBColorField(label="Highlight Color", initial="#ffb60c")

    background = forms.ImageField(label="Background Image", required=False)
