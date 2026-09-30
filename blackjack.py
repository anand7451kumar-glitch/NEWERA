import random

def draw_card():
    return random.randint(1, 11)

player = [draw_card(), draw_card()]
dealer = [draw_card(), draw_card()]

while True:
    print("\nYour cards:", player)
    print("Your total:", sum(player))

    if sum(player) > 21:
        print("You busted!")
        break

    choice = input("Hit or stand? ").lower()

    if choice == "hit":
        player.append(draw_card())

    elif choice == "stand":
        break

    else:
        print("Enter hit or stand.")

if sum(player) <= 21:
    while sum(dealer) < 17:
        dealer.append(draw_card())

    print("\nDealer cards:", dealer)
    print("Dealer ttotal:", sum(dealer))

    if sum(dealer) > 21 or sum(player) > sum(dealer):
        print("You Win!")
    elif sum(player) < sum(dealer):
        print("Dealer Wins!")
    else:
        print("draw!")