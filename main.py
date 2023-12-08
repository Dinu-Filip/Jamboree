import math
import random


def detriment_x(whites, blacks, N, R):
    total = 0
    for i in range(N):
        for k in range(R):
            total += abs(whites[i][k] - blacks[i][k])
    return total


def detriment_y(up_floats, down_floats, N):
    total = 0
    for i in range(N):
        up_total = sum(up_floats[i])
        down_total = sum(down_floats[i])
        total += abs(up_total - down_total)
    return total


def detriment_z(whites, B, R, N):
    total = 0
    factor = 4 / (R * B * (B + 1))
    for i in range(N):
        board_count = 0
        for l in range(B):
            board_count += l * whites[i][l]
        prod = factor * board_count
        total += abs(1 - prod)
    return total


#
# whites_per_round = [[1, 3, 2], [1, 3, 2], [3, 1, 2], [2, 1, 3], [2, 2, 2], [3, 2, 1]]
# blacks_per_round = [[3, 1, 2], [3, 1, 2], [1, 3, 2], [2, 3, 1], [2, 2, 2], [1, 2, 3]]
#
# whites_per_board = [[1, 2, 1, 2], [2, 1, 2, 1], [2, 1, 2, 1], [2, 1, 1, 2], [1, 2, 1, 2], [1, 2, 2, 1]]
# blacks_per_board = [[2, 1, 2, 1], [1, 2, 1, 1], [1, 2, 1, 2], [1, 2, 2, 1], [2, 1, 2, 1], [2, 1, 1, 2]]
#
# R = 3
# B = 4
# N = 6
# x = detriment_x(whites_per_round, blacks_per_round, N, R)
# z = detriment_z(whites_per_board, B, R, N)
# print(round(x + z, 4))

def initialise_pairings(N, R, B, player_names):
    jamboree = [[[] for _ in range(R)] for _ in range(B)]
    # Determines max number of times each team plays every other team
    max_plays = math.ceil((R * B) / (N - 1))
    # 2D matrix stores number of times team plays another team
    num_plays = [[0 for _ in range(N)] for _ in range(N)]
    # Number of times a player is white for certain board
    num_player_white = [[0 for _ in range(N)] for _ in range(B)]
    for b in range(B):
        # Stores pairings for each team player for current board
        current_pairings = {}
        for r in range(R):
            # Stores players that have already been paired up in current round
            added_players = []
            rand_players = [_ for _ in range(N)]
            random.shuffle(rand_players)
            for player in rand_players:
                # Checks that player has not already been assigned partner in round
                if player not in added_players:
                    # Rule 8
                    # Checks that player has not already been assigned white twice
                    if num_player_white[b][player] == 2:
                        continue
                    # Rule 9
                    # Checks that number of whites does not exceed half of total number of games
                    total_team_white = sum([l[player] for l in num_player_white])
                    if total_team_white == (B * R) / 2:
                        continue
                    # Rule 2
                    valid_players = [_ for _ in range(N)]
                    valid_players.pop(player)
                    idx = 0
                    while idx < len(valid_players):
                        p = valid_players[idx]
                        # Rule 1
                        if p in added_players:
                            valid_players.pop(idx)
                            continue
                        # Rule 3
                        if num_plays[player][p] == max_plays:
                            valid_players.pop(idx)
                            continue
                        # Ensures that all players are white at least once by not assigning a player that has been black
                        # twice already
                        if r == 2 and num_player_white[b][p] == 0:
                            valid_players.pop(idx)
                            continue
                        # Ensures the players have not already played each other in a previous round
                        if player in current_pairings:
                            if p in current_pairings[player]:
                                valid_players.pop(idx)
                                continue
                        idx += 1
                    if not valid_players:
                        return None
                    partner = random.choice(valid_players)
                    if player not in current_pairings:
                        current_pairings[player] = [partner]
                    else:
                        current_pairings[player].append(partner)
                    if partner not in current_pairings:
                        current_pairings[partner] = [player]
                    else:
                        current_pairings[partner].append(player)
                    added_players.append(player)
                    added_players.append(partner)
                    num_player_white[b][player] += 1
                    num_plays[player][partner] += 1
                    num_plays[partner][player] += 1
                    jamboree[b][r].append((player_names[player], player_names[partner]))
        if len(jamboree[b][r]) != N / 2:
            return None
    return jamboree


pairs = []
res = initialise_pairings(12, 3, 6, ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"])
while not res:
    res = initialise_pairings(12, 3, 6, ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"])

for r in res:
    print(r)
