# Pip's Quest <img src="https://user-images.githubusercontent.com/8831999/217668505-10ab2292-303a-4e26-876a-4df39993b9a3.png" width="32">

A roguelite involving a hamster wizard, cursed critters, and an evil snake. Inspired by EarthBound and Slay The Spire. Hastily hacked together in Python.

Play [online](https://benwakefield.dev/pips-quest) or download the [latest release](https://github.com/wenbakefield/PipsQuest/releases)!

https://user-images.githubusercontent.com/8831999/216470287-0950ce77-a133-4106-b28a-7875c05fc3d7.mp4

## Tutorial
You will play as a hamster wizard, journeying through the land, encountering demonic critters who are trying to stop you.
The critters are held captive under a spell, something seems to be controlling them.
You've detected a high concentration of arcane energy, emanating from Conda Cavern in the East.

What could it be?

### Runes
You will have a collection of runes for each encounter that you can use to craft your spell.
If you are unsatisfied with the hand that you were dealt, you can reroll it once per turn using the reroll button.
Each rune has an element type and a power level.

### Element Types
Offensive element types are: Fire (Red) and Spark (Yellow)

Defensive element types are: Ice (Blue) and Earth (Green)

The wildcard element type is: Arcane (Purple)

The first rune in your spell will determine whether the spell is offensive or defensive.
You may not use an arcane rune as the first rune in your spell.

### Power Levels
In your spell, you can chain runes together if their power level differs by 1.
Arcane runes will automatically be given a power level that satisfies this rule.
Press the + icon underneath a rune to add it to your spell.
Press the - icon underneath a rune to remove it from your spell.

Examples of valid spells:

![E3](<https://github.com/wenbakefield/pips-quest/blob/master/images/rune_earth/3.png>) ![F2](<https://github.com/wenbakefield/pips-quest/blob/master/images/rune_fire/2.png>) ![F3](<https://github.com/wenbakefield/pips-quest/blob/master/images/rune_fire/3.png>)

![I4](<https://github.com/wenbakefield/pips-quest/blob/master/images/rune_ice/4.png>) ![F3](<https://github.com/wenbakefield/pips-quest/blob/master/images/rune_fire/3.png>) ![E2](<https://github.com/wenbakefield/pips-quest/blob/master/images/rune_earth/2.png>) ![S3](<https://github.com/wenbakefield/pips-quest/blob/master/images/rune_spark/3.png>)

![I1](<https://github.com/wenbakefield/pips-quest/blob/master/images/rune_ice/1.png>) ![F2](<https://github.com/wenbakefield/pips-quest/blob/master/images/rune_fire/2.png>) ![A?](<https://github.com/wenbakefield/pips-quest/blob/master/images/rune_arcane/1.png>) ![S4](<https://github.com/wenbakefield/pips-quest/blob/master/images/rune_spark/4.png>) ![F3](<https://github.com/wenbakefield/pips-quest/blob/master/images/rune_fire/3.png>)

A cast button will appear once you have crafted a valid spell.
Runes that you don't use will remain in your hand for the current battle, but will be rerolled for the next battle.

### Encounters
You will journey through five areas, with three encounters in each, with a final boss in the sixth area.
The game will automatically save between each area.

### The Shop
At the end of each area, you will come across a shop.
If you are running low on health, you can spend your gold to heal.
The rate is 1 gold for 1 health point.
However, you are scored at the end of your adventure based on how much gold you have, so spend wisely.

After leaving the shop, you will choose an area to go to next.

Good luck, and have fun!

## Credits
- Ben Wakefield (Programming)
- Stone Chang (System Design)
- Luna Le (Character Art/Animation)
- Liam Thornton (UI/Background Art)

## Special Thanks
- Professor Chris Barney (Northeastern University)
