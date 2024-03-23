import math

def change(amount, coins):
    """
    Returns the minimum number of coins required to make up the given amount of money.

    Args:
    - amount (int): The amount of change to be made.
    - coins (list): A list of coin values.

    Returns:
    - int: The minimum number of coins required to make up the given amount of money.
    If there is no possible solution, returns math.inf.
    """
    if amount == 0:
        return 0
    elif amount < 0:
        return math.inf

    min_coins = math.inf
    for coin in coins:
        if amount - coin >= 0:
            num_coins = change(amount - coin, coins)
            min_coins = min(min_coins, num_coins + 1)

    return min_coins

def giveChange(amount, coins):
    """
    Returns a list whose first member is the minimum number of coins and whose second
    member is a list of the coins in that optimal solution.

    Args:
    - amount (int): The amount of change to be made.
    - coins (list): A list of coin values.

    Returns:
    - list: A list of the form [numberOfCoins, listOfCoins].
    """
    if amount == 0:
        return [0, []]
    elif amount < 0:
        return [math.inf, []]

    min_coins = math.inf
    best_coins = []
    for coin in coins:
        if amount - coin >= 0:
            num_coins, coin_list = giveChange(amount - coin, coins)
            if num_coins + 1 < min_coins:
                min_coins = num_coins + 1
                best_coins = coin_list + [coin]

    return [min_coins, best_coins]

if __name__ == "__main__":
    # Test cases
    print(change(48, [1, 5, 10, 25, 50]))  # Output: 6
    print(change(48, [1, 7, 24, 42]))      # Output: 2
    print(change(35, [1, 3, 16, 30, 50]))  # Output: 3
    print(change(6, [4, 5, 9]))            # Output: math.inf

    print(giveChange(48, [1, 5, 10, 25, 50]))  # Output: [6, [1, 1, 1, 1, 1, 1, 5, 10, 10, 25]]
    print(giveChange(48, [1, 7, 24, 42]))      # Output: [2, [24, 24]]
    print(giveChange(35, [1, 3, 16, 30, 50]))  # Output: [3, [3, 16, 16]]
    print(giveChange(6, [4, 5, 9]))            # Output: [math.inf, []]