# How to help top8er.com

This project got significantly bigger than I inititally anticipated. There are still many improvements I want to do with the code and games I want to add. 
However, for certain games it takes me a while to collect, organize and adjust the assets. I'm writing this guide in case there is anyone who wants to help me add any particular game to Top8er.  

There are a few things that are necessary to add a game to Top8er:
- 512x512 Portraits for all the colors of all the characters
- 64x64 Icons for all the characters (optional)
- 1423x800 Background relative to the game
- A json file with additional data
- A transparent logo of the game

## About assets

All images must be in `png` format. Dimensions are in pixels and aren't strict. As long as they aren't too big or too small, it'll be fine. 
Both portraits and icons must have transparent backgrounds. "Portraits" is used a loose term here. 
Sprites, cropped full art or anything that would fit nicely on the layout's squares are all valid as "portraits".  

The folder structure must be as follows:
```
        game/
             game.json
             logo.png
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
Where `bg.png` is the background and `0.png 1.png ... n.png` are the character portraits/icons in the order in which they appear in the original game.  

## About the json file

JSON stands for JavaScript Object Notation. It's a text format with strict syntax. It is adviced to use a [JSON Validator](https://jsonlint.com) to verify it is correct. The JSON file must be named `game.json` and must have the following data:  
`name`: The full name of the game (written without any abbreviations).  
`characters`: A list with all the names of the characters (must match the names of their respective folders).  
`colors`: A dictionary where the keys are the character names and the values are lists with a description of each of the character's skins in order (The first description in the list must match with the corresponding `0.png` file, the second one with the `1.png` file and so on). If your game has no alternate colors, you can leave it as `null` (which is a special value, not a string).  
`iconColors`: Analogous to `colors` but as a separate dict for icons. Use only if the "characters" available (For example, Melty Blood AACC Moons). Leave it as         `null` otherwise.  
`hasIcons`: Boolean indicating whether your game has icons (used for secondaries).  
`blackSquares`: Boolean indicating whether the "Black Squares" settings will be on by default (when this setting is on, there will be a black background behind each character).  
`defaultLayoutColors`: List containing two 24-bit colors in hexadecimal where the first will be the default main layout color and the second will be the default highlight color. For this you can use a [Color Picker](https://www.w3schools.com/colors/colors_picker.asp).  
`colorGuide`: An external URL detailing the game alternate skins for better clarity. This is optional, leave as `null` if you don't wish to include it.  

Below there's an example of what a `game.json` could look like for Super Smash Bros Melee. Notice that the only difference between `colors` and `iconColors` is the inclusion/exclusion of "Random".
```
{
    "name": "Super Smash Bros Melee",
    "characters": ["Random", "Bowser", "Captain Falcon", "Donkey Kong", "Dr Mario", "Falco", "Fox", "Ganondorf", "Ice Climbers", "Jigglypuff", "Kirby", "Link", "Luigi", "Mario", "Marth", "Mewtwo", "Mr Game & Watch", "Ness", "Peach", "Pichu", "Pikachu", "Roy", "Samus", "Sheik", "Yoshi", "Young Link", "Zelda"],
    "colors": {
        "Random": ["Sandbag", "Quetion Mark"],
        "Bowser": ["Default", "Red", "Blue", "Black"], 
        "Captain Falcon": ["Default", "Black", "Red", "White", "Green", "Blue"], 
        "Donkey Kong": ["Default", "Black", "Red", "Blue", "Green"], 
        "Dr Mario": ["Default", "Red", "Blue", "Green", "Black"], 
        "Falco": ["Default", "Red", "Blue", "Green"], 
        "Fox": ["Default", "Red", "Blue", "Green"], 
        "Ganondorf": ["Default", "Red", "Blue", "Green", "Purple"], 
        "Ice Climbers": ["Default", "Green", "Orange", "Red"], 
        "Jigglypuff": ["Default", "Red", "Blue", "Green", "Yellow"], 
        "Kirby": ["Default", "Yellow", "Blue", "Red", "Green", "White"], 
        "Link": ["Default", "Red", "Blue", "Black", "White"], 
        "Luigi": ["Default", "White", "Blue", "Pink"], 
        "Mario": ["Default", "Yellow", "Black", "Blue", "Green"], 
        "Marth": ["Default", "Red", "Green", "Black", "White"], 
        "Mewtwo": ["Default", "Red", "Blue", "Green"], 
        "Mr Game & Watch": ["Default", "Red", "Blue", "Green"], 
        "Ness": ["Default", "Yellow", "Blue", "Green"], 
        "Peach": ["Default", "Yellow", "White", "Blue", "Green"], 
        "Pichu": ["Default", "Red", "Blue", "Green"], 
        "Pikachu": ["Default", "Red", "Blue", "Green"], 
        "Roy": ["Default", "Red", "Blue", "Green", "Yellow"], 
        "Samus": ["Default", "Pink", "Black", "Green", "Purple"], 
        "Sheik": ["Default", "Red", "Blue", "Green", "White"], 
        "Yoshi": ["Default", "Red", "Blue", "Yellow", "Pink", "Cyan"], 
        "Young Link": ["Default", "Red", "Blue", "White", "Black"], 
        "Zelda": ["Default", "Red", "Blue", "Green", "White"]
    },
    "iconColors": {
        "Bowser": ["Default", "Red", "Blue", "Black"], 
        "Captain Falcon": ["Default", "Black", "Red", "White", "Green", "Blue"], 
        "Donkey Kong": ["Default", "Black", "Red", "Blue", "Green"], 
        "Dr Mario": ["Default", "Red", "Blue", "Green", "Black"], 
        "Falco": ["Default", "Red", "Blue", "Green"], 
        "Fox": ["Default", "Red", "Blue", "Green"], 
        "Ganondorf": ["Default", "Red", "Blue", "Green", "Purple"], 
        "Ice Climbers": ["Default", "Green", "Orange", "Red"], 
        "Jigglypuff": ["Default", "Red", "Blue", "Green", "Yellow"], 
        "Kirby": ["Default", "Yellow", "Blue", "Red", "Green", "White"], 
        "Link": ["Default", "Red", "Blue", "Black", "White"], 
        "Luigi": ["Default", "White", "Blue", "Pink"], 
        "Mario": ["Default", "Yellow", "Black", "Blue", "Green"], 
        "Marth": ["Default", "Red", "Green", "Black", "White"], 
        "Mewtwo": ["Default", "Red", "Blue", "Green"], 
        "Mr Game & Watch": ["Default", "Red", "Blue", "Green"], 
        "Ness": ["Default", "Yellow", "Blue", "Green"], 
        "Peach": ["Default", "Yellow", "White", "Blue", "Green"], 
        "Pichu": ["Default", "Red", "Blue", "Green"], 
        "Pikachu": ["Default", "Red", "Blue", "Green"], 
        "Roy": ["Default", "Red", "Blue", "Green", "Yellow"], 
        "Samus": ["Default", "Pink", "Black", "Green", "Purple"], 
        "Sheik": ["Default", "Red", "Blue", "Green", "White"], 
        "Yoshi": ["Default", "Red", "Blue", "Yellow", "Pink", "Cyan"], 
        "Young Link": ["Default", "Red", "Blue", "White", "Black"], 
        "Zelda": ["Default", "Red", "Blue", "Green", "White"]
    },
    "hasIcons": true,
    "blackSquares": false,
    "defaultLayoutColors": ["#FF281A", "#FFB60C"],
    "colorGuide": "https://www.ssbwiki.com/Alternate_costume_(SSBM)"
}
```

## Contact
If you have followed these instructions or have any questions please join the [Top8er discord](https://discord.gg/pPS92jYvJT) and post on the appropriate channel. 
Make sure to send a `.zip`, `.rar` or any other format of your choice containing all the files to prevent any unwanted compression and preserve the folder structure.
