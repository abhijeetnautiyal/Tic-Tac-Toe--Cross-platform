from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.modalview import ModalView
from kivy.lang import Builder

from kivy.uix.button import Button

from kivy.properties import ListProperty, NumericProperty

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

import time
import random
import random


class MenuScreen(Screen):
    pass


class GameScreen(Screen):
    pass


class SelectDifficultyScreen(Screen):
    pass


class EasyDifficultyScreen(Screen):
    pass


class HardDifficultyScreen(Screen):
    pass






class GridEntry(Button):
    coords = ListProperty([0, 0])


class GameGrid(GridLayout):
    status = ListProperty([0, 0, 0, 0, 0, 0, 0, 0, 0])
    current_player = NumericProperty(1)

    def __init__(self, *args, **kwargs):
        super(GameGrid, self).__init__(*args, **kwargs)
        for row in range(3):
            for column in range(3):
                grid_entry = GridEntry(coords=(row, column))
                grid_entry.bind(on_release=self.button_pressed)
                self.add_widget(grid_entry)

    def button_pressed(self, button):
        # player roles
        player = {1: 'O', -1: 'X'}
        colours = {1: (1, 0, 0, 1), -1: (0, 1, 0, 1)}

        row, column = button.coords

        # save 2d coords as status 1d list
        status_index = 3*row + column
        # already filled the box
        already_played = self.status[status_index]

        if not already_played:
            self.status[status_index] = self.current_player
            # display x / o accordingly
            button.text = player[self.current_player]

            # set color red/green
            button.background_color = colours[self.current_player]

            self.current_player *= -1 # alternate bw players

    def on_status(self, instance, new_value):
        status = new_value

        sums = [sum(status[0:3]), sum(status[3:6]), sum(status[6:9]), # rows
                sum(status[0::3]), sum(status[1::3]), sum(status[2::3]),#every third elemnt satring from 0,3,6= columns
                sum(status[::4]), sum(status[2:-2:2])]#diagonals
        """
                if 3 in sums:
            #print "Os wins!!!"
        elif -3 in sums:
            #print "Xs wins!!!"
        elif 0 not in self.status:
            #print 'Draw!!!'

        """

        winner = None
        if -3 in sums:
            winner = "Xs wins!"
        elif 3 in sums:
            winner = 'Os wins!'
        elif 0 not in self.status:
            winner = 'Draw....nobody wins!'

        if winner:
            popup = ModalView(size_hint=(0.75, 0.5))
            victory_label = Label(text=winner, font_size= 50)
            popup.add_widget(victory_label)
            popup.bind(on_dismiss=self.reset)
            popup.open()

    def reset(self, *args):
        self.status = [0 for _ in range(9)]

        for child in self.children:
            child.text = ''
            child.background_color = (1, 1, 1, 1,)

        self.current_player = 1


