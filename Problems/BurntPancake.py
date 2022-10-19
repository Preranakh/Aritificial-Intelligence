class DirectedGraphPancake:
    # PancakeStates are represented as an array of strings (where each element is a pancake #C with the ID number followed by
    # its orientation),NodePointer stores a pointer to the node with the
    # PancakeState that preceded the current one, and
    # PcakeAction stores where the PcakeFLip was located to create the current
    # PancakeState from the NodePointers.
    def __init__(self, PancakeState=[], NodePointer=None, CostForBackward=0, CostForForward=0, PcakeAction=0):
        self.PancakeState = PancakeState
        self.NodePointer = NodePointer
        self.CostForBackward = CostForBackward
        self.CostForForward = CostForForward
        self.PcakeAction = PcakeAction

    def __str__(self):
        pancake_string = ""
        for pancake in self.PancakeState: pancake_string += pancake
        return pancake_string

    def __eq__(self, obj):
        return isinstance(obj, DirectedGraphPancake) and self.PancakeState == obj.PancakeState

    def __lt__(self, other):
        if (self.CostForBackward + self.CostForForward != other.CostForBackward + other.CostForForward):
            return self.CostForBackward + self.CostForForward < other.CostForBackward + other.CostForForward
        else:
            return PcakeID(self.PancakeState) > PcakeID(other.PancakeState)


# Checks if the given PancakeState is a goal PancakeState.
def FinalGoal(PancakeState):
    for i in range(len(PancakeState)):
        if (PancakeState[i] != str(i + 1) + "w"):
            return False
    return True


# Returns the ID of the PancakeState for tie-breaking.
def PcakeID(PancakeState):
    ID = ""
    for pancake in PancakeState:
        if (pancake[1] == 'w'):
            ID += pancake[0] + "1"
        else:
            ID += pancake[0] + "0"
    return int(ID)


# Returns a new PancakeState that is the given PancakeState PcakeFLipped at the index.
def PcakeFLip(PancakeState, index):
    PcakeFLipped = []
    for i in range(index):
        PcakeFLipped.append(PancakeState[index - i - 1])
        if (PcakeFLipped[i][1] == 'w'):
            PcakeFLipped[i] = PcakeFLipped[i][0] + "b"
        else:
            PcakeFLipped[i] = PcakeFLipped[i][0] + "w"
    return PcakeFLipped + PancakeState[index:]


def PathTraverse(end):
    TraversedPath = []
    CurrentNode = end
    while (CurrentNode):
        TraversedPath.append(CurrentNode)
        CurrentNode = CurrentNode.NodePointer
    return TraversedPath


# rinting the path in the desired format.
def printTraversedPath(TraversedPath, isPrintCost):
    if (TraversedPath):
        for i in range(len(TraversedPath) - 1, 0, -1):
            barIndex = 2 * TraversedPath[i - 1].PcakeAction
            PancakeStateStr = TraversedPath[i].__str__()
            print(PancakeStateStr[:barIndex] + "|" + PancakeStateStr[barIndex:], end="")
            if (isPrintCost):
                print(" g:" + str(TraversedPath[i].CostForBackward) + ", h:" + str(TraversedPath[i].CostForForward))
            else:
                print()
        print(TraversedPath[0], end="")
        if (isPrintCost):
            print(" g:" + str(TraversedPath[0].CostForBackward) + ", h:" + str(TraversedPath[0].CostForForward) + "\n")
        else:
            print("\n")


# Cost calculation function for AS.
def ACost(NodePointerNode, increment):
    return NodePointerNode.CostForBackward + increment


# Cost calculation function for BFS.
def BFSCost(NodePointerNode, increment):
    return NodePointerNode.CostForBackward + 1


# Heuristic function for AS.
def AStarHeuristics(PancakeState):
    maxOut = 0
    for i in range(len(PancakeState)):
        if (PancakeState[i][0] != str(i + 1)): maxOut = max(i + 1, maxOut)
    return maxOut


# Heuristic function for BFS.
def BFSHeuristics(PancakeState):
    return 0


# It is a generized search algorithm type where BFS can be represented as a special case of AS with
# heuristic of 0 and costs of 1.
def re_arrange(startPancakeState, costCalc, heuristic, method):
    start = DirectedGraphPancake(startPancakeState, None, 0, heuristic(startPancakeState), 0)
    fringe = [start]
    visited = [start]
    while fringe:
        if method == "a":
            fringe.sort()
        CurrentNode = fringe.pop(0)
        if (FinalGoal(CurrentNode.PancakeState)):
            return CurrentNode
        else:
            for i in range(1, len(CurrentNode.PancakeState) + 1):
                newPancakeState = PcakeFLip(CurrentNode.PancakeState, i)
                NewNode = DirectedGraphPancake(newPancakeState, CurrentNode, costCalc(CurrentNode, i),
                                               heuristic(newPancakeState), i)
                if NewNode not in visited:
                    fringe.append(NewNode)
                    visited.append(NewNode)
    print("Solution is not reached.\n")
    return None


# Input from the user is processes and then it feeds correct input to desired Algo_Type.
def InputFormat():
    EnterInput = input("Enter the input pattern of the pancake: ").lower()
    Input1 = convertInput(EnterInput)
    startPancakeState = Input1[0]
    Algo_Type = Input1[1]
    if (Algo_Type == 'b'):
        BFS(startPancakeState)
    else:
        AS(startPancakeState)


# Extracts the PancakeState and Algorithm_Type choice from the string input entered by the user.
def convertInput(EnterInput):
    PancakeState = []
    for i in range(0, len(EnterInput) - 2, 2):
        PancakeState.append(EnterInput[i] + EnterInput[i + 1])
    return (PancakeState, EnterInput[len(EnterInput) - 1])


def BFS(startPancakeState):
    printTraversedPath(PathTraverse(re_arrange(startPancakeState, BFSCost, BFSHeuristics, "b")), False)


def AS(startPancakeState):
    printTraversedPath(PathTraverse(re_arrange(startPancakeState, ACost, AStarHeuristics, "a")), True)


# Runs the algorithm and checks for the exit
def run():
    InputFormat()


run()