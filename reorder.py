from graphs import Graph

def get_node_capacity(graph):
    """To calculate the capacity of the node, we need some attributed from validator nodes
       such as processing capacity, number of neighbours, and buffer size.
       The formulas to calculate confirmation time and number of confirmed transactions 
       are machine dependent, for our case we implemented the coeficients from our machine
    """
    for node in graph.vertices():
        #append the node to the working dict
        validator_node[node] = []
        #calculate time to confirm transactions
        tc = int(660*2**(-C/5))
        #calculate number of confirmed transactions
        N = graph.vertex_degree(node)
        confTxns = int(9100*(2**(-N/5) + (200 * 0.00002)))
        #calculate overall capacity of node
        z = confTxns / tc
        #append value to node list    
        validator_node[node].append(int(z))
    #print("Node's capacity (transactions/sec): ", validator_node)

def get_node_load(graph):
    """Each validator node has two set of connections
       one to other validators and another to sensor nodes
        we calculate the load of each validator node by
        getting the degree of the node and the flow of sensor transactions
    """
    for node in graph.vertices():
        #get load from other validator nodes
        load_val = graph.vertex_degree(node) * f0
        #get load of sensor nodes
        load_sensor = numSensor[node] * rate
        validator_node[node].append(load_sensor + load_val)
    #print ("Node's load (transactions/sec): ", validator_node)

def get_replication_time(graph):
    degree = 0
    for node in graph.vertices():
        #get the degree of each node
        degree += graph.vertex_degree(node)
    return degree * t0

def get_submission_rate():
    submission_rate = 0
    for sensor in numSensor.keys():
        submission_rate += numSensor[sensor]
    return submission_rate * rate

def validate_graph():
    if len(validator_node) == 0:
        return False
    for node in validator_node.keys():
        if ( validator_node[node][0] < validator_node[node][1] ):
            return False
    return True

