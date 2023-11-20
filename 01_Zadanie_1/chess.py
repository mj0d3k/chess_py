def show(chessboard):
    """Shows the chessboard in the console."""
    WHITE = {
        Pawn: chr(9817),
        Knight: chr(9816),
        Queen: chr(9813),
        King: chr(9812),
        Rook: chr(9814),
        Bishop: chr(9815),
    }
    BLACK = {
        Pawn: chr(9823),
        Knight: chr(9818),
        Queen: chr(9819),
        King: chr(9812),
        Rook: chr(9820),
        Bishop: chr(9821),
    }
    for y in range(7, -1, -1):
        print(y, end='\t')
        for x in range(8):
            if chessboard.board[x][y] is not None:
                if chessboard.board[x][y].color == 'white':
                    print(WHITE[type(chessboard.board[x][y])], end='\t')
                else:
                    print(BLACK[type(chessboard.board[x][y])], end='\t')
            else:
                print('\t', end='')
        print('\n')
    print('\t', end='')
    for x in range(8):
        print(x, end='\t')
    print()


class Chessboard:
    def __init__(self):
        self.color = 'white'
        # [None, ] * 8 =>  [None, None, None, None, None, None, None, None]
        self.board = [[None, ] * 8 for _ in range(8)]

    def setup(self):
        # Ustawianie pionków
        for i in range(8):
            # Ustawienie czarnych pionków na pozycjach [i, 6]
            self.board[i][6] = Pawn(color='black', x=i, y=6)
            # Ustawienie białych pionków na pozycjach [i, 1]
            self.board[i][1] = Pawn(color='white', x=i, y=1)

        # Ustawienie reszty figur
        # Białe
        self.board[0][0] = Rook('white', 0, 0)  # Wieża
        self.board[7][0] = Rook('white', 7, 0)
        self.board[1][0] = Knight('white', 1, 0)  # Skoczek
        self.board[6][0] = Knight('white', 6, 0)
        self.board[2][0] = Bishop('white', 2, 0)  # Goniec
        self.board[5][0] = Bishop('white', 5, 0)
        self.board[3][0] = Queen('white', 3, 0)  # Królowa
        self.board[4][0] = King('white', 4, 0)  # Król

        # Czarne
        self.board[0][7] = Rook('black', 0, 7)  # Wieża
        self.board[7][7] = Rook('black', 7, 7)
        self.board[1][7] = Knight('black', 1, 7)  # Skoczek
        self.board[6][7] = Knight('black', 6, 7)
        self.board[2][7] = Bishop('black', 2, 7)  # Goniec
        self.board[5][7] = Bishop('black', 5, 7)
        self.board[3][7] = Queen('black', 3, 7)  # Królowa
        self.board[4][7] = King('black', 4, 7)  # Król

    def list_allowed_moves(self, x, y):
        figure = self.board[x][y]  # Pobieramy figurę z planszy lub wartość pustą

        # Sprawdzamy, czy figura jest obiektem klasy ChessPiece i czy jej kolor odpowiada kolorowi obecnego gracza
        if isinstance(figure, ChessPiece) and self.color == figure.color:  #fig.c nie czaje do konca
            # Jeśli figura jest figurą szachową, wywołujemy jej metodę list_allowed_moves, aby uzyskać listę dozwolonych ruchów
            allowed_moves = figure.list_allowed_moves(self)
            # Zwracamy listę dozwolonych ruchów dla wcześniej pobranej figury z planszy
            return allowed_moves

        return None

    def check_if_king_killed(self, chess_piece):
        # Sprawdzamy, czy przekazana figura jest królem i czy jej kolor różni się od koloru obecnego gracza
        return isinstance(chess_piece, King) and chess_piece.color != self.color

    def move(self, from_x, from_y, to_x, to_y):
        allowed_moves = self.list_allowed_moves(from_x, from_y)
        if allowed_moves is None:
            raise ValueError('wrong move')
        if (to_x, to_y) in allowed_moves:
            figure = self.board[from_x][from_y]
            figure.move(to_x, to_y)
            if self.check_if_king_killed(chess_piece=self.board[to_x][to_y]):
                # Jeśli król został zabity, zwracamy odpowiednią informację o zwycięstwie
                return 'WHITE WON' if self.color == 'white' else 'BLACK WON'
            self.board[to_x][to_y] = figure
            self.board[from_x][from_y] = None
            self.color = 'black' if self.color == 'white' else 'white'
        else:
            raise ValueError('wrong move')


