import pygame

selected_atom = None
Vector2 = pygame.math.Vector2

class Atom():
    def __init__(self, type, image):
        self.type = image
        self.x = 400
        self.y = 200  
        self.xvel = 0
        self.yvel = 0

        self.rect = self.type.get_rect()
        self.rect.topleft = (self.x, self.y)

        self.dragging = False  
        self.offset = Vector2(0, 0)
        self.prev_pos = Vector2(self.x, self.y) 

    def check_dragging_priority(self, event):
        global selected_atom

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and selected_atom is None:
                
                self.dragging = True
                mousepos = pygame.mouse.get_pos()
                self.offset = Vector2(mousepos[0] - self.x, mousepos[1] - self.y)

                selected_atom = self

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                selected_atom = None

    # basically only free physics so change this later
    def physics(self):
        mousepos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # EVENTS
        if self.dragging:
            self.x = mousepos[0] - self.offset.x
            self.y = mousepos[1] - self.offset.y
            self.xvel = self.x - self.prev_pos.x
            self.yvel = self.y - self.prev_pos.y

        if not mouse_pressed:
            self.dragging = False  

        if not self.dragging:
            self.x += self.xvel
            self.y += self.yvel
            self.xvel *= 0.9
            self.yvel *= 0.9

        self.prev_pos = Vector2(self.x, self.y)
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.type, (self.x, self.y))
