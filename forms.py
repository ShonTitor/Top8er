import re
from django import forms
from colorful.forms import RGBColorField
from .generar.getsets import check_event, check_challonge

class AncestorForm(forms.Form) :
    background = forms.ImageField(label="Background Image", required=False)
    darken_bg = forms.BooleanField(label="Darken Background", widget=forms.CheckboxInput, initial=True, required=False)
    blacksquares = forms.BooleanField(label="Black Background for characters", widget=forms.CheckboxInput, initial=True, required=False)
    prmode = forms.BooleanField(label="PR Mode", widget=forms.CheckboxInput, initial=False, required=False)
    charshadow = forms.BooleanField(label="Character Shadow", widget=forms.CheckboxInput, initial=True, required=False)
    fonts = [("auto", "Auto"),
             ("DFGothic-SU-WIN-RKSJ-H-01.ttf", "SSBU font (japanese characters)"),
             ("sansthirteenblack.ttf", "SansThirteenBlack (european characters)")]
    fontt = forms.ChoiceField(label='Font Type', choices=fonts)
    fcolor1  = RGBColorField(label="Font Color", initial="#ffffff")
    fscolor1 = RGBColorField(label="Font Shadow Color", initial="#000000")
    fcolor2  = RGBColorField(label="Font Color", initial="#ffffff")
    fscolor2 = RGBColorField(label="Font Shadow Color", initial="#000000")

class SmashggForm(forms.Form) :
    event = forms.RegexField(label="External link",
                             regex = "https://smash.gg/tournament/[^/]+/event/[^/]+.*|https://challonge.com/[^/]+.*",
                             max_length=200)
    def clean(self):
        cleaned_data = super().clean()
        try :
            e = cleaned_data.get("event")
            match = re.search("https://smash.gg/tournament/[^/]+/event/[^/]+", e)
            if match :
                if not check_event(e[17:match.end()]) :
                    msg = "Event not found, has too few players or an iguana bit a cable."
                    self.add_error('event', msg)
            else :
                match = re.search("https://challonge.com/[^/]+", e)
                if not check_challonge(e[22:match.end()]) :
                    msg = "Event not found, has too few players or an iguana bit a cable."
                    self.add_error('event', msg)
        except :
            pass
        return cleaned_data

