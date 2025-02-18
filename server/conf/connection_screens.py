# -*- coding: utf-8 -*-
"""
Connection screen

This is the text to show the user when they first connect to the game (before
they log in).

To change the login screen in this module, do one of the following:

- Define a function `connection_screen()`, taking no arguments. This will be
  called first and must return the full string to act as the connection screen.
  This can be used to produce more dynamic screens.
- Alternatively, define a string variable in the outermost scope of this module
  with the connection string that should be displayed. If more than one such
  variable is given, Evennia will pick one of them at random.

The commands available to the user when the connection screen is shown
are defined in evennia.default_cmds.UnloggedinCmdSet. The parsing and display
of the screen is done by the unlogged-in "look" command.
"""

CONNECTION_SCREEN = """
 `Y .oooooo..o                                           
 d8P'    Y8                                           
 Y88bo.        oooo  oooo  ooo.oooo     .ooooo.  oooo d8b 
  "Y8888o.     888   888   '88'  88b  d88' 88O'  888""8P 
     ""Y88b   .888   888   888  888  888ooo'''  888     
 oo     .d8P  888   888   888   88  888    .n  888     
 8""88888P'   V8'\"""V8P  888bod8P'  Y8bod8P' d888b    
                        888                          
                      o888o                         
                                                      
 ooo        ooooo  ooooo     ooo  oooooooooo.            
  88.       .888'   888       8    888'   Y8D.
  888b     d'888    888       8   888      888          
  8 Y88. .P  888   888       8   888      888          
  8  888'    888  '88       8   '88      888          
  8    Y     888   88.    .8'   888     d88'          
 o8o        o888o   'YbodP'   o8888bood8P'`x
 
SuperMUD Phase 2 code by Printer and Editor, using the Evennia framework
Combat system inspired by Haven, written by Tyr and Discordance
World created by MEZ
Special Thanks to Bustahemo, Petal, and dkasak
Dedicated to Torn
 
`cWelcome to SuperMUD, a love letter to superhero media that takes place in an
alternate Earth where the existence of superhumans have shaped American history 
significantly since the 1940s. While our game is a love letter to comic book
giants DC and Marvel, the characters created in SuperMUD are pastiches, analogs 
and tributes to these characters, and should otherwise be original.
 
Our game takes place in Bendis City, a sprawling metropolis in California, that
just so conveniently happens to be the center of the fantastic, where heroes and
villains brawling is the price you pay for the cheap real estate and the chance
to rub shoulders with greatness.`x
"""