class GameGridEasy(GridLayout):
    status = ListProperty([0, 0, 0, 0, 0, 0, 0, 0, 0])
    current_player = NumericProperty(1)
    index_already_played = []
    possible_status_index = range(9)

    def __init__(self, *args, **kwargs):
        super(GameGridEasy, self).__init__(*args, **kwargs)
        for row in range(3):
            for column in range(3):
                grid_entry = GridEntry(coords=(row, column))
                self.ids[str(3*row + column)] = grid_entry
                grid_entry.bind(on_release=self.button_pressed)
                self.add_widget(grid_entry)

    def button_pressed(self, button):
        colours = {1: (1, 0, 0, 1), -1: (0, 1, 0, 1)}

        row, column = button.coords

        # save 2d coords as status 1d list
        status_index = 3*row + column

        # already filled the box
        already_played = self.status[status_index]

        if not already_played:
            self.index_already_played.append(status_index)
            self.status[status_index] = 1
            # display x / o accordingly
            button.text = 'O'

            # set color red/green
            button.background_color = colours[1]
            #####cpus turn
            ###only after players
            """
            available_choices = list( set(self.possible_status_index)-set(self.index_already_played) )
            #print self.possible_status_index
            #print self.index_already_played
            #print available_choices
            """
            available_choices = []
            for i in range(len(self.status)):
                if self.status[i] == 0:
                    available_choices.append(i)
            if available_choices:
                cpu_move_index = random.choice(available_choices)
                self.index_already_played.append(cpu_move_index)

                self.status[cpu_move_index] = -1
                ##print [(x, x.id) for x in self.walk()]
                ##print self.ids
                cpu_button = self.ids[str(cpu_move_index)]

                cpu_button.text = 'X'
                cpu_button.background_color = colours[-1]


    def on_status(self, instance, new_value):
        status = new_value

        sums = [sum(status[0:3]), sum(status[3:6]), sum(status[6:9]), # columns
                sum(status[0::3]), sum(status[1::3]), sum(status[2::3]),#every third elemnt satring from 0,3,6= columns
                sum(status[::4]), sum(status[2:-2:2])]

        winner = None
        if -3 in sums:
            winner = "Cpu wins!"
        elif 3 in sums:
            winner = 'You win!'
        elif 0 not in self.status:
            winner = 'Draw....nobody wins!'

        if winner:
            popup = ModalView(size_hint=(0.75, 0.5))
            victory_label = Label(text=winner, font_size=50)
            popup.add_widget(victory_label)
            popup.bind(on_dismiss=self.reset)
            popup.open()

    def reset(self, *args):
        self.status = [0 for _ in range(9)]
        self.index_already_played = []
        for child in self.children:
            child.text = ''
            child.background_color = (1, 1, 1, 1,)

        self.current_player = 1


