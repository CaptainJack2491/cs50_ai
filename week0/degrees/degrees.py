import csv
import time
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory: str):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass



def shortest_path(source:str, target:str):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    initial_state = Node(source,None,None)
    frontier = StackFrontier()
    frontier.add(initial_state)
    # Main loop
    print('loop starting')
    times: int = 0
    seen: list[str] = []
    while True:
        if frontier.empty():
            return None

        # print_frontier(frontier)
        times += 1
        print('loop ran ', times, 'times')
        # time.sleep(1)
        
        # if not, select a node from the frontier
        node: Node = frontier.remove()
        print(node.state, 'node removed')

        # print_frontier(frontier)
        # if the node is the target node, return the frontier list
        if node.state == target:
            print('found target node')
            ans:list[tuple] = []
            while node.parent is not None:
                ans += [(node.state,node.action)]
                node = node.parent

            print(ans)
            return ans

        # expand node, getting resulting nodes to the frontier
        neighbors:set = neighbors_for_person(node.state)
        print(neighbors)

        # adding it to the frontier
        for movie_ids, person_id in neighbors:
            temp_node: Node = Node(state=person_id,parent=node,action=movie_ids)
            if frontier.contains_state(person_id):
                continue
            elif temp_node.state in seen:
                continue
            else:
                seen.append(temp_node.state)
                frontier.add(temp_node)
                print(seen)
        # print_frontier(frontier)

    
def print_frontier(frontier):
    nodes = []
    for node in frontier.frontier:
        nodes.append(node.state)
    print(nodes)


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors

def display_dictonary(dictionary: dict) -> None:
    for key, value in dictionary.items():
        print(f"{key}: {value}")

def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "small"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")
    print(shortest_path('129','1697'))
    # if source is None:
    #     sys.exit("Person not found.")
    # target = person_id_for_name(input("Name: "))
    # if target is None:
    #     sys.exit("Person not found.")
    #
    # path = shortest_path(source, target)
    #
    # if path is None:
    #     print("Not connected.")
    # else:
    #     degrees = len(path)
    #     print(f"{degrees} degrees of separation.")
    #     path = [(None, source)] + path
    #     for i in range(degrees):
    #         person1 = people[path[i][1]]["name"]
    #         person2 = people[path[i + 1][1]]["name"]
    #         movie = movies[path[i + 1][0]]["title"]
    #         print(f"{i + 1}: {person1} and {person2} starred in {movie}")



if __name__ == "__main__":
    main()
