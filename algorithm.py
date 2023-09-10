import random

class RandomizedPrim_ThreeDimensionMaze():
    def __init__(self, size):
        x, y, z = size
        self.createGrid(x, y, z)

        # 미로 생성 시작점 설정
        nowX = random.randrange(1, x, 2)
        nowY = random.randrange(1, y, 2)
        nowZ = random.randrange(1, z, 2)

        # 미로 생성
        self.setRoad(nowX, nowY, nowZ)

        # 시작점 설정
        self.gridData[1][1][1] = 10
        # 도착점 설정
        self.gridData[x - 2][y - 2][z - 2] = 11

    # 그리드 생성
    # 0:빈 공간 혹은 벽, 1:통로, 2:프론티어, 3:벽 미존재, 10:시작점, 11:도착점
    def createGrid(self, x, y, z):
        self.gridData = []
        for _ in range(0, x):
            temp = []
            for _ in range(0, y):
                temp.append([0] * z)
            self.gridData.append(temp)

    # 그리드에서 특정 값의 인덱스 알아내기
    def findIndices(self, target):
        indices = []
        for i, xd in enumerate(self.gridData):
            for k, yd in enumerate(xd):
                for j, element in enumerate(yd):
                    if element == target:
                        indices.append((i, k, j))
        return indices

    # 인접한 칸 인덱스 가져오기
    def getAdjacentCells(self, pos, filterVal):
        x, y, z = pos
        adjacentCells = []
        if x - 2 >= 0 and self.gridData[x - 2][y][z] == filterVal:
            adjacentCells.append((x - 2, y, z))
        if x + 2 < len(self.gridData) and self.gridData[x + 2][y][z] == filterVal:
            adjacentCells.append((x + 2, y, z))
        if y - 2 >= 0 and self.gridData[x][y - 2][z] == filterVal:
            adjacentCells.append((x, y - 2, z))
        if y + 2 < len(self.gridData[0]) and self.gridData[x][y + 2][z] == filterVal:
            adjacentCells.append((x, y + 2, z))
        if z - 2 >= 0 and self.gridData[x][y][z - 2] == filterVal:
            adjacentCells.append((x, y, z - 2))
        if z + 2 < len(self.gridData[0][0]) and self.gridData[x][y][z + 2] == filterVal:
            adjacentCells.append((x, y, z + 2))
        return adjacentCells

    def setRoad(self, x, y, z):
        # 통로 설정
        self.gridData[x][y][z] = 1
        # 프론티어 설정
        self.setFrontier(x, y, z)
        # 프론티어 인덱스 검색
        frontier_indices = self.findIndices(2) 
        # 남은 프론티어가 없으면 종료
        if len(frontier_indices) == 0:
            return False
        
        # 프론티어 중 랜덤으로 하나 선택
        nowPos = random.choice(frontier_indices)
        nowX, nowY, nowZ = nowPos
        self.gridData[nowX][nowY][nowZ] = 1

        # 프론티어와 인접한 통로 중 하나 선택해 벽 허물기
        adjacentRoads = self.getAdjacentCells(nowPos, 1)
        selectedRoad = random.choice(adjacentRoads)
        middle = [(selectedRoad[0] + nowX) // 2,
                       (selectedRoad[1] + nowY) // 2,
                       (selectedRoad[2] + nowZ) // 2]
        self.gridData[middle[0]][middle[1]][middle[2]] = 3

        # 새로운 프론티어 설정
        self.setFrontier(nowX, nowY, nowZ)
        # 다음 통로 개척
        self.setRoad(nowX, nowY, nowZ)

    def setFrontier(self, x, y, z):
        adjacentVoids = self.getAdjacentCells(
            (x, y, z), 0)  # 인접한 빈 공간 인덱스 가져오기
        for (v_x, v_y, v_z) in adjacentVoids:
            # 프론티어 설정
            self.gridData[v_x][v_y][v_z] = 2

    def render(self):
        return self.gridData
