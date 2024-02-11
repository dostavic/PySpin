import random
from typing import Dict, List, Tuple

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}


def check_winnings(columns: List[List[str]], lines: int, bet: int, values: Dict[str, int]) -> Tuple[int, List[int]]:
    """
    Calculates the total winnings from a slot machine spin.
    :param columns: (Dict[str, int]) A 2D list where each sublist represents a slot machine column.
    Each element in a sublist is a string representing a symbol.
    :param lines: (int) The number of lines to check for winnings.
    :param bet: (int) The bet amount pre line.
    :param values: (Dict[str, int]) A dictionary that correlates each symbol with its value (possible winnings)
    :return:
    Tuple[int, List[int]]: A tuple containing the total winnings and a list fo the line numbers that won.
    Line numbers are 1-indexed.
    """
    winnings = 0
    winnings_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winnings_lines.append(line + 1)

    return winnings, winnings_lines


def get_slot_machine_spin(rows: int, cols: int, symbols: Dict[str, int]) -> List[List[str]]:
    """
    Generates a simulated spin of a slot machine.
    :param rows: (int) The number of rows in the slot machine.
    :param cols: (int) The number of columns in the slot machine
    :param symbols: (Dict[str, int]) A dictionary where keys are symbol characters as strings,
    and values are the counts of how many times each symbol appears.
    :return:
    List[List[str]]: A 2D list representing the columns and rows of a slot machine with randomly assigned symbols.
    """
    all_symbols = []
    for symbol, symbolCount in symbols.items():
        for _ in range(symbolCount):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns


def print_slot_machine(columns: List[List[str]]) -> None:
    """
    Print the slot machine spit result.
    :param columns: (List[List[str]]) A 2D list where each sublist represents a column in the slot machine.
    Each element in a sublist is a string representing a symbol.
    :return:
    None: This function prints the slot machine layout to the console but returns nothing.
    """
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")

        print()


def deposit() -> int:
    """
    Prompts the user to deposit a positive integer amount of money.
    :return:
    int: The deposit amount entered by the user.
    """
    while True:
        amount = input("What would you like to deposit? $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a number.")

    return amount


def get_number_of_lines() -> int:
    """
    Prompts the user to enter number of betting lines.
    :return:
    int: The number of lines the user wishes to bet on,  validated to be within the range 1 to MAX_LINES.
    """
    while True:
        lines = input("Enter the number of lines to bet on (1-" + str(MAX_LINES) + ")? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a number.")

    return lines


def get_bet() -> int:
    """
    Prompts the user to enter a betting amount pre line.
    :return:
    int: The validated betting amount pre line, within the range of MIN_BET to MAX_BET.
    """
    while True:
        amount = input("What would you like to bet on each line? $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}.")
        else:
            print("Please enter a number.")

    return amount


def spin(balance: int) -> int:
    """
    Executes a single spin on the slot machine.
    :param balance: (int) The player's current balance.
    :return:
    int: The net change in the player's balance after the spin (winnings minus the total bet).
    """
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(f"Tou do not have enough to bet that amount, your current balance is: ${balance}.")
        else:
            break

    print(f"You are betting ${bet} on {lines} lines. Total bet in equal to ${total_bet}.")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}.")
    print(f"You won on lines:", *winning_lines)
    return winnings - total_bet


def main() -> None:
    """
    The main function for running the slot machine game.
    :return:
    """
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press enter to play (q to quit).")
        if answer == "q":
            break
        balance += spin(balance)

    print(f"You left with ${balance}.")


if __name__ == "__main__":
    main()


# TODO: write README
