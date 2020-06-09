import re
from math import sqrt

# FUNCTIONS
def Input(type, context, key="NULL"): # custom input function, validates at end
    if context == "add_name": prompt = "Input coordinate name (ENTER key to advance): "
    elif context == "add_point": prompt = "Input coordinate (x,y): "
    elif context == "add_neighbor": prompt = "Input neighbor of {0} (ENTER key to advance): ".format(key)
    elif context == "set_start": prompt = "Input starting point by name: "
    elif context == "set_end": prompt = "Input ending point by name: "
    elif context == "ask_replay": prompt = "Do another calculation? ('yes' or 'no'): "
    elif context == "ask_reuse": prompt = "Use the same points and connections? ('yes' or 'no'): "

    i = input(prompt)
    v_i = Validate(i, type, context, key)
    return v_i

def Validate(input, type, context, key="NULL"): # validate <input> from user as <type> with <context>, pass <key> if needed
    try:
        input = input.upper()  # make uppercase

        if input == "QUIT": quit() # global quit
        elif type == "key": # if name, check for numbers
            if input == '':
                if context != "add_name" and context != "add_neighbor":
                    print("Cannot be empty.")
            elif input.isalpha() != True:
                print("Letters only please.")
                input = Input("key", context)
            elif context == "add_neighbor":
                if input == key:
                    print("You cannot add yourself as a neighbor...")
                    return

                for k, v in neighbors.items(): # this whole for loop is just to check duplicates in each sublist of neighbors. much confuse
                    if key == k:
                        if input in v:
                            print("You cannot add duplicates...")
                            return
        elif type == "value": # if point, check against regex and empty
            match = re.search('^-?[0-9][0-9]?[0-9]?,-?[0-9][0-9]?[0-9]?$', input) # regex check: -999,999

            if not match or input == '':
                print("Invalid input. Please use this format: 0,0")
                input = Input("value", context) # dont return input until its clean
    except:
        print("Something went horribly wrong...")
        quit()

    return input

def CheckPlane(n): # check if: null, in plane
    if n == None: # this is a null return check (from adding dupes & yourself as a neighbor from Validate)
        return False
    elif n not in plane.keys():
        print(n, "is not in the plane...")
        return False
    else: # key exists in the plane
        return True

def AddNodes(): # get name and coord point, validate, then add to plane
    while (True):
        print("\nPLANE -", plane)
        name = Input("key", "add_name")
        if name == '': break # leave if CRLF
        point = Input("value", "add_point")
        plane[name] = point # add to plane

def AddNeighbors(): # ask for neighboring points
    print("\nPLANE -", plane)
    
    for key in plane.keys(): # loop through nodes
        while (True): # stay at node until advance
            n = Input("key", "add_neighbor", key) # pass key to iterate
            if n == '': break # go to next key
            check = CheckPlane(n)
            if check != True: continue # restart if not good
            neighbors.setdefault(key, []).append(n) # append a value (n) to a key
            neighbors.setdefault(n, []).append(key) # connect node on both ends (could make this fancier but wont)
            print("NEIGHBORS -", neighbors)

def AddStartEnd(): # ask for start and end points
    print("\nPLANE -", plane)
    GetStartEnd(context = "set_start")
    GetStartEnd(context = "set_end")

    if len(startend) == 1: # if start and end are the same when inputted (keys overwrite)
        print("No calculating needs to be done. Distance is 0.")
        quit()

def GetStartEnd(context): # add input to startend list
    while (True):
        v = Input("key", context)
        if v == '': continue # restart if empty
        check = CheckPlane(v)

        if check == True: # add to startend if exists in plane
            startend[v] = plane[v]
            print(startend)
            break

