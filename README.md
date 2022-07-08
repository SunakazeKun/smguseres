# Super Mario Galaxy 2 UseResource Generator
This is a Python tool to aid with the generation of UseResource archives in *Super Mario Galaxy 2*. These files store preload lists containing the archives and sounds to be loaded while the game is running. This drastically speeds up loading times and should always be used for more professional mods. The tool operates with log files from the Dolphin emulator and generates the actual *UseResource.arc* files from the logged information.

# Setup
This library requires **Python 3.6** or newer, [pyjmap](https://github.com/SunakazeKun/pyjmap) and [pyjkernel](https://github.com/SunakazeKun/pyjkernel). You can use pip to install this tool; the other dependencies will be installed automatically.
```
pip install smguseres
```

# Tutorial
At first, the process may appear a bit confusing and tedious, but it's actually fairly simple. This small tutorial guides you through the basics of this tool. Again, make sure that you have installed the tool using pip.

## Preparations
There are only two more things you need, but I'm pretty sure you got those already.
- The **Dolphin Emulator**. I recommend version 5.0-16380 or newer.
- The dumped files from **Super Mario Galaxy 2**.
- **smg2_useres_helper_EJP.xml** and **smg2_useres_helper_WK**. You can find these in this repository.

Now, it's time to prepare the folders and Dolphin configurations.
1. Open *Dolphin* and right click on *Super Mario Galaxy 2* and select *Start with Riivolution Patches*. Hit the button that says *Open Riivolution XML...* and navigate to one of the two XML files that you downloaded earlier. If you are playing the American, European, Australian or Japanese version of the game, select **smg2_useres_helper_EJP.xml**. If you are playing the Taiwanese or Korean version of the game, select **smg2_useres_helper_WK.xml** instead. Then, make sure that the option *Use UseResource helper?* is set to *Enabled*.
2. Now, select *View* in the menu bar and make sure that *Show Log* and *Show Log Configuration* are checked. Then, go to the *Log Configuration* panel and make sure that the *OSReport EXI (OSREPORT)* option is enabled.
3. Go to the folder that contains the game's files. It's the one that contains the StageData, ObjectData and several other folders. Here, create a new folder called *UseResourceLogs*. This is where you'll have to write the logged files in.

## Scripting
As we are using Python, we can automatize the process of generating our archives. Below is an example script that you can freely copy and use. Just copy the lines and save them to a *.py* file. In this example we'll call this file ``useresgen.py``.

```python
import argparse
from smguseres import UseResourceGenerator

game_path = "D:/Modding/Super Mario Galaxy/SMG2/files"
builders = [
    # Takes three arguments. Game files path, Galaxy name and number of scenarios.
    # Number of scenarios does not include Green Stars and Hidden Stars.
    UseResourceGenerator(game_path, "IslandFleetGalaxy", 3),
    UseResourceGenerator(game_path, "YosshiHomeGalaxy", 3),
    UseResourceGenerator(game_path, "DigMineGalaxy", 3),
    UseResourceGenerator(game_path, "MokumokuValleyGalaxy", 2),
    UseResourceGenerator(game_path, "AbekobeGalaxy", 2),
    UseResourceGenerator(game_path, "RedBlueExGalaxy", 2)
]

def generate(args):
    for builder in builders:
        builder.write_analyzed()

def clear(args):
    for builder in builders:
        builder.write_dummy()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    subs = parser.add_subparsers(dest="command", help="Command")
    subs.required = True

    clear_parser = subs.add_parser("clear", description="Create dummy UseResource archives.")
    clear_parser.set_defaults(func=clear)

    generate_parser = subs.add_parser("generate", description="Generate UseResource archives from logs.")
    generate_parser.set_defaults(func=generate)

    args = parser.parse_args()
    args.func(args)

```

Don't worry, you need basically zero coding knowledge in order to use this.
1. In the script file, add new UseResourceGenerator entries for your galaxies. The file already contains examples from World 1. It's important to note that you should not count Hidden and Green Stars among scenarios.
2. Also, don't forget to adjust ``game_path`` to the folder that contains your game files.
2. Open the command prompt and navigate to the folder containing ``useresgen.py``. Now, type in  ``python useresgen.py clear``. This clears the UseResource archives for these galaxies. You'll always have to do this if you want to generate new UseResource files for your galaxies. Since UseResource generation is one of the last steps during level creation, you won't be doing this often.

## Logging
In order to generate our archives, we need input data. In this example we'll use *RedBlueExGalaxy* which has two main scenarios in the final game. The normal Star (Scenario 1) and the Comet Star (Scenario 2).
1. Go to the *Log* view in Dolphin, right click on the game and select *Start with Riivolution Patches...*. Again, make sure the UseResource helper is enabled. Then, just launch the game. You'll see that the log fills with all sorts of information. But we don't need this for now.
2. Go to the world map and move over the galaxy you want to generate the logs for. Don't access the Star Select screen, though. In Dolphin's *Log* panel, click on *Clear* to clear the entire log.
3. Now you can access the galaxy' Star Select. You'll notice that the log fills with a few file paths for stage-related files. 
4. Select Star 1. The log will be filled with even more lines. Once the log does not fill anymore, copy all the logged lines and open a text editor (Notepad, Notepad++, etc.). Create a new file and paste the lines in there. Then, save the file as *RedBlueExGalaxy_Scenario1.txt* and store it in the *UseResourceLogs* folder you created earlier.
5. Exit out of the level and you'll be on the world map again. Clear the Dolphin log yet again and go to the Star Select screen again. However, now you should select Star 2. Like above, wait for the game to load all the data first. Copy all the lines, save them as *RedBlueExGalaxy_Scenario2.txt* and store it in the *UseResourceLogs* folder.
6. Repeat this process for all of the galaxies you want to generate *UseResource* files for.
7. After this, close the game again.

## Packing
We're almost done.
1. Open the command prompt again and navigate to the folder containing ``useresgen.py``. Now, type in  ``python useresgen.py generate``. This will scan the logs and generate the *UseResource* archives. The archives will be automatically stored in the StageData folders.
2. Boot the game again and select one of the missions you were logging earlier. You should notice that the loading time is pretty much non-existent anymore.