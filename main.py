import copy
import pandas as pd
import re
import networkx as nx
import time


def make_graph(act_n, mov_n, edges):
    graph = nx.Graph()
    print("Adding movies to graph...")
    graph.add_nodes_from(mov_n, bipartite='Movies')
    print("Adding actors to graph...")
    graph.add_nodes_from(act_n, bipartite='Actors/Actresses')
    print("Adding edges to graph...")
    graph.add_edges_from(edges)
    # pos = nx.spring_layout(graph)
    # nx.draw(graph, pos=pos, with_labels=False)
    # color_map = ['#F8C471' if node in act_n else '#82E0AA' for node in graph]
    # print("graph drawn")
    # plt.show()
    return graph


def to_rev_dicts(input):
    return dict((v, k) for k, v in input.items())


def binary_search(arr, n, x):
    low = 0
    high = n - 1
    result = -1
    while low <= high:
        mid = int((low + high) / 2)
        if x == arr[mid]:
            result = mid
            low = mid + 1
        elif x < arr[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return result


def bfs(node, graph):
    visited = [False] * (len(graph))
    queue = []
    visited[node] = True
    queue.append(node)
    while queue:
        node = queue.pop(0)
        print(node, end="")
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited[neighbor] = True
                queue.append(neighbor)


def q1_f(x, years):
    s_years = sorted(years.values())
    counter = binary_search(s_years, len(s_years), x) + 1
    result = format(counter / (int(x) - int(s_years[0])), '.2f')
    print("\nThe average number of movies per year up to year " + str(x) + " is " + str(result)+"\n")


def q2_f(graph, x, year):
    movies_to_rm = {''}
    for m in movie_node_dict.values():
        if year[m] > x:
            movies_to_rm.add(m)
    graph.remove_nodes_from(movies_to_rm)
    largest_cc = max(nx.connected_components(graph), key=len)
    gmax = graph.subgraph(largest_cc)


    # for node in list(gmax.nodes()):
    #     i = eccentricity(node)
    #     lb = i
    #     ub = 2 * i
    #     while ub > lb:
    #         if max(lb, Bi(u)) > 2 * (i - 1):
    #             print(max(lb, Bi(u)))
    #         else:
    #             lb = max(lb, Bi(u))
    #             ub = 2 * (i - 1)
    #     break
    #     print(lb)


# def q3_f(graph):
#     print(graph.adj)


start_time = time.time()

# Read Data
file = "imdb-actors-actresses-movies.tsv"
print("Reading file...")
df = pd.read_table(file)
df.columns = ['Actors/Actresses', 'Movies']

# Dictionaries
print("Making actor dictionary...")
actor_node_dict = df['Actors/Actresses'].drop_duplicates(keep="first").to_dict()
rev_actors = to_rev_dicts(actor_node_dict)
print("Making movie dictionary...")
movie_node_dict = df['Movies'].drop_duplicates(keep="first").to_dict()
rev_movies = to_rev_dicts(movie_node_dict)
print("Making edges dictionary...")
edges_dict = df.to_dict(orient='split')
movie_year_dict = {}
regex = r'\(\d{4}[\)|\/]'
print("Separating movie years...")
for movie in movie_node_dict.values():
    match_str = re.search(regex, movie)
    if match_str is not None:
        res = match_str.group()
        res = re.sub("[()/]", "", res)
    else:
        res = "9999"
    movie_year_dict[movie] = res

# Bipartite graph
G = make_graph(actor_node_dict, movie_node_dict, edges_dict['data'])


yearSet = {'1930', '1940', '1950', '1960', '1970', '1980', '1990', '2000', '2010', '2020'}
option = ""

print("--- %s seconds ---" % (time.time() - start_time))


# Q1 | Q2 | Q3
print("Entering main menu")
while option != "exit":
    option = input("Q1|Average Movies per Year\nQ2|Diameter of largest connected component\nQ3|Pair of movies with "
                   "largest shared actors\nExit|Close the menu\nEnter choice (q1,q2,q3,exit): ")
# Q1
    if option == "q1":
        year_choice = input(str(sorted(yearSet))+"\nEnter one of the above years: ")
        if year_choice in yearSet:
            q1_f(year_choice, movie_year_dict)
        else:
            print("\nInvalid year\n")
# Q2
    elif option == "q2":
        S = copy.deepcopy(G)
        year_choice = input(str(sorted(yearSet)) + "\nEnter one of the above years: ")
        if year_choice in yearSet:
            q2_f(S, year_choice, movie_year_dict)
        else:
            print("Invalid year\n")
# Q3
    elif option == "q3":
        print("No solution yet")
    elif option == "exit":
        break
    else:
        print("\nInvalid option\n")



# QUESTION 1
# Considering only the movies up to year x with x in {1930,1940,1950,1960,1970,1980,1990,2000,2010,2020},
# write a function which, given x, computes:
# F # Average number of movies per year up to year x.

# QUESTION 2
# Considering only the movies up to year x with x in {1930,1940,1950,1960,1970,1980,1990,2000,2010,2020}
# and restricting to the largest connected component of the graph.
# 1 #  Compute exactly the diameter of G.

# QUESTION 3
# III # Which is the pair of movies that share the largest number of actors?

