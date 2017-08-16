# Programming 1

As a part of this challenge we were given a python script named [maze_client.py](./maze_client.py). I ran it to get more information about the task.

```
Find the path to your goal...
For example, given this maze:
###########
#>  #     #
# ### ### #
# # X   # #
# ### ### #
#   # #   #
### ### # #
# #     # #
# ####### #
#         #
###########

The solution would be: VVVV>>VV>>>>^^>>^^^^<<<<VV<
```

I used python module [NetworkX](https://networkx.github.io/) for representing the labyrinth as a graph. The shortest path could then be calculated simply by calling shortest_path().

``` python
import networkx as nx

road = ' '
start = '>'
end = 'X'
left = '>'
right = '<'
up = '^'
down = 'V'

def find_point(labyrinth, character):
    '''
    Find a character 'character' from a labyrinth
    and return its coordinates.
    '''
    s = ()
    for i, line in enumerate(labyrinth):
        try:
            s = (i, line.index(character))
            break
        except ValueError:
            continue
    return s

def create_graph(labyrinth):
    ''' Create and return a graph. '''
    G = nx.Graph()
    nodes = get_nodes(labyrinth)
    edges = get_edges(labyrinth, nodes)
    G.add_nodes_from(nodes) # Add nodes
    G.add_edges_from(edges) # Add edges
    return G

def get_nodes(labyrinth):
    '''
    Based on the input labyrinth,
    find all nodes of the graph.
    '''
    nodes = []
    for i in range(len(labyrinth[0])):
        for j in range(len(labyrinth)):
            if labyrinth[j][i] in [road, start, end]:
                nodes.append((j,i))
    return nodes

def get_edges(labyrinth, nodes):
    '''
    Based on the input labyrinth,
    find all edges of the graph.
    '''
    edges = []
    for node in nodes:
        i = node[0]
        j = node[1]
        if labyrinth[i+1][j] == road:
            edges.append(((i,j),(i+1,j)))
        if labyrinth[i][j+1] == road:
            edges.append(((i,j),(i,j+1)))
        if labyrinth[i-1][j] == road:
            edges.append(((i,j),(i-1,j)))
        if labyrinth[i][j-1] == road:
            edges.append(((i,j),(i,j-1)))
    return edges

def convert_path_to_string(path):
    '''
    Takes a networkx path as input parameter, and
    uses it to create a task specific response string.
    '''
    path_str = ''
    for i, node in enumerate(path):
        if i == 0:
            previous = node
            continue
        if node[0] > previous[0]:
            path_str += down
        elif node[0] < previous[0]:
            path_str += up
        elif node[1] > previous[1]:
            path_str += left
        elif node[1] < previous[1]:
            path_str += right
        previous = node
    return path_str

def get_path(labyrinth_str):
    labyrinth_str = labyrinth_str.split('\n')
    labyrinth = [list(line) for line in labyrinth_str]

    start = find_point(labyrinth, '>') # Get path start point coordinates
    end = find_point(labyrinth, 'X') # Get path end point coordinates
    graph = create_graph(labyrinth)

    path = nx.shortest_path(graph,source=start,target=end)
    return convert_path_to_string(path) # Convert path to task format
```

Finally, I called the get_path() function from the maze_client.py script. The flag was PAN{my_f1rst_labyM4z3.jpeg}.