class ChessPiece:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y

    def move(self, x, y):
        self.x = x
        self.y = y

    def list_allowed_moves(self, chessboard):
        return []

    def get_and_check_coordinates(self, chessboard, x, y):
        chessboard_square = chessboard.board[x][y]
        if chessboard_square is None:
            # Jeśli pole na planszy jest puste, zwracamy współrzędne (x, y) oraz wartość logiczną False
            return (x, y), False
        elif chessboard_square.color != self.color:
            # Jeśli pole na planszy zawiera figurę przeciwnika, zwracamy współrzędne (x, y) oraz wartość logiczną True
            return (x, y), True
        else:
            # Jeśli pole na planszy zawiera figurę należącą do aktualnego gracza, zwracamy wartość None dla współrzędnych i None dla wartości logicznej
            return None, None

    def _get_diagonal_moves(self, chessboard):
        allowed_moves = []
        directions = [(1, 1), (-1, 1), (-1, -1), (1, -1)]  # Kierunki: góra-prawo, dół-prawo, dół-lewo, góra-lewo

        for dx, dy in directions:
            for i in range(1, 8):
                x = self.x + dx * i
                y = self.y + dy * i

                if 0 <= x < 8 and 0 <= y < 8:  # Sprawdzamy, czy nowe współrzędne są w zakresie planszy
                    checked_coordinates, break_loop = self.get_and_check_coordinates(chessboard, x, y)
                    if checked_coordinates is not None:
                        allowed_moves.append(checked_coordinates)
                    if break_loop or checked_coordinates is None:
                        break  # Przerywamy pętlę jeśli napotkano przeszkodę lub wykraczamy poza planszę
                else:
                    break  # Przerywamy pętlę jeśli wykraczamy poza zakres planszy

        return allowed_moves

    def _get_horizontal_and_vertical_moves(self, chessboard):
        allowed_moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Kierunki: prawo, lewo, góra, dół

        for dx, dy in directions:
            for i in range(1, 8):
                x = self.x + dx * i
                y = self.y + dy * i

                if 0 <= x < 8 and 0 <= y < 8:  # Sprawdzamy, czy nowe współrzędne są w zakresie planszy
                    checked_coordinates, break_look = self.get_and_check_coordinates(chessboard, x, y)
                    if checked_coordinates is not None:
                        allowed_moves.append(checked_coordinates)
                    if break_look or checked_coordinates is None:
                        break  # Przerywamy pętlę jeśli napotkano przeszkodę lub wykraczamy poza planszę
                else:
                    break  # Przerywamy pętlę jeśli wykraczamy poza zakres planszy

        return allowed_moves


