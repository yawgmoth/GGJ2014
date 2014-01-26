GGJ2014
=======

My attempt at writing a game for the Global Game Jam 2014. The game itself is nowhere near finished, but the basic infrastructure is there. The idea was to write a fully scriptable Jump'n'Run. Of course, for accessibility, the scripting language of choice was Brainfuck...

Game Idea
---------
The theme "We don't see things as they are, we see them as we are" inspired me to write a Jump'n'Run in which the player character would change size when certain powerups are encountered or regions traversed. This would change their perspective of the whole world, as there would suddenly be obstacles where none where before (e.g. a gap that is too small now), while other obstactles would disappear (like cliffs that where impossible to climb/jump onto before).

Things that do work
-------------------
 - calling Brainfuck code as a function from Python
 - calling Python functions from Brainfuck 
 - loading levels which set up geometry, players and (potentially) enemies
 - collision detection (AABB only)
 
How calling Brainfuck from Python works
---------------------------------------

The call_bf function in the brainfuck module expects a string of Brainfuck source code, an input vector (list of integers), and two dictionaries with callable functions (usually locals() and globals()). Whenever the "read character" BF instruction is encountered, an element from the input vector is consumed and used as input. Conversely, all output is appended to an output list, which is returned by call_bf upon termination of the BF program. Calling python functions works with the special operator ":", which should followed by the name of the function to call, and a list of parameters in parenthesis. The way parameters are parsed is that the brainfuck code between the parenthesis is executed and all output (produced by the BF output operator) is passed to the function as a parameter. For example, to call a python function "f" with 1 as parameter, one would use ":f(+.)" (assuming the current cell was 0 before). The return value of the function can only be a single integer, which is written into the current cell. So, e.g. ":f(:g(+.).)" could be used to call g with 1 as parameter and then pass its return value to f. By convention, string arguments in the API are passed as a list of ASCII values.
 
How the game is supposed to work
--------------------------------
The levels/ directory contains level files. As far as the game is concerned, the menu is just another level (see e.g. level1, which simply spawns a button). The Brainfuck code describing the level has access to the :sp function which expects an id and a name and spawns the named object with default attributes. The :sd function can be used to set attributes of any game object. It expects an id, an attribute index and the new value. Using this it is possible to set up geometry and modify its location/size. Game objects are expected to reside in the rules/ directory, and consist of several files. When they are created the $NAME.init file is executed, and all its output is used as the initial value of the game objects attributes. In each iteration of the update loop, the $NAME.update file is executed for each game object. It is passed the time delta since the last update, input events that happened and the game objects attributes. It is expected to return the new values for each attribute. Finally, if a game object has a $NAME.bb file, this is called to determine its bounding box, expecting it to return the x and y coordinates of the top left corner, a width and a height. With this information, the engine checks for collisions and if any are found, the $NAME.col file is called with an indicator of where the collision occurred (LEFT = 1, RIGHT = 2, TOP = 3, BOTTOM = 4), followed by a zero, followed by the game object's attributes, followed by a zero, followed by the other object's id, followed by the other object's attributes. The call is expected to return the new values of the game object's attributes (but can of course modify the other object's attribute by using :sd). Game objects can also modify the zoom factor of the whole game, to allow the growing/shrinking mechanic to actually work with the player's viewport.



