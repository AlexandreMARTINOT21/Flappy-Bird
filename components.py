import pygame
import random
import assets

class Ground:
    # Set initially to default, but we should update this based on assets!
    # However, class attributes are static. We can update it in Init or make it dynamic.
    # But Pipes accesses it as Ground.ground_level
    # Let's set it to a safe value or rely on config.
    # Wait, config imports components. Components imports assets.
    # assets.load_assets() is called in main.
    # So when components is imported, assets.GROUND_IMG is None.
    # We must construct Ground AFTER load_assets.
    # In main.py: `ground = components.Ground(...)` is in `config.py`?
    # NO: `config.py` does `ground = components.Ground(win_width)`.
    # `config.py` is imported at top of `main.py`.
    # So `Ground` is instantiated BEFORE `main()` runs and BEFORE `load_assets`.
    # This means `draw` works because it looks up `assets.GROUND_IMG` later.
    # BUT `ground_level` is needed for Pipes which are spawned later.
    # We can update `Ground.ground_level` inside `Ground.draw` (hacky) or
    # explicitly set it in `main.py` after loading assets.
    # BETTER: Set it in `main.py`.
    ground_level = 500
    
    def __init__(self, win_width):
        self.x = 0
        # self.y will be set correctly in update or draw or we just update y here?
        # If we update ground_level later, we need to update self.y too.
        self.y = Ground.ground_level 
        self.rect = pygame.Rect(self.x, self.y, win_width, 112) # 112 is approx height, will override

    def draw(self, window):
        # Tile the ground image to cover the window width
        img_width = assets.GROUND_IMG.get_width()
        # We need two images to create a seamless scrolling effect usually, 
        # or just tile enough to cover. For now, simple tiling based on x position.
        # Since I don't control scrolling variable here easily (it's in loop), 
        # I'll just draw enough tiles starting from 0.
        # Ideally, we should receive an offset or handle scrolling here.
        # But per current logic, ground doesn't seem to scroll in `update` (it has no update).
        # Let's just draw it static or make it scroll if requested.
        # The user said "ground should slide at same speed as pipes".
        # Current code has no ground update. I should add `update` to Ground or handle it in main.
        # For now, let's just implement the draw using the image.
        
        # We'll just draw it repeated. To make it scroll, we need an x offset.
        # I will change this to use `self.x` which I can update.
        
        # Draw tiles
        for i in range(int(self.rect.width / img_width) + 2):
            window.blit(assets.GROUND_IMG, (self.x + i * img_width, self.y))

    def update(self):
        # Move ground
        self.x -= 1 # Matched pipe speed
        
        # Reset position for seamless loop
        img_width = assets.GROUND_IMG.get_width()
        if self.x <= -img_width:
            self.x = 0


class Pipes:
    width = 52 # Updated from 15
    opening = 100

    def __init__(self, win_width, pipe_type='normal'):
        self.x = win_width
        self.type = pipe_type
        
        # Ranges for height to ensure no "floating" with proportional scale (~416px image height)
        self.bottom_height = random.randint(100, 400) 
        self.top_height = Ground.ground_level - self.bottom_height - self.opening
        
        self.bottom_rect, self.top_rect = pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0)
        self.passed = False
        self.off_screen = False
        
        # Moving pipe properties
        self.vel_y = 0
        self.speed_direction = 0 # 1 UP, -1 DOWN, 0 NONE
        if self.type == 'moving':
            self.vel_y = random.choice([-1, -0.5, 0.5, 1])
            self.speed_direction = -1 if self.vel_y > 0 else 1 # y+ is DOWN in pygame

    def draw(self, window):
        self.bottom_rect = pygame.Rect(self.x, Ground.ground_level - self.bottom_height, self.width, self.bottom_height)
        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        
        # Draw Normal/Moving pipes (same visual base)
        window.blit(assets.PIPE_BOTTOM_IMG, (self.x, self.bottom_rect.y))
        window.blit(assets.PIPE_TOP_IMG, (self.x, self.top_rect.bottom - assets.PIPE_TOP_IMG.get_height()))

    def update(self):
        # Horizontal movement
        self.x -= 1
        
        # Vertical movement for moving pipes
        if self.type == 'moving':
            self.bottom_height += self.vel_y
            self.top_height = Ground.ground_level - self.bottom_height - self.opening
            
            # Bounce logic
            if self.bottom_height > 400 or self.bottom_height < 100:
                self.vel_y *= -1
                self.speed_direction *= -1

        if self.x + Pipes.width <= 50:
            self.passed = True
        if self.x <= -self.width:
            self.off_screen = True