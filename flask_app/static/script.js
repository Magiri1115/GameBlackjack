function startGame() {
    fetch('/start_game').then(response => response.json()).then(data => {
        document.getElementById('playerCards').textContent = data.player_cards.join(', ');
        document.getElementById('dealerCards').textContent = data.dealer_cards.join(', ');
    });
}

function hit() {
    fetch('/hit').then(response => response.json()).then(data => {
        document.getElementById('playerCards').textContent = data.player_cards.join(', ');
        if (data.result) {
            document.getElementById('gameResult').textContent = data.result;
        }
    });
}

function stand() {
    fetch('/stand').then(response => response.json()).then(data => {
        document.getElementById('dealerCards').textContent = data.dealer_cards.join(', ');
        if (data.result) {
            document.getElementById('gameResult').textContent = data.result;
        }
    });
}
