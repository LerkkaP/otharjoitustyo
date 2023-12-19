import pygame
from game_phases.start import Start
from game_phases.gameplay import Gameplay
from game_phases.end import End
from game_phases.stats import Stats
from utils.phase_manager import PhaseManager
from utils.score import Score
import sys


class GameManager():
    def __init__(self, screen_width, screen_height):
        self.start_phase = Start(screen_width, screen_height)
        self.gameplay_phase = Gameplay(screen_width, screen_height)
        self.end_phase = End(screen_width)
        self.stats_phase = Stats()
        self.phase_manager = PhaseManager()
        self.score = Score()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._handle_quit()
            self._handle_gameplay_events(event)

    def _handle_quit(self):
        pygame.quit()
        sys.exit() # sys.exit() is for removing pygame error: display Surface quit

    def _handle_gameplay_events(self, event):
        if self.phase_manager.game_in_start():
            self._handle_start_events(event)
        if self.phase_manager.game_in_gameplay():
            self._handle_gameplay_phase_events(event)
        else:
            self._handle_end_events(event)

    def _handle_start_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.phase_manager.set_phase("gameplay")
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.phase_manager.set_phase("gameplay")

    def _handle_gameplay_phase_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.gameplay_phase.handle_bird_fly(0, -10)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.gameplay_phase.handle_bird_fly(0, -20)

    def _handle_end_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.end_phase.handle_restart_click(mouse_pos):
                    self._restart_game()
                elif self.end_phase.handle_statistics_click(mouse_pos):
                    self._handle_stats()
                elif self.stats_phase.handle_back_click(mouse_pos):
                    self.phase_manager.set_phase("end")


    def _restart_game(self):
        self.phase_manager.set_phase("start")
        self.gameplay_phase.reset_bird()
        self.gameplay_phase.pipe_movement.reset_pipes()
        self.score.reset_score()

    def _handle_stats(self):
        self.phase_manager.set_phase("stats")
        
    def handle_game_state(self):
        if self.phase_manager.game_in_start():
            self.start_phase.update()
            self.start_phase.handle_text_hover()
        elif self.phase_manager.game_in_gameplay():
            self._update_gameplay()
        elif self.phase_manager.game_in_end():
            self._update_gameplay()

    def _update_gameplay(self):
        if not self.phase_manager.game_in_end():
            self.gameplay_phase.update()
            self.gameplay_phase.bird.update()
            self.gameplay_phase.handle_collision()

        self.gameplay_phase.handle_bird_fall()