def reconnect():
    nodes = []
    #find overloaded nodes
    for node in validator_node.keys():
        nodes.append((node, validator_node[node][0] - validator_node[node][1]))
    print("Remaining capacity of nodes: ")
    print(sorted(nodes, key = lambda x : x[1], reverse=True))
    nodes = sorted(nodes, key = lambda x : x[1], reverse=True)
    #reset load of nodes to only the flow of sensors
    for node in validator_node.keys():
        validator_node[node][1] = numSensor[node] * rate
    # print (nodes)
    # print (validator_node)
    #reoder the connection of validators, we follow a greeydy-type connection
    for x in range(len(nodes)):
        curr_node = nodes[x][0]
        for y in range(x+1, len(nodes)):
            next_node = nodes[y][0]
            #get load of validator nodes
            # print(validator_node)
            # print(curr_node)
            curr_load = validator_node[curr_node][1]
            curr_cap = validator_node[curr_node][0]
            next_load = validator_node[next_node][1]
            next_cap = validator_node[next_node][0]
            # print(curr_node, curr_load, next_node, next_load)
            if ( curr_load + f0 < curr_cap and next_load + f0 < next_cap ):
                new_graph.add_edge({curr_node, next_node})
                # new_graph.add_edge({next_node, curr_node})
                validator_node[curr_node][1] += f0
                validator_node[next_node][1] += f0
                # print (validator_node)
                # print(new_graph.edges())


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
    #Machine dependent attributes
    f0 = 2                       #cost to dispatch transactions to other validator nodes (transaction/sec)
    t0 = 3                       #time to dispatch a transaction (in seconds)
    rate = 4                     #transactions's rate

    #Global variables, given from the deployed architecture
    C = 6                        #cpu capacity of validator nodes
    B = 200                      #buffer size to store unprocess transactions
    #deployed architecture
    currGraph = { "a" : ["b", "d"],
          "b" : ["c"],
          "c" : ["b", "d", "e"],
          "d" : ["a", "c"],
          "e" : ["c"]
        }
    #connections to sensor nodes
    numSensor = {"a" : 4,
                "b" : 1,
                "c" : 4,
                "d" : 1,
                "e" : 0
            }
    #dict to store nodes attributes
    validator_node = {}
    bck_validator_node = {}
    
    deployedTopology = Graph(currGraph)
    
    #Verify if the current deployed network is capable to process all transactions.
    print("Deployed Network ('validator node': [capacity, load])")
    get_node_capacity(deployedTopology)
    get_node_load(deployedTopology)
    print(validator_node)
    print("Time to replicate transactions to all validator nodes (in seconds): ", get_replication_time(deployedTopology))
    print("Total submission rate of sensor nodes (transactions/sec): ", get_submission_rate())
    #check if the deployed network is suited to fulfill the demand of sensor nodes
    #traverse the nodes until the load overpass the capacity
    if ( validate_graph() == True ):
        print("The current deployed network can fulfull the demand of sensor nodes")
        print(deployedTopology.edges())
    else: #we start relaxing the network
        #first we reduce the flow of sensor nodes, each iteration we reduce it by 20%
        print("*****************************************************************************")
        print("*****************************************************************************")
        print("Relax network (reduce submission flow): ")
        index = 1
        back_rate = rate
        while ( validate_graph() == False ):
            rate =  int(rate - (rate * .2))
            if (rate < 1):
                print("**No optimal solution found**")
                break
            validator_node.clear()
            get_node_capacity(deployedTopology)
            get_node_load(deployedTopology)
            print("Reduce sensor rate by (percentage) %d -- new rate %d: " % (index * 20, rate))
            print(validator_node)
            index += 1
        print("New topology with reduced rate: ")
        print(deployedTopology.edges())
        print("Time to replicate transactions to all validator nodes (in seconds): ", get_replication_time(deployedTopology))
        print("Total submission rate of sensor nodes (transactions/sec): ", get_submission_rate())

        #second we increase the capacity of our nodes
        #we increase the cpu by one and buffer size by 20%
        print("*****************************************************************************")
        print("*****************************************************************************")
        print("Relax network (increase capacity): ")
        rate = back_rate
        back_B = B
        back_C = C
        index = 1 
        validator_node.clear()
        while ( validate_graph() == False ):
            B = int(B - (B * .2))
            C += 1
            validator_node.clear()
            get_node_capacity(deployedTopology)
            get_node_load(deployedTopology)
            print("Increase buffer size by (percentage) %d -- new buffer %d: " % (index * 20, B))
            print("Increase processing capacity by %d -- new buffer %d: " % (index, C))
            print(validator_node)
            index += 1
        print("New topology with increased capacity: ")
        print(deployedTopology.edges())
        print("Time to replicate transactions to all validator nodes (in seconds): ", get_replication_time(deployedTopology))
        print("Total submission rate of sensor nodes (transactions/sec): ", get_submission_rate())

        #third we reconnect the nodes to freeup overloaded nodes
        print("*****************************************************************************")
        print("*****************************************************************************")
        print("Relax network (reconnect network): ")
        B = back_B
        C = back_C
        #create new graph
        reorder_graph = {}
        for node in validator_node:
            reorder_graph[node] = []
        new_graph = Graph(reorder_graph)
        validator_node.clear()
        get_node_capacity(deployedTopology)
        get_node_load(deployedTopology)
        reconnect()
        print("Updated nodes' capacity: ")
        print(validator_node)
        print("New topology: ")
        print(new_graph.edges())
        print("Time to replicate transactions to all validator nodes (in seconds): ", get_replication_time(new_graph))
        print("Total submission rate of sensor nodes (transactions/sec): ", get_submission_rate())
    
    # #load of validator nodes
    # load_validator=[]    
    # #cost to process a transaction
    # v0 = 2
    # #rate of sensor node
    # rate = 5
    # #capacity of validators (transaction/sec)
    # zi = 25
    # #total capacity
    # z = 0
    # #total flow
    # f = 0

    

    # #get total capacity of the network
    # for validator_node in graph.vertices():
    #     z += zi
    # print ("Network Total Capacity: ", z)
    # #get total transaction flow
    # for validator_node in currFlow.keys():
    #     f += currFlow[validator_node] * rate
    # print ("Network Total Transaction Flow: ", f)
    # #get load of each validator node
    # for edge in graph.vertices():
    #     load_validator.append((edge, get_validator_load(edge, graph)))
    
    # #reoder topology
    # #create new graph
    # reorder_graph = {}
    # for edge, __ in load_validator:
    #     reorder_graph[edge] = []
    # new_graph = Graph(reorder_graph)
    # print("Load of nodes: " ,sorted(load_validator, key = lambda x : x[1]))
    # relax(sorted(load_validator, key = lambda x : x[1]))
    
    # print("Old graph:")
    # print(graph.edges())
    # print("New graph:")
    # print(new_graph.edges())



