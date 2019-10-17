# BFS
# Source: https://en.wikipedia.org/wiki/Breadth-first_search

import json
from graphviz import Graph

def json2graph(fileName):
    graph, pausing = None, None
    with open(fileName) as fs:
        src = json.load(fs)

        graph = dict.fromkeys(src["station"])
        for i in range(len(src["station"])):
            paths = list(filter(lambda j: src["link"][i][j] > 0, range(len(src["link"][i]))))
            if len(paths) > 0:
                graph[src["station"][i]] = set(map(lambda path: src["station"][path], paths))

        pausing = src["pausing"]
    return (graph, pausing)

def json2dot(direction, color='green', view=True, DOTfileName="Metro-scheme", JSONfileName="graph.json"):
    src = json.load(open(JSONfileName))
    dot = Graph(DOTfileName, format='png')
    
    dot.attr('node', shape='circle')
    
    for station in src["station"]:
        if direction != None and station in set(direction):
            dot.node(station, fillcolor=color, style='filled')
        elif station in set(src["pausing"]):
            dot.node(station, fillcolor='gray', style='filled')
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

def shortest_path(paths):
    return min(paths, key=len)

def bfs_pause(graph, st1, st2, pausing=None):
    paths = list(bfs(graph, st1, st2))
    if len(pausing) > 0:
        paths = [path for path in paths if not len(set(path).intersection(set(pausing)))]
    return paths

def display(graph, pausing, st1, st2, flag=False):
    try:
        print("\nPath from " + st1 + " to " + st2 + ":")
        paths = bfs_pause(graph, st1, st2, pausing)
        if len(paths) > 0:
            if not flag:
                for path in paths: print(path)
            else:
                path = shortest_path(paths)
                color = str(input("---- Fillcolor: "))
                print(' -> '.join(path))
                json2dot(direction=path, DOTfileName=st1+"-"+st2, color=color)
        else:
            print("!!! No path from " + st1 + " to " + st2 + ".")
    except KeyError:
        print("!!! No path from " + st1 + " to " + st2 + ".")


if __name__ == "__main__":
    graph, pausing = json2graph("graph.json")
    json2dot(direction=None, DOTfileName="Metro-scheme")
    print("List of stations: ")
    stations = "\t".join([key for key, _ in graph.items()])
    print(stations)

    st1  = str(input("Select FROM: "))
    st2  = str(input("Select   TO: "))
    flag = input("Shortest? (Y/N) ")[0].capitalize() == 'Y'

    display(graph, pausing, st1, st2, flag)