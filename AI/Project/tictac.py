import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
BOARD_SIZE = 5
CELL_SIZE = 80
BOARD_WIDTH = BOARD_SIZE * CELL_SIZE
BOARD_HEIGHT = BOARD_SIZE * CELL_SIZE

# Adjusted Window Dimensions for better UI fit
# Increased width for more UI space, slightly increased height for overall balance
WINDOW_WIDTH = BOARD_WIDTH + 480  # Further increased
WINDOW_HEIGHT = BOARD_HEIGHT + 180 # Further increased

# Board Offsets to center it a bit or give it a margin
# Calculate to roughly center the board vertically, and give it a left margin
BOARD_OFFSET_X = 75
BOARD_OFFSET_Y = (WINDOW_HEIGHT - BOARD_HEIGHT) // 2 # Center board vertically

# Colors - Modern color palette
BACKGROUND = (15, 23, 42)  # Dark slate
BOARD_BG = (30, 41, 59)    # Slate
GRID_COLOR = (71, 85, 105)  # Slate 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player colors with gradients
PLAYER1_MAIN = (239, 68, 68)    # Red 500
PLAYER1_LIGHT = (248, 113, 113)  # Red 400
PLAYER1_DARK = (220, 38, 38)    # Red 600

PLAYER2_MAIN = (59, 130, 246)   # Blue 500
PLAYER2_LIGHT = (96, 165, 250)  # Blue 400
PLAYER2_DARK = (37, 99, 235)    # Blue 600

# UI Colors
ACCENT = (139, 92, 246)  # Violet 500
SUCCESS = (34, 197, 94)  # Green 500
HIGHLIGHT = (255, 215, 0)  # Gold
CARD_BG = (51, 65, 85)   # Slate 700
TEXT_PRIMARY = (248, 250, 252)  # Slate 50
TEXT_SECONDARY = (203, 213, 225)  # Slate 300
CARD_BORDER = (99, 102, 241, 100) # Indigo 400 with transparency for border

