import pygame
from collections import deque
pygame.init()
# ---------------- WINDOW ----------------
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS Paint - Ultimate")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)
# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
colors = [
   (0, 0, 0), (128, 128, 128), (255, 255, 255),
   (255, 0, 0), (255, 165, 0), (255, 255, 0),
   (0, 255, 0), (0, 255, 255), (0, 0, 255),
   (128, 0, 128), (255, 0, 255), (165, 42, 42),
]
# ---------------- CANVAS ----------------
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)
undo_stack = deque(maxlen=5)
def save_state():
   undo_stack.append(canvas.copy())
def flood_fill(surface, x, y, target_color, replacement_color):
   if target_color == replacement_color:
       return
   width, height = surface.get_size()
   stack = [(x, y)]
   while stack:
       px, py = stack.pop()
       if px < 0 or px >= width or py < 0 or py >= height:
           continue
       current = surface.get_at((px, py))[:3]
       if current != target_color:
           continue
       surface.set_at((px, py), replacement_color)
       stack.extend([
           (px+1, py), (px-1, py),
           (px, py+1), (px, py-1)
       ])
# ---------------- STATE ----------------
drawing = False
current_color = BLACK
brush_size = 5
eraser = False
tool = "pen"
start_pos = None
# ---------------- PALETTE ----------------
color_buttons = []
for i, c in enumerate(colors):
   rect = pygame.Rect(10 + (i % 6) * 45, 10 + (i // 6) * 45, 40, 40)
   color_buttons.append((rect, c))
# ---------------- BUTTONS ----------------
eraser_btn = pygame.Rect(320, 10, 80, 40)
clear_btn = pygame.Rect(320, 60, 80, 40)
line_btn = pygame.Rect(420, 10, 80, 40)
rect_btn = pygame.Rect(420, 60, 80, 40)
circle_btn = pygame.Rect(520, 10, 80, 40)
fill_btn = pygame.Rect(520, 60, 80, 40)
plus_btn = pygame.Rect(620, 10, 40, 40)
minus_btn = pygame.Rect(670, 10, 40, 40)
save_btn = pygame.Rect(720, 10, 80, 40)
# ---------------- LOOP ----------------
running = True
while running:
   screen.fill(GRAY)
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False
       # ---------------- KEYBOARD ----------------
       if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
               if undo_stack:
                   canvas = undo_stack.pop()
       # ---------------- MOUSE DOWN ----------------
       if event.type == pygame.MOUSEBUTTONDOWN:
           pos = event.pos
           drawing = True
           start_pos = pos
           save_state()
           # palette
           for rect, c in color_buttons:
               if rect.collidepoint(pos):
                   current_color = c
                   eraser = False
                   tool = "pen"
           if eraser_btn.collidepoint(pos):
               eraser = True
               tool = "pen"
           if clear_btn.collidepoint(pos):
               canvas.fill(WHITE)
           if line_btn.collidepoint(pos):
               tool = "line"
           if rect_btn.collidepoint(pos):
               tool = "rect"
           if circle_btn.collidepoint(pos):
               tool = "circle"
           if fill_btn.collidepoint(pos):
               tool = "fill"
           if plus_btn.collidepoint(pos):
               brush_size += 2
           if minus_btn.collidepoint(pos):
               brush_size = max(2, brush_size - 2)
           if save_btn.collidepoint(pos):
               pygame.image.save(canvas, "drawing.png")
               print("Saved!")
           # fill tool
           if tool == "fill":
               target = canvas.get_at(pos)[:3]
               flood_fill(canvas, pos[0], pos[1], target, current_color)
       # ---------------- MOUSE UP ----------------
       if event.type == pygame.MOUSEBUTTONUP:
           drawing = False
           if tool == "line" and start_pos:
               pygame.draw.line(canvas, current_color, start_pos, event.pos, brush_size)
           if tool == "rect" and start_pos:
               x = min(start_pos[0], event.pos[0])
               y = min(start_pos[1], event.pos[1])
               w = abs(start_pos[0] - event.pos[0])
               h = abs(start_pos[1] - event.pos[1])
               pygame.draw.rect(canvas, current_color, (x, y, w, h), brush_size)
           if tool == "circle" and start_pos:
               radius = int(((event.pos[0]-start_pos[0])**2 + (event.pos[1]-start_pos[1])**2) ** 0.5)
               pygame.draw.circle(canvas, current_color, start_pos, radius, brush_size)
           start_pos = None
       # ---------------- DRAW ----------------
       if event.type == pygame.MOUSEMOTION:
           if drawing and tool == "pen":
               color = WHITE if eraser else current_color
               pygame.draw.circle(canvas, color, event.pos, brush_size)
   # ---------------- DRAW CANVAS ----------------
   screen.blit(canvas, (0, 0))
   # ---------------- PALETTE ----------------
   for rect, c in color_buttons:
       pygame.draw.rect(screen, c, rect)
       pygame.draw.rect(screen, BLACK, rect, 2)
   # ---------------- UI ----------------
   pygame.draw.rect(screen, (220, 220, 220), eraser_btn)
   pygame.draw.rect(screen, (220, 220, 220), clear_btn)
   pygame.draw.rect(screen, (220, 220, 220), line_btn)
   pygame.draw.rect(screen, (220, 220, 220), rect_btn)
   pygame.draw.rect(screen, (220, 220, 220), circle_btn)
   pygame.draw.rect(screen, (220, 220, 220), fill_btn)
   pygame.draw.rect(screen, (220, 220, 220), plus_btn)
   pygame.draw.rect(screen, (220, 220, 220), minus_btn)
   pygame.draw.rect(screen, (220, 220, 220), save_btn)
   # ---------------- TEXT ----------------
   screen.blit(font.render("Eraser", True, BLACK), (325, 20))
   screen.blit(font.render("Clear", True, BLACK), (325, 70))
   screen.blit(font.render("Line", True, BLACK), (435, 20))
   screen.blit(font.render("Rect", True, BLACK), (435, 70))
   screen.blit(font.render("Circle", True, BLACK), (530, 20))
   screen.blit(font.render("Fill", True, BLACK), (530, 70))
   screen.blit(font.render("+", True, BLACK), (632, 12))
   screen.blit(font.render("-", True, BLACK), (685, 12))
   screen.blit(font.render("Save", True, BLACK), (735, 20))
   screen.blit(font.render(f"Brush: {brush_size}", True, BLACK), (620, 70))
   pygame.display.update()
   clock.tick(60)
pygame.quit()