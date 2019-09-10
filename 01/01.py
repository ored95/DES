# BFS
# Source: https://en.wikipedia.org/wiki/Breadth-first_search

import json
from graphviz import Graph

def json2graph(fileName):
    graph = None
    with open(fileName) as fs:
        src = json.load(fs)

        graph = dict.fromkeys(src["station"])
        for i in range(len(src["station"])):
            paths = list(filter(lambda j: src["link"][i][j] > 0, range(len(src["link"][i]))))
            if len(paths) > 0:
                graph[src["station"][i]] = set(map(lambda path: src["station"][path], paths))
    return graph

def json2dot(direction, color='green', view=True, DOTfileName="Metro-scheme", JSONfileName="graph.json"):
    src = json.load(open(JSONfileName))
    dot = Graph(DOTfileName, format='png')
    
    dot.attr('node', shape='circle')
    
    for station in src["station"]:
        if direction != None and station in set(direction):
            dot.node(station, fillcolor=color, style='filled')
        else:
            dot.node(station)

    for i in range(len(src["station"])):
        paths = list(filter(lambda j: (src["link"][i][j] > 0) and (j > i), range(len(src["link"][i]))))
        for path in paths:
            dot.edge(src["station"][i], src["station"][path])
    
    return dot.render(view=view)

def bfs(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for head in graph[vertex] - set(path):
            if head == goal:
                yield path + [head]
            else:
                queue.append((head, path + [head]))

def shortest_path(graph, start, goal):
    try:
        return next(bfs(graph, start, goal))
    except StopIteration:
        return None

def display(graph, st1, st2, flag=False):
    try:
        print("\nPath from " + st1 +" to " + st2 + ":")
        if not flag:
            for path in list(bfs(graph, st1, st2)):
                print(path)
        else:
            path = shortest_path(graph, st1, st2)
            color = str(input("---- Fillcolor: "))
            print(' -> '.join(path))
            json2dot(direction=path, DOTfileName=st1+"-"+st2, color=color)
    except KeyError:
        print("!!! No path from " + st1 +" to " + st2 + ".")

if __name__ == "__main__":
    graph = json2graph("graph.json")
    # json2dot(direction=None, DOTfileName="Metro-scheme", view=False)

    print("List of stations: ")
    stations = "\t".join([key for key, _ in graph.items()])
    print(stations)

    st1  = str(input("Select FROM: "))
    st2  = str(input("Select   TO: "))
    flag = input("Shortest? (Y/N) ")[0].capitalize() == 'Y'

    display(graph, st1, st2, flag)