import pygame

class SFX():
    def __init__(self, theme):
        pygame.mixer.init()
        pygame.mixer.set_num_channels(10)
        self.ambient_channel = pygame.mixer.Channel(1)

        self.step_channel = pygame.mixer.Channel(2)

        self.fight_channel = pygame.mixer.Channel(3)
        self.fight_channel_two = pygame.mixer.Channel(4)
        self.fight_channel_three = pygame.mixer.Channel(5)

        self.dialog_channel = pygame.mixer.Channel(6)
        self.equipment_channel = pygame.mixer.Channel(6)
        self.plot_channel = pygame.mixer.Channel(7)

        self.bonfire_channel = pygame.mixer.Channel(3)
        self.village_channel = pygame.mixer.Channel(4)

        if theme == "md":
            self.bgm = pygame.mixer.Sound("./sfx/md/world_bgm.wav")
            self.ambient = pygame.mixer.Sound("./sfx/md/ambient.wav")
            self.walk = pygame.mixer.Sound("./sfx/md/walking.wav")
            self.enemy_slash = pygame.mixer.Sound("./sfx/md/enemy_slash.wav")
            self.umph = pygame.mixer.Sound("./sfx/md/umph.wav")
            self.page_turn = pygame.mixer.Sound("./sfx/md/page_turn.wav")
            self.equip = pygame.mixer.Sound("./sfx/md/equip.wav")
            self.blood = pygame.mixer.Sound("./sfx/md/blood.wav")
            self.draw_sword = pygame.mixer.Sound("./sfx/md/draw_sword.wav")
            self.bonfire = pygame.mixer.Sound("./sfx/md/bonfire.wav")
            self.scream = pygame.mixer.Sound("./sfx/md/scream.wav")
            self.door_open = pygame.mixer.Sound("./sfx/md/door_open.wav")
            self.player_miss = pygame.mixer.Sound("./sfx/md/player_miss.wav")
            self.enemy_miss = pygame.mixer.Sound("./sfx/md/enemy_miss.wav")
            self.falling = pygame.mixer.Sound("./sfx/md/falling.wav")
            
            self.player_slashs = []
            for i in range(8):
                self.player_slashs.append(pygame.mixer.Sound(f"./sfx/md/player_slash_{i}.wav"))

            self.monster_roars = []
            for i in range(15):
                self.monster_roars.append(pygame.mixer.Sound(f"./sfx/md/monster_roar_{i}.wav"))
            self.monster_die = pygame.mixer.Sound("./sfx/md/monster_die.wav")

        elif theme == "gs":
            self.bgm = pygame.mixer.Sound("./sfx/md/world_bgm.wav")
            self.ambient = pygame.mixer.Sound("./sfx/md/ambient.wav")
            self.walk = pygame.mixer.Sound("./sfx/md/walking.wav")
            self.enemy_slash = pygame.mixer.Sound("./sfx/md/enemy_slash.wav")
            self.umph = pygame.mixer.Sound("./sfx/md/umph.wav")
            self.page_turn = pygame.mixer.Sound("./sfx/md/page_turn.wav")
            self.equip = pygame.mixer.Sound("./sfx/md/equip.wav")
            self.blood = pygame.mixer.Sound("./sfx/md/blood.wav")
            self.draw_sword = pygame.mixer.Sound("./sfx/md/draw_sword.wav")
            self.bonfire = pygame.mixer.Sound("./sfx/md/bonfire.wav")
            self.scream = pygame.mixer.Sound("./sfx/md/scream.wav")
            self.door_open = pygame.mixer.Sound("./sfx/md/door_open.wav")
            self.player_miss = pygame.mixer.Sound("./sfx/md/player_miss.wav")
            self.enemy_miss = pygame.mixer.Sound("./sfx/md/enemy_miss.wav")
            self.falling = pygame.mixer.Sound("./sfx/md/falling.wav")
            
            self.player_slashs = []
            for i in range(8):
                self.player_slashs.append(pygame.mixer.Sound(f"./sfx/md/player_slash_{i}.wav"))

            self.monster_roars = []
            for i in range(15):
                self.monster_roars.append(pygame.mixer.Sound(f"./sfx/md/monster_roar_{i}.wav"))
            self.monster_die = pygame.mixer.Sound("./sfx/md/monster_die.wav")
            
        self.volume_setting()
        
        self.bgm.play(-1)
        self.ambient_channel.play(self.ambient, -1)

    def volume_setting(self):
        self.bgm.set_volume(0.4)
        self.ambient.set_volume(0.2)
        self.bonfire.set_volume(0.4)
        self.enemy_slash.set_volume(0.4)
        for slash in self.player_slashs: slash.set_volume(0.7)
        for roar in self.monster_roars: roar.set_volume(0.6)