import menu
import game



def main():
    StartButtons=['play','pvp','aram','confirm','find']
    LoopButtons=['play','find']
    menu.LaunchGame(StartButtons)
    game.PlayGame()
    while True:
        menu.LaunchGame(LoopButtons)
        game.PlayGame()


if __name__ == '__main__':
    main()