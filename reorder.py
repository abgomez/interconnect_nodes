from graphs import Graph

def get_validator_load(edge, curr_graph):
    """Each validator node has two set of connections
       one to other validators and another to sensor nodes
        we calculate the load of each validator node by
        getting the degree of the node and the flow of sensor transactions
    """
    #get load from other validator nodes
    load_val = curr_graph.vertex_degree(edge) * v0
    #get load of sensor nodes
    load_sensor = currFlow[edge] * rate
    return load_sensor + load_val

def relax(load_validator):
    #reoder the connection of validators
    for x in range(len(load_validator)):
       curr_edge, load = load_validator[x]
       for y in range(x+1, len(load_validator)):
            nxt_edge, load = load_validator[y]
            #get the load of validator nodes
            curr_load = get_validator_load(curr_edge, new_graph)
            nxt_load = get_validator_load(nxt_edge, new_graph)
            #print(curr_edge, curr_load, nxt_edge, nxt_load)
            if (curr_load+v0) < zi and (nxt_load+v0) < zi:
                new_graph.add_edge({curr_edge, nxt_edge})
                new_graph.add_edge({nxt_edge, curr_edge})
                print(new_graph.edges())

    
if __name__ == "__main__":
    #deployed architecture
    currGraph = { "a" : ["b", "d"],
          "b" : ["c"],
          "c" : ["b", "d", "e"],
          "d" : ["a", "c"],
          "e" : ["c"]
        }
    #connections to sensor nodes
    currFlow = {"a" : 4,
                "b" : 1,
                "c" : 4,
                "d" : 1,
                "e" : 0
            }
    #load of validator nodes
    load_validator=[]    
    #cost to process a transaction
    v0 = 2
    #rate of sensor node
    rate = 5
    #capacity of validators (transaction/sec)
    zi = 25
    #total capacity
    z = 0
    #total flow
    f = 0

    graph = Graph(currGraph)

    #get total capacity of the network
    for validator_node in graph.vertices():
        z += zi
    print ("Network Total Capacity: ", z)
    #get total transaction flow
    for validator_node in currFlow.keys():
        f += currFlow[validator_node] * rate
    print ("Network Total Transaction Flow: ", f)
    #get load of each validator node
    for edge in graph.vertices():
        load_validator.append((edge, get_validator_load(edge, graph)))
    
    #reoder topology
    #create new graph
    reorder_graph = {}
    for edge, __ in load_validator:
        reorder_graph[edge] = []
    new_graph = Graph(reorder_graph)
    print("Load of nodes: " ,sorted(load_validator, key = lambda x : x[1]))
    relax(sorted(load_validator, key = lambda x : x[1]))
    
    print("Old graph:")
    print(graph.edges())
    print("New graph:")
    print(new_graph.edges())
    
    


    

    # print("Vertices of graph:")
    # print(graph.vertices())

    # print("Edge of graph:")
    # print(graph.edges())

    # print("Add vertex:")
    # graph.add_vertex("z")

    # print("Vertices of graph:")
    # print(graph.vertices())

    # print("Add and edge:")
    # graph.add_edge({"a","z"})

    # print("Edge of graph:")
    # print(graph.edges())

    # print('Adding and edge {"x", "y"} with new vertices:')
    # graph.add_edge({"x","y"})
    # print("Vertices of graph:")
    # print(graph.vertices())
    # print("Edge of graph:")
    # print(graph.edges())




