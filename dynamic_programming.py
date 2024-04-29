import math

def change(amount, coins):
    """Calculate the minimum number of coins needed to make up a specific amount.

    Args:
        amount (int): The total amount for which change is required.
        coins (list): The list of coin denominations available.

    Returns:
        int: The minimum number of coins needed to make the amount, or math.inf if not possible.
    """
    # Initialize the dp array where dp[i] will be the minimum coins needed for amount i
    dp = [math.inf] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins needed to make amount 0
    
    # Update the dp array for each coin
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)

    return dp[amount] if dp[amount] != math.inf else math.inf



def giveChange(amount, coins):
    """Calculate the minimum number of coins and list of coins to make up a specific amount.

    Args:
        amount (int): The total amount for which change is required.
        coins (list): The list of coin denominations available.

    Returns:
        list: A list containing the minimum number of coins and a list of these coins.
    """
    # dp will store minimum coins, and last_used tracks the last coin used to reach the amount
    dp = [math.inf] * (amount + 1)
    last_used = [-1] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins needed to make amount 0
    
    for coin in coins:
        for x in range(coin, amount + 1):
            if dp[x] > dp[x - coin] + 1:
                dp[x] = dp[x - coin] + 1
                last_used[x] = coin

    if dp[amount] == math.inf:
        return [math.inf, []]

    # Trace back to find the coins used
    result_coins = []
    current = amount
    while current > 0:
        coin = last_used[current]
        result_coins.append(coin)
        current -= coin

    return [dp[amount], result_coins]
