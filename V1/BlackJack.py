import random
import time

start_Game = False
wantRestart = False


class Player:
    money = 1000
    price = 0
    has_split = False
    card = []
    card_value = []
    total = 0
    can_play = False
    newCard_Total = 0


class Croupier:
    AIcard = []
    card_value = []
    total = 0
    can_play = False


class Card:
    value = 0
    jeux_de_carte = []
    current = []
    noms_couleurs = [" trèfle ", " carreau ", " coeur ", " pique "]
    noms_valeurs = ['as', '2', '3', '4', '5', '6', '7',
                    '8', '9', '10', 'valet', 'dame', 'roi']
    nv = []
    nv2 = []
    nv3 = []
    nv4 = []

    for i in range(len(noms_valeurs)):
        nv.append(noms_valeurs[i] + noms_couleurs[0])
        nv2.append(noms_valeurs[i] + noms_couleurs[1])
        nv3.append(noms_valeurs[i] + noms_couleurs[2])
        nv4.append(noms_valeurs[i] + noms_couleurs[3])

    jeux_de_carte = nv + nv2 + nv3 + nv4


def Start_the_game():

   # if start_Game == False: return

   # print("je commence")

    continue_the_game = True

    while continue_the_game:
        playerMise()
        print("Distribution des cartes....")
        time.sleep(3)
        croupierAction()


def GameOver():
    print("Game Over, Au revoir!")
    exit()


def Restart():

    wantRestart = True
    while wantRestart:
        if Player.money <= 0:
            print("Vous etes ruiner, c'est la fin au revoir")
            continue_the_game = False
            wantRestart = False
        else:
            restart = input("Again ? (y/n) : ")
            if restart == "y":
                print("Lancement d'une nouvelle partie...")
                Player.price = 0
                Player.has_split = False
                Player.card.clear()
                Player.card_value.clear()
                Player.total = 0
                Player.can_play = False
                Player.newCard_Total = 0

                Croupier.AIcard.clear()
                Croupier.card_value.clear()
                Croupier.total = 0
                Croupier.can_play = False

                Card.value = 0
                Card.jeux_de_carte = Card.nv + Card.nv2 + Card.nv3 + Card.nv4
                Card.current.clear()
                wantRestart = False
                Start_the_game()

            elif restart == "n":
                continue_the_game = False
                wantRestart = False
                GameOver()
            else:
                print("ERROR REPONSE Réessayer")


def playerMise():

    # Give your price
    while Player.price <= 0 or Player.price > Player.money:
        print("Vous avez en poche :", Player.money, "$")
        Player.price = int(input("Entrez votre mise : "))
        if Player.money < Player.price:
            print("Error: You don't have enough money, please retry.")
        elif Player.price <= 0:
            print("Error: Negative price or null, please retry.")
        elif Player.price <= Player.money:
            print("Vous avez misez :", Player.price, "$")
            Player.money -= Player.price
            time.sleep(2)
            print("Il vous reste alors :", Player.money, "$")
            break


def croupierAction():
    Card.current = Card.jeux_de_carte.copy()
    random.shuffle(Card.current)  # Melange les cartes

    for a in range(2):
        i = random.randrange(len(Card.current))
        Player.card.append(Card.current[i])
        Card.current.remove(Player.card[a])
        Croupier.AIcard.append(Card.current[a])
        Card.current.remove(Croupier.AIcard[a])

    ValueOfTheCard(Croupier.AIcard[0], Croupier.total)
    Croupier.card_value.append(Card.value)
    Croupier.total = sum(Croupier.card_value)
    ValueOfTheCard(Croupier.AIcard[1], Croupier.total)
    Croupier.card_value.append(Card.value)
    Croupier.total = sum(Croupier.card_value)
    choix_Player()


def ValueOfTheCard(name_card, total_card):
    nb = ['2', '3', '4', '5', '6', '7', '8', '9', '10']

    name = name_card.split()
    if name[0] in nb:
        Card.value = int(name[0])
        return Card.value
    elif name[0] == "as":
        if total_card + 11 <= 21:
            Card.value = 11
        else:
            Card.value = 1
        return Card.value
    else:
        Card.value = 10
        return Card.value


