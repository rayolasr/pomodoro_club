import configparser
import counter


class Pomodoro:
    def __init__(self):
        print('Creating Pomodoro')

        # Leo archivo de coniguración
        config = configparser.ConfigParser()
        config.sections()
        config.read('config.ini')
        self.productionTime = int(config['POMODORO_DEFAULT']['productionTime'])
        self.distractionTime = int(config['POMODORO_DEFAULT']['distractionTime'])

        print(f'Pomodoro creado con tiempo de producción: {self.productionTime}segs y tiempo de distracción: {self.distractionTime}segs')

    #def start(self):
    #    print('Calling start_countdown')
    #    thecounter.start_countdown(productionTime)
    #    self.extend()
    #    pass

    #def jump_to_disctraction(self):
    #    pass

    #@staticmethod
    #def extend():
    #    thecounter.start_countup()