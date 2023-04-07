# pathfinder by a-star algorithm

![obraz](https://user-images.githubusercontent.com/83815021/230569429-03fe77f6-862c-43d5-a5d6-a089c9d40075.png)

This program is an example of an a* algorithm. The program has a function find_way(maze, start, end). The maze is a 2D map (labyrinth), the start is the start point (x,y) and the end is the end point (x,y). The algorithm will try to find a way between these two points using the open and close lists. It is not perfect. There are bugs and sometimes the algorithm searches the same nodes. But it was enough and fast to use it in my games.

The program allows you to choose the starting point, ending point and build the maze. On line 140 there is time.sleep(0.1) to slow down the program and show the user how the algorithm finds its way. The blue squares are the current path, the white squares are the search nodes, the orange squares are the endpoint, and finally the red squares are the walls.

You can rebuild line 78:

    moves = ((1, 0), (-1, 0), (0, 1), (0, -1)) 

Algorithm is searching only up, down, right and left nodes. You can add 4 more nodes diagonally.