class Pawn(ChessPiece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.moved = False  # Flaga informująca czy pionek się ruszył w grze

    def check_figures_on_board(self, chessboard, allowed_moves):
        move_by_one = allowed_moves[0]
        front = chessboard.board[move_by_one[0]][move_by_one[1]]

        # Sprawdzanie czy pole przed pionkiem jest zajęte przez figurę tego samego koloru
        if front is not None and front.color == self.color:
            allowed_moves = []

        # Sprawdzanie czy pionek nie został wcześniej przesunięty oraz czy ruch o dwie pozycje w przód jest możliwy
        if not self.moved and allowed_moves != []:
            move_by_two = allowed_moves[1]
            front = chessboard.board[move_by_two[0]][move_by_two[1]]

            # Sprawdzanie czy pole przed pionkiem na odległość dwóch pozycji jest zajęte przez figurę tego samego koloru
            if front is not None and front.color == self.color:
                allowed_moves = allowed_moves[:1]

        # Sprawdzanie skosów pionka
        side_moves = []
        if self.color == 'white':
            left_side_move = (self.x + 1, self.y + 1)
            right_side_move = (self.x - 1, self.y + 1)
        elif self.color == 'black':
            left_side_move = (self.x + 1, self.y - 1)
            right_side_move = (self.x - 1, self.y - 1)
        right_side = chessboard.board[right_side_move[0]][right_side_move[1]]
        left_side = chessboard.board[left_side_move[0]][left_side_move[1]]

        # Sprawdzanie czy pola na skos od pionka są zajęte przez figury przeciwnego koloru
        if left_side is not None and left_side.color != self.color:
            side_moves.append(left_side_move)
        if right_side is not None and right_side.color != self.color:
            side_moves.append(right_side_move)

        return allowed_moves + side_moves

    def list_allowed_moves(self, chessboard):
        if self.y + 1 >= 8 or self.y - 1 < 0:  # Kiedy pionek jest na skraju planszy zwracamy pustą listę
            return []

        allowed_moves = []
        # Przygotowanie potencjalnych ruchów
        if self.moved:  # Pionek ruszył się w grze
            if self.color == 'white':
                allowed_moves = [(self.x, self.y + 1)]
            elif self.color == 'black':
                allowed_moves = [(self.x, self.y - 1)]

        else:  # Pionek nie ruszył się w grze
            if self.color == 'white':
                allowed_moves = [(self.x, self.y + 1), (self.x, self.y + 2)]
            elif self.color == 'black':
                allowed_moves = [(self.x, self.y - 1), (self.x, self.y - 2)]
        allowed_moves = self.check_figures_on_board(chessboard, allowed_moves)
        return allowed_moves

    def move(self, x, y):
        super().move(x, y)
        self.moved = True


class Knight(ChessPiece):
    def list_allowed_moves(self, chessboard):
        # Lista wszystkich potencjalnych ruchów skoczka
        all_moves = [
            (self.x + 2, self.y + 1), (self.x + 2, self.y - 1), (self.x - 2, self.y + 1), (self.x - 2, self.y - 1),
            (self.x - 1, self.y + 2), (self.x + 1, self.y + 2), (self.x - 1, self.y - 2), (self.x + 1, self.y - 2),
        ]
        # Lista do przechowywania dozwolonych ruchów
        allowed_moves = []
        # Iteracja przez wszystkie potencjalne ruchy
        for move in all_moves:
            x, y = move
            # Sprawdzenie, czy ruch mieści się na planszy
            if 0 <= x < 8 and 0 <= y < 8:
                # Sprawdzenie, czy ruch jest dozwolony (czy na docelowym polu nie ma figury o tym samym kolorze)
                checked_coordinates, _ = self.get_and_check_coordinates(chessboard, x, y)
                if checked_coordinates is not None:
                    allowed_moves.append(move)
        # Zwrócenie listy dozwolonych ruchów
        return allowed_moves


class Rook(ChessPiece):
    def list_allowed_moves(self, chessboard):
        return self._get_horizontal_and_vertical_moves(chessboard)


class King(ChessPiece):
    def list_allowed_moves(self, chessboard):
        # Wszystkie możliwe ruchy króla w górę, dół, na skos i w poziomie
        all_moves = [
            (self.x, self.y + 1), (self.x, self.y - 1), (self.x + 1, self.y + 1), (self.x + 1, self.y - 1),
            (self.x - 1, self.y + 1), (self.x - 1, self.y - 1), (self.x - 1, self.y), (self.x + 1, self.y),
        ]
        allowed_moves = []

        # Sprawdzanie każdego potencjalnego ruchu
        for move in all_moves:
            x, y = move
            # Sprawdzanie czy ruch jest w zakresie planszy
            if 0 <= x < 8 and 0 <= y < 8:
                checked_coordinates, _ = self.get_and_check_coordinates(chessboard, x, y)
                # Sprawdzanie czy ruch nie koliduje z innymi figurami
                if checked_coordinates is not None:
                    allowed_moves.append(move)

        return allowed_moves


class Bishop(ChessPiece):
    def list_allowed_moves(self, chessboard):
        return self._get_diagonal_moves(chessboard)


class Queen(ChessPiece):
    def list_allowed_moves(self, chessboard):
        diagonal_moves = self._get_diagonal_moves(chessboard)
        horizontal_and_vertical_moves = self._get_horizontal_and_vertical_moves(chessboard)
        return diagonal_moves + horizontal_and_vertical_moves


chessboard = Chessboard()
chessboard.setup()
show(chessboard)

cb = Chessboard()
p = Pawn("black", 4, 2)
k2 = Knight("black", 7, 7)
print(p.list_allowed_moves(cb))

