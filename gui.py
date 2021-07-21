from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.button import Button, Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import NoTransition
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy_garden.graph import Graph, PointPlot

from load_json import get_json_data, get_all_environments
from wifi_positioning_system import get_current_position
from time import sleep

from sys import platform

assert ('linux' in platform), "This code runs on Linux only."


# sudo /home/barak/.local/share/virtualenvs/wifi_navigation_app-mlXzYshZ/bin/python /home/barak/barak/wifi_navigation_app/app/wifi_positioning_system/gui.py


# problem - install sudo apt-get install xclip xsel.
# https://stackoverflow.com/questions/33534976/kivy-error-with-text-input


class GuiData:
    current_environment = ""
    current_new_environment = ""
    x_y_update_interval = None


class BackendData:
    known_aps = []
    path_loss = 0
    x, y = 0, 0


class MenuScreen(Screen):
    """
    first screen of the app.
    """

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.root_widget = None

    def on_pre_enter(self, **kwargs):
        """
        dynamically loads environment-selection buttons, button for each environment in the json, and 1 extra for new
        environment.
        """
        if self.root_widget is not None:
            self.remove_widget(self.root_widget)

        environments = get_all_environments()
        sv = ScrollView(size_hint=(1, 1))

        layout = GridLayout(rows=len(environments) + 1, cols=1, size_hint_y=None, row_default_height=Window.size[1] / 5,
                            row_force_default=True)

        button = Button(text="new environment", size_hint_y=None, pos_hint={'center_x': 0.5, 'center_y': 0.5},
                        padding_y=0, on_press=self.change_to_new_env1_screen)
        layout.add_widget(button)

        for i in range(0, len(environments)):
            button = Button(text=environments[i], size_hint_y=None, pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            padding_y=0, on_press=self.get_environment_selection)
            layout.add_widget(button)

        sv.add_widget(layout)
        self.add_widget(sv)
        self.root_widget = sv

    # noinspection PyMethodMayBeStatic
    def get_environment_selection(self, instance):
        """
        function is called when user selects an existing environment. updates the GuiData.current environment and
        switches to the environment menu.
        """
        GuiData.current_environment = instance.text
        BackendData.aps, BackendData.path_loss = get_json_data(GuiData.current_environment)
        sm.current = 'environment menu'

    # noinspection PyMethodMayBeStatic
    def change_to_new_env1_screen(self, instance):
        sm.current = 'new environment 1'


class NewEnvironmentScreen1(Screen, GuiData):
    """
    new env screen 1
    """

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

        layout = FloatLayout()

        self.text_input = TextInput(multiline=False,
                                    keyboard_suggestions=True,
                                    on_touch_down=self.clear_text,
                                    size_hint=(.8, .3), pos_hint={'x': .1, 'y': .5},
                                    font_size=Window.size[1] / 18)
        # on_touch_up = self.write_text,
        layout.add_widget(self.text_input)

        button = Button(text="next", on_press=self.get_new_name, pos_hint={'x': .1, 'y': .25}
                        , size_hint=(.8, .25), font_size=Window.size[1] / 18)

        layout.add_widget(button)

        self.add_widget(layout)

    def on_pre_enter(self):
        self.text_input.text = "enter the name of the new environment"

    def clear_text(self, instance, event):
        self.text_input.text = ""

    def get_new_name(self, instance):
        GuiData.current_new_environment = self.text_input.text
        sm.current = "new environment 2"


class NewEnvironmentScreen2(Screen):
    """
    new env screen 2
    """

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

        layout = FloatLayout()

        button = Button(text="add access points", pos_hint={'center_x': 0.5, 'center_y': 0.6}, size_hint=(1, .4),
                        on_press=self.to_edit_ap_menu)

        layout.add_widget(button)

        button = Button(text="back to the main menu", pos_hint={'center_x': 0.5, 'center_y': 0.2}, size_hint=(1, .4),
                        on_press=self.back_to_main_menu)

        layout.add_widget(button)

        self.add_widget(layout)

        self.layout = layout
        self.label = None

    def on_pre_enter(self):
        if self.label is not None:
            self.layout.remove_widget(self.label)

        self.label = Label(text="new environment - {0}".format(GuiData.current_new_environment),
                           pos_hint={'center_x': 0.5, 'center_y': 0.9}, size_hint=(1, .2))
        self.layout.add_widget(self.label)

    # noinspection PyMethodMayBeStatic
    def back_to_main_menu(self, instance):
        sm.current = "main menu"

    # noinspection PyMethodMayBeStatic
    def to_edit_ap_menu(self, instance):
        sm.current = "edit aps menu"