def choix_Player():
    Player.can_play = True
    print("Vos cartes sont :", Player.card[0], "et", Player.card[1])
    ValueOfTheCard(Player.card[0], Player.total)
    Player.card_value.append(Card.value)
    Player.total = sum(Player.card_value)
    ValueOfTheCard(Player.card[1], Player.total)
    Player.card_value.append(Card.value)
    Player.total = sum(Player.card_value)
    print("Vous avez un total de :", Player.total)
    time.sleep(3)
    print("La premiere carte du croupier est :", Croupier.AIcard[0])
    time.sleep(3)
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

            i = random.randrange(len(Card.current))  # Tirage d'une carte
            # Ajout de la carte tirée dans la nouvelle main
            newCard.append(Card.current[i])
            # supprimer la carte tirée de la pioche
            Card.current.remove(newCard[len(newCard)-1])

            i = random.randrange(len(Card.current))  # Tirage d'une carte
            # Ajout de la carte tirée dans la nouvelle main
            Player.card.append(Card.current[i])
            # supprimer la carte tirée de la pioche
            Card.current.remove(Player.card[len(Player.card) - 1])

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

            Player.price = Player.price * 2

            print("Votre première main est :", newCard[0], "et", newCard[1],
                  ". Le total est donc de :", Player.newCard_Total)
            time.sleep(3)
            print("Votre seconde main est :",
                  Player.card[0], "et", Player.card[1], ". Le total est donc de :", Player.total)
            time.sleep(3)
            print("Vous misez donc le double :", Player.price, "$")
            time.sleep(3)
            print("Prenons votre premiere main :",
                  newCard[0], "et", newCard[1],)

            piocher_or_stop_for_split(Player.newCard_Total, newCard)

        elif answer == "1" and Player.card_value[0] != Player.card_value[1]:
            print("Vous ne pouvez pas split car il faut avoir les deux mêmes cartes")
            continue

        elif answer == "2":
            piocher_or_stop(Player.total, Player.card)

        elif answer == "3":
            i = random.randrange(len(Card.current))  # Tirage d'une carte
            # Ajout de la carte tirée dans la nouvelle main
            Player.card.append(Card.current[i])
            # supprimer la carte tirée de la pioche
            Card.current.remove(Player.card[len(Player.card) - 1])
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
            Player.price *= 2
            print("Votre mise est de :", Player.price)
            time.sleep(2)
            Player.can_play = False
            print("Votre tour est terminé, au tour du Croupier")
            time.sleep(2)
            croupier_Turn()

        elif answer == "4":
            print("Votre tour est terminé, au tour du Croupier")
            time.sleep(2)
            Player.can_play = False
            croupier_Turn()

        else:
            print("Erreur : vous devez ecrire soi : 1 / 2 / 3 / 4 sans espace")


