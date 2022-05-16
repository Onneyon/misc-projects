import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
from time import sleep

from cards import draw_card
from ui import Ui_window

card_pos = 0
player_score = 0
ai_score = 0

def draw_new_card(is_human):
    global card_pos, player_score, ai_score

    if card_pos == 9:
        ui.draw_button.setEnabled(False)
    elif card_pos > 9:
        return
    elif card_pos == 4 and is_human:
        ui.draw_button.setEnabled(False)
    elif is_human:
        ui.draw_button.setEnabled(True)
    else:
        ui.draw_button.setEnabled(False)
    
    new_card = draw_card()
    eval(f"ui.card_{card_pos}").setPixmap(QtGui.QPixmap(new_card.image))
    eval(f"ui.card_{card_pos}").setVisible(True)
    card_pos += 1

    if is_human:
        player_score += new_card.value
        score = player_score
    else:
        ai_score += new_card.value
        score = ai_score

    status_message = str(score)

    if score < 13 and card_pos < 5:
        ui.stick_button.setEnabled(False)
    elif score > 21:
        status_message += " - Bust!"

        if is_human:
            player_score = 0
            ai_play()
        else:
            ai_score = 0
    elif is_human:
        ui.stick_button.setEnabled(True)
    else:
        ui.stick_button.setEnabled(False)

    if is_human:
        ui.player_score_label.setText(status_message)
    else:
        ui.ai_score_label.setText(status_message)

def ai_play():
    global card_pos, ai_score

    ui.draw_button.setEnabled(False)
    ui.stick_button.setEnabled(False)

    card_pos = 5

    while ai_score < 15 and card_pos < 10:
        draw_new_card(False)

        if ai_score == 0:
            break
    
    ui.reset_button.setVisible(True)    

def reset_game():
    global card_pos, player_score, ai_score

    card_pos = 0
    player_score = 0
    ai_score = 0

    for x in range(10):
        eval(f"ui.card_{x}").setVisible(False)

    ui.player_score_label.setText("")
    ui.ai_score_label.setText("")

    ui.draw_button.setEnabled(True)
    ui.reset_button.setVisible(False)

    draw_new_card(True)
    draw_new_card(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_window()
    ui.setupUi(window)

    ui.draw_button.clicked.connect(partial(draw_new_card, True))
    ui.stick_button.clicked.connect(ai_play)
    ui.reset_button.clicked.connect(reset_game)

    draw_new_card(True)
    draw_new_card(True)

    window.show()
    sys.exit(app.exec_())
