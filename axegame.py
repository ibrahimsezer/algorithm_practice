# 30 wood = 50 gold
# 1 axe = 60 wood to be collected
# 1 axe price = 50 gold
# axe health = 120
# 4 hits * 15 wood = 60 wood collected

import constvalue


def game_start():

    # Definitions for the game.
    my_wood = 0
    my_gold = 50.0
    my_axe = False
    my_axe_health = 0
    print("----------------------------------------------------------------------------")
    display(my_axe, my_axe_health, my_wood, my_gold)
    control_axe(my_axe, my_axe_health, my_wood, my_gold)
    if not my_axe:
        visit_market(my_axe, my_axe_health, my_wood, my_gold)


def control_axe(my_axe, my_axe_health, my_wood, my_gold):
    if my_axe:
        print(f"You have an axe and its health: {my_axe_health}")
        print("Start collecting wood.")
        collect_wood(my_axe, my_axe_health, my_wood, my_gold)
    else: # Go here when axe is broken
        print(constvalue.require_axe)

def visit_market(my_axe, my_axe_health, my_wood, my_gold):
    print("--------------------------------------------")
    print("Welcome to the market. Axe : 50 Gold.")
    print("--------------------------------------------")

    buy_or_sell = input("Press 'b' to buy an axe or 's' to sell your wood: ")
    if buy_or_sell == "b":
        if not my_axe and my_gold >= constvalue.AXE_PRICE:
            my_axe = True
            my_axe_health = constvalue.MAX_AXE_HEALTH
            my_gold -= constvalue.AXE_PRICE
            display(my_axe, my_axe_health, my_wood, my_gold)
            print("You can now start collecting wood.")
            collect_wood(my_axe, my_axe_health, my_wood, my_gold)
        elif not my_axe and my_gold <= 0:
            print("You can't buy an axe. Try selling some wood.")
            visit_market(my_axe, my_axe_health, my_wood, my_gold)
    elif buy_or_sell == "s" and my_wood > 0:
        sell_wood(my_axe, my_axe_health, my_wood, my_gold)
    else:
        error_game(my_axe, my_axe_health, my_wood, my_gold)

def collect_wood(my_axe, my_axe_health, my_wood, my_gold):
    if my_axe_health > 0:
        _collect = input("Press Enter to collect wood.")
        if _collect == "":

            my_axe_health -= 30
            my_wood += constvalue.WOOD_COLLECT_PER_HIT
            print(f"Axe Health: {my_axe_health}")
            if my_axe_health <= 0:
                my_axe = False
                print("--------------------------------------------")
                print("Your axe broke. Visit the market to get a new one.")
                display(my_axe, my_axe_health, my_wood, my_gold)
                visit_market(my_axe, my_axe_health, my_wood, my_gold)
            else:
                collect_wood(my_axe, my_axe_health, my_wood, my_gold)
    else:
        print("Your axe is broken. Visit the market to get a new one.")
        visit_market(my_axe, my_axe_health, my_wood, my_gold)

def error_game(my_axe, my_axe_health, my_wood, my_gold):
        print("--------------------------------------------")
        controller = input("You entered an invalid input. Do you want to go to the market or collect wood? (Market: m, Wood: w)")
        if controller == "m":
            visit_market(my_axe, my_axe_health, my_wood, my_gold)
        elif controller == "w":
            collect_wood(my_axe, my_axe_health, my_wood, my_gold)
        else:
            print("You made an invalid entry. Please try again.")
            error_game(my_axe, my_axe_health, my_wood, my_gold)

def sell_wood(my_axe, my_axe_health, my_wood, my_gold):
    print("--------------------------------------------")
    _sell_control = int(input("How many units of wood would you like to sell?"))
    if _sell_control <= my_wood:
        my_wood -= _sell_control
        gold_earned = _sell_control * constvalue.WOOD_PRICE_PER_UNIT
        my_gold += gold_earned
        print(f"You sold { _sell_control } units of wood for { gold_earned } gold.\n\n----Current Gold : {my_gold}----\n\n")
        collect_wood(my_axe, my_axe_health, my_wood, my_gold)
    elif _sell_control > my_wood:
        print("You entered more wood than you have. Please try again.")
        sell_wood(my_axe, my_axe_health, my_wood, my_gold)
    else:
        print("You made an invalid entry. Please try again.")
        visit_market(my_axe, my_axe_health, my_wood, my_gold)

def display(my_axe, my_axe_health, my_wood, my_gold):
    print(f"My Gold: {my_gold}, My Axe: {my_axe}, Axe Health: {my_axe_health}, My Wood: {my_wood}")

