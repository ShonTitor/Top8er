# How to help top8er.com

This project got significantly bigger than I inititally anticipated. There are still many improvements I want to do with the code and games I want to add. 
However, for certain games it takes me a while to collect, organize and adjust the assets. I'm writing this guide in case there is anyone who wants to help me add any particular game to Top8er.  

There are a few things that are necessary to add a game to Top8er:
- 512x512 Portraits for all the colors of all the characters
- 64x64 Icons for all the characters (optional)
- 1423x800 Background relative to the game
- A json file with color descriptions

## About assets

All images must be in `png` format. Dimensions are in pixels and aren't strict. As long as they aren't too big or too small, it'll be fine. 
Both portraits and icons must have transparent backgrounds. "Portraits" is used a loose term here. 
Sprites, cropped full art or anything that would fit nicely on the layout's squares are all valid as "portraits".  

The folder structure must be as follows:
```
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
Where `bg.png` is the background and `0.png 1.png ... n.png` are the character portraits/icons in the order in which they appear in the original game.  

## About the json file

It doesn't necessarily need to be in `.json` format, but it must have the json structure. Here is an example:
```
{
'Bowser': ['Default', 'Red', 'Blue', 'Black'], 
'Captain Falcon': ['Default', 'Black', 'Red', 'White', 'Green', 'Blue'], 
'Donkey Kong': ['Default', 'Black', 'Red', 'Blue', 'Green'], 
'Dr Mario': ['Default', 'Red', 'Blue', 'Green', 'Black'], 
'Falco': ['Default', 'Red', 'Blue', 'Green'], 
'Fox': ['Default', 'Red', 'Blue', 'Green'], 
'Ganondorf': ['Default', 'Red', 'Blue', 'Green', 'Purple'], 
'Ice Climbers': ['Default', 'Green', 'Orange', 'Red'], 
'Jigglypuff': ['Default', 'Red', 'Blue', 'Green', 'Yellow'], 
'Kirby': ['Default', 'Yellow', 'Blue', 'Red', 'Green', 'White'], 
'Link': ['Default', 'Red', 'Blue', 'Black', 'White'], 
'Luigi': ['Default', 'White', 'Blue', 'Pink'], 
'Mario': ['Default', 'Yellow', 'Black', 'Blue', 'Green'], 
'Marth': ['Default', 'Red', 'Green', 'Black', 'White'], 
'Mewtwo': ['Default', 'Red', 'Blue', 'Green'], 
'Mr Game & Watch': ['Default', 'Red', 'Blue', 'Green'], 
'Ness': ['Default', 'Yellow', 'Blue', 'Green'], 
'Peach': ['Default', 'Yellow', 'White', 'Blue', 'Green'], 
'Pichu': ['Default', 'Red', 'Blue', 'Green'], 
'Pikachu': ['Default', 'Red', 'Blue', 'Green'], 
'Roy': ['Default', 'Red', 'Blue', 'Green', 'Yellow'], 
'Samus': ['Default', 'Pink', 'Black', 'Green', 'Purple'], 
'Sheik': ['Default', 'Red', 'Blue', 'Green', 'White'], 
'Yoshi': ['Default', 'Red', 'Blue', 'Yellow', 'Pink', 'Cyan'], 
'Young Link': ['Default', 'Red', 'Blue', 'White', 'Black'], 
'Zelda': ['Default', 'Red', 'Blue', 'Green', 'White']
}
```
Each character's name is followed by a list of "descriptions" or "labels" for the characters alts. 
These can be the color of the alt, a button combination or anything descriptive and easy to understand by the game's playerbase.

## Contact
If you have all these ready or have any questions please contact me on [twitter](https://twitter.com/Riokaru) or discord (Riokaru#7131). 
Make sure to send a `.zip`, `.rar` or any other format of your choice containing all the files to prevent any unwanted compression and preserve the folder structure.