def croupier_Turn():

    if Croupier.total != 21:
        print("La deuxieme carte du croupier est :", Croupier.AIcard[1])
        time.sleep(3)
        print("Le croupier a :", Croupier.AIcard, "pour un total de :",
              Croupier.total)
        time.sleep(3)

        if Player.newCard_Total != 0 and Croupier.total > Player.newCard_Total:  # j'ai split
            print(
                "Le croupier gagne par rapport a votre permier main, voyons pour votre deuxieme main !")
            time.sleep(3)
            if Croupier.total > Player.total or Player.total > 21:
                print("Croupier gagne, tu perds tous ton argent :",
                      Player.price, "$")
                time.sleep(3)
                print("Le croupier avait :", Croupier.AIcard, "pour un total de :",
                      Croupier.total)
                time.sleep(3)
                Player.money = 1000 - Player.price
                print("Il vous reste:", Player.money, "$")
                time.sleep(3)
            elif Croupier.total <= Player.total <= 21:
                draw_or_stop()

        elif Player.newCard_Total != 0 and Croupier.total < Player.newCard_Total:
            draw_or_stop()
            print("Le total des cartes du croupier est :", Croupier.total)
            print("Votre premiere main a pour total:", Player.newCard_Total)
            print("Votre deuxieme main a pour total:", Player.total)

            if Player.total < Croupier.total < 21 and Croupier.total > Player.newCard_Total:
                print(
                    "Le croupier gagne vous avez perdu vorte mise qui est de:", Player.price, "$")
                print("Le croupier avait :", Croupier.AIcard, "pour un total de :",
                      Croupier.total)
                Player.money = 1000 - Player.price
                print("Il vous reste:", Player.money, "$")
            elif Player.total < Croupier.total < Player.newCard_Total < 21\
                    or Player.newCard_Total < Croupier.total < Player.total < 21:
                print("Le croupier avait :", Croupier.AIcard, "pour un total de :",
                      Croupier.total)
                print("Le croupier gagne la moité des gains et vous aussi:", Player.price, "$", "/ 2 =",
                      Player.price / 2, "$")
                Player.money = 1000 - (Player.price/2)
                print("Il vous reste:", Player.money, "$")
            elif Croupier.total > 21 and Player.total > 21 and Player.newCard_Total > 21:
                print("Vous avez tous perdu! Vous récupérez votre mise:",
                      Player.price, "$")
                print("Le croupier avait :", Croupier.AIcard, "pour un total de :",
                      Croupier.total)
                Player.money = 1000
                print("Il vous reste:", Player.money, "$")

        # player a soi piocher ou doubler ou arreter
        elif Player.newCard_Total == 0 and 21 >= Player.total >= Croupier.total:
            draw_or_stop()
            if Player.total < Croupier.total < 21:
                print("Vous avez perdu votre mise:", Player.price, "$")
                print("Le croupier avait :", Croupier.AIcard, "pour un total de :",
                      Croupier.total)
                Player.money = 1000 - Player.price
                print("Il vous reste:", Player.money, "$")
            elif Croupier.total <= 21 and Player.total > 21:
                print("Vous avez perdu votre mise:", Player.price, "$")
                print("Le croupier avait :", Croupier.AIcard, "pour un total de :",
                      Croupier.total)
                Player.money = 1000 - Player.price
                print("Il vous reste:", Player.money, "$")
            elif Croupier.total < Player.total <= 21 or Croupier.total > 21 >= Player.total:
                print(
                    "Vous avez gagné ! Votre gains est de 2 x votre mise:", Player.price, "$")
                print("Le croupier avait :", Croupier.AIcard, "pour un total de :",
                      Croupier.total)
                Player.money = 1000 + Player.price
                print("Il vous reste:", Player.money, "$")
            elif Croupier.total > 21 and Player.total > 21:
                print("Vous avez tous perdu! Vous récupérez votre mise:",
                      Player.price, "$")
                print("Le croupier avait :", Croupier.AIcard, "pour un total de :",
                      Croupier.total)
                Player.money = 1000
                print("Il vous reste:", Player.money, "$")

        elif Player.newCard_Total == 0 and Player.total > 21:
            print("Vous avez perdu votre mise:", Player.price, "$")
            print("Le croupier avait :", Croupier.AIcard, "pour un total de :",
                  Croupier.total)
            Player.money = 1000 - Player.price
            print("Il vous reste:", Player.money, "$")

        elif Player.newCard_Total == 0 and 21 >= Player.total < Croupier.total:
            print("Vous avez perdu !")
            print("Le croupier avait :", Croupier.AIcard, "pour un total de :",
                  Croupier.total)
            print("Vous avez perdu votre mise:", Player.price, "$")
            Player.money = 1000 - Player.price
            print("Il vous reste:", Player.money, "$")

        elif Player.newCard_Total == 0 and Player.total == Croupier.total:
            print("Egalité vous récuperez votre mise! :", Player.price, "$")
            print("Le croupier avait :", Croupier.AIcard, "pour un total de :",
                  Croupier.total)
            Player.money = 1000
            print("Il vous reste:", Player.money, "$")

    Restart()