class BudhiChaal5x5:
    def __init__(self):
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 1
        self.game_phase = "placement"
        self.pieces_placed = {1: 0, 2: 0}
        self.max_pieces = 5  # 5 pieces per player for 5x5 board
        self.selected_piece = None
        self.winner = None
        self.hover_cell = None
        self.animation_time = 0
        
        # Fonts
        self.title_font = pygame.font.Font(None, 56) # Larger title
        self.font = pygame.font.Font(None, 36) # Slightly larger card titles
        self.small_font = pygame.font.Font(None, 26) # Slightly larger content font
        self.large_font = pygame.font.Font(None, 40)
        
        # Animation variables
        self.piece_scale = {}
        self.selection_pulse = 0
    
    def get_cell_from_pos(self, pos):
        """Convert mouse position to board cell coordinates"""
        x, y = pos
        # Adjust for board offset
        x -= BOARD_OFFSET_X
        y -= BOARD_OFFSET_Y

        if x < 0 or x >= BOARD_WIDTH or y < 0 or y >= BOARD_HEIGHT:
            return None
        col = x // CELL_SIZE
        row = y // CELL_SIZE
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return (row, col)
        return None
    
    def is_valid_move(self, from_pos, to_pos):
        """Check if movement is valid (adjacent cells only)"""
        if not to_pos or not from_pos:
            return False
        
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        if self.board[to_row][to_col] != 0:
            return False
        
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)
        
        return row_diff <= 1 and col_diff <= 1 and (row_diff + col_diff) > 0
    
    def check_winner(self):
        """Check if there's a winner (5 in a row)"""
        # Check rows
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE - 4):
                if all(self.board[row][col + i] == self.board[row][col] != 0 for i in range(5)):
                    return self.board[row][col]
        
        # Check columns
        for col in range(BOARD_SIZE):
            for row in range(BOARD_SIZE - 4):
                if all(self.board[row + i][col] == self.board[row][col] != 0 for i in range(5)):
                    return self.board[row][col]
        
        # Check diagonals
        for row in range(BOARD_SIZE - 4):
            for col in range(BOARD_SIZE - 4):
                if all(self.board[row + i][col + i] == self.board[row][col] != 0 for i in range(5)):
                    return self.board[row][col]
        
        for row in range(BOARD_SIZE - 4):
            for col in range(4, BOARD_SIZE):
                if all(self.board[row + i][col - i] == self.board[row][col] != 0 for i in range(5)):
                    return self.board[row][col]
        
        return None
    
    def handle_click(self, pos):
        """Handle mouse click based on current game phase"""
        cell = self.get_cell_from_pos(pos)
        if not cell:
            return
        
        row, col = cell
        
        if self.winner:
            return
        
        if self.game_phase == "placement":
            if self.board[row][col] == 0 and self.pieces_placed[self.current_player] < self.max_pieces:
                self.board[row][col] = self.current_player
                self.pieces_placed[self.current_player] += 1
                self.piece_scale[(row, col)] = 0  # Start animation
                
                if self.pieces_placed[1] == self.max_pieces and self.pieces_placed[2] == self.max_pieces:
                    self.game_phase = "movement"
                    self.winner = self.check_winner()
                    if self.winner:
                        return
                
                self.current_player = 2 if self.current_player == 1 else 1
        
        elif self.game_phase == "movement":
            if self.selected_piece is None:
                if self.board[row][col] == self.current_player:
                    self.selected_piece = (row, col)
            else:
                if self.is_valid_move(self.selected_piece, (row, col)):
                    old_row, old_col = self.selected_piece
                    self.board[old_row][old_col] = 0
                    self.board[row][col] = self.current_player
                    self.piece_scale[(row, col)] = 0
                    
                    self.winner = self.check_winner()
                    self.current_player = 2 if self.current_player == 1 else 1
                    self.selected_piece = None
                else:
                    # If clicking on own piece, re-select it; otherwise, deselect
                    if self.board[row][col] == self.current_player:
                        self.selected_piece = (row, col)
                    else:
                        self.selected_piece = None
    
    def handle_hover(self, pos):
        """Handle mouse hover for UI feedback"""
        self.hover_cell = self.get_cell_from_pos(pos)
    
    def draw_gradient_circle(self, screen, center, radius, color_main, color_light):
        """Draw a circle with gradient effect"""
        for i in range(radius, 0, -1):
            alpha = i / radius
            color = (
                int(color_main[0] * alpha + color_light[0] * (1 - alpha)),
                int(color_main[1] * alpha + color_light[1] * (1 - alpha)),
                int(color_main[2] * alpha + color_light[2] * (1 - alpha))
            )
            pygame.draw.circle(screen, color, center, i)
    
    def draw_board(self, screen):
        """Draw the game board with modern styling"""
        # Draw board background with rounded corners
        board_rect = pygame.Rect(BOARD_OFFSET_X - 10, BOARD_OFFSET_Y - 10, BOARD_WIDTH + 20, BOARD_HEIGHT + 20)
        pygame.draw.rect(screen, BOARD_BG, board_rect, border_radius=15)
        
        # Draw subtle shadow
        shadow_rect = pygame.Rect(BOARD_OFFSET_X - 7, BOARD_OFFSET_Y - 7, BOARD_WIDTH + 20, BOARD_HEIGHT + 20)
        pygame.draw.rect(screen, (0, 0, 0, 50), shadow_rect, border_radius=15) # Darker shadow
        
        # Draw grid with modern styling
        for i in range(BOARD_SIZE + 1):
            # Vertical lines
            start_pos = (BOARD_OFFSET_X + i * CELL_SIZE, BOARD_OFFSET_Y)
            end_pos = (BOARD_OFFSET_X + i * CELL_SIZE, BOARD_OFFSET_Y + BOARD_HEIGHT)
            pygame.draw.line(screen, GRID_COLOR, start_pos, end_pos, 2)
            
            # Horizontal lines
            start_pos = (BOARD_OFFSET_X, BOARD_OFFSET_Y + i * CELL_SIZE)
            end_pos = (BOARD_OFFSET_X + BOARD_WIDTH, BOARD_OFFSET_Y + i * CELL_SIZE)
            pygame.draw.line(screen, GRID_COLOR, start_pos, end_pos, 2)
        
        # Draw hover effect
        if self.hover_cell and not self.winner:
            row, col = self.hover_cell
            is_valid_hover_for_placement = (self.game_phase == "placement" and self.board[row][col] == 0 and 
                                             self.pieces_placed[self.current_player] < self.max_pieces)
            is_valid_hover_for_movement = (self.game_phase == "movement" and self.selected_piece is not None and
                                            self.is_valid_move(self.selected_piece, (row, col)))
            
            if is_valid_hover_for_placement or is_valid_hover_for_movement:
                center_x = BOARD_OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
                center_y = BOARD_OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.circle(screen, (*HIGHLIGHT, 150), (center_x, center_y), 25, 4) # Brighter, thicker hover
        
        # Draw pieces with animations
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                center_x = BOARD_OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
                center_y = BOARD_OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2
                
                if self.board[row][col] != 0:
                    # Animate piece placement
                    scale = self.piece_scale.get((row, col), 1.0)
                    if scale < 1.0:
                        scale = min(1.0, scale + 0.1)
                        self.piece_scale[(row, col)] = scale
                    
                    radius = int(25 * scale)
                    
                    if self.board[row][col] == 1:
                        self.draw_gradient_circle(screen, (center_x, center_y), radius, 
                                                PLAYER1_MAIN, PLAYER1_LIGHT)
                        # Add subtle glow
                        pygame.draw.circle(screen, (*PLAYER1_LIGHT, 80), (center_x, center_y), radius + 5, 2) # Brighter glow
                    else:
                        self.draw_gradient_circle(screen, (center_x, center_y), radius, 
                                                PLAYER2_MAIN, PLAYER2_LIGHT)
                        pygame.draw.circle(screen, (*PLAYER2_LIGHT, 80), (center_x, center_y), radius + 5, 2) # Brighter glow
                
                # Highlight selected piece with pulsing effect
                if self.selected_piece == (row, col):
                    pulse_radius = 30 + int(7 * math.sin(self.selection_pulse)) # More prominent pulse
                    pygame.draw.circle(screen, HIGHLIGHT, (center_x, center_y), pulse_radius, 4)
    
    def draw_card(self, screen, rect, title, content, color=CARD_BG, border_color=None):
        """Draw a modern card UI element with optional border"""
        # Draw card background with shadow
        shadow_offset = 5 # Increased shadow offset
        shadow_rect = pygame.Rect(rect.x + shadow_offset, rect.y + shadow_offset, rect.width, rect.height)
        pygame.draw.rect(screen, (0, 0, 0, 70), shadow_rect, border_radius=12) # Darker, slightly larger shadow
        
        pygame.draw.rect(screen, color, rect, border_radius=12) # Slightly larger border radius
        
        if border_color:
            pygame.draw.rect(screen, border_color, rect, border_radius=12, width=2) # Add border
        
        # Draw title - centered
        title_surface = self.font.render(title, True, TEXT_PRIMARY)
        title_rect = title_surface.get_rect(center=(rect.x + rect.width / 2, rect.y + 25)) # Center title
        screen.blit(title_surface, title_rect)
        
        # Draw content - adjust y_offset and line spacing
        y_offset = 55 # Start content below title
        line_height = 30 # Increased line spacing
        for line in content:
            text_surface = self.small_font.render(line, True, TEXT_SECONDARY)
            # Center content if it's a single line, otherwise left-align
            if len(content) == 1:
                 text_rect = text_surface.get_rect(center=(rect.x + rect.width / 2, rect.y + y_offset))
                 screen.blit(text_surface, text_rect)
            else:
                screen.blit(text_surface, (rect.x + 15, rect.y + y_offset))
            y_offset += line_height
    
    def draw_ui(self, screen):
        """Draw modern game UI"""
        # UI starts to the right of the board, with some padding
        UI_OFFSET_X = BOARD_OFFSET_X + BOARD_WIDTH + 70 # More space from board
        
        # Calculate vertical center point for the UI title
        title_text_height = self.title_font.get_height()
        title_x = UI_OFFSET_X
        title_y = BOARD_OFFSET_Y - title_text_height - 20 # Position above the very first card, aligned with board top
        
        # Game title
        title_surface = self.title_font.render("Budhi Chaal 5x5", True, TEXT_PRIMARY)
        title_rect = title_surface.get_rect(centerx=UI_OFFSET_X + 100) # Center title over the card column
        title_rect.top = 40 # Fixed top position for the main title
        screen.blit(title_surface, title_rect)

        # Start Y for the first UI card, after the title
        current_y = title_rect.bottom + 30 # Start cards below title

        card_width = 240 # Wider cards
        card_padding = 25 # Increased vertical space between cards
        
        # Game phase card
        phase_rect = pygame.Rect(UI_OFFSET_X, current_y, card_width, 80)
        phase_color = ACCENT if self.game_phase == "placement" else SUCCESS
        self.draw_card(screen, phase_rect, "Game Phase", 
                      [f"{self.game_phase.capitalize()}"], phase_color, CARD_BORDER)
        current_y += phase_rect.height + card_padding
        
        # Current player card
        if not self.winner:
            player_rect = pygame.Rect(UI_OFFSET_X, current_y, card_width, 80)
            player_color = PLAYER1_MAIN if self.current_player == 1 else PLAYER2_MAIN
            self.draw_card(screen, player_rect, "Current Player", 
                          [f"Player {self.current_player}"], player_color, CARD_BORDER)
            current_y += player_rect.height + card_padding
        
        # Pieces counter during placement
        if self.game_phase == "placement":
            pieces_rect = pygame.Rect(UI_OFFSET_X, current_y, card_width, 100)
            content = [
                f"Player 1: {self.pieces_placed[1]}/{self.max_pieces}",
                f"Player 2: {self.pieces_placed[2]}/{self.max_pieces}"
            ]
            self.draw_card(screen, pieces_rect, "Pieces Placed", content, CARD_BG, CARD_BORDER)
            current_y += pieces_rect.height + card_padding
        
        # Instructions card
        # This card should take the place of the "pieces placed" if game_phase is movement
        if self.game_phase == "movement" and not self.winner:
            inst_rect = pygame.Rect(UI_OFFSET_X, current_y, card_width, 100) # Ensure consistent height
            if self.selected_piece:
                instruction = ["Click adjacent cell", "to move piece"]
            else:
                instruction = ["Click your piece", "to select it"]
            self.draw_card(screen, inst_rect, "Instructions", instruction, CARD_BG, CARD_BORDER)
            current_y += inst_rect.height + card_padding
        
        # Winner announcement
        if self.winner:
            winner_rect = pygame.Rect(UI_OFFSET_X, current_y, card_width, 120)
            winner_color = PLAYER1_MAIN if self.winner == 1 else PLAYER2_MAIN
            content = [f"Player {self.winner} Wins!", "", "Press R to restart"]
            self.draw_card(screen, winner_rect, "Game Over", content, winner_color, CARD_BORDER)
            current_y += winner_rect.height + card_padding
        
        # Game rules card - always at the bottom, adjusting its Y to fill space nicely
        rules_card_height = 180 # Increased height for rules
        # Calculate starting y for the rules card, ensuring it fits and is aligned
        rules_rect_y = WINDOW_HEIGHT - BOARD_OFFSET_Y - rules_card_height - 10 # 10px margin from bottom
        
        rules_rect = pygame.Rect(UI_OFFSET_X, rules_rect_y, card_width, rules_card_height)
        rules_content = [
            "Rules:",
            "• Place 5 pieces each",
            "• Get 5 in a row to win",
            "• Move to adjacent cells",
            "• Strategic positioning!",
            "• Avoid 5-in-a-row for opponent!" # Added a rule for more content
        ]
        self.draw_card(screen, rules_rect, "How to Play", rules_content, CARD_BG, CARD_BORDER)
    
    def update_animations(self):
        """Update animation variables"""
        self.animation_time += 0.1
        self.selection_pulse += 0.2
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 1
        self.game_phase = "placement"
        self.pieces_placed = {1: 0, 2: 0}
        self.selected_piece = None
        self.winner = None
        self.piece_scale = {}
        self.selection_pulse = 0

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Budhi Chaal 5x5 - Beautiful Edition")
    clock = pygame.time.Clock()
    
    game = BudhiChaal5x5()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    game.handle_click(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEMOTION:
                game.handle_hover(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset_game()
        
        # Update animations
        game.update_animations()
        
        # Clear screen with gradient background
        screen.fill(BACKGROUND)
        
        # Draw game
        game.draw_board(screen)
        game.draw_ui(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()