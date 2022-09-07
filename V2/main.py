import time
import random
from Player import Player
from Dealer import Dealer
from Card import Card

start_Game = False
wantRestart = False


def Start_the_game():

   # if start_Game == False: return

   # print("je commence")

    continue_the_game = True

    while continue_the_game:
        playerBet()
        print("Distribution des cartes....")
        time.sleep(2)
        dealerActions()


def GameOver():
    print("Game Over, Au revoir!")
    exit()


def Restart():
    wantRestart = True
    while wantRestart:
        if Player.cur_Money <= 0:
            print("Vous etes ruiner, c'est la fin au revoir")
            wantRestart = False
            GameOver()
        else:
            restart = input("Again ? (y/n) : ")
            if restart == "y":
                print("Lancement d'une nouvelle partie...")
                Player.bet = 0
                Player.has_split = False
                Player.card.clear()
                Player.card_value.clear()
                Player.total = 0
                Player.can_play = False
                Player.newCard_Total = 0

                Dealer.AIcard.clear()
                Dealer.card_value.clear()
                Dealer.total = 0
                Dealer.can_play = False

                Card.value = 0
                Card.init_deck = Card.club_deck + Card.diamond_deck + \
                    Card.heart_deck + Card.spade_deck
                Card.current_deck.clear()
                wantRestart = False
                Start_the_game()

            elif restart == "n":
                wantRestart = False
                GameOver()
            else:
                print("ERROR RESPONSE Try again")


# Player choose the amount of money he's playing with
def playerBet():

    # Give your bet
    while Player.bet <= 0 or Player.bet > Player.cur_Money:
        print("Vous avez en poche :", Player.cur_Money, "$")
        Player.bet = int(input("Entrez votre mise : "))
        if Player.cur_Money < Player.bet:
            print("Error: You don't have enough cur_Money, please try again.")
        elif Player.bet <= 0:
            print("Error: Negative bet or null, please try again.")
        elif Player.bet <= Player.cur_Money:
            print("Vous avez misez :", Player.bet, "$")
            Player.cur_Money -= Player.bet
            time.sleep(2)
            print("Il vous reste alors :", Player.cur_Money, "$")
            break


def dealerActions():
    Card.current_deck = Card.init_deck.copy()

    random.shuffle(Card.current_deck)  # Melange les cartes

    for a in range(2):
        i = random.randrange(len(Card.current_deck))
        Player.card.append(Card.current_deck[i])
        Card.current_deck.remove(Player.card[a])
        Dealer.AIcard.append(Card.current_deck[a])
        Card.current_deck.remove(Dealer.AIcard[a])

    ValueOfTheCard(Dealer.AIcard[0], Dealer.total)
    Dealer.card_value.append(Card.value)
    Dealer.total = sum(Dealer.card_value)
    ValueOfTheCard(Dealer.AIcard[1], Dealer.total)
    Dealer.card_value.append(Card.value)
    Dealer.total = sum(Dealer.card_value)
    player_choice()


def ValueOfTheCard(name_card, total_card):
    nb = ['2', '3', '4', '5', '6', '7', '8', '9', '10']

    name = name_card.split()
    if name[0] in nb:
        Card.value = int(name[0])
        return Card.value
    elif name[0] == "ace":
        if((total_card + 11) <= 21):
            Card.value = 11
        else:
            Card.value = 1
        return Card.value
    else:
        Card.value = 10
        return Card.value