def makeform(chars=None, numerito=None, numerito_extra=None,
             echars=None, hasextra=True, efz=False, mb=False,
             color1="#ff281a", color2="#ffb60c") :
    if chars is None :
        chars = ['Random', 'Banjo & Kazooie', 'Bayonetta', 'Bowser', 'Bowser Jr', 'Byleth',
                 'Captain Falcon', 'Chrom', 'Cloud', 'Corrin', 'Daisy', 'Dark Pit', 'Dark Samus',
                 'Diddy Kong', 'Donkey Kong', 'Dr Mario', 'Duck Hunt', 'Falco', 'Fox', 'Ganondorf',
                 'Greninja', 'Hero', 'Ice Climbers', 'Ike', 'Incineroar', 'Inkling', 'Isabelle',
                 'Jigglypuff', 'Joker', 'Ken', 'King Dedede', 'King K Rool', 'Kirby', 'Link', 'Little Mac',
                 'Lucario', 'Lucas', 'Lucina', 'Luigi', 'Mario', 'Marth', 'Mega Man', 'Meta Knight',
                 'Mewtwo', 'Mii Brawler', 'Mii Gunner', 'Mii Swordfighter', 'Min Min', 'Mr Game & Watch',
                 'Ness', 'Olimar', 'Pac-Man', 'Palutena', 'Peach', 'Pichu', 'Pikachu', 'Piranha Plant', 'Pit',
                 'Pokémon Trainer', 'Richter', 'Ridley', 'ROB', 'Robin', 'Rosalina & Luma', 'Roy', 'Ryu', 'Samus',
                 'Sephirot',
                 'Sheik', 'Shulk', 'Simon', 'Snake', 'Sonic', 'Steve', 'Terry', 'Toon Link', 'Villager', 'Wario',
                 'Wii Fit Trainer', 'Wolf', 'Yoshi', 'Young Link', 'Zelda', 'Zero Suit Samus']
        chars = ['Banjo & Kazooie', 'Bayonetta', 'Bowser', 'Bowser Jr', 'Byleth',
                 'Captain Falcon', 'Chrom', 'Cloud', 'Corrin', 'Daisy', 'Dark Pit', 'Dark Samus',
                 'Diddy Kong', 'Donkey Kong', 'Dr Mario', 'Duck Hunt', 'Falco', 'Fox', 'Ganondorf',
                 'Greninja', 'Hero', 'Ice Climbers', 'Ike', 'Incineroar', 'Inkling', 'Isabelle',
                 'Jigglypuff', 'Joker', 'Ken', 'King Dedede', 'King K Rool', 'Kirby', 'Link', 'Little Mac',
                 'Lucario', 'Lucas', 'Lucina', 'Luigi', 'Mario', 'Marth', 'Mega Man', 'Meta Knight',
                 'Mewtwo', 'Mii Brawler', 'Mii Gunner', 'Mii Swordfighter', 'Min Min', 'Mr Game & Watch',
                 'Ness', 'Olimar', 'Pac-Man', 'Palutena', 'Peach', 'Pichu', 'Pikachu', 'Piranha Plant', 'Pit',
                 'Pokémon Trainer', 'Richter', 'Ridley', 'ROB', 'Robin', 'Rosalina & Luma', 'Roy', 'Ryu', 'Samus',
                 #'Sephirot',
                 'Sheik', 'Shulk', 'Simon', 'Snake', 'Sonic', 'Steve', 'Terry', 'Toon Link', 'Villager', 'Wario',
                 'Wii Fit Trainer', 'Wolf', 'Yoshi', 'Young Link', 'Zelda', 'Zero Suit Samus']

    if numerito is None :
        numerito = 8
    numeritos = tuple([(str(i), str(i)) for i in range(numerito)])
    if numerito_extra is None :
        numerito_extra = numerito
    num_e = tuple([(str(i), str(i)) for i in range(numerito_extra)])

    if echars == None :
        if chars[0] == "Random" :
            e_chars = ['None']+chars[1:]
        else :
            e_chars = ['None']+chars
    else :
        e_chars = [None]+echars
    chars = tuple([(i, i) for i in chars])
    e_chars = tuple([(i, i) for i in e_chars])

    cc1 = color1
    cc2 = color2

    if mb :
        extra_label1 = 'Main Moon'
        extra_label2 = 'Secondary Moon'
    else :
        extra_label1 = "Secondary Character"
        extra_label2 = "Tertiary Character"

    class NoExtraForm(AncestorForm) :
        lcolor1 = RGBColorField(label="Main Color", initial=cc1)
        lcolor2 = RGBColorField(label="Highlight Color", initial=cc2)
        
        name1 = forms.CharField(label='Player Name', max_length=23)
        twitter1 = forms.CharField(label='Twitter Handle', max_length=16, required=False)
        char1 = forms.ChoiceField(label='Main Character', choices=chars)
        color1 = forms.ChoiceField(label='Main Character Color', choices=numeritos)

        name2 = forms.CharField(label='Player Name', max_length=23)
        twitter2 = forms.CharField(label='Twitter Handle', max_length=16, required=False)
        char2 = forms.ChoiceField(label='Main Character', choices=chars)
        color2 = forms.ChoiceField(label='Main Character Color', choices=numeritos)

        name3 = forms.CharField(label='Player Name', max_length=23)
        twitter3 = forms.CharField(label='Twitter Handle', max_length=16, required=False)
        char3 = forms.ChoiceField(label='Main Character', choices=chars)
        color3 = forms.ChoiceField(label='Main Character Color', choices=numeritos)

        name4 = forms.CharField(label='Player Name', max_length=23)
        twitter4 = forms.CharField(label='Twitter Handle', max_length=16, required=False)
        char4 = forms.ChoiceField(label='Main Character', choices=chars)
        color4 = forms.ChoiceField(label='Main Character Color', choices=numeritos)

        name5 = forms.CharField(label='Player Name', max_length=23)
        twitter5 = forms.CharField(label='Twitter Handle', max_length=16, required=False)
        char5 = forms.ChoiceField(label='Main Character', choices=chars)
        color5 = forms.ChoiceField(label='Main Character Color', choices=numeritos)

        name6 = forms.CharField(label='Player Name', max_length=23)
        twitter6 = forms.CharField(label='Twitter Handle', max_length=16, required=False)
        char6 = forms.ChoiceField(label='Main Character', choices=chars)
        color6 = forms.ChoiceField(label='Main Character Color', choices=numeritos)

        name7 = forms.CharField(label='Player Name', max_length=23)
        twitter7 = forms.CharField(label='Twitter Handle', max_length=16, required=False)
        char7 = forms.ChoiceField(label='Main Character', choices=chars)
        color7 = forms.ChoiceField(label='Main Character Color', choices=numeritos)

        name8 = forms.CharField(label='Player Name', max_length=23)
        twitter8 = forms.CharField(label='Twitter Handle', max_length=16, required=False)
        char8 = forms.ChoiceField(label='Main Character', choices=chars)
        color8 = forms.ChoiceField(label='Main Character Color', choices=numeritos)

        ttext = forms.CharField(label='Top Left Text', max_length=50, required=False)
        btext = forms.CharField(label='Bottom Text', max_length=70, required=False)
        url = forms.CharField(label='Top Right', max_length=55, required=False, initial="https://top8er.com/")

        if efz :
            palette1 = forms.FileField(label="Color Palette", required=False)
            palette2 = forms.FileField(label="Color Palette", required=False)
            palette3 = forms.FileField(label="Color Palette", required=False)
            palette4 = forms.FileField(label="Color Palette", required=False)
            palette5 = forms.FileField(label="Color Palette", required=False)
            palette6 = forms.FileField(label="Color Palette", required=False)
            palette7 = forms.FileField(label="Color Palette", required=False)
            palette8 = forms.FileField(label="Color Palette", required=False)
            
    class GenForm(NoExtraForm):
        extra11 = forms.ChoiceField(label=extra_label1, choices=e_chars, required=False)
        extra_color11 = forms.ChoiceField(label='Secondary Character Color', choices=num_e, required=False)
        extra12 = forms.ChoiceField(label=extra_label2, choices=e_chars, required=False)
        extra_color12 = forms.ChoiceField(label='Tertiary Character Color', choices=num_e, required=False)

        extra21 = forms.ChoiceField(label=extra_label1, choices=e_chars, required=False)
        extra_color21 = forms.ChoiceField(label='Secondary Character Color', choices=num_e, required=False)
        extra22 = forms.ChoiceField(label=extra_label2, choices=e_chars, required=False)
        extra_color22 = forms.ChoiceField(label='Tertiary Character Color', choices=num_e, required=False)

        extra31 = forms.ChoiceField(label=extra_label1, choices=e_chars, required=False)
        extra_color31 = forms.ChoiceField(label='Secondary Character Color', choices=num_e, required=False)
        extra32 = forms.ChoiceField(label=extra_label2, choices=e_chars, required=False)
        extra_color32 = forms.ChoiceField(label='Tertiary Character Color', choices=num_e, required=False)

        extra41 = forms.ChoiceField(label=extra_label1, choices=e_chars, required=False)
        extra_color41 = forms.ChoiceField(label='Secondary Character Color', choices=num_e, required=False)
        extra42 = forms.ChoiceField(label=extra_label2, choices=e_chars, required=False)
        extra_color42 = forms.ChoiceField(label='Tertiary Character Color', choices=num_e, required=False)

        extra51 = forms.ChoiceField(label=extra_label1, choices=e_chars, required=False)
        extra_color51 = forms.ChoiceField(label='Secondary Character Color', choices=num_e, required=False)
        extra52 = forms.ChoiceField(label=extra_label2, choices=e_chars, required=False)
        extra_color52 = forms.ChoiceField(label='Tertiary Character Color', choices=num_e, required=False)

        extra61 = forms.ChoiceField(label=extra_label1, choices=e_chars, required=False)
        extra_color61 = forms.ChoiceField(label='Secondary Character Color', choices=num_e, required=False)
        extra62 = forms.ChoiceField(label=extra_label2, choices=e_chars, required=False)
        extra_color62 = forms.ChoiceField(label='Tertiary Character Color', choices=num_e, required=False)

        extra71 = forms.ChoiceField(label=extra_label1, choices=e_chars, required=False)
        extra_color71 = forms.ChoiceField(label='Secondary Character Color', choices=num_e, required=False)
        extra72 = forms.ChoiceField(label=extra_label2, choices=e_chars, required=False)
        extra_color72 = forms.ChoiceField(label='Tertiary Character Color', choices=num_e, required=False)

        extra81 = forms.ChoiceField(label=extra_label1, choices=e_chars, required=False)
        extra_color81 = forms.ChoiceField(label='Secondary Character Color', choices=num_e, required=False)
        extra82 = forms.ChoiceField(label=extra_label2, choices=e_chars, required=False)
        extra_color82 = forms.ChoiceField(label='Tertiary Character Color', choices=num_e, required=False)

    if hasextra : return GenForm
    else : return NoExtraForm
    
