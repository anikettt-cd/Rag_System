def solve():
    N, M = map(int, input().split())

    graph = [[] for _ in range(N)]

    for _ in range(M):
        a, b = map(int, input().split())
        a -= 1
        b -= 1

        graph[a].append(b)
        graph[b].append(a)

    start1, start2 = map(int, input().split())
    destination = int(input())

    start1 -= 1
    start2 -= 1
    destination -= 1
    
    def get_paths(start):
        paths = []
        def dfs(node, mask):
            if node == destination:
                paths.append(mask)
                return

            for nxt in graph[node]:
                bit = 1 << nxt

                # Don't visit a town twice
                if mask & bit:
                    continue
                dfs(nxt, mask | bit)

        dfs(start, 1 << start)
        return paths

    paths1 = get_paths(start1)
    paths2 = get_paths(start2)

    destination_bit = 1 << destination

    answer = float('inf')

    for mask1 in paths1:
        for mask2 in paths2:
            common = mask1 & mask2

            common_without_destination = common & ~destination_bit
            if common_without_destination != 0:
                continue


            total = (mask1 | mask2).bit_count()

            answer = min(answer, total)

    if answer == float('inf'):
        print("Impossible")
    else:
        print(answer)


solve()