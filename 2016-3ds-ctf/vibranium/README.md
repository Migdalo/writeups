# Vibranium Circuit Challenge
Programming 400

> Access the server in 54.175.35.248:8003  
EN: Cycles are forbidden. 

In the task description we were only given an IP address to the server and a note that circles are not allowed. To find out what this task was about, we needed to connect to the server. I made a netcat connection to the given IP address and received a bit more information on what we were supposed to do. The info included the following:

>  [+] To save material, we need you to tell us the minimum number of movements
     required to build this circuit.
     
> [+] The print starts from the given point, must run the entire circuit and
     return to the starting point.
     
>  [+] Example: 

                   +-+    +-+    +-+
      start +--->  |1|    |2|    |3|
                   +++    +-+    +++
                    |             |
                    |             |
                   +++    +-+    +++
                   |4+----+5+----+6|
                   +++    +++    +++
                    |      |      |
                    |      |      |
                   +++    +++    +++
                   |7|    |8|    |9|
                   +-+    +-+    +-+
                   
>  [+] To solve this example, we will give to you, the number of nodes (9), the 
     number of connections with the start point (7 + 1) and the start point 
     (position 1).

> [+] This is the format of the input diagram to the example: 
 [(1, 1), (1, 4), (4, 5), (4, 7), (5, 8), (5, 6), (6, 9), (6, 3)]

> [+] The answer to the example is 14

So, the first tuple in the connections list represents the starting point, in the example that's (1, 1). From there onwards we had to visit all the nodes, and then return to the starting node without traveling in circles. Because circles were not allowed, the circuit could be presented as a tree structure, and it could be traveled recursively.

I used [NetworkX](https://networkx.github.io/) for graph related functions and came up with the following script to solve the task:

``` python
import networkx as nx
import ast

def travel_graph(graph, current_node, visited_nodes):
    found = 0
    visited_nodes.append(current_node)
    for neighbor in graph.neighbors(current_node):
        if neighbor not in visited_nodes:
            found += travel_graph(graph, neighbor, visited_nodes) + 2
    return found

def get_shortest_path(nodes, connections):
    edges = ast.literal_eval(connections.strip())
    node_range = range(1, nodes + 1)
    G = nx.Graph()
    G.add_nodes_from(node_range) # Add nodes
    G.add_edges_from(edges) # Add edges
    result =  travel_graph(G, edges[0][0], [])
    return result
```

The other part of the task was to create code to interract with the server. The server printed information in the following way:

>  [+] To start the challenge inform the number 86: 86  
     OK, let's go!

 > [+] Stage 1  
     Number of nodes: 9  
     Connections: [(7, 7), (7, 4), (4, 1), (1, 4), (4, 5), (5, 2)]  
     The minimum is: 

I used the following script to interract with the server:
``` python
from pwn import *
r = remote('54.175.35.248', 8003) # nc 54.175.35.248 8003
print r.recvuntil('To start the challenge inform the number '), 
line = r.recv(3)
print line

if ':' not in line:
    print r.recv()
else:
    line = line.replace(':', '')
print line
r.send(line.replace(' ', '') + '\n')

while True:
    try:
        l = r.recvuntil('Stage')
        print l ,
        l = r.recvuntil('Number of nodes: ')
        nodes = r.recvline()
        print l, nodes,
        l = r.recvuntil('Connections: ')
        connections = r.recvline()
        print l, connections,
        l = r.recvuntil('The minimum is: ')
        
        path_len = get_shortest_path(int(nodes), connections)
        print l, path_len,
        r.send(str(path_len) + '\n')
        
        line = r.recvline()
        if 'Wrong!' in line:
            print line
            print r.recvall()
            break
    except:
        print r.recvall()
        break
r.close()
```

After 100 rounds we were given the flag. The flag was: 3DS{m4st3r_0f_Th3_l4byrInth}
