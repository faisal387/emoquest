import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Game settings
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
BACKGROUND_COLOR = (100, 100, 100)  # Darker color
FONT_PATH = os.path.join('assets', 'ThaleahFat.ttf')

# Define some colors
BLACK = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("EmoQuest")

# Load game assets (images and sounds)
sprite_img = pygame.image.load(os.path.join('assets', 'sprite.png'))
sprite_img = pygame.transform.scale(sprite_img, (50, 100))
background_img = pygame.image.load(os.path.join('assets', 'background.png'))
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
checkpoint_img = pygame.image.load(os.path.join('assets', 'checkpoint.png'))
checkpoint_img = pygame.transform.scale(checkpoint_img, (50, 50))
end_screen_img = pygame.image.load(os.path.join('assets', 'end_screen.jpg'))  # Load the end screen image
end_screen_img = pygame.transform.scale(end_screen_img, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale the end screen image to match the screen size
pygame.mixer.music.load(os.path.join('assets', 'background_music.mp3'))
pygame.mixer.music.set_volume(0.5)

# Ensure the font file exists
if not os.path.isfile(FONT_PATH):
    raise SystemExit(f"Could not find font file {FONT_PATH}")

# Define sprite class
class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    # Function to move the sprite
    def move_right(self, speed):
        self.rect.x += speed

    # Function to reset the sprite to its starting position
    def reset_position(self):
        self.rect.topleft = (0, SCREEN_HEIGHT // 2)

sprite = Sprite(sprite_img, 0, SCREEN_HEIGHT // 2)  # Initialize the sprite at the middle left of the screen

# Define checkpoints
checkpoints = [(200, SCREEN_HEIGHT // 2), (400, SCREEN_HEIGHT // 2), (600, SCREEN_HEIGHT // 2), (700, SCREEN_HEIGHT // 2), (800, SCREEN_HEIGHT // 2)]

# Scenarios
scenarios = [
    ("You overhear a friend being mocked by others. What do you do?", ["Stand up for your friend.", "Ignore the situation.", "Join in the mockery."]),
    ("You see someone drop their wallet. What do you do?", ["Return the wallet to the person.", "Ignore it and walk away.", "Take the money and leave the wallet."]),
    ("A friend confides in you about a problem they're having. What do you do?", ["Listen attentively and offer support.", "Change the subject.", "Share their problem with others."]),
    ("You've accidentally been given too much change at a shop. What do you do?", ["Give the extra change back.", "Keep the extra change.", "Donate the extra change."]),
    ("A coworker is struggling with a task you're good at. What do you do?", ["Offer to help.", "Let them figure it out on their own.", "Tell others about their struggle."])
]

def show_scenario(scenario_text, options):
    # Draw the scenario text and options and get player's choice
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the background
        screen.blit(background_img, (0, 0))

        # Draw the sprite
        screen.blit(sprite.image, sprite.rect)

        # Draw the dialogue box
        dialogue_box = pygame.Surface((SCREEN_WIDTH, 200))  # Create a new surface for the dialogue box
        dialogue_box.fill((100, 100, 100))  # Fill the dialogue box with a color (change to suit your game's aesthetic)
        dialogue_box.set_alpha(200)  # Set transparency (0 = fully transparent, 255 = fully opaque)
        screen.blit(dialogue_box, (0, SCREEN_HEIGHT - 200))  # Draw the dialogue box at the bottom of the screen

        # Draw the scenario text
        font = pygame.font.Font(FONT_PATH, 36)
        text_surface = font.render(scenario_text, True, BLACK)
        screen.blit(text_surface, (50, SCREEN_HEIGHT - 200 + 10))  # Draw the text inside the dialogue box

        # Draw the options
        option_font = pygame.font.Font(FONT_PATH, 28)
        for i, option in enumerate(options, 1):
            option_surface = option_font.render(f"{i}. {option}", True, BLACK)
            screen.blit(option_surface, (50, SCREEN_HEIGHT - 200 + 50 + 30 * i))

        pygame.display.flip()

        # Get player's choice
        choice = None
        while not choice:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if pygame.K_1 <= event.key <= pygame.K_3:
                        choice = event.key - pygame.K_0

        return choice

def main_menu():
    menu_font = pygame.font.Font(FONT_PATH, 50)
    instruction_font = pygame.font.Font(FONT_PATH, 30)

    menu_options = ["Start Game", "Instructions", "Quit"]
    instructions = ["Press 'D' to move right", "Reach a checkpoint for a scenario", 
                    "Answer the questions to affect your score", 
                    "After all scenarios, your score will be displayed"]

    selected_option = 0
    showing_instructions = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not showing_instructions:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN and not showing_instructions:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Start Game
                        return True
                    elif selected_option == 1:  # Instructions
                        showing_instructions = not showing_instructions
                    else:  # Quit
                        return False
                elif event.key == pygame.K_ESCAPE:
                    showing_instructions = False

        screen.blit(background_img, (0, 0))

        if not showing_instructions:
            for i, text in enumerate(menu_options):
                label = menu_font.render(text, 1, (255, 255, 255))
                screen.blit(label, (SCREEN_WIDTH // 2 - label.get_rect().width // 2,
                                    SCREEN_HEIGHT // 2 - label.get_rect().height // 2 + i * 60))

                if i == selected_option:
                    pygame.draw.rect(screen, (255, 255, 255), label.get_rect(center=(SCREEN_WIDTH // 2, 
                                        SCREEN_HEIGHT // 2 + i * 60)), 2)
        else:
            for i, text in enumerate(instructions):
                label = instruction_font.render(text, 1, (255, 255, 255))
                screen.blit(label, (SCREEN_WIDTH // 2 - label.get_rect().width // 2,
                                    SCREEN_HEIGHT // 2 - label.get_rect().height // 2 - 100 + i * 60))

            label = menu_font.render("Back", 1, (255, 255, 255))
            screen.blit(label, (SCREEN_WIDTH // 2 - label.get_rect().width // 2, SCREEN_HEIGHT // 2 + 200))

        pygame.display.flip()

# Game loop
def main():
    pygame.mixer.music.play(-1)  # Start playing the background music

    while True:
        start_game = main_menu()

        if not start_game:
            pygame.quit()
            sys.exit()

        # Initialize player's emotional intelligence score
        emotional_intelligence_score = 0

        scenario_index = 0
        checkpoint_index = 0

        sprite.reset_position()  # Reset sprite to its starting position

        # Create checkpoints at equal distances
        checkpoints = [(i * SCREEN_WIDTH // (len(scenarios) + 1), SCREEN_HEIGHT // 2) for i in range(1, len(scenarios) + 1)]

        # Main game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Draw the background
            screen.blit(background_img, (0, 0))

            # Draw the sprite
            screen.blit(sprite.image, sprite.rect)

            # Draw checkpoints
            for checkpoint in checkpoints:
                screen.blit(checkpoint_img, checkpoint)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:  # If 'D' key is pressed, move the sprite to the right
                if sprite.rect.x < SCREEN_WIDTH - sprite.rect.width:  # Prevent sprite from moving off screen
                    sprite.move_right(5)

            # If the sprite has reached the next checkpoint in the list and there are remaining scenarios, present the next scenario
            if (abs(sprite.rect.x - checkpoints[checkpoint_index][0]) < 5 and abs(sprite.rect.y - checkpoints[checkpoint_index][1]) < 5) and scenario_index < len(scenarios):
                scenario_text, options = scenarios[scenario_index]
                player_choice = show_scenario(scenario_text, options)
                # Update emotional intelligence score based on the player's choice
                emotional_intelligence_score += 3 - player_choice
                scenario_index += 1
                checkpoint_index += 1  # Move to the next checkpoint

            # If we've presented all the scenarios, show the end screen
            if scenario_index == len(scenarios):
                end_screen(emotional_intelligence_score)
                break  # This should exit the inner while loop and return to the main menu loop

            pygame.display.flip()

# End screen
def end_screen(score):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Press "r" to restart the game
                    main()
                elif event.key == pygame.K_q:  # Press "q" to quit the game
                    pygame.quit()
                    sys.exit()

        # Draw the end screen
        screen.blit(end_screen_img, (0, 0))  # Draw the end screen image

        font = pygame.font.Font(FONT_PATH, 36)
        text_surface = font.render(f"Your emotional intelligence score is: {score}", True, BLACK)
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT // 2 - text_surface.get_height() // 2))

        text_surface = font.render("Press 'R' to restart or 'Q' to quit", True, BLACK)
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT // 2 - text_surface.get_height() // 2 + 50))

        pygame.display.flip()

if __name__ == "__main__":
    main()