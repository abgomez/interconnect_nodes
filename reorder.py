from graphs import Graph

def get_node_capacity(graph, procPower, bufferSize):
    """To calculate the capacity of the node, we need some attributed from validator nodes
       such as processing capacity, number of neighbours, and buffer size.
       The formulas to calculate confirmation time and number of confirmed transactions 
       are machine dependent, for our case we implemented the coeficients from our machine
    """
    for node in graph.vertices():
        #append the node to the working dict
        validator_node[node] = []
        #calculate time to confirm transactions
        tc = int(660*2**(-procPower/5))
        #print(tc)
        #calculate number of confirmed transactions
        N = graph.vertex_degree(node)
        confTxns = int(9100*(2**(-N/5) + (bufferSize * 0.03)))
        #print(confTxns)
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
        load_sensor = conSensor[node] * rate
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
    #Global variables
    #Attributes of validator nodes, this attributes will varied by each node
    #max and min processing power
    min_C = 1
    max_C = 8
    #max and min buffer size
    min_B = 100
    max_B = 200
    
    f0 = 10                       #cost to dispatch transactions to other validator nodes (transaction/sec)
    t0 = 10                       #time to dispatch a transaction (in seconds)
    #rate = 4                     #transactions's rate
    
    #deployed architecture
    currGraph = { "a" : ["b", "d"],
          "b" : ["c"],
          "c" : ["b", "d", "e"],
          "d" : ["a", "c"],
          "e" : ["c"]
        }
    #connections to sensor nodes
    conSensor = {"a" : 2,
                "b" : 1,
                "c" : 4,
                "d" : 1,
                "e" : 0
            }
    #desire throughput to achieve, for this case we assume a norma distribution among all sensor nodes
    throughput =  400           #(measure in transaction/sec)

    #find the require transaction rate to achieve the throughput
    numSensor = 0
    for node in conSensor.keys():
        numSensor += conSensor[node]
    rate = throughput / numSensor
    print ("Transaction rate (transactions/sec): ", rate)

    deployedGraph = Graph(currGraph)
    validator_node = {}
    f = open("full.txt", "w+")
    #with our topology fix, we need to find the setup that fullfills the rate
    for C in range(min_C, max_C + 1):
        for B in range(min_B, max_B+1):
            print("C = %d -- B = %d" % (C,B))
            f.write("C = %d -- B = %d \n" % (C,B))
            get_node_capacity(deployedGraph, C, B)
            get_node_load(deployedGraph)
            # for node in validator_node.keys():
            #     if (validator_node[node][0] <= validator_node[node][1]):
            #         break
            #     if (node == 'e'):
            #         print(validator_node)
            #         f.write(str(validator_node) + "\n")
            
            f.write(str(validator_node) + "\n")
            validator_node.clear()
            #break
    #start a loop to go over all possible capacities 1 - 8
    #inner loop to go over all possible bufer

    # #dict to store nodes attributes
    # validator_node = {}
    # bck_validator_node = {}
    
    # deployedTopology = Graph(currGraph)
    
    # #Verify if the current deployed network is capable to process all transactions.
    # print("Deployed Network ('validator node': [capacity, load])")
    # get_node_capacity(deployedTopology)
    # get_node_load(deployedTopology)
    # print(validator_node)
    # print("Time to replicate transactions to all validator nodes (in seconds): ", get_replication_time(deployedTopology))
    # print("Total submission rate of sensor nodes (transactions/sec): ", get_submission_rate())
    # #check if the deployed network is suited to fulfill the demand of sensor nodes
    # #traverse the nodes until the load overpass the capacity
    # if ( validate_graph() == True ):
    #     print("The current deployed network can fulfull the demand of sensor nodes")
    #     print(deployedTopology.edges())
    # else: #we start relaxing the network
    #     #first we reduce the flow of sensor nodes, each iteration we reduce it by 20%
    #     print("*****************************************************************************")
    #     print("*****************************************************************************")
    #     print("Relax network (reduce submission flow): ")
    #     index = 1
    #     back_rate = rate
    #     while ( validate_graph() == False ):
    #         rate =  int(rate - (rate * .2))
    #         if (rate < 1):
    #             print("**No optimal solution found**")
    #             break
    #         validator_node.clear()
    #         get_node_capacity(deployedTopology)
    #         get_node_load(deployedTopology)
    #         print("Reduce sensor rate by (percentage) %d -- new rate %d: " % (index * 20, rate))
    #         print(validator_node)
    #         index += 1
    #     print("New topology with reduced rate: ")
    #     print(deployedTopology.edges())
    #     print("Time to replicate transactions to all validator nodes (in seconds): ", get_replication_time(deployedTopology))
    #     print("Total submission rate of sensor nodes (transactions/sec): ", get_submission_rate())

    #     #second we increase the capacity of our nodes
    #     #we increase the cpu by one and buffer size by 20%
    #     print("*****************************************************************************")
    #     print("*****************************************************************************")
    #     print("Relax network (increase capacity): ")
    #     rate = back_rate
    #     back_B = B
    #     back_C = C
    #     index = 1 
    #     validator_node.clear()
    #     while ( validate_graph() == False ):
    #         B = int(B - (B * .2))
    #         C += 1
    #         validator_node.clear()
    #         get_node_capacity(deployedTopology)
    #         get_node_load(deployedTopology)
    #         print("Increase buffer size by (percentage) %d -- new buffer %d: " % (index * 20, B))
    #         print("Increase processing capacity by %d -- new buffer %d: " % (index, C))
    #         print(validator_node)
    #         index += 1
    #     print("New topology with increased capacity: ")
    #     print(deployedTopology.edges())
    #     print("Time to replicate transactions to all validator nodes (in seconds): ", get_replication_time(deployedTopology))
    #     print("Total submission rate of sensor nodes (transactions/sec): ", get_submission_rate())

    #     #third we reconnect the nodes to freeup overloaded nodes
    #     print("*****************************************************************************")
    #     print("*****************************************************************************")
    #     print("Relax network (reconnect network): ")
    #     B = back_B
    #     C = back_C
    #     #create new graph
    #     reorder_graph = {}
    #     for node in validator_node:
    #         reorder_graph[node] = []
    #     new_graph = Graph(reorder_graph)
    #     validator_node.clear()
    #     get_node_capacity(deployedTopology)
    #     get_node_load(deployedTopology)
    #     reconnect()
    #     print("Updated nodes' capacity: ")
    #     print(validator_node)
    #     print("New topology: ")
    #     print(new_graph.edges())
    #     print("Time to replicate transactions to all validator nodes (in seconds): ", get_replication_time(new_graph))
    #     print("Total submission rate of sensor nodes (transactions/sec): ", get_submission_rate())
    
    