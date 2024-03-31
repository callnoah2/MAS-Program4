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
    for i in range(min(voters, len(names))):
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

def update_ballots(candidateRanking, neighbors):
    updated_candidateRanking = [voter_ranking[:] for voter_ranking in candidateRanking]

    for voter_idx, neighbors_idx in enumerate(neighbors):
        last_choice = updated_candidateRanking[voter_idx][0][CAND]
        neighbor_choices = [updated_candidateRanking[neighbor_idx][0][CAND] for neighbor_idx in neighbors_idx]
        second_choice = updated_candidateRanking[voter_idx][1][CAND]
        third_choice = updated_candidateRanking[voter_idx][2][CAND]

        # Strategy: If everyone else likes my last choice or if others are split between my second and third choices,
        # change my vote to my second choice if it's not their favorite, otherwise to my third choice.
        if all(choice == last_choice for choice in neighbor_choices) or \
                (neighbor_choices.count(second_choice) + neighbor_choices.count(third_choice)) >= 2:
            if second_choice not in neighbor_choices:
                updated_candidateRanking[voter_idx][0][CAND], updated_candidateRanking[voter_idx][1][CAND] = \
                    updated_candidateRanking[voter_idx][1][CAND], updated_candidateRanking[voter_idx][0][CAND]
            elif third_choice not in neighbor_choices:
                updated_candidateRanking[voter_idx][0][CAND], updated_candidateRanking[voter_idx][2][CAND] = \
                    updated_candidateRanking[voter_idx][2][CAND], updated_candidateRanking[voter_idx][0][CAND]

    return updated_candidateRanking

def simulate_voting(names, candidateRanking, connections, voters, candidates, max_revisions=10):
    rounds = 1
    stable = False
    max_rounds = max_revisions

    while not stable and rounds <= max_rounds:
        # print(f"Round {rounds}")
        neighbors = [[] for _ in range(voters)]
        for i in range(voters):
            neighbors[i] = [j for j in range(voters) if connections[j][i] == 1]

        # print("Neighbors:", neighbors)

        # get rankings before update
        prev_rankings = []
        for voter_ranking in candidateRanking:
            temp_ranking = []
            for choice in voter_ranking:
                temp_ranking.append(choice[CAND])
            prev_rankings.append(temp_ranking)

        # Update ballots at the beginning of each round
        updated_candidateRanking = update_ballots(candidateRanking, neighbors)

        # Check if the ballots have changed
        changed_rankings = any(prev_rankings[i] != [choice[CAND] for choice in voter_ranking] for i, voter_ranking in enumerate(updated_candidateRanking))

        if not changed_rankings:
            stable = True
        else:
            rounds += 1

        candidateRanking = updated_candidateRanking

        ordered = order_candidates(candidateRanking, voters, candidates)

    if stable:
        print(f"\nVotes are stable after {rounds} rounds.\n")
    else:
        print("\nMaximum rounds reached without achieving stability.\n")
        
    print_rankings(names, candidateRanking, voters, candidates, ordered)

    winner_pt2, _ = ranked_choice_voting(candidateRanking, ordered, voters, candidates)
    cardinal_utility_pt2, ordinal_utility_pt2 = calculate_social_welfare(winner_pt2, candidateRanking, voters)

    return rounds, winner_pt2, cardinal_utility_pt2, ordinal_utility_pt2

def create_voting(voters, candidates):
    names = ["Alice ", "Bart  ", "Cindy ", "Darin ", "Elmer ", "Finn  ", "Greg  ", "Hank  ", "Ian   ", "Jim   ",
             "Kate  ", "Linc  ", "Mary  ", "Nancy ", "Owen  ", "Peter ", "Quinn ", "Ross  ", "Sandy ", "Tom   ",
             "Ursula", "Van   ", "Wendy ", "Xavier", "Yan   ", "Zach  ", "Glenn ", "Chip  ", "Smith ", "Bob   ",
             "Mike  ", "Sam   ", "Jason ", "Ben,  ", "Joe   ", "Ryan  ", "Chris ", "Tobey ", "Andrew", "Kayla ",
             "Lilly ", "Jordan", "Gwen  ", "Stacy ", "Marie ", "Jane  ", "Peggy ", "Phoebe", "Tate  ", "Katie "][:voters]  # Use only required number of names

    connections = [[0 for _ in range(voters)] for _ in range(voters)]
    np.random.seed(1052)

    for i in range(voters):
        conn = round(np.random.uniform(0, voters / 2))
        for _ in range(conn):
            connectTo = np.random.randint(0, voters)
            if connectTo != i:
                connections[i][connectTo] = 1

    candidateRanking = [[list() for _ in range(candidates)] for _ in range(voters)]

    for i in range(voters):
        for j in range(candidates):
            candidateRanking[i][j] = [j + 1, round(np.random.uniform(0, 100)) / 10, 0]

    print("\n")
    print_connections(names, connections, voters, candidates)
    
    winner_borda, _ = ranked_choice_voting(candidateRanking, order_candidates(candidateRanking, voters, candidates), voters, candidates)

    cardinal_utility_borda, ordinal_utility_borda = calculate_social_welfare(winner_borda, candidateRanking, voters)

    rounds_network, winner_network, cardinal_utility_network, ordinal_utility_network = simulate_voting(names, candidateRanking, connections, voters, candidates)
    
    print("\nBorda Method:")
    print("Winner:", winner_borda)
    print("Social Welfare - Cardinal Utility:", cardinal_utility_borda)
    print("Social Welfare - Ordinal Utility:", ordinal_utility_borda)

    print("\nSocial Network Method:")
    print("Rounds to Stability:", rounds_network)
    print("Winner:", winner_network)
    print("Social Welfare - Cardinal Utility:", cardinal_utility_network)
    print("Social Welfare - Ordinal Utility:", ordinal_utility_network)

    # Determine how often the methods give the same result
    all_same_result = winner_borda == winner_network
    if all_same_result:
        print("\nThe methods give the same result.")
    else:
        print("\nGot Different results")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Run simulations for different numbers of voters
    for num_voters in range(10, 51, 10):
        print(f"\nSimulations for {num_voters} voters:")
        create_voting(num_voters, 5)  # Use 5 candidates in each simulation