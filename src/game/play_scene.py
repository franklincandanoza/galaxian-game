import json
import pygame
from src.ecs.components.c_enemy_choose_steering import CEnemyChooseSteering
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.systems.debug.s_steering_draw_debug import system_steering_draw_debug
from src.ecs.systems.s_choise_enemy_steering import system_choose_enemy_steering
from src.ecs.systems.s_collision_enemy_screen import system_collision_enemy_screen
from src.ecs.systems.s_enemy_steering import system_enemy_steering
from src.ecs.systems.s_enemy_steering_fire import system_enemy_steering_fire

from src.engine.scenes.scene import Scene
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform 
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_movement import system_movement
import json
import pygame
import esper
from src.ecs.components.c_enemy_basic_fire import CEnemyBasicFire
from src.ecs.components.c_ready_level import CReadyLevel
from src.ecs.components.tags.messages.c_tag_pause_message import CTagPauseMessage 
from src.ecs.systems.s_animation import system_animation
import random
from src.ecs.systems.s_collision_player_bullet import system_collision_player_bullet

from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_collision_enemy_bullet import system_collision_enemy_bullet
from src.ecs.systems.s_screen_info import system_screen_info
from src.ecs.systems.s_enemy_basic_fire import system_basic_enemy_fire

from src.ecs.systems.s_enemy_spawner_new import system_enemy_spawner_new
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_screen_pause import system_screen_pause
from src.ecs.systems.s_screen_player import system_screen_player
from src.ecs.systems.s_screen_star import system_screen_star
from src.ecs.systems.s_screen_bullet import system_screen_bullet

from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_explosion_kill import system_explosion_kill
from src.ecs.systems.s_up_level_game import system_up_level_game
from src.ecs.systems.s_screen_level import system_screen_level
from src.ecs.systems.s_synchronization_enemies import system_synchronization_enemies

from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet import CTagBullet

from src.ecs.components.c_input_command import CInputCommand, CommandPhase

from src.create.prefab_creator import create_input_player, create_player_square, create_bullet, create_level_square
from src.create.prefab_creator  import create_score_info, create_level_info, create_start, create_enemy_spawner_new, create_score_value, create_lifes_info
from src.ecs.systems.s_system_ready import system_ready_level
from src.engine.service_locator import ServiceLocator


