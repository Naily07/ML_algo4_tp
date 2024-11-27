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


def get_gradient_color(start_color, end_color, t):
    """Calcule une couleur intermédiaire entre start_color et end_color."""
    r = int(start_color[0] + t * (end_color[0] - start_color[0]))
    g = int(start_color[1] + t * (end_color[1] - start_color[1]))
    b = int(start_color[2] + t * (end_color[2] - start_color[2]))
    return (r, g, b)


def draw_text_with_text_gradient(screen, text, x, y, font, start_color, end_color, center=True):
    """Dessine un texte où chaque caractère a un dégradé de couleurs."""
    # Calculer la largeur totale du texte pour centrer si nécessaire
    text_surface = font.render(text, True, (255, 255, 255))  # Texte blanc pour mesure
    text_width, text_height = text_surface.get_width(), text_surface.get_height()

    if center:
        x -= text_width // 2

    # Parcourir chaque caractère pour appliquer le dégradé
    for i, char in enumerate(text):
        char_surface = font.render(char, True, (255, 255, 255))  # Crée une surface pour le caractère
        char_width, char_height = char_surface.get_width(), char_surface.get_height()

        # Crée une surface pour le dégradé avec alpha
        gradient_surface = pygame.Surface((char_width, char_height), pygame.SRCALPHA)
        
        # Dessiner le dégradé ligne par ligne
        for j in range(char_width):
            t = j / char_width  # Interpolation (0 à 1)
            r = int(start_color[0] + t * (end_color[0] - start_color[0]))
            g = int(start_color[1] + t * (end_color[1] - start_color[1]))
            b = int(start_color[2] + t * (end_color[2] - start_color[2]))
            color = (r, g, b, 255)  # Ajout de l'alpha (255 pour opaque)
            pygame.draw.line(gradient_surface, color, (j, 0), (j, char_height))

        # Appliquer le dégradé sur la surface du caractère
        char_surface.blit(gradient_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Dessiner le caractère sur l'écran
        screen.blit(char_surface, (x, y))
        x += char_width  # Décaler pour le prochain caractère


def draw_text(screen, text, x, y, font=small_font, color=TEXT_COLOR, center=True):
    """Dessine du texte centré ou aligné."""
    print()
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