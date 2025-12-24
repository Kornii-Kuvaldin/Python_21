import os

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, \
    QGridLayout, QGroupBox, QMessageBox
from PyQt6.QtCore import Qt
import sys


# Bruno Kennedy Lisboa de Queiroz - 3141551
# Kornii Kulvaldin -3134926

# all the references comes from the library documentation https://doc.qt.io/qt-6/qwidget.html

# this project should use a modular approach - try to keep UI logic and game logic separate
from game_logic import Game21


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.playerCardsLayout = QHBoxLayout()
        self.setWindowTitle("Game of 21")

        # set the windows dimensions and bascis strucute to run the game
        self.resize(1200, 800)


        self.game = Game21()

        self.wins = 0
        self.losses = 0
        self.pushes = 0

        self.ui_font_size = 16
        self.high_contrast = False

        self.initUI()
        self.apply_theme()

    def initUI(self):
        # the main Layout

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        main = QGridLayout()
        centralWidget.setLayout(main)

        # Group 1: Dealer Cards
        dealerCardsBox = QGroupBox("Dealer Cards")
        self.dealerCardsLayout = QHBoxLayout()
        self.dealerCardsLayout.setSpacing(15)
        dealerCardsBox.setLayout(self.dealerCardsLayout)

        # Group 2: Dealer Info
        dealerInfoBox = QGroupBox("Dealer Info")
        dealerInfoLayout = QVBoxLayout()
        dealerInfoBox.setLayout(dealerInfoLayout)

        self.d_score_label = QLabel("Total: ?")
        self.d_score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.d_score_label.setStyleSheet("""
            font-size: 26px;
            font-weight: 800;
        """)
        dealerInfoLayout.addWidget(self.d_score_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Group 3: Player Cards
        playerCardsBox = QGroupBox("Player Cards")
        self.playerCardsLayout = QHBoxLayout()
        self.playerCardsLayout.setSpacing(15)
        playerCardsBox.setLayout(self.playerCardsLayout)

        # Group 4: Controls / Result
        controlsBox = QGroupBox("Controls")
        controlsLayout = QVBoxLayout()
        controlsBox.setLayout(controlsLayout)

        self.p_total_label = QLabel("Total: 0")
        self.p_total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.p_total_label.setStyleSheet("""
            font-size: 26px;
            font-weight: 800;
        """)

        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("""
            font-size: 22px;
            font-weight: 700;
        """)
        controlsLayout.addWidget(self.result_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.button_hit = QPushButton("Hit")
        self.button_hit.clicked.connect(self.on_hit)

        self.button_stand = QPushButton("Stand")
        self.button_stand.clicked.connect(self.on_stand)

        self.button_newRound = QPushButton("New Round")
        self.button_newRound.clicked.connect(self.on_new_round)

        buttonRow = QHBoxLayout()
        buttonRow.addWidget(self.button_newRound)
        buttonRow.addWidget(self.button_stand)
        buttonRow.addWidget(self.button_hit)
        controlsLayout.addLayout(buttonRow)

        # Printin the 4 boxes in a 2x2 grid
        main.addWidget(dealerCardsBox, 0, 0)
        main.addWidget(dealerInfoBox, 0, 1)
        main.addWidget(playerCardsBox, 1, 0)
        main.addWidget(controlsBox, 1, 1)

        # control how much space each column/row gets
        main.setColumnStretch(0, 3)  # cards area wider
        main.setColumnStretch(1, 1)  # info/controls narrower
        main.setRowStretch(0, 1)
        main.setRowStretch(1, 1)

        # Card image configuration and direction file from assets
        self.card_pixmaps = {}
        self.cards_dir = os.path.join(os.path.dirname(__file__), "assets")
        self.card_size = (140, 200)
        self.button_hit.setObjectName("hitButton")
        self.button_stand.setObjectName("standButton")
        self.button_newRound.setObjectName("newRoundButton")

        #Button restart game
        self.button_restart = QPushButton("Restart Game")
        self.button_restart.clicked.connect(self.on_restart_game)
        self.button_restart.setObjectName("restartButton")

        buttonRow.addWidget(self.button_restart)

        #Winners and Losers Information
        self.stats_label = QLabel("Winners: 0  Losses: 0  Pushes: 0")
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controlsLayout.addWidget(self.stats_label, alignment=Qt.AlignmentFlag.AlignCenter) #control style layour of the game

        self.new_round_setup()
        controlsLayout.addWidget(self.p_total_label, alignment=Qt.AlignmentFlag.AlignCenter) # control style layout of game

    # BUTTON ACTIONS
    # Method to label the Infor
    def update_stats_label(self):
        self.stats_label.setText(f"Winners: {self.wins}  Losses: {self.losses}  Pushes: {self.pushes}")
    #method to get values
    def reset_statistics(self):
        self.wins = 0
        self.losses = 0
        self.pushes = 0
        self.update_stats_label()


    #method to hit values
    def on_hit(self):
        # Player takes a card
        card = self.game.player_hit()
        self.add_card(self.playerCardsLayout, card)
        # Hand total update
        total = self.game.player_total()
        self.p_total_label.setText(str(total))

        if self.game.player_total() > 21:
            self.end_round()



    #method to stand values dealers
    def on_stand(self):
        # Shows dealer's cards
        self.game.reveal_dealer_card()
        # Dealer draws to 17


        self.game.play_dealer_turn()
        # Shows dealer's cards
        self.update_dealer_cards(full=True)
        self.end_round()

    #method to select new round
    def on_new_round(self):
        self.game.new_round()
        self.new_round_setup()

    # HELPER METHODS

    #action of animation from layour
    def clear_layout(self, layout):
        # Remove all widgets from a layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    #method to add new card from the value
    def add_card(self, layout, card_code: str, face_down: bool = False):
        label = QLabel()
        code = "BACK" if face_down else card_code

        pix = self.get_card_pixmap(code)

        w, h = self.card_size
        pix = pix.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        label.setPixmap(pix)
        label.setProperty("card", True)
        layout.addWidget(label)

    #update the information from dealer
    def update_dealer_cards(self, full=False):
        # Show dealer cards; hide the first card until revealed
        self.clear_layout(self.dealerCardsLayout)

        for i, card in enumerate(self.game.dealer_hand):
            if i == 0 and not full:
                self.add_card(self.dealerCardsLayout, card, face_down=True)
            else:
                self.add_card(self.dealerCardsLayout, card, face_down=False)


        # full is true when the round is complete and the cards are shown
        if full:
            self.d_score_label.setText(f"Total: {self.game.dealer_total()}")
        else:
            self.d_score_label.setText(f"Total: ?")

    def new_round_setup(self):
        #method to setup new round getting labels
        self.clear_layout(self.dealerCardsLayout)
        self.clear_layout(self.playerCardsLayout)
        self.result_label.setText("")



      #start from deal

        self.game.deal_initial_cards()
        # Player
        # Visual update to display player's hand
        for card in self.game.player_hand:
            self.add_card(self.playerCardsLayout, card)
        # Dealer
        self.update_dealer_cards(full=False)

        # enable buttons for Stand and Hit - Remove pass when complete
        self.button_hit.setEnabled(True)
        self.button_stand.setEnabled(True)
        self.button_newRound.setEnabled(False)

    def end_round(self):

        #method to finish the round and clear the layout
        self.button_newRound.setEnabled(True)
        self.button_hit.setEnabled(False)
        self.button_stand.setEnabled(False)

        winnermessage = self.game.decide_winner()
        self.result_label.setText(winnermessage)

        msg = winnermessage.lower()
        if "player won" in msg or "dealer bust" in msg:
            self.wins += 1
        elif "dealer won" in msg or "player bust" in msg:
            self.losses += 1
        elif "draw" in msg:
            self.pushes += 1

        self.update_stats_label()

    def get_card_pixmap(self, card_code: str) -> QPixmap:
        """
        card_code: 'AS', '10H', ... or 'BACK'
        expects files like cards/AS.png and cards/back.png
        """
        filename = "back.png" if card_code == "BACK" else f"{card_code}.png"
        path = os.path.join(self.cards_dir, filename)

        if filename not in self.card_pixmaps:
            pix = QPixmap(path)
            if pix.isNull():
                raise FileNotFoundError(f"Could not load image: {path}")
            self.card_pixmaps[filename] = pix

        return self.card_pixmaps[filename]

    def on_restart_game(self):
        #similuar function to erase the layour but using the button reset for the player get the info
        msg = QMessageBox(self)
        msg.setWindowTitle("Restart Game")
        msg.setText("Restart the game?")
        msg.setInformativeText("This will reset the current round and clear statistics.")
        msg.setIcon(QMessageBox.Icon.Question)

        yes_btn = msg.addButton("Restart", QMessageBox.ButtonRole.AcceptRole)
        msg.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)

        msg.exec()

        if msg.clickedButton() == yes_btn:
            self.reset_statistics()
            self.game.new_round()
            self.new_round_setup()


        #one of the most important method for desing game, here we could implement the entire structure to make the game similar a real game table
        #using all desing of card and buttons to simulate a table of game
    def apply_theme(self):
        self.setStyleSheet("""
            /* Base */
            QMainWindow, QWidget {
                background-color: #0B1F17;
                color: #EAF2EE;
                font-size: 16px;
            }

            QLabel {
                color: #EAF2EE;
            }

            /* Group boxes */
            QGroupBox {
                background-color: #102A21;
                border: 1px solid #1F3A31;
                border-radius: 12px;
                margin-top: 10px;
                padding: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                color: #2DD4BF;
                font-weight: 600;
            }

            /* Buttons (default) */
            QPushButton {
                background-color: #1F3A31;
                color: #EAF2EE;
                border: 1px solid #2A4B40;
                border-radius: 10px;
                padding: 10px 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #275044;
            }
            QPushButton:pressed {
                background-color: #1B3A31;
            }
            QPushButton:disabled {
                background-color: #142C24;
                color: #7FA195;
                border-color: #1B3A31;
            }

            /* Card labels: remove borders/margins if you want tighter rows */
            QLabel[card="true"] {
                background: transparent;
                padding: 0px;
                margin: 0px;
            }
            
                    /* Specific buttons */
        QPushButton#hitButton {
            background-color: #22C55E;
            color: #06210F;
            border-color: #16A34A;
        }
        QPushButton#hitButton:hover { background-color: #34D399; }
        QPushButton#hitButton:disabled { background-color: #12301F; color: #7FA195; border-color: #12301F; }

        QPushButton#standButton {
            background-color: #F59E0B;
            color: #2A1600;
            border-color: #D97706;
        }
        QPushButton#standButton:hover { background-color: #FBBF24; }
        QPushButton#standButton:disabled { background-color: #2B220F; color: #A89B7A; border-color: #2B220F; }

        QPushButton#newRoundButton {
            background-color: #3B82F6;
            color: #07162E;
            border-color: #2563EB;
        }
        QPushButton#newRoundButton:hover { background-color: #60A5FA; }
        QPushButton#newRoundButton:disabled { background-color: #14233A; color: #7D94B3; border-color: #14233A; }
        /* Group boxes (container) */
QGroupBox {
    background-color: #102A21;
    border: 1px solid #1F3A31;
    border-radius: 14px;
    margin-top: 28px;      /* space for the title pill */
    padding: 16px;
}

/* Button-style title */
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;

    background-color: #1F3A31;   /* same family as buttons */
    color: #EAF2EE;

    border: 1px solid #2DD4BF;
    border-radius: 10px;

    padding: 6px 14px;
    margin-left: 12px;

    font-weight: 700;
    font-size: 14px;
}

QPushButton#restartButton:hover {
    background-color: #E20303;
}

        """)


# complete

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # macOS only fix for icons appearing
    app.setAttribute(Qt.ApplicationAttribute.AA_DontShowIconsInMenus, False)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
