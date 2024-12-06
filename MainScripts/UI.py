import pygame
import pygame_gui

class UIManager:
    def __init__(self, screen_size, theme_path=None):
        """
        Initialize the UIManager.
        :param screen_size: Tuple (width, height) of the screen.
        :param theme_path: Path to a custom theme file (optional).
        """
        self.manager = pygame_gui.UIManager(screen_size, theme_path)
        self.buttons = []

    def add_button(self, text, position, size, callback):
        """
        Add a button to the UI.
        :param text: Button text.
        :param position: Tuple (x, y) for button position.
        :param size: Tuple (width, height) for button size.
        :param callback: Function to call on button press.
        """
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(position, size),
            text=text,
            manager=self.manager
        )
        self.buttons.append((button, callback))

    def process_events(self, event):
        """
        Process Pygame events for the UI.
        :param event: A Pygame event to process.
        """
        self.manager.process_events(event)

        # Handle button clicks
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                for button, callback in self.buttons:
                    if event.ui_element == button:
                        callback()

    def update(self, time_delta):
        """Update the UI."""
        self.manager.update(time_delta)

    def draw(self, screen):
        """Draw the UI to the screen."""
        self.manager.draw_ui(screen)
