import sys
import re
from collections import defaultdict

visit = defaultdict(bool)
REACHABLEIn = defaultdict(lambda: [0, 0, 0])
sys.setrecursionlimit(100000)  # for large graph

def update_reachable(parent_reachable, child_reachable):
    for i in range(3):
        if child_reachable[i] == 1 and parent_reachable[(i + 1) % 3] != 1:
            parent_reachable[(i + 1) % 3] = 1

def ModifiedDFS(graph, node):
    visit[node] = True
    for child in graph[node]:
        if visit[child]:
            update_reachable(REACHABLEIn[node], REACHABLEIn[child])
        else:
            ModifiedDFS(graph, child)
            update_reachable(REACHABLEIn[node], REACHABLEIn[child])

if __name__ == "__main__":
    adj_list = defaultdict(list)
    with open("input.txt", "r") as f:
        content = f.readlines()
        n = int(content[0])
        if n == 0:
            print("No graph")
            sys.exit()
        #print(n)
        remainder_graph = content[1:n+1]
        start_node = int(re.findall(r"\d+", content[-1])[0])
        for line in remainder_graph:
            x = re.findall(r"\d+", line)
            if len(x) == 1:
                adj_list[int(x[0])] = []
            else:
                for i in range(1, len(x)):
                    adj_list[int(x[0])].append(int(x[i]))
    REACHABLEIn[start_node] = [0,0,1]
    visit[start_node] = 1
    for node in adj_list.keys():
        if not visit[node]:
            if len(adj_list[node]) > 0:  # If node has descendants
                ModifiedDFS(adj_list, node)
            else:
                REACHABLEIn[node] = [0, 0, 0]  # Node doesn't have descendants
            visit[node] = True

    count = 0
    result = []

    for node in sorted(adj_list.keys()):
        if REACHABLEIn[node][2] == 1:
            count += 1
            result.append(node)
    #print(count)
    #print(result) 

    with open("output.txt", "w") as f:
      f.write(str(len(result)) + "\n")
      formatted_result = ",".join(["v" + str(i) for i in result])
      f.write(formatted_result)