def draw_or_stop():
    list_value_cards = []

    for i in range(len(Card.current)):
        list_value_cards.append(ValueOfTheCard(
            Card.current[i], Croupier.total))

    count = 0
    nb_before_21 = 21 - Croupier.total

    for i in list_value_cards:
        if i <= nb_before_21:
            count += 1

    percentage_before_playing = (count * 100 / len(list_value_cards))
    Croupier.can_play = True

    while Croupier.can_play:

        if percentage_before_playing < 40:
            Croupier.can_play = False
        else:
            i = random.randrange(len(Card.current))  # Tirage d'une carte
            # Ajout de la carte tirée dans la nouvelle main
            Croupier.AIcard.append(Card.current[i])
            # supprimer la carte tirée de la pioche
            Card.current.remove(Croupier.AIcard[len(Croupier.AIcard) - 1])

            ValueOfTheCard(Croupier.AIcard[len(Croupier.AIcard) - 1], Croupier.total)
            Croupier.card_value.append(Card.value)
            Croupier.total = sum(Croupier.card_value)

            print("Le croupier a pioché la carte :", Croupier.AIcard[len(Croupier.AIcard) - 1])
            time.sleep(2)
            print("Ses cartes sont :", Croupier.AIcard)
            time.sleep(2)
            print("Le total de ses cartes est :", Croupier.total)
            time.sleep(2)

            draw_or_stop()


def piocher_or_stop(card_total, list_card):
    if card_total > 21:
        EndGame(card_total, list_card)
    else:
        i = random.randrange(len(Card.current))
        list_card.append(Card.current[i])
        last_card = len(list_card) - 1
        Card.current.remove(list_card[last_card])
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
                    print("Votre tour est terminer ! Regardons les cartes du croupier")
                    Player.can_play = False

                    time.sleep(3)

                    croupier_Turn()
                elif answer == "2":
                    i = random.randrange(len(Card.current))
                    list_card.append(Card.current[i])
                    last_card = len(list_card) - 1
                    Card.current.remove(list_card[last_card])
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
                print("Le croupier avait :", Croupier.AIcard[0], "et", Croupier.AIcard[1], "pour un total de :",
                      Croupier.total)
                Player.can_play = False
                time.sleep(2)
                print("Vous avez perdu votre mise:", Player.price, "$")
                Player.money = 1000 - Player.price
                time.sleep(2)
                print("Il vous reste:", Player.money, "$")
                GameOver()


def piocher_or_stop_for_split(card_total, list_card):
    if card_total > 21:
        EndGame(card_total, list_card)
    else:
        answer = input(
            "Que Voulez vous faire ? (Arreter/ Piocher) (Ecrivez : 1 / 2  :")

        if answer == "1" and list_card != Player.card:
            Player.newCard_Total = card_total
            print("Prenons votre deuxieme main :", Player.card)
            piocher_or_stop_for_split(Player.total, Player.card)
        elif answer == "1" and list_card == Player.card:
            print("Votre tour est terminer ! Regardons les cartes du croupier")
            time.sleep(2)
            Player.can_play = False
            croupier_Turn()

        elif answer == "2":
            i = random.randrange(len(Card.current))
            list_card.append(Card.current[i])
            last_card = len(list_card) - 1
            Card.current.remove(list_card[last_card])
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

            piocher_or_stop_for_split(card_total, list_card)


def EndGame(total, list_card):
    if list_card == Player.card:
        print("Dommage vous avez perdu!")
        croupier_Turn()
        time.sleep(2)
        print("Vous avez depassé 21, vous avez fait :", total, "et le croupier avait :",
              Croupier.AIcard, "pour un total de :", Croupier.total,)
        time.sleep(2)
        Player.can_play = False
    else:
        print("Dommage vous avez perdu!")
        time.sleep(2)
        print("Vous avez depassé 21, vous avez fait :", total)
        time.sleep(2)
        print("Prenons votre deuxieme main :", Player.card)
        time.sleep(2)
        piocher_or_stop_for_split(Player.total, Player.card)
        Player.can_play = False


Start_the_game()
