import pygame
import sys
from uiComponents import draw_text, draw_button, draw_input_box
from gameEngine import create_puzzle, astar_solver  # Assure-toi que astar_solver est bien importé

# Dimensions de la fenêtre
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 400

# Initialisation de Pygame
pygame.init()
font = pygame.font.Font(None, 25)
title_font = pygame.font.Font(None, 30)

def menu_selection(screen):
    """Affiche une interface conviviale pour choisir les options."""
    selected_grid_size = None  # Valeur sélectionnée : 3 ou 4
    k_value = ""  # Saisie initiale
    input_active = False  # Indique si le champ de saisie est actif

    button_width, button_height = 250, 50
    menu_running = True
    while menu_running:
        screen.fill((240, 240, 240))  # Gris clair pour le fond

        # Titre
        draw_text(screen, "Choisissez les options du jeux", WINDOW_WIDTH // 2.5, 50, title_font)

        # Boutons pour la taille du puzzle
        button_3_rect = pygame.Rect(80, 80, button_width, button_height)  # Premier bouton
        button_4_rect = pygame.Rect(80, 140, button_width, button_height)  # Deuxième bouton, décalé verticalement

        mouse_pos = pygame.mouse.get_pos()
        button_3_hover = button_3_rect.collidepoint(mouse_pos)
        button_4_hover = button_4_rect.collidepoint(mouse_pos)

        draw_button(
            screen, 
            "8-puzzle", 
            button_3_rect.x, 
            button_3_rect.y, 
            button_width, 
            button_height, 
            font, 
            is_hovered=button_3_hover, 
            is_selected=(selected_grid_size == 3)
        )
        draw_button(
            screen, 
            "15-puzzle", 
            button_4_rect.x, 
            button_4_rect.y, 
            button_width, 
            button_height, 
            font, 
            is_hovered=button_4_hover, 
            is_selected=(selected_grid_size == 4)
        )

        # Label pour K
        label_x = 80
        label_y = 200  # La position Y du texte
        text_height = font.size("Nombre de tour avant swap?")[1]  # Calculer la hauteur du texte
        label_bottom_y = label_y + text_height  # Le bas du texte

        draw_text(screen, "Nombre de tour avant swap?", label_x, label_y, font, center=False)

        # Champ de saisie pour K
        input_x = label_x # Décalage horizontal pour aligner à droite du texte
        input_y = label_bottom_y + 10  # Aligner au bas du texte
        input_rect = pygame.Rect(input_x, input_y, 250, 50)  # Ajustez la largeur si nécessaire
        draw_input_box(screen, input_rect, font, k_value, input_active, placeholder="(exemple: 5)")

        # Bouton "Commencer"
        start_button_rect = pygame.Rect(label_x, 300, button_width, button_height)
        start_hover = start_button_rect.collidepoint(mouse_pos)
        draw_button(screen, "Commencer le jeu", start_button_rect.x, start_button_rect.y, button_width, button_height, font, is_hovered=start_hover)

        # Bouton "IA"
        startAi_button_rect = pygame.Rect(label_x, 360, button_width, button_height)
        startAi_hover = startAi_button_rect.collidepoint(mouse_pos)
        draw_button(screen, "IA", startAi_button_rect.x, startAi_button_rect.y, button_width, button_height, font, is_hovered=startAi_hover)

        pygame.display.flip()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_3_rect.collidepoint(event.pos):
                    selected_grid_size = 3
                elif button_4_rect.collidepoint(event.pos):
                    selected_grid_size = 4
                elif input_rect.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False
                if start_button_rect.collidepoint(event.pos):
                    if selected_grid_size and k_value.isdigit() and int(k_value) > 0:
                        return selected_grid_size, int(k_value), False  # Mode manuel
                    else:
                        print("Veuillez sélectionner une taille de puzzle et entrer une valeur valide pour K.")
                elif startAi_button_rect.collidepoint(event.pos):
                    if selected_grid_size:
                        return selected_grid_size, int(k_value) if k_value.isdigit() else None, True  # Mode IA
                    else:
                        print("Veuillez sélectionner une taille de puzzle pour utiliser l'IA.")
            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    k_value = k_value[:-1]
                elif event.unicode.isdigit():
                    k_value += event.unicode

    return selected_grid_size, int(k_value) if k_value.isdigit() else None, False  # Valeurs par défaut pour mode manuel
