# Readme file to explain the tool

## Arrange Mecabrick imports

This tools cleans, organizes and prepares a blender scene that contains an imported file from [MecaBricks](https://mecabricks.com/en/) website.

The tools is inspired by another great tutorial from Arvid Schneider: [Rendering Photoreal Lego - Applying advanced shading techniques with Arnold | ep#604](https://www.youtube.com/watch?v=ytNta8JHkU8)

## Getting Started

Once you import a file inside all the elements appears to be ungrouped and with ununderstandable names. Now you will need to rename the shaders manually. Once you it's done it's time to run the tool.

### Prerequisites

Blender 2.8x

```text
Just copy or open the code into the script editor and run it.
```

## Running the tool

### Break down into end to end tests

The tool does the following steps:

* Get Materials in scene & objects.
* Creates default grey material.
* Create collections and add items.

Extra:

* Adds default grey material to all the renamed pieces, clearing all materials first.

## Finish

Once is completed the scene contains all the elements properly named ready to be exported as Alembic or any other file format.
