from flask import Flask, render_template, request, session, jsonify , redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッション管理に使われる秘密鍵
'''
Game関数の定義
'''
class Game:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

    def deal_initial_cards(self):
        for _ in range(2):
            self.player_hand.add_card(self.deck.deal())
            self.dealer_hand.add_card(self.deck.deal())

    def hit(self, hand):
        hand.add_card(self.deck.deal())
        hand.adjust_for_ace()

    def player_busts(self):
        return self.player_hand.value > 21

    def dealer_busts(self):
        return self.dealer_hand.value > 21

    def player_wins(self):
        return self.player_hand.value > self.dealer_hand.value and not self.player_busts()

    def dealer_wins(self):
        return self.dealer_hand.value > self.player_hand.value and not self.dealer_busts()

    def push(self):
        return self.player_hand.value == self.dealer_hand.value

    def show_some(self):
        print("\nDealer's Hand:")
        print(" <card hidden>")
        print('', self.dealer_hand.cards[1])
        print("\nPlayer's Hand:", *self.player_hand.cards, sep='\n ')

    def show_all(self):
        print("\nDealer's Hand:", *self.dealer_hand.cards, sep='\n ')
        print("Dealer's Hand =", self.dealer_hand.value)
        print("\nPlayer's Hand:", *self.player_hand.cards, sep='\n ')
        print("Player's Hand =", self.player_hand.value)
import random

# カードのデッキ
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

# カードの値
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
          '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

'''
以下バックエンド上のプログラム
'''
@app.route('/start_game', methods=['POST'])
def start_game():
    # ゲームの初期化と最初のカード配布を行う
    # 例えば、Gameクラスを使ってゲームを初期化し、プレイヤーとディーラーの最初のカードを取得する
    game = Game()
    game.deal_initial_cards()
    player_cards = [str(card) for card in game.player_hand.cards]
    dealer_cards = [str(card) for card in game.dealer_hand.cards]
    return jsonify({
        'player_cards': player_cards,
        'dealer_cards': dealer_cards
    })

@app.route('/hit', methods=['POST'])
def hit():
    # プレイヤーにカードを配る
    # ゲームインスタンスを取得し、プレイヤーにカードを配り、ゲームの状態を更新する
    game = get_current_game_from_session()  # ゲームの状態をセッションから取得する関数
    game.hit(game.player_hand)
    player_cards = [str(card) for card in game.player_hand.cards]
    return jsonify({
        'player_cards': player_cards
    })

@app.route('/stand', methods=['POST'])
def stand():
    # プレイヤーがスタンドした場合、ディーラーの手番に移行する
    # ゲームインスタンスを取得し、ディーラーの手番を実行し、ゲームの結果を取得する
    game = get_current_game_from_session()  # ゲームの状態をセッションから取得する関数
    while game.dealer_hand.value < 17:
        game.hit(game.dealer_hand)
    dealer_cards = [str(card) for card in game.dealer_hand.cards]
    # ゲームの結果を判定して返す
    result = determine_game_result(game)
    return jsonify({
        'dealer_cards': dealer_cards,
        'result': result
    })
# ゲームの状態をセッションから取得する関数
def get_current_game_from_session():
    if 'game' not in session:
        session['game'] = Game()
    return session['game']

# ゲームの結果を判定する関数
def determine_game_result(game):
    if game.player_busts():
        return "Player busts! Dealer wins."
    elif game.dealer_busts() or game.player_wins():
        return "Player wins!"
    elif game.dealer_wins():
        return "Dealer wins!"
    else:
        return "It's a tie!"
