import re
from django import forms
from collections import Mapping
from typing import Type
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
                 'Pokémon Trainer', 'Pyra and Mythra', 'Mythra and Pyra', 'Richter', 'Ridley', 'ROB', 'Robin', 'Rosalina & Luma', 'Roy', 'Ryu', 'Samus',
                 'Sephiroth',
                 'Sheik', 'Shulk', 'Simon', 'Snake', 'Sonic', 'Steve', 'Terry', 'Toon Link', 'Villager', 'Wario',
                 'Wii Fit Trainer', 'Wolf', 'Yoshi', 'Young Link', 'Zelda', 'Zero Suit Samus']
        echars = ['Banjo & Kazooie', 'Bayonetta', 'Bowser', 'Bowser Jr', 'Byleth',
                 'Captain Falcon', 'Chrom', 'Cloud', 'Corrin', 'Daisy', 'Dark Pit', 'Dark Samus',
                 'Diddy Kong', 'Donkey Kong', 'Dr Mario', 'Duck Hunt', 'Falco', 'Fox', 'Ganondorf',
                 'Greninja', 'Hero', 'Ice Climbers', 'Ike', 'Incineroar', 'Inkling', 'Isabelle',
                 'Jigglypuff', 'Joker', 'Ken', 'King Dedede', 'King K Rool', 'Kirby', 'Link', 'Little Mac',
                 'Lucario', 'Lucas', 'Lucina', 'Luigi', 'Mario', 'Marth', 'Mega Man', 'Meta Knight',
                 'Mewtwo', 'Mii Brawler', 'Mii Gunner', 'Mii Swordfighter', 'Min Min', 'Mr Game & Watch',
                 'Ness', 'Olimar', 'Pac-Man', 'Palutena', 'Peach', 'Pichu', 'Pikachu', 'Piranha Plant', 'Pit',
                 'Pokémon Trainer', 'Pyra and Mythra', 'Mythra and Pyra', 'Richter', 'Ridley', 'ROB', 'Robin', 'Rosalina & Luma', 'Roy', 'Ryu', 'Samus',
                 'Sephiroth',
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
        e_chars = ["None"]+echars
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

    flag_choices = ['None', 'Abkhazia', 'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 
                    'Antigua and Barbuda', 'Argentina', 'Armenia', 'Artsakh', 'Australia', 'Austria', 
                    'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 
                    'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 
                    'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 
                    'Cape Verde', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 
                    'Comoros', 'Cook Islands', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 
                    'Democratic Republic of Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 
                    'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 
                    'Eswatini', 'Ethiopia', 'Federated States of Micronesia', 'Fiji', 'Finland', 'France', 
                    'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 
                    'Guinea-Bissau', 'Guinea', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 
                    'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 
                    'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 
                    'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar', 
                    'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 
                    'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 
                    'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'North Korea', 
                    'North Macedonia', 'Northern Cyprus', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 
                    'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 
                    'Republic of China (Taiwan)', 'Republic of Congo', 'Romania', 'Russia', 'Rwanda', 
                    'Sahrawi Arab Democratic Republic', 'Saint Kitts and Nevis', 'Saint Lucia', 
                    'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Saudi Arabia', 'Senegal', 'Serbia', 
                    'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 
                    'Somaliland', 'South Africa', 'South Korea', 'South Ossetia', 'South Sudan', 'Spain', 'Sri Lanka', 
                    'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'São Tomé and Príncipe', 'Tajikistan', 
                    'Tanzania', 'Thailand', 'Togo', 'Tonga', 'Transnistria', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 
                    'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 
                    'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe', 
                    'Agender Pride', 'Aromantic Pride', 'Asexual Pride', 'Bigender Pride', 'Bisexual Pride', 'Demiromantic Pride', 
                    'Demisexual Pride', 'Gay Pride', 'Gender Fluid', 'Genderqueer Pride', 'Intersex Pride', 'Lesbian Pride', 
                    'Non-binary', 'Pansexual Pride', 'Polyamory Pride', 'Polysexual Pride', 'Transgender Pride']
    flag_choices = [(c,c) for c in flag_choices]

    player_fields = {'name': forms.CharField(label='Player Name', max_length=40), 
                     'twitter': forms.CharField(label='Twitter Handle', max_length=16, required=False),
                     'char': forms.ChoiceField(label='Main Character', choices=chars),
                     'color': forms.ChoiceField(label='Main Character Color', choices=numeritos),
                     'flag': forms.ChoiceField(label='Flag', choices=flag_choices)
                    }
    if hasextra :
        player_fields['extra1'] = forms.ChoiceField(label=extra_label1, choices=e_chars, required=False)
        player_fields['extra_color1'] = forms.ChoiceField(label='Secondary Character Color', choices=num_e, required=False)
        player_fields['extra2'] = forms.ChoiceField(label=extra_label2, choices=e_chars, required=False)
        player_fields['extra_color2'] = forms.ChoiceField(label='Tertiary Character Color', choices=num_e, required=False)
    if efz :
        player_fields['palette'] = forms.FileField(label="Color Palette", required=False)

    class PlayerField(forms.MultiValueField) :
        def __init__(self, *args, **kwargs):

            fields = tuple(player_fields.values())
            super().__init__(fields, 
                             require_all_fields=False, 
                             widget=PlayerWidget(), 
                             *args, **kwargs)
 
        def compress(self, data_list):
            return {key: data_list[i] for i, key in enumerate(player_fields.keys())}

    class PlayerWidget(forms.MultiWidget):
        if hasextra :
            template_name = "player_form_with_extra.html"
        else :
            template_name = "player_form.html"

        def __init__(self, *args, **kwargs):
            widgets = {}
            for name, field in player_fields.items() :
                widget = field.widget
                widget.attrs['label'] = field.label
                widget.attrs['required'] = widget.is_required
                widgets[name] = widget
            super().__init__(widgets=widgets, *args, **kwargs)
        
        # Weird hack I shouldn't have to do
        def get_context(self, name, value, attrs):
            context = super().get_context(name, value, attrs)
            for i in range(len(context['widget']['subwidgets'])):
                subwidget = context['widget']['subwidgets'][i]
                context['widget']['subwidgets'][i]["attrs"]["required"] = subwidget["required"]
            return context

        def decompress(self, value):
            if isinstance(value, Mapping):
                return [value.get(name) for name in player_fields.keys()]
            else :
                return [None for i in player_fields.keys()]

    class GenForm(AncestorForm) :
        lcolor1 = RGBColorField(label="Main Color", initial=cc1)
        lcolor2 = RGBColorField(label="Highlight Color", initial=cc2)

        player1 = PlayerField()
        player2 = PlayerField()
        player3 = PlayerField()
        player4 = PlayerField()
        player5 = PlayerField()
        player6 = PlayerField()
        player7 = PlayerField()
        player8 = PlayerField()

        ttext = forms.CharField(label='Top Left Text', max_length=50, required=False)
        btext = forms.CharField(label='Bottom Text', max_length=70, required=False)
        url = forms.CharField(label='Top Right', max_length=55, required=False, initial="https://top8er.com/")

    return GenForm
    
