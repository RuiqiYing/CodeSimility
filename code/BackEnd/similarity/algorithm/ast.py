import math

import numpy

import ast

Similarity = []


def point(x, y):
    return '[' + str(x) + ',' + str(y) + ']'


class CodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.seq = []

    def generic_visit(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        self.seq.append(type(node).__name__)

    def visit_FunctionDef(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        self.seq.append(type(node).__name__)

    def visit_Assign(self, node):
        self.seq.append(type(node).__name__)


class CodeParse(object):
    def __init__(self, fileA, fileB):
        self.visitorB = None
        self.visitorA = None
        self.codeA = open(fileA, encoding="utf-8").read()
        self.codeB = open(fileB, encoding="utf-8").read()
        self.nodeA = ast.parse(self.codeA)
        self.nodeB = ast.parse(self.codeB)
        self.seqA = ""
        self.seqB = ""
        self.work()

    def work(self):
        self.visitorA = CodeVisitor()
        self.visitorA.visit(self.nodeA)
        self.seqA = self.visitorA.seq
        self.visitorB = CodeVisitor()
        self.visitorB.visit(self.nodeB)
        self.seqB = self.visitorB.seq


class CalculateSimilarity(object):
    def __init__(self, A, B, W, M, N):
        self.A = A
        self.B = B
        self.W = W
        self.M = M
        self.N = N
        self.similarity = []
        self.SimthWaterman(self.A, self.B, self.W)

    def score(self, a, b):
        if a == b:
            return self.M
        else:
            return self.N

    def traceback(self, A, B, H, path, value, result):
        if value:
            temp = value[0]
            result.append(temp)
            value = path[temp]
            x = int((temp.split(',')[0]).strip('['))
            y = int((temp.split(',')[1]).strip(']'))
        else:
            return
        if H[x, y] == 0:  # 终止条件
            xx = 0
            yy = 0
            sim = 0
            for item in range(len(result) - 2, -1, -1):
                position = result[item]
                x = int((position.split(',')[0]).strip('['))
                y = int((position.split(',')[1]).strip(']'))
                if x == xx:
                    pass
                elif y == yy:
                    pass
                else:
                    sim = sim + 1
                xx = x
                yy = y
            self.similarity.append(sim * 2 / (len(A) + len(B)))

        else:
            self.traceback(A, B, H, path, value, result)

    def SimthWaterman(self, A, B, W):
        n, m = len(A), len(B)
        H = numpy.zeros([n + 1, m + 1], int)
        path = {}
        for i in range(0, n + 1):
            for j in range(0, m + 1):
                if i == 0 or j == 0:
                    path[point(i, j)] = []
                else:
                    s = self.score(A[i - 1], B[j - 1])
                    L = H[i - 1, j - 1] + s
                    P = H[i - 1, j] - W
                    Q = H[i, j - 1] - W
                    H[i, j] = max(L, P, Q, 0)

                    # 添加进路径
                    path[point(i, j)] = []
                    if math.floor(L) == H[i, j]:
                        path[point(i, j)].append(point(i - 1, j - 1))
                    if math.floor(P) == H[i, j]:
                        path[point(i, j)].append(point(i - 1, j))
                    if math.floor(Q) == H[i, j]:
                        path[point(i, j)].append(point(i, j - 1))

        end = numpy.argwhere(H == numpy.max(H))
        for pos in end:
            key = point(pos[0], pos[1])
            value = path[key]
            result = [key]
            self.traceback(A, B, H, path, value, result)

    def Answer(self):  # 取均值
        return sum(self.similarity) / len(self.similarity)