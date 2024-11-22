import pygame

# Couleurs
BACKGROUND_COLOR = (240, 240, 240) 
BUTTON_COLOR = (96, 165, 250)       # Blue-400
BUTTON_HOVER_COLOR = (59, 130, 246) # Blue-500
BUTTON_SELECTED_COLOR = (74, 222, 128)  # Green-400
TEXT_COLOR = (0, 0, 0)
TEXT_WHITE = (255, 255, 255)
INPUT_COLOR = (255, 255, 255)
INPUT_ACTIVE_COLOR = (220, 220, 220)

# Initialisation de Pygame et création de la police de taille 15
pygame.init()
small_font = pygame.font.Font(None, 15)

def draw_text(screen, text, x, y, font=small_font, color=TEXT_COLOR, center=True):
    """Dessine du texte centré ou aligné."""
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y)) if center else (x, y)
    screen.blit(surface, rect)

def draw_button(screen, text, x, y, width, height, font=small_font, is_hovered=False, is_selected=False):
    """Dessine un bouton avec gestion des états (normal, survolé, sélectionné)."""
    if is_selected:
        button_color = BUTTON_SELECTED_COLOR
    elif is_hovered:
        button_color = BUTTON_HOVER_COLOR
    else:
        button_color = BUTTON_COLOR

    pygame.draw.rect(screen, button_color, (x, y, width, height), border_radius=10)
    draw_text(screen, text, x + width // 2, y + height // 2, font)

def draw_placeholder(screen, rect, font, text="", color=TEXT_COLOR):
    """Dessine un placeholder centré à l'intérieur d'une boîte."""
    surface = font.render(text, True, color)
    
    # Calculer le rectangle du texte pour le centrer
    text_rect = surface.get_rect(center=rect.center)  # Centrer le texte dans le rectangle
    screen.blit(surface, text_rect)

    
def draw_input_box(screen, rect, font=small_font, text="", active=False, placeholder=""):
    """Dessine une boîte de saisie."""
    color = INPUT_ACTIVE_COLOR if active else INPUT_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=10)
    # Si le champ est vide et non actif, dessiner le placeholder
    if not text and not active:
        draw_placeholder(screen, rect, font, placeholder, TEXT_COLOR)
    else:
        draw_placeholder(screen, rect, font, text, TEXT_COLOR)