# Player choose what he want to do (draw, split, double, stop)
def player_choice():
    Player.can_play = True
    print("Vos cartes sont :", Player.card[0], "et", Player.card[1])
    ValueOfTheCard(Player.card[0], Player.total)
    Player.card_value.append(Card.value)
    Player.total = sum(Player.card_value)
    ValueOfTheCard(Player.card[1], Player.total)
    Player.card_value.append(Card.value)
    Player.total = sum(Player.card_value)
    print("Vous avez un total de :", Player.total)
    time.sleep(2)
    print("La premiere carte du Dealer est :", Dealer.AIcard[0])
    time.sleep(2)
    print("Vous pouvez séparer les deux cartes, vous arretez, ou piocher encore")

    while Player.can_play:

        answer = input(
            "Que voulez-vous faire ? (split / piocher / doubler / arreter)(Ecrivez : 1 / 2 / 3 / 4) : ")
        if answer == "1" and Player.card_value[0] == Player.card_value[1]:

            has_split = True

            # creation liste la derniere valeur de la liste du player
            newCard = [Player.card.pop(len(Player.card) - 1)]
            # Montre les deux nouvelle main (1 carte dans chaque main)

            # print(newCard, Player.card)

            i = random.randrange(len(Card.current_deck))  # Tirage d'une carte
            # Ajout de la carte tirée dans la nouvelle main
            newCard.append(Card.current_deck[i])
            # supprimer la carte tirée de la pioche
            Card.current_deck.remove(newCard[len(newCard)-1])

            i = random.randrange(len(Card.current_deck))  # Tirage d'une carte
            # Ajout de la carte tirée dans la nouvelle main
            Player.card.append(Card.current_deck[i])
            # supprimer la carte tirée de la pioche
            Card.current_deck.remove(Player.card[len(Player.card) - 1])

            # Montre les deux nouvelle main (2 cartes dans chaque main)
            # print(newCard, Player.card)

            ValueOfTheCard(Player.card[0], Player.total)
            Player.card_value.clear()
            Player.card_value.append(Card.value)
            Player.total = sum(Player.card_value)

            ValueOfTheCard(Player.card[1], Player.total)
            Player.card_value.append(Card.value)
            Player.total = sum(Player.card_value)

            ValueOfTheCard(newCard[0], Player.newCard_Total)
            Player.newCard_Total = Card.value
            ValueOfTheCard(newCard[1], Player.newCard_Total)
            Player.newCard_Total += Card.value

            Player.bet = Player.bet * 2

            print("Votre première main est :", newCard[0], "et", newCard[1],
                  ". Le total est donc de :", Player.newCard_Total)
            time.sleep(3)
            print("Votre seconde main est :",
                  Player.card[0], "et", Player.card[1], ". Le total est donc de :", Player.total)
            time.sleep(3)
            print("Vous misez donc le double :", Player.bet, "$")
            time.sleep(3)
            print("Prenons votre premiere main :",
                  newCard[0], "et", newCard[1],)

            double_or_quits(Player.newCard_Total, newCard)

        elif answer == "1" and Player.card_value[0] != Player.card_value[1]:
            print("Vous ne pouvez pas split car il faut avoir les deux mêmes cartes")
            continue

        elif answer == "2":
            player_Draw(Player.total, Player.card)

        elif answer == "3":
            if Player.bet > Player.cur_Money / 2:
                print("Vous n'avez pas assez d'argent pour doubler votre mise choisissez une autre option")
                continue

            i = random.randrange(len(Card.current_deck))  # Tirage d'une carte
            # Ajout de la carte tirée dans la nouvelle main
            Player.card.append(Card.current_deck[i])
            # supprimer la carte tirée de la pioche
            Card.current_deck.remove(Player.card[len(Player.card) - 1])
            print("Vous avez piocher la carte :",
                  Player.card[len(Player.card) - 1])
            time.sleep(2)
            print("Vos carte :", Player.card)
            time.sleep(2)

            ValueOfTheCard(Player.card[len(Player.card) - 1], Player.total)
            Player.card_value.append(Card.value)
            Player.total = sum(Player.card_value)

            print("Vos cartes sont :", Player.card,
                  ". Le total est donc de :", Player.total)
            time.sleep(2)
            Player.bet *= 2
            print("Votre mise est de :", Player.bet)
            time.sleep(2)
            Player.can_play = False
            print("Votre tour est terminé, au tour du Dealer")
            time.sleep(2)
            dealer_Turn()

        elif answer == "4":
            print("Votre tour est terminé, au tour du Dealer")
            time.sleep(2)
            Player.can_play = False
            dealer_Turn()

        else:
            print("Erreur : vous devez ecrire soi : 1 / 2 / 3 / 4 sans espace")


def dealer_Turn():

    if Dealer.total != 21:
        print("La deuxieme carte du Dealer est :", Dealer.AIcard[1])
        time.sleep(3)
        print("Le Dealer a :", Dealer.AIcard, "pour un total de :",
              Dealer.total)
        time.sleep(3)

        if Player.newCard_Total != 0 and Dealer.total > Player.newCard_Total:  # j'ai split
            print(
                "Le Dealer gagne par rapport a votre permier main, voyons pour votre deuxieme main !")
            time.sleep(3)
            if Dealer.total > Player.total or Player.total > 21:
                print("Dealer gagne, tu perds tous ton argent :",
                      Player.bet, "$")
                time.sleep(3)
                print("Le Dealer avait :", Dealer.AIcard, "pour un total de :",
                      Dealer.total)
                time.sleep(3)
                Player.cur_Money = 1000 - Player.bet
                print("Il vous reste:", Player.cur_Money, "$")
                time.sleep(3)
            elif Dealer.total <= Player.total <= 21:
                dealer_Draw()

        elif Player.newCard_Total != 0 and Dealer.total < Player.newCard_Total:
            dealer_Draw()
            print("Le total des cartes du Dealer est :", Dealer.total)
            print("Votre premiere main a pour total:", Player.newCard_Total)
            print("Votre deuxieme main a pour total:", Player.total)

            if Player.total < Dealer.total < 21 and Dealer.total > Player.newCard_Total:
                print(
                    "Le Dealer gagne vous avez perdu vorte mise qui est de:", Player.bet, "$")
                print("Le Dealer avait :", Dealer.AIcard, "pour un total de :",
                      Dealer.total)
                Player.cur_Money = 1000 - Player.bet
                print("Il vous reste:", Player.cur_Money, "$")
            elif Player.total < Dealer.total < Player.newCard_Total < 21\
                    or Player.newCard_Total < Dealer.total < Player.total < 21:
                print("Le Dealer avait :", Dealer.AIcard, "pour un total de :",
                      Dealer.total)
                print("Le Dealer gagne la moité des gains et vous aussi:", Player.bet, "$", "/ 2 =",
                      Player.bet / 2, "$")
                Player.cur_Money = 1000 - (Player.bet/2)
                print("Il vous reste:", Player.cur_Money, "$")
            elif Dealer.total > 21 and Player.total > 21 and Player.newCard_Total > 21:
                print("Vous avez tous perdu! Vous récupérez votre mise:",
                      Player.bet, "$")
                print("Le Dealer avait :", Dealer.AIcard, "pour un total de :",
                      Dealer.total)
                Player.cur_Money = 1000
                print("Il vous reste:", Player.cur_Money, "$")

        # player a soi piocher ou doubler ou arreter
        elif Player.newCard_Total == 0 and 21 >= Player.total >= Dealer.total:
            dealer_Draw()
            if Player.total < Dealer.total < 21:
                print("Vous avez perdu votre mise:", Player.bet, "$")
                print("Le Dealer avait :", Dealer.AIcard, "pour un total de :",
                      Dealer.total)
                Player.cur_Money = 1000 - Player.bet
                print("Il vous reste:", Player.cur_Money, "$")
            elif Dealer.total <= 21 and Player.total > 21:
                print("Vous avez perdu votre mise:", Player.bet, "$")
                print("Le Dealer avait :", Dealer.AIcard, "pour un total de :",
                      Dealer.total)
                Player.cur_Money = 1000 - Player.bet
                print("Il vous reste:", Player.cur_Money, "$")
            elif Dealer.total < Player.total <= 21 or Dealer.total > 21 >= Player.total:
                print(
                    "Vous avez gagné ! Votre gains est de 2 x votre mise:", Player.bet, "$")
                print("Le Dealer avait :", Dealer.AIcard, "pour un total de :",
                      Dealer.total)
                Player.cur_Money = 1000 + Player.bet
                print("Il vous reste:", Player.cur_Money, "$")
            elif Dealer.total > 21 and Player.total > 21:
                print("Vous avez tous perdu! Vous récupérez votre mise:",
                      Player.bet, "$")
                print("Le Dealer avait :", Dealer.AIcard, "pour un total de :",
                      Dealer.total)
                Player.cur_Money = 1000
                print("Il vous reste:", Player.cur_Money, "$")

        elif Player.newCard_Total == 0 and Player.total > 21:
            print("Vous avez perdu votre mise:", Player.bet, "$")
            print("Le Dealer avait :", Dealer.AIcard, "pour un total de :",
                  Dealer.total)
            Player.cur_Money = 1000 - Player.bet
            print("Il vous reste:", Player.cur_Money, "$")

        elif Player.newCard_Total == 0 and 21 >= Player.total < Dealer.total:
            print("Vous avez perdu !")
            print("Le Dealer avait :", Dealer.AIcard, "pour un total de :",
                  Dealer.total)
            print("Vous avez perdu votre mise:", Player.bet, "$")
            Player.cur_Money = 1000 - Player.bet
            print("Il vous reste:", Player.cur_Money, "$")

        elif Player.newCard_Total == 0 and Player.total == Dealer.total:
            print("Egalité vous récuperez votre mise! :", Player.bet, "$")
            print("Le Dealer avait :", Dealer.AIcard, "pour un total de :",
                  Dealer.total)
            Player.cur_Money = 1000
            print("Il vous reste:", Player.cur_Money, "$")

    Restart()