def Calculate(): # calculate distances between all points
    print("\nPLANE -", plane)
    print("NEIGHBORS -", neighbors)
    print("START & END -", startend)

    adjacents = neighbors.copy()

    for node in plane.keys(): # fill distances list to perform algorithm on
        while(True): # stay in node until break!
            if adjacents.get(node) is None: # if no sublist of neighbors found
                print("No neighboring points found for node", node, ". Skipping over...")
                break

            subNode = adjacents[node][0] # retrieve first subnode in adjacents
            del adjacents[node][0] # delete first subnode
            coord1 = plane[node]
            coord2 = plane[subNode]
            dist = Distance(coord1, coord2) # input node and subnode into distance formula
            if distances.get(node) is None: distances[node] = {} # if there is no dictionary inside node, create new one
            distances[node][subNode] = dist # add dist as a value to subnode, while inside node (much confuse sorry)

            if len(adjacents[node]) == 0: # if subnode list is empty
                del adjacents[node] # delete parent node
                break # go to next parent node
            else: # restart (until subnode list is empty)
                continue # go to next subnode

def Distance(c1, c2): # distance formula - split out integers and perform distance math
    x1, y1 = c1.split(',')
    x2, y2 = c2.split(',')
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert all to ints

    d = sqrt( (x2 - x1)**2 + (y2 - y1)**2 ) # distance formula
    return round(d, 2)

def Dijkstra(): # dijkstra algorithm
    print("DISTANCES -", distances)

    shortest = {} # keeps track of shortest distances between nodes
    path = [] # optimal path
    predecessors = {} # keeps track of previous path
    unseen = distances.copy()
    inf = 999999
    start = list(startend.keys())[0]
    end = list(startend.keys())[1]

    for node in unseen: # fill every node in shortest as distance = inf
        shortest[node] = inf
    shortest[start] = 0 # make distance to self 0

    while unseen:
        minDistance = None

        for node in unseen: # loop through nodes and check which one has the smallest distance
            if minDistance is None:
                minDistance = node # make starting node
            elif shortest[node] < shortest[minDistance]:
                minDistance = node # assign shortest distance to minDistance

        pathOptions = distances[minDistance].items() # create paths from min distance node

        for subnode, weight in pathOptions: # check each node and weight (distance) of node in pathOptions
            if weight + shortest[minDistance] < shortest[subnode]: # check if weight + minDistance < subnode distance
                shortest[subnode] = round(weight + shortest[minDistance], 3) # assign weight to shortest list
                predecessors[subnode] = minDistance # add minDistance into predecessors dict

        unseen.pop(minDistance) # pop out that specific min distance

    currentNode = end

    # create optimal path
    while currentNode != start:
        try:
            path.insert(0, currentNode) # insert at beginning of path
            currentNode = predecessors[currentNode] # assign to next in predecessors
        except KeyError:
            print("Path is not reachable!")
            break

    path.insert(0, start) # add start to beginning of path list

    # print out optimal path and distance
    if len(shortest) != 1:
        if shortest[end] != inf: # if end value != inf
            print("\nOptimal path is:", str(path))
            print("Distance travelled is:", str(shortest[end]))

def AskReplay(): # ask if play again
    r = Input("NULL", "ask_replay")

    if r == "YES": # yes, play again
        AskReuse()
    elif r == "NO": # no, quit
        quit()
    else: # recurse until yes or no
        AskReplay()

def AskReuse(): # ask if use same plot
    p = Input("NULL", "ask_reuse")

    if p == "YES": # yes, reuse points
        startend.clear()
        AddStartEnd()
        Dijkstra()
        AskReplay()
    elif p == "NO": # no, use different points
        RefreshLists()
        Main()
    else: # recurse until yes or no
        AskReuse()

def RefreshLists():
    global plane, neighbors, startend, distances
    plane, neighbors, startend, distances = {}, {}, {}, {}

def Main():
    AddNodes()
    AddNeighbors()
    AddStartEnd()
    Calculate()
    Dijkstra()
    AskReplay()

# MAIN
plane, neighbors, startend, distances = {}, {}, {}, {} # globals
print("Quit at anytime! - just type 'quit'")
Main()