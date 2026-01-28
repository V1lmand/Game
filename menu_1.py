import arcade
from arcade.gui import UIManager, UITextureButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Game"
SPEED = 2


class Player(arcade.Sprite):
    def __init__(self, n):
        super().__init__()
        self.hero = n


class MyGUIWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.DARK_BLUE)

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = arcade.gui.UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)

        self.anchor_layout = UIAnchorLayout(padding=(40, 40, 0, 0))
        self.anchor_layout.add(
            child=self.box_layout,
            anchor_x="left",
            anchor_y="top"
        )

        self.setup_widgets()

        self.manager.add(self.anchor_layout)

        self.all_sprites = arcade.SpriteList()
        self.game_active = False

    def setup_widgets(self):
        texture_normal = arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png")
        texture_hovered = arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png")
        texture_pressed = arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png")

        button_select_hero = UITextureButton(text='Выбор героя',
                                             texture=texture_normal,
                                             texture_hovered=texture_hovered,
                                             texture_pressed=texture_pressed,
                                             scale=1.2)
        self.box_layout.add(button_select_hero)

        button_start_game = UITextureButton(text='Начать игру',
                                            texture=texture_normal,
                                            texture_hovered=texture_hovered,
                                            texture_pressed=texture_pressed,
                                            scale=1.2)
        button_start_game.on_click = self.start_game
        self.box_layout.add(button_start_game)

        button_exit = UITextureButton(text='Выход',
                                      texture=texture_normal,
                                      texture_hovered=texture_hovered,
                                      texture_pressed=texture_pressed,
                                      scale=1.2)
        button_exit.on_click = self.exit_game
        self.box_layout.add(button_exit)

    def setup(self):
        self.player = Player(0)
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.all_sprites.append(self.player)

    def start_game(self, event):
        """Начать игру"""

    def exit_game(self, event):
        """Выйти из игры"""
        arcade.close_window()

    def on_draw(self):
        self.clear()
        self.manager.draw()

        arcade.draw_text(SCREEN_TITLE,
                         SCREEN_WIDTH // 2,
                         SCREEN_HEIGHT - 100,
                         arcade.color.BLACK,
                         48,
                         anchor_x="center",
                         bold=True)

    def on_update(self, delta_time: float):
        if self.game_active and hasattr(self, 'player'):
            self.all_sprites.update(delta_time)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        elif key == arcade.key.ENTER:
            self.start_game(None)
        elif key == arcade.key.S:
            pass


def setup_game(width=800, height=600, title="Game"):
    game = MyGUIWindow(width, height, title)
    game.setup()
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()