class GameGridHard(GridLayout):
    status = ListProperty([0, 0, 0, 0, 0, 0, 0, 0, 0])
    current_player = NumericProperty(1)
    index_already_played = []
    possible_status_index = range(9)

    def __init__(self, *args, **kwargs):
        super(GameGridHard, self).__init__(*args, **kwargs)
        for row in range(3):
            for column in range(3):
                grid_entry = GridEntry(coords=(row, column))
                self.ids[str(3*row + column)] = grid_entry
                grid_entry.bind(on_release=self.button_pressed)
                self.add_widget(grid_entry)
        #init with first cpu move
        self.ids['7'].text = 'X'
        self.ids['7'].background_color = (0, 1, 0, 1)
        self.status[7] = -1

    def button_pressed(self, button):
        colours = {1: (1, 0, 0, 1), -1: (0, 1, 0, 1)}

        row, column = button.coords

        # save 2d coords as status 1d list
        status_index = 3*row + column

        # already filled the box
        already_played = self.status[status_index]
        
        


        
        
        #################

        if not already_played:
            self.index_already_played.append(status_index)
            self.status[status_index] = 1
            # display x / o accordingly
            button.text = 'O'

            # set color red/green
            button.background_color = colours[1]

            #################################

            #####cpus turn
            ###only after players
            """
            available_choices = list( set(self.possible_status_index)-set(self.index_already_played) )
            #print self.possible_status_index
            #print self.index_already_played
            #print available_choices
            """
            ######cpu move
            stopping_the_player = False
            trying_to_win = False
            all_possible_lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                                  [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

            ###check if player is winning
            ### or if there is a chance for cpu to win
            cpu_move_index = None
            win_move = None
            stop_move = None
            random_move = None
            strategic_move = None

            for line in all_possible_lines:
                if trying_to_win:
                    break
                x, y, z = self.status[line[0]], self.status[line[1]], self.status[line[2]]

                if x + y + z == -2:
                    ##print  "trying to win"
                    trying_to_win = True
                    if x == 0:
                        win_move = line[0]
                    elif y == 0:
                        win_move = line[1]
                    elif z == 0:
                        win_move = line[2]

            for line in all_possible_lines:
                if stopping_the_player:
                    break
                x, y, z = self.status[line[0]], self.status[line[1]], self.status[line[2]]


                if x + y + z == 2:
                    stopping_the_player = True
                    ##print "Stopping the player"
                    if x == 0:
                        stop_move = line[0]
                    elif y == 0:
                        stop_move = line[1]
                    elif z == 0:
                        stop_move = line[2]



            if not stopping_the_player and not trying_to_win:
                ##print "just random"
                available_choices = []
                for i in range(len(self.status)):
                    if self.status[i] == 0:
                        available_choices.append(i)
                        #print available_choices
                if available_choices:
                    random_move = random.choice(available_choices)


            ############strategic move

            no_of_moves = self.status.count(-1)
            #print "yo", no_of_moves
            if no_of_moves == 1:
                if self.status[0] == 0:
                    strategic_move = 0
                else:
                    strategic_move = 2

            if no_of_moves == 2:
                possible_moves = [6, 4, 8]
                for e in possible_moves:
                    if self.status[e] == 0:
                        strategic_move = e
                        break




            ##################################
            """
            if not trying_to_win and not stopping_the_player:
                if strategic_move:
                    cpu_move_index = strategic_move
                    #print "strategic move",cpu_move_index
                else:
                    cpu_move_index = random_move
                    #print "Random", cpu_move_index
            else:

                if win_move:
                    cpu_move_index = win_move
                    #print "trying to win",cpu_move_index
                elif stop_move:
                    cpu_move_index = stop_move
                    #print "Stopping the player",cpu_move_index

            """

            if trying_to_win:
                cpu_move_index = win_move
                #print "win", cpu_move_index
            elif stopping_the_player:
                cpu_move_index = stop_move
                #print "stopping", cpu_move_index
            elif strategic_move != None:
                cpu_move_index = strategic_move
                #print "strategic", cpu_move_index
            else:
                cpu_move_index = random_move
                #print "random", cpu_move_index

            if cpu_move_index != None:
                self.index_already_played.append(cpu_move_index)

                self.status[cpu_move_index] = -1
                # #print [(x, x.id) for x in self.walk()]
                # #print self.ids
                cpu_button = self.ids[str(cpu_move_index)]

                cpu_button.text = 'X'
                cpu_button.background_color = colours[-1]

    def on_status(self, instance, new_value):
        status = new_value

        sums = [sum(status[0:3]), sum(status[3:6]), sum(status[6:9]), # columns
                sum(status[0::3]), sum(status[1::3]), sum(status[2::3]),#every third elemnt satring from 0,3,6= columns
                sum(status[::4]), sum(status[2:-2:2])]

        #print "\n status-> \n"
        #print range(9)
        #print self.status

        winner = None
        if -3 in sums:
            winner = "Cpu wins!"
        elif 3 in sums:
            winner = 'You win!'
        elif 0 not in self.status:
            winner = 'Draw....nobody wins!'

        if winner:
            popup = ModalView(size_hint=(0.75, 0.5))
            victory_label = Label(text=winner, font_size=50)
            popup.add_widget(victory_label)
            popup.bind(on_dismiss=self.reset)
            popup.open()

    def reset(self, *args):
        self.status = [0 for _ in range(9)]
        self.index_already_played = []
        for child in self.children:
            child.text = ''
            child.background_color = (1, 1, 1, 1,)



        # init with first cpu move
        self.ids['7'].text = 'X'
        self.ids['7'].background_color = (0, 1, 0, 1)
        self.status[7] = -1


class Sm(ScreenManager):
    pass

root_widget = Builder.load_file('tictactoe.kv')


"""
gameScObj = GameScreen()
ticObj = GameGrid()
gameScObj.add_widget(ticObj)
sm = ScreenManager()
sm.add_widget(gameScObj)

"""


class TicTacToe(App):
    def build(self):
        return root_widget


if __name__ == "__main__":
    TicTacToe().run()