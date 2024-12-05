import pygame
import pygame_gui

class UIManager:
    def __init__(self, screen_size, button_callback):
        self.manager = pygame_gui.UIManager(screen_size)
        self.button_callback = button_callback  # Store the callback function

        # Add UI Elements
        self.topbutton = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((185, 200), (100, 50)),
            text="Press Me",
            manager=self.manager,
        )

    def process_events(self, event):
        self.manager.process_events(event)

        # Handle button clicks
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.topbutton:
                    self.button_callback()  # Call the callback

    def update(self, time_delta):
        self.manager.update(time_delta)

    def draw(self, screen):
        self.manager.draw_ui(screen)