class PlayScene(Scene):
    def __init__(self, level_path:str, screen:pygame.Surface) -> None:
        super().__init__(screen)
        with open("assets/cfg/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open(level_path) as level_file:
            self.level_cfg = json.load(level_file)
        with open("assets/cfg/enemies.json") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open("assets/cfg/level_01.json") as level_01_file:
            self.level_01_cfg = json.load(level_01_file)
        with open("assets/cfg/player.json") as player_file:
            self.player_cfg = json.load(player_file)
        with open("assets/cfg/bullet.json") as bullet_file:
            self.bullet_cfg = json.load(bullet_file)
        with open("assets/cfg/explosion.json") as explosion_file:
            self.explosion_cfg = json.load(explosion_file)
        with open("assets/cfg/starfield.json") as star_field_file:
            self.star_field_cfg = json.load(star_field_file)
        with open("assets/cfg/game_start.json") as game_start_file:
            self.game_start_cfg = json.load(game_start_file)
        with open("assets/cfg/pause.json") as pause_file:
            self.pause_cfg = json.load(pause_file)
        with open("assets/cfg/interface.json") as interface_file:
            self.interface_cfg = json.load(interface_file)
        self._paddle_ent = -1
        self.is_paused = False
        self.is_ready = False
        self.screen = screen

    def do_create(self):
        enemy_basic_fire = self.ecs_world.create_entity()
        self._steering_debug = False
        self.ecs_world.add_component(enemy_basic_fire,
                         CEnemyBasicFire(self.level_01_cfg["enemy_basic_fire"]))
        self._game_info_entity = create_score_info(self.ecs_world, self.interface_cfg)
        self._game_info_entity = create_score_value(self.ecs_world, self.interface_cfg)
        create_lifes_info(self.ecs_world, self.interface_cfg, self.player_cfg)
        #self._game_info_entity = create_instructions_info(self.ecs_world, self.interface_cfg, explosion_info=self.explosion_cfg)
        self._game_dead_enemy = create_level_info(self.ecs_world, self.interface_cfg, dead_enemies=0)
        
        
        create_enemy_spawner_new(self.ecs_world, self.level_01_cfg)
        create_input_player(self.ecs_world)
        #create_level_square(self.ecs_world, self.interface_cfg)
        
        
        ready_level = self.ecs_world.create_entity()

        self.ecs_world.add_component(ready_level,
                         CReadyLevel(self.game_start_cfg))
        
        self._create_stars()
        ServiceLocator.sounds_service.play(self.game_start_cfg["sound"])
        self._player_left_start = False
        self._player_right_start = False
        
    def _create_stars(self)->None:
        y_window_zize = self.window_cfg["size"]["h"] # Vertical
        w_window_zize =  self.window_cfg["size"]["w"] # Horizontal
        stars_number = self.star_field_cfg["number_of_stars"]
        # Recorremos la cantidad de estrellas a crear
        x_delta = w_window_zize / stars_number
        current_x_position = 0
        
        for i in range(1,stars_number):
            
            y_position = random.randint(0, y_window_zize)
            
            
            x_position = current_x_position + x_delta
            create_start(self.ecs_world, star_pos=pygame.Vector2(x_position, y_position), star_info= self.star_field_cfg)    
            current_x_position = x_position
        # La posición de arranque de cada estrella es aleatorio en Y
        
        
    def do_process_events(self, event:pygame.event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.is_paused = not self.is_paused
            self.pause()
            
        if self.is_ready:
            super().do_process_events(event)
            if event.type == pygame.QUIT:
                self.is_running = False    
            
        
        
    def do_update(self, delta_time: float):
        system_screen_star(self.ecs_world, self.screen)
        system_screen_pause(self.ecs_world, self.screen, delta_time)
        if not self.is_paused:
            #if not self.is_ready:
            system_ready_level(self.ecs_world,delta_time,self.game_start_cfg,self.screen)
            self._is_level_ready(self.ecs_world)
                
            
            system_enemy_spawner_new(self.ecs_world, self.enemies_cfg, self.screen)
            system_movement(self.ecs_world, delta_time)
            system_synchronization_enemies(self.ecs_world, self.screen)

            system_screen_bounce(self.ecs_world, self.screen)
            
            system_screen_player(self.ecs_world, self.screen)
            
            system_screen_bullet(self.ecs_world, self.screen)
            
            if self.is_ready:
                system_choose_enemy_steering(self.ecs_world,self.level_01_cfg["enemy_steering"], delta_time)
                system_enemy_steering(self.ecs_world, None, delta_time)
                system_collision_enemy_screen(self.ecs_world, self.screen)
                system_basic_enemy_fire(self.ecs_world,delta_time, self.level_01_cfg["enemy_basic_fire"],self.bullet_cfg["enemy"])
                system_enemy_steering_fire(self.ecs_world, delta_time,self.bullet_cfg["enemy"])
                system_collision_player_bullet(self.ecs_world, self._player_entity,
                                    self.level_01_cfg,self.explosion_cfg)
                system_collision_enemy_bullet(self.ecs_world, self.explosion_cfg, self._player_entity)
                system_collision_player_enemy(self.ecs_world, self._player_entity,
                                            self.level_01_cfg, self.explosion_cfg)
                system_screen_info(self.ecs_world, self._player_entity, self.explosion_cfg, self.interface_cfg)
                system_screen_level(self.ecs_world, self._player_entity, self.explosion_cfg, self.interface_cfg)

                system_explosion_kill(self.ecs_world)
                system_player_state(self.ecs_world)
                system_up_level_game(self.ecs_world, self.explosion_cfg, self._player_entity, self.game_start_cfg, self.level_01_cfg)
                
                system_collision_player_enemy(self.ecs_world, self._player_entity,self.level_01_cfg,self.explosion_cfg)         
                
            #system_enemy_hunter_state(self.ecs_world, self._player_entity, self.enemies_cfg["TypeHunter"])

            system_animation(self.ecs_world, delta_time)

            self.ecs_world._clear_dead_entities()
            self.num_bullets = len(self.ecs_world.get_component(CTagBullet))
            self._is_game_over(self.ecs_world)
    def do_clean(self):
        self.ecs_world.clear_database()

    def do_action(self, c_input: CInputCommand):
        if self.is_ready:
            if c_input.name == "PLAYER_LEFT":
                if c_input.phase == CommandPhase.START:
                    self._player_left_start = True
                    self._player_c_v.vel.x -= self.player_cfg["input_velocity"]
                elif c_input.phase == CommandPhase.END  and self._player_left_start:
                    self._player_c_v.vel.x += self.player_cfg["input_velocity"]
            if c_input.name == "PLAYER_RIGHT":
                if c_input.phase == CommandPhase.START:
                    self._player_right_start = True
                    self._player_c_v.vel.x += self.player_cfg["input_velocity"]

                elif c_input.phase == CommandPhase.END and self._player_right_start:
                    self._player_c_v.vel.x -= self.player_cfg["input_velocity"]
                
            if c_input.name == "TOGGLE_STEERING_DEBUG" and c_input.phase == CommandPhase.START: 
                self._steering_debug = not self._steering_debug    
            if c_input.name == "PLAYER_Z" and self.num_bullets < self.level_01_cfg["player_spawn"]["max_bullets"]:
                if not self.is_paused:
                    create_bullet(self.ecs_world, self._player_c_t.pos,
                            self._player_c_s.area.size, self.bullet_cfg)
            
        if c_input.name == "QUIT_TO_MENU" and c_input.phase == CommandPhase.START:
            self.switch_scene("MENU_SCENE")
            
            
    def text_objects(self,text, font):
        c = self.pause_cfg["color"]
        color = (c["r"],c["g"],c["b"])
        text_surface = font.render(text, True, color)
        return text_surface
                    
    def pause(self):
        if self.is_paused:
            largeText = ServiceLocator.fonts_service.get(self.pause_cfg["font"], self.pause_cfg["size"])
            text_surf = self.text_objects(self.pause_cfg["text"], largeText) 
        
            ready_message = self.ecs_world.create_entity()
            self.ecs_world.add_component(ready_message, CSurface.from_surface(text_surf))
            self.ecs_world.add_component(ready_message, CTagPauseMessage(self.pause_cfg))
            self.ecs_world.add_component(ready_message,CTransform(pygame.Vector2(self.screen.get_rect().w/2-text_surf.get_width()/2, self.screen.get_rect().h/2)))
            ServiceLocator.sounds_service.play("assets/snd/pause.ogg")
        else:
            component = self.ecs_world.get_component(CTagPauseMessage)
            ServiceLocator.sounds_service.play("assets/snd/unpause.ogg")
            for entity,(_) in component:
                self.ecs_world.delete_entity(entity)
                
    def _create_player(self):          
        self._player_entity = create_player_square(self.ecs_world, self.player_cfg, self.level_01_cfg)
        self._player_c_v = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        self._player_c_t = self.ecs_world.component_for_entity(self._player_entity, CTransform)
        self._player_c_s = self.ecs_world.component_for_entity(self._player_entity, CSurface)
                   
    def _create_steerling(self):
        steering_choose_entity = self.ecs_world.create_entity()
        self.ecs_world.add_component(steering_choose_entity,CEnemyChooseSteering(self.level_01_cfg) )
        
 
    def _is_level_ready(self,world: esper.World):
            components = world.get_component(CReadyLevel)
            c_rl: CReadyLevel

            for _, (c_rl) in components: 
                
                self.is_ready = c_rl.ready
                if self.is_ready and not c_rl.player_showed:
                    self._create_player()
                    self._create_steerling()
                    
                    c_rl.player_showed = True


    def _is_game_over(self,world:esper.World):
        
        if not self.is_ready:
            return
        components = world.get_component(CTagPlayer)
        c_p : CTagPlayer
        for _, (c_p) in components:
            if c_p.current_lifes ==0:
                self.switch_scene(Scene.Scenes.GAME_OVER_SCENE)


    def do_draw(self, screen):
        super().do_draw(screen)
        if self._steering_debug:
            system_steering_draw_debug(self.ecs_world, screen)