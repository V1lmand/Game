import arcade
from arcade import Camera2D
from pyglet.graphics import Batch

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 640
SCREEN_TITLE = "level_one"
TILE_SCALING = 2.5

# Физика и движение
GRAVITY = 0.5  # Пикс/с^2
MOVE_SPEED = 2.5  # Пикс/с
JUMP_SPEED = 7  # Начальный импульс прыжка, пикс/с
# Качество жизни прыжка
COYOTE_TIME = 0.08  # Сколько после схода с платформы можно ещё прыгнуть
JUMP_BUFFER = 0.12  # Если нажали прыжок чуть раньше приземления, мы его «запомним» (тоже лайфхак для улучшения качества жизни игрока)
MAX_JUMPS = 1  # С двойным прыжком всё лучше, но не сегодня
CAMERA_LERP = 0.12

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        # arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.player = arcade.Sprite(
            ":resources:/images/animated_characters/female_adventurer/femaleAdventurer_idle.png", scale=0.5)
        self.player.center_x = 100
        self.player.center_y = 100
        self.player_spritelist = arcade.SpriteList()
        self.player_spritelist.append(self.player)

        map_name = "level_one.tmx"
        tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)
        self.scene = arcade.Scene.from_tilemap(tile_map)
        self.scene.remove_sprite_list_by_name("collision")

        # self.wall_list = tile_map.sprite_lists["walls"]
        # self.ladders_list = tile_map.sprite_lists["ladders"]
        # self.lava_list = tile_map.sprite_lists["lava"]
        # self.doors_list = tile_map.sprite_lists["doors"]
        # self.background_list = tile_map.sprite_lists["background"]
        # self.collision_list = tile_map.sprite_lists["collision"]

        self.batch = Batch()

        self.left = self.right = self.up = self.down = self.jump_pressed = False
        self.jump_buffer_timer = 0.0
        self.time_since_ground = 999.0
        self.jumps_left = MAX_JUMPS
        self.score = 0

        self.world_camera = Camera2D()
        self.gui_camera = Camera2D()

        self.engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            gravity_constant=GRAVITY,
            walls=self.scene['walls']
        )
        self.physics_engine1 = arcade.PhysicsEngineSimple(self.player, self.scene["lava"])

    def on_draw(self):
        self.clear()

        # self.background_list.draw()
        # self.wall_list.draw()
        # self.ladders_list.draw()
        # self.lava_list.draw()
        # self.doors_list.draw()
        # self.collision_list.draw()

        self.world_camera.use()

        self.scene.draw()
        self.player_spritelist.draw()

        self.gui_camera.use()
        self.batch.draw()

    def on_update(self, delta_time):
        self.player.change_y -= GRAVITY

        move = 0
        if self.left and not self.right:
            move = -MOVE_SPEED
        elif self.right and not self.left:
            move = MOVE_SPEED
        self.player.change_x = move

        grounded = self.engine.can_jump(y_distance=6)
        if grounded:
            self.time_since_ground = 0
            self.jumps_left = MAX_JUMPS
        else:
            self.time_since_ground += delta_time

        if self.jump_buffer_timer > 0:
            self.jump_buffer_timer -= delta_time
        want_jump = self.jump_pressed or (self.jump_buffer_timer > 0)

        if want_jump:
            can_coyote = (self.time_since_ground <= COYOTE_TIME)
            if grounded or can_coyote:
                self.engine.jump(JUMP_SPEED)
                self.jump_buffer_timer = 0

        self.engine.update()
        self.physics_engine1.update()


        self.text = arcade.Text(f'Score: {self.score}',
                                10, self.height - 30, arcade.color.WHITE,
                                24, batch=self.batch)

        target = (self.player.center_x, self.player.center_y)
        cx, cy = self.world_camera.position
        smooth = (cx + (target[0] - cx) * CAMERA_LERP,
                  cy + (target[1] - cy) * CAMERA_LERP)

        half_w = self.world_camera.viewport_width / 2
        half_h = self.world_camera.viewport_height / 2

        world_w = 2500
        world_h = 1000
        cam_x = max(half_w, min(world_w - half_w, smooth[0]))
        cam_y = max(half_h, min(world_h - half_h, smooth[1]))

        self.world_camera.position = (cam_x, cam_y)
        self.gui_camera.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right = True
        elif key in (arcade.key.UP, arcade.key.W):
            self.up = True
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down = True
        elif key == arcade.key.SPACE:
            self.jump_pressed = True
            self.jump_buffer_timer = JUMP_BUFFER

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right = False
        elif key in (arcade.key.UP, arcade.key.W):
            self.up = False
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down = False
        elif key == arcade.key.SPACE:
            self.jump_pressed = False
            if self.player.change_y > 0:
                self.player.change_y *= 0.45

def setup_game(width=1300, height=640, title="level_one"):
    game = MyGame(width, height, title)
    game.setup()
    return game

def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    main()