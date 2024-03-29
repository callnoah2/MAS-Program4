import numpy as np

CAND = 0
SCORE = 1
PLACE = 2

def print_connections(names, c, voters, candidates):
    print("CONNECTIONS")
    for i in range(voters):
        print("%10s" % (names[i]), end=" ")
        for j in range(voters):
            print(c[i][j], end=' ')
        print()

def print_rankings(names, r, voters, candidates, ordered):
    print("CANDIDATE Rankings")
    for i in range(voters):
        print(names[i], end=" ")
        for j in range(candidates):
            print(r[i][j], end='')
        print(" ORDER ", ordered[i])

def order_candidates(candidateRanking, voters, candidates):
    ordered = [[] for _ in range(voters)]

    for i in range(voters):
        s = sorted(candidateRanking[i], reverse=True, key=lambda v: v[SCORE])
        ordered[i] = [s[k][CAND] for k in range(candidates)]
        for v in range(candidates):
            candidate = s[v][CAND] - 1
            candidateRanking[i][candidate][PLACE] = v + 1

    return ordered

def calculate_social_welfare(winner, candidateRanking, voters):
    cardinal_utility = 0
    ordinal_utility = 0
    for i in range(voters):
        first_choice = candidateRanking[i][0][CAND]
        selected_choice = winner
        cardinal_utility += abs(candidateRanking[i][first_choice - 1][SCORE] - candidateRanking[i][selected_choice - 1][SCORE])
        ordinal_utility += abs(candidateRanking[i][first_choice - 1][PLACE] - candidateRanking[i][selected_choice - 1][PLACE])
    return cardinal_utility, ordinal_utility

def ranked_choice_voting(candidateRanking, ordered, voters, candidates):
    eliminated_candidates = []
    remaining_candidates = list(range(1, candidates + 1))
    
    while len(remaining_candidates) > 1:
        votes_count = [0] * candidates

        for voter, preferences in zip(candidateRanking, ordered):
            for preference in preferences:
                if preference in remaining_candidates:
                    votes_count[preference - 1] += 1
                    break

        # Increment each valid candidate's count by 1
        for i in range(len(votes_count)):
            if i + 1 in remaining_candidates:
                votes_count[i] += 1

        # Find the candidate with the lowest non-zero votes
        min_votes = min([count for count in votes_count if count > 0])
        eliminated_candidate = votes_count.index(min_votes) + 1

        eliminated_candidates.append(eliminated_candidate)
        remaining_candidates.remove(eliminated_candidate)

    winner = remaining_candidates[0]
    return winner, eliminated_candidates

def create_voting(voters, candidates):
    names = ["Alice ", "Bart  ", "Cindy ", "Darin ", "Elmer ", "Finn  ", "Greg  ", "Hank  ", "Ian   ", "Jim   ",
             "Kate  ", "Linc  ", "Mary  ", "Nancy ", "Owen  ", "Peter ", "Quinn ", "Ross  ", "Sandy ", "Tom   ",
             "Ursula", "Van   ", "Wendy ", "Xavier", "Yan   ", "Zach  "]

    connections = [[0 for _ in range(voters)] for _ in range(voters)]
    np.random.seed(1052)

    for i in range(voters):
        conn = round(np.random.uniform(0, voters / 2))
        for _ in range(conn):
            connectTo = np.random.randint(0, voters)
            if connectTo != i:
                connections[i][connectTo] = 1

    print_connections(names, connections, voters, candidates)

    candidateRanking = [[list() for _ in range(candidates)] for _ in range(voters)]

    for i in range(voters):
        for j in range(candidates):
            candidateRanking[i][j] = [j + 1, round(np.random.uniform(0, 100)) / 10, 0]

    ordered = order_candidates(candidateRanking, voters, candidates)
    print_rankings(names, candidateRanking, voters, candidates, ordered)

    winner, eliminated_candidates = ranked_choice_voting(candidateRanking, ordered, voters, candidates)

    cardinal_utility, ordinal_utility = calculate_social_welfare(winner, candidateRanking, voters)
    print("Eliminated canidates in order: ", eliminated_candidates)
    print("Winner: ", winner)
    print("Social Welfare - Cardinal Utility:", cardinal_utility)
    print("Social Welfare - Ordinal Utility:", ordinal_utility)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_voting(20, 5)