import menu
import game
from utils import sleep



def main():
    StartButtons=['play','pvp','aram','confirm','find']
    LoopButtons=['play','find']
    menu.LaunchGame(StartButtons)
    game.PlayGame()
    while True:
        menu.LaunchGame(LoopButtons)
        sleep(40)
        game.PlayGame()


if __name__ == '__main__':
    main()