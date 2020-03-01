# Readme file to explain the tool

## Arrange Mecabrick OBJ and DAE imports

## Getting Started

This tools cleans, organizes and prepares a blender scene that contains an imported file from [MecaBricks](https://mecabricks.com/en/) website.

The tools is inspired by a great tutorial from Arvid Schneider: [Rendering Photoreal Lego - Applying advanced shading techniques with Arnold | ep#604](https://www.youtube.com/watch?v=ytNta8JHkU8) and [ElephantVFX](http://www.elephantvfx.com/) tutorial using Lego sets.

When importing an OBJ or DAE (Collada) file into Blender all the elements appears to be ungrouped and with ununderstandable names. With this simnple tool I create a basic of sctructure and naming convention to make working with the file easier.

### Prerequisites

Blender 2.8x

```text
Just copy or open the code into the script editor and run it.
```

## Running the tool

### Breakdown

The tool does the following steps:

* Get Materials in scene & objects.
* Creates default grey material.
* Create collections and add items into them.

Extra:

* If selected, adds default grey material to all the renamed pieces, clearing all materials first.

## Result

Once is completed the scene contains all the elements properly named ready to be exported as Alembic or any other file format. You can see example [screengrabs](#screengrabs) below.

**Final Collection structure**

```text
Lego_GRP
├── ShaderName_GRP
│   └── Piece_ShaderName.####
│   └── Piece_ShaderName.####
├── ShaderName_GRP
│   └── Piece_ShaderName.####
├── ShaderName_GRP
│   └── Piece_ShaderName.####
...
```

## Screengrabs

The file imported has non-descriptive part names and non-understandable names on the shaders, making it hard to work with the file as is.
![Alt text](images/arrange_0-import_web.PNG?raw=true "Imported file")
*Imported file*

The first step is to rename the shaders accordingly manually. A bit tidious, so if you don't want to do it... it will work but you will have weird names. Once it's done it's time to run the tool.
![Alt text](images/arrange_1-import_web.PNG?raw=true "Cleaned shader names")
*Cleaned shader names*

Load the script to run it in the script editor.
![Alt text](images/arrange_2-import_web.PNG?raw=true "Load Script")
*Load Script*

The final result once the tool is executed is a tree structure in the outliner.
![Alt text](images/arrange_3-import_web.PNG?raw=true "Final scene")
*Final scene*

If you want to keep the materials linked in the scene you just need to change the variable value to "False".

## TO-DO

* Provide a UI to easy setup and run the tool.