class EditApsScreen(Screen):
    """
    edit aps screen
    """

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

        layout = FloatLayout()

        button = Button(text="add new access points", pos_hint={'center_x': 0.5, 'center_y': 0.6}, size_hint=(1, .4))

        layout.add_widget(button)

        button = Button(text="edit existing access points", pos_hint={'center_x': 0.5, 'center_y': 0.2},
                        size_hint=(1, .4))

        layout.add_widget(button)

        self.add_widget(layout)

        self.layout = layout
        self.label = None

    def on_pre_enter(self, *args):
        if self.label is not None:
            self.layout.remove_widget(self.label)

        self.label = Label(text=GuiData.current_environment, pos_hint={'center_x': 0.5, 'center_y': 0.9},
                           size_hint=(1, .2))
        self.layout.add_widget(self.label)


class NavigationScreen(Screen):
    """
    the navigation screen
    """

    def __init__(self, **kwargs):
        """
        sets the screen - the graph and the plots
        """
        super(Screen, self).__init__(**kwargs)

        self.graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=0, y_ticks_minor=0,
                           x_ticks_major=10, y_ticks_major=10,
                           y_grid_label=True, x_grid_label=True, padding=5,
                           x_grid=True, y_grid=True, xmin=-20, xmax=20, ymin=-20, ymax=20)

        self.update_interval = None

        aps_plot = PointPlot(color=[1, 0, 0, 1])
        aps_plot.point_size = 4

        user_plot = PointPlot(color=[0, 1, 1, 1])
        user_plot.point_size = 5

        self.graph.add_plot(aps_plot)
        self.graph.add_plot(user_plot)

        self.add_widget(self.graph)

    def on_pre_enter(self, *args):
        """
        sets the update interval
        """
        self.update_interval = Clock.schedule_interval(self.update_location_and_graph, 3)

    # noinspection PyMethodMayBeStatic
    def update_location_and_graph(self, *args):
        """
        function that is being called by an interval, calls the backend function which determines the position,
        and than updates the graph according to the output
        """
        ap1_coordinates, ap2_coordinates, ap3_coordinates, user_coordinates = \
            get_current_position(BackendData.path_loss, BackendData.aps)

        if ap1_coordinates is None:
            return

        self.graph.plots[0].points = [ap1_coordinates, ap2_coordinates, ap3_coordinates]
        self.graph.plots[1].size = 10

        self.graph.plots[1].points = [user_coordinates]
        self.graph.plots[1].size = 10

    def on_pre_leave(self, *args):
        """
        for future use
        """
        Clock.unschedule(self.update_interval)


class EnvironmentMenu(Screen):
    """
    the env menu
    """

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        layout = FloatLayout()

        button = Button(text="navigate", pos_hint={'center_x': 0.5, 'center_y': 0.6}, size_hint=(1, .4),
                        on_press=self.to_navigation_page)

        layout.add_widget(button)
        #
        # button = Button(text="edit access points", pos_hint={'center_x': 0.5, 'center_y': 0.3}, size_hint=(1, .2),
        #                 on_press=self.to_edit_ap_menu)
        #
        # layout.add_widget(button)

        button = Button(text="back to main menu", pos_hint={'center_x': 0.5, 'center_y': 0.2}, size_hint=(1, .4),
                        on_press=self.back_to_main_menu)

        layout.add_widget(button)

        self.add_widget(layout)

        self.label = None
        self.layout = layout

    def on_pre_enter(self, *args):
        if self.label is not None:
            self.layout.remove_widget(self.label)

        self.label = Label(text=GuiData.current_environment, pos_hint={'center_x': 0.5, 'center_y': 0.9},
                           size_hint=(1, .2))
        self.layout.add_widget(self.label)

    # noinspection PyMethodMayBeStatic
    def back_to_main_menu(self, instance):
        sm.current = "main menu"

    # noinspection PyMethodMayBeStatic
    def to_edit_ap_menu(self, instance):
        sm.current = "edit aps menu"

    # noinspection PyMethodMayBeStatic
    def to_navigation_page(self, instance):
        sm.current = 'navigation page'


sm = ScreenManager(transition=NoTransition())
sm.add_widget(MenuScreen(name='main menu'))
sm.add_widget(NewEnvironmentScreen1(name='new environment 1'))
sm.add_widget(NewEnvironmentScreen2(name='new environment 2'))
sm.add_widget(EditApsScreen(name='edit aps menu'))
sm.add_widget(EnvironmentMenu(name='environment menu'))
sm.add_widget(NavigationScreen(name='navigation page'))


class MainApp(App):

    def build(self):
        print("\n\n\n******\npositioning system - by Barak Yaffe\n******\n\n\n")
        return sm


if __name__ == '__main__':
    MainApp().run()
