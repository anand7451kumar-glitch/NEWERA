import random

suits = ["♠", "♥", "♦", "♣"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

deck = [(rank, suit) for suit in suits for rank in ranks]

wins = 0
losses = 0
draws = 0


def card_value(card):
    rank = card[0]

    if rank in ["J", "Q", "K"]:
        return 10
    if rank == "A":
        return 11
    return int(rank)


def hand_value(hand):
    total = sum(card_value(card) for card in hand)
    aces = sum(card[0] == "A" for card in hand)

    while total > 21 and aces:
        total -= 10
        aces -= 1

    return total


def show_hand(name, hand):
    cards = " ".join(rank + suit for rank, suit in hand)
    print(f"{name}: {cards}  ({hand_value(hand)})")


while True:
    deck = [(rank, suit) for suit in suits for rank in ranks]
    random.shuffle(deck)

    player = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]

    print("\n========== BLACKJACK ==========")
    print("Wins:", wins, "| Losses:", losses, "| Draws:", draws)

    show_hand("Your hand", player)
    print("Dealer:", dealer[0][0] + dealer[0][1], "??")

    while hand_value(player) < 21:
        choice = input("Hit or stand? ").lower()

        if choice == "hit":
            player.append(deck.pop())
            show_hand("Your hand", player)

        elif choice == "stand":
            break

        else:
            print("Enter hit or stand.")

    player_score = hand_value(player)

    if player_score > 21:
        print("You busted!")
        losses += 1
    else:
        while hand_value(dealer) < 17:
            dealer.append(deck.pop())

        print()
        show_hand("Dealer", dealer)

        dealer_score = hand_value(dealer)

        if dealer_score > 21:
            print("Dealer busted — You win!")
            wins += 1
        elif player_score > dealer_score:
            print("You win!")
            wins += 1
        elif player_score < dealer_score:
            print("Dealer wins!")
            losses += 1
        else:
            print("Draw!")
            draws += 1

    again = input("\nPlay another round? (y/n): ").lower()

    if again != "y":
        break

print("\n========== FINAL SCORE ==========")
print("Wins:", wins)
print("Losses:", losses)
print("Draws:", draws)
print("Thanks for playing!")