# the dealer take a card
def dealer_Draw():
    list_value_cards = []

    for i in range(len(Card.current_deck)):
        list_value_cards.append(ValueOfTheCard(
            Card.current_deck[i], Dealer.total))

    count = 0
    nb_before_21 = 21 - Dealer.total

    for i in list_value_cards:
        if i <= nb_before_21:
            count += 1

    percentage_before_playing = (count * 100 / len(list_value_cards))
    Dealer.can_play = True

    while Dealer.can_play:

        if percentage_before_playing < 40:
            Dealer.can_play = False
        else:
            i = random.randrange(len(Card.current_deck))  # Tirage d'une carte
            # Ajout de la carte tirée dans la nouvelle main
            Dealer.AIcard.append(Card.current_deck[i])
            # supprimer la carte tirée de la pioche
            Card.current_deck.remove(Dealer.AIcard[len(Dealer.AIcard) - 1])

            ValueOfTheCard(
                Dealer.AIcard[len(Dealer.AIcard) - 1], Dealer.total)
            Dealer.card_value.append(Card.value)
            Dealer.total = sum(Dealer.card_value)

            print("Le Dealer a pioché la carte :",
                  Dealer.AIcard[len(Dealer.AIcard) - 1])
            time.sleep(2)
            print("Ses cartes sont :", Dealer.AIcard)
            time.sleep(2)
            print("Le total de ses cartes est :", Dealer.total)
            time.sleep(2)

            dealer_Draw()


# The player take a card
def player_Draw(card_total, list_card):
    if card_total > 21:
        EndGame(card_total, list_card)
    else:
        i = random.randrange(len(Card.current_deck))
        list_card.append(Card.current_deck[i])
        last_card = len(list_card) - 1
        Card.current_deck.remove(list_card[last_card])
        print("Vous avez piocher la carte :", list_card[last_card])

        time.sleep(2)

        ValueOfTheCard(list_card[last_card], card_total)
        card_total += Card.value
        Player.total = card_total
        print("Vos cartes sont :", list_card,
              ". Le total est donc de :", card_total)
        time.sleep(3)

        while Player.can_play:
            if Player.total <= 21:
                answer = input(
                    "Que Voulez vous faire ? (Arreter/ Piocher) (Ecrivez : 1 / 2  :")
                if answer == "1":
                    print("Votre tour est terminer ! Regardons les cartes du Dealer")
                    Player.can_play = False

                    time.sleep(3)

                    dealer_Turn()
                elif answer == "2":
                    i = random.randrange(len(Card.current_deck))
                    list_card.append(Card.current_deck[i])
                    last_card = len(list_card) - 1
                    Card.current_deck.remove(list_card[last_card])
                    print("Vous avez piocher la carte :", list_card[last_card])

                    time.sleep(2)

                    ValueOfTheCard(list_card[last_card], card_total)
                    card_total += Card.value
                    Player.total = card_total
                    print("Vos cartes sont :", list_card,
                          ". Le total est donc de :", card_total)
                    continue
            else:
                print("Vous avez dépasser 21, Vous avez perdu !")
                time.sleep(2)
                print("Le Dealer avait :", Dealer.AIcard[0], "et", Dealer.AIcard[1], "pour un total de :",
                      Dealer.total)
                Player.can_play = False
                time.sleep(2)
                print("Vous avez perdu votre mise:", Player.bet, "$")
                Player.cur_Money = 1000 - Player.bet
                time.sleep(2)
                print("Il vous reste:", Player.cur_Money, "$")
                Restart()


# The player has double. Will he win double or loose double ?
def double_or_quits(card_total, list_card):
    if card_total > 21:
        EndGame(card_total, list_card)
    else:
        answer = input(
            "Que Voulez vous faire ? (Arreter/ Piocher) (Ecrivez : 1 / 2  :")

        if answer == "1" and list_card != Player.card:
            Player.newCard_Total = card_total
            print("Prenons votre deuxieme main :", Player.card)
            double_or_quits(Player.total, Player.card)
        elif answer == "1" and list_card == Player.card:
            print("Votre tour est terminer ! Regardons les cartes du Dealer")
            time.sleep(2)
            Player.can_play = False
            dealer_Turn()

        elif answer == "2":
            i = random.randrange(len(Card.current_deck))
            list_card.append(Card.current_deck[i])
            last_card = len(list_card) - 1
            Card.current_deck.remove(list_card[last_card])
            print("Vous avez piocher la carte :", list_card[last_card])
            time.sleep(2)

            if list_card == Player.card:
                ValueOfTheCard(list_card[last_card], card_total)
                card_total += Card.value
                Player.total = card_total
                time.sleep(2)
                print("Vos cartes sont :", str(list_card),
                      ". Le total est donc de :", card_total)
            else:
                ValueOfTheCard(list_card[last_card], card_total)
                card_total += Card.value
                Player.newCard_Total = card_total
                time.sleep(2)
                print("Vos cartes sont :", str(list_card),
                      ". Le total est donc de :", card_total)

            double_or_quits(card_total, list_card)


def EndGame(total, list_card):
    if list_card == Player.card:
        print("Dommage vous avez perdu!")
        dealer_Turn()
        time.sleep(2)
        print("Vous avez depassé 21, vous avez fait :", total, "et le Dealer avait :",
              Dealer.AIcard, "pour un total de :", Dealer.total,)
        time.sleep(2)
        Player.can_play = False
    else:
        print("Dommage vous avez perdu!")
        time.sleep(2)
        print("Vous avez depassé 21, vous avez fait :", total)
        time.sleep(2)
        print("Prenons votre deuxieme main :", Player.card)
        time.sleep(2)
        double_or_quits(Player.total, Player.card)
        Player.can_play = False


Start_the_game()
