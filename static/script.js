let score = 0;
let matrix = [];

function render() {
    $('#board').empty();
    matrix.forEach(row => {
        row.forEach(value => {
            const tile = $('<div class="tile"></div>');
            tile.text(value ? value : '');
            if (value) {
                tile.addClass('tile-' + value);
            }
            $('#board').append(tile);
        });
    });
    $('#score').text('Score: ' + score);
}

function newGame() {
    $.get('/new_game', function(data) {
        matrix = data.matrix;
        score = data.score;
        render();
    });
}

function move(direction) {
    $.get('/move/' + direction, function(data) {
        matrix = data.matrix;
        score = data.score;
        render();
    });
}

$(document).ready(function() {
    newGame();

    $(document).keydown(function(e) {
        switch (e.which) {
            case 37: // left arrow
                move('left');
                break;
            case 38: // up arrow
                move('up');
                break;
            case 39: // right arrow
                move('right');
                break;
            case 40: // down arrow
                move('down');
                break;
            default:
                return; // exit this handler for other keys
        }
        e.preventDefault(); // prevent the default action (scroll / move caret)
    });

    $('#newGame').click(newGame);
});

$(document).ready(function() {
    $('#playGame').click(function() {
        $('.menu-screen').hide();
        $('.game-container').show();
        // Khởi tạo trò chơi
    });

    $('#rank').click(function() {
        window.location.href = '/rank';  // Chuyển đến trang bảng xếp hạng
    });

    $('#quit').click(function() {
        window.close(); // Đóng cửa sổ hoặc quay lại menu chính
    });

    $('#backToMenu').click(function() {
        $('.game-container').hide();
        $('.menu-screen').show();
        // Reset game state if necessary
    });
});

