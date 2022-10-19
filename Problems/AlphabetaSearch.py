import math
MAX, MIN = math.inf, -math.inf

def minimax(depth, nodeIndex, maximizingPlayer, values, alpha, beta):
    if depth == 3:
        not_pruned.append(nodeIndex)
        return values[nodeIndex]
    if depth == 0:
        if maximizingPlayer:
            best = MIN
            for i in range(0, 3):
                val = minimax(depth + 1, nodeIndex * 3 + i, False, values, alpha, beta)
                best = max(best, val)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return best
        else:
            best = MAX
            for i in range(0, 3):
                val = minimax(depth + 1, nodeIndex * 3 + i, True, values, alpha, beta)
                best = min(best, val)
                beta = min(beta, best)
                if beta <= alpha:
                    break
            return best

    if 1 <= depth < 3:
        if maximizingPlayer:
            best = MIN
            for i in range(0, 2):
                val = minimax(depth + 1, nodeIndex * 2 + i, False, values, alpha, beta)
                best = max(best, val)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return best
        else:
            best = MAX

            for i in range(0, 2):
                val = minimax(depth + 1, nodeIndex * 2 + i, True, values, alpha, beta)
                best = min(best, val)
                beta = min(beta, best)
                if beta <= alpha:
                    break
            return best


def Diff(li1, li2):
    return list(set(li1) - (set(li2)))

nodes = []
not_pruned = []
y = list(map(str, input("enter the node values:").split()))

for i in range(0, len(y)):
    y[i] = int(y[i])
    nodes.append(y[i])

minimax(0, 0, True, nodes, MIN, MAX)

li1 = range(0, 12)
li2 = not_pruned
pruned = Diff(li1, li2)
pruned.sort()

a = []
for item in range(0, len(pruned)):
    pruned[item] = str(pruned[item])
    a.append(pruned[item])
pruned_str = ' '.join(pruned)
print(pruned_str)
