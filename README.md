# Name: Jacob Lorenzo
# Date: 4/16/25 - 5/3/25
# Course: COS 598
# Instructor: Dr. Hutchinson
# Assignment: Homework 5

# Notes:
- What do we want to do with the project? 
- Make a game?
- Make a generator?
- Make a rougelite?

## Concept:
- Roguelite game with DragonQuest Elements.
- Class-based system
- AI for monsters

## Ideas:
- Cellular automata similar to the in class
    - Could work, but we want smooth walls, I want the hero to be going through the halls of Moria, not of a cave. Could do a pathfinding algorithm around the cave surface to smooth it out.

- Binary space partitioning:
    - Tried and true, but I have an idea for a twist:
        - We partition the spaces, then randomly create rectangles within the area. We deteremine the number of rectangles based on the size of the area. 
        - We then effectively use a form of cellular automata to update the outer wall of the structure. In a 3x3 area, we know that if at least 1 of the tiles is empty, then it has to be a wall. 
        - Hopefully the randomness will mean that it's lumpy. 

## Notes:
- I decided to install mypy recently to improve my code quality and reduce bugs. That's why everything is statically typed.

- Making dungeons is hard, after slamming my head against the desk for days trying to figure out something, my solution is to randomly generate doorway points along the walls and then use a pathfinding algorithm to connect the rooms. 

- In a flash of insight, I realized that the algorithm I created for generating the horizontal corridors could be used on the vertical corridors as I can effectively rotate the map and it uses the same structure. 

# Sources:
- https://medium.com/pythoneers/getting-started-with-trees-in-python-a-beginners-guide-4e68818e7c05

- https://www.pcgbook.com/chapter03.pdf

- https://medium.com/@guribemontero/dungeon-generation-using-binary-space-trees-47d4a668e2d0

- https://jonoshields.com/post/bsp-dungeon

- https://www.redblobgames.com/pathfinding/a-star/implementation.html