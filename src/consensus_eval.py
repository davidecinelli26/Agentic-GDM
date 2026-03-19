def evaluate_individual_satisfaction(poi_category):
    """
    Evaluates the satisfaction level (0 to 1) of each agent based on the chosen POI category.
    This simulates the 'fuzzy' preferences of the agents.
    """
    # Preference matrix: rows are agents, columns are POI categories
    preferences = {
        "Sophia (Culture)": {"Culture": 1.0, "Food": 0.4, "Nightlife": 0.1, "Viewpoint": 0.7},
        "Marco (Foodie)":   {"Culture": 0.5, "Food": 1.0, "Nightlife": 0.6, "Viewpoint": 0.5},
        "Liam (Party)":     {"Culture": 0.1, "Food": 0.8, "Nightlife": 1.0, "Viewpoint": 0.5},
        "Emma (Budget)":    {"Culture": 0.4, "Food": 0.6, "Nightlife": 0.2, "Viewpoint": 1.0} 
    }
    
    satisfactions = []
    print("\n--- INDIVIDUAL SATISFACTION ---")
    for agent, prefs in preferences.items():
        sat = prefs.get(poi_category, 0.0)
        satisfactions.append(sat)
        print(f"- {agent}: {sat:.2f}")
        
    return satisfactions

def owa_consensus(satisfactions, weights):
    """
    Applies the Ordered Weighted Averaging (OWA) operator.
    """
    # Step 1: Sort satisfactions in descending order
    sorted_sat = sorted(satisfactions, reverse=True)
    
    # Step 2: Multiply by weights and sum
    consensus = sum(w * y for w, y in zip(weights, sorted_sat))
    return consensus

def calculate_group_consensus(poi_category):
    """
    Calculates the final global consensus using a fair/pessimistic weight vector.
    """
    print(f"\n[GDM MODULE] Evaluating consensus for category: {poi_category}")
    satisfactions = evaluate_individual_satisfaction(poi_category)
    
    # OWA Weights: [0.1, 0.2, 0.3, 0.4]
    # We give the lowest weight (0.1) to the most satisfied person, 
    # and the highest weight (0.4) to the LEAST satisfied person to guarantee fairness.
    weights = [0.1, 0.2, 0.3, 0.4] 
    
    consensus_score = owa_consensus(satisfactions, weights)
    print(f"\n=> GLOBAL GROUP CONSENSUS (OWA): {consensus_score:.2f} / 1.00")
    
    if consensus_score >= 0.7:
        print("Result: STRONG CONSENSUS REACHED. The group is happy!")
    elif consensus_score >= 0.5:
        print("Result: MODERATE CONSENSUS. An acceptable compromise.")
    else:
        print("Result: POOR CONSENSUS. High risk of conflict in the group.")
        
    return consensus_score

# For testing the module independently
if __name__ == "__main__":
    # Test what happens if they choose "Food"
    calculate_group_consensus("Food")
    
    # Test what happens if they choose "Nightlife" (Liam is happy, Sophia hates it)
    calculate_group_consensus("Nightlife")