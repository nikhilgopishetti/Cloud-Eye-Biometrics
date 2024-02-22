def countPurchases(budget, costs):
    n = len(costs)
    purchases = 0
    current_index = 0
    purchases_details = []

    while True:
        if costs[current_index] <= budget:
            budget -= costs[current_index]
            purchases += 1
            purchases_details.append((current_index, costs[current_index], budget, "Bought"))

        else:
            purchases_details.append((current_index, costs[current_index], budget, "Not enough budget"))

        current_index = (current_index + 1) % n

        if current_index == 0:
            break

    return purchases_details

# Prompt for input
n = int(input("Enter the number of elements in cost: "))
print("Enter the costs:")
costs = []
for i in range(n):
    cost = int(input(f"Cost[{i+1}]: "))
    costs.append(cost)
budget = int(input("Enter the budget: "))

# Calculate purchases and details
purchases_details = countPurchases(budget, costs)

# Output purchases details
print("\nNumber\tCost\tBudget\tExplanation")
for i, (index, cost, new_budget, explanation) in enumerate(purchases_details):
    print(f"{i+1}\t{cost}\t{new_budget}\t{explanation}")
