from numpy import inf
import copy

init_costs = {'1': inf, '2': inf, '3': inf, '4': inf, '5': inf, '6': inf, '7': inf, '8': inf, '9': inf,
            '10': inf, '11': inf, '12': inf, '13': inf, '14': inf, '15': inf}

init_graph = {'1': {'2':1,'10':1}, '2': {'1':1,'3':1}, '3': {'2':1,'4':1}, '4': {'3':1,'5':1}, '5': {'4':1,'6':1},
        '6': {'5':1,'7':1,'15':1}, '7': {'6':1,'8':1}, '8': {'7':1,'9':1}, '9': {'8':1,'10':1},
        '10': {'1':1,'9':1,'11':1}, '11': {'10':1,'12':1}, '12': {'11':1,'13':1},
        '13': {'12':1,'14':1}, '14': {'13':1,'15':1}, '15': {'6':1,'14':1}}

def _search(source, target, graph, costs, parents):
    
    nextNode = source
    
    while nextNode != target:
        
        for neighbor in graph[nextNode]:
            
            if graph[nextNode][neighbor] + costs[nextNode] < costs[neighbor]:
                
                costs[neighbor] = graph[nextNode][neighbor] + costs[nextNode]
                
                parents[neighbor] = nextNode
                
            del graph[neighbor][nextNode]
            
        del costs[nextNode]
        
        nextNode = min(costs, key=costs.get)
        
    return parents

def _backpedal(source, target, searchResult):
    
    node = target
    
    backpath = [target]
    
    path = []
    
    while node != source:
        
        backpath.append(searchResult[node])
        
        node = searchResult[node]
        
    for i in range(len(backpath)):
        
        path.append(backpath[-i - 1])
        
    return path

def find_route(source, destination):
    source = str(source)
    destination = str(destination)

    graph = copy.deepcopy(init_graph)
    costs = copy.deepcopy(init_costs)
    costs[source] = 0

    parents = {}

    result = _search(source, destination, graph, costs, parents)

    return _backpedal(source, destination, result)


