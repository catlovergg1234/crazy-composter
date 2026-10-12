# Crazy Composter'ı size sunmak için birkaç ay boyunca çalışıyoruz. Bu oyun için çok uğraştık.
# İyi Oyunlar Dileriz! ^_^

#!/usr/bin/env python3

import pygame
import sys
import random
import json
import os


script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

pygame.init()

clock = pygame.time.Clock()
pygame.display.set_icon(pygame.image.load("composter.png"))
POINT_GET = pygame.USEREVENT
do_break = False
img_files = ["apple.png", "carrot.png", "egg.png", "grass.png", "leaf.png", "wheat.png", "metal.png", "milk.png", "naylon.png", "plastic.png", "paper.png", "bone.png", "glass.png", "coin.png"]
img_test = ["apple.png", "carrot.png", "egg.png", "grass.png", "leaf.png", "wheat.png", "metal.png", "milk.png", "naylon.png", "plastic.png", "paper.png", "bone.png", "glass.png"]
point_dict = {
    "apple.png": 2, "carrot.png": 2, "egg.png": 2, "grass.png": 1, "leaf.png": 1, "wheat.png": 2, "metal.png": -3, "glass.png": -3, "bone.png": -3, "milk.png": -2, "naylon.png": -2,
    "plastic.png": -2, "paper.png": -1, "coin.png": 0
}
with open("data.json", "r") as f:
    data = json.load(f)
percentages = [data["max_per"]]
scores = [data["high_score"]]
money = data["money"]
points_2 = data["points"]
speed_boosts_left = data["speed_boosts"]
version = data["version"]
def save():
    pygame.quit()
    with open("data.json", "w") as f:
        json.dump({"high_score": max(scores),
                   "max_per": max(percentages),
                   "money": money,
                   "points": points_2,
                   "speed_boosts": speed_boosts_left,
                   "version": version}, f)
def fixed_max(li):
    big = li[0]
    for i in li[1:]:
        if i > big:
            big = i
    return big
def exists(var):
    return (var in locals()) or (var in globals())
items_existed = []
run = True
in_main_menu = True
speed_boost_activated = False
coin_img = pygame.image.load("coin.png")
coin_img = pygame.transform.scale_by(coin_img, 1/40)
point_img = pygame.image.load("point.png")
point_img = pygame.transform.scale_by(point_img, 1/40)
speed_img = pygame.image.load("speed_boost.png")
speed_img = pygame.transform.scale_by(speed_img, 5 / 128)
width, height = 600, 600
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Crazy Composter")
font = pygame.font.SysFont("Comic Sans", 20)
coin_text_font = pygame.font.SysFont("Comic Sans", 30)
class Button:
    def __init__(self, pos: tuple[int, int], screenobj: pygame.Surface, fontobject: pygame.font.Font, topleft_border_radius = -1, topright_border_radius = -1, bottomleft_border_radius = -1, bottomright_border_radius = -1, hitbox="rect", width=100, height=50, text="", color: tuple[int, int, int]=(255, 255, 255), text_color: tuple[int, int, int] = (0, 0, 0), outline_color: tuple[int, int, int] = (0, 0, 0), outline_width=1):
        self.width = width
        self.height = height
        self.pos = pos
        self.text = text
        self.color = color
        self.fontobject = fontobject
        self.text_color = text_color
        self.hitbox = hitbox
        if self.hitbox == "rect":
            self.bottom_right_rad = bottomright_border_radius
            self.top_left_rad = topleft_border_radius
            self.top_right_rad = topright_border_radius
            self.bottom_left_rad = bottomleft_border_radius
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.screenobj = screenobj
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.size = 100
        if hitbox not in ['rect', 'ellipse']:
            raise ValueError("Hitbox must be 'rect' or 'ellipse'.")
    def is_clicked(self):
        return self.is_on_hover() and any(pygame.mouse.get_pressed())
    def draw(self):
        if self.hitbox == 'ellipse':
            pygame.draw.ellipse(self.screenobj, self.color, self.rect, width=0)
            pygame.draw.ellipse(self.screenobj, self.outline_color, self.rect, width=self.outline_width)
            text_rendered = self.fontobject.render(self.text, True, self.text_color)
            text_rect = text_rendered.get_rect(center=self.rect.center)
            self.screenobj.blit(text_rendered, text_rect)
        if self.hitbox == 'rect':
            pygame.draw.rect(self.screenobj, self.color, self.rect, border_bottom_left_radius=self.bottom_left_rad, border_bottom_right_radius=self.bottom_right_rad, border_top_right_radius=self.top_right_rad, border_top_left_radius=self.top_left_rad)
            pygame.draw.rect(self.screenobj, self.outline_color, self.rect, width = self.outline_width, border_bottom_left_radius=self.bottom_left_rad, border_bottom_right_radius=self.bottom_right_rad, border_top_right_radius=self.top_right_rad, border_top_left_radius=self.top_left_rad)
            text_rendered = self.fontobject.render(self.text, True, self.text_color)
            text_rect = text_rendered.get_rect(center=self.rect.center)
            self.screenobj.blit(text_rendered, text_rect)
    def is_on_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.hitbox == 'ellipse':
            dx = mouse_pos[0] - self.rect.centerx
            dy = mouse_pos[1] - self.rect.centery
            rx = self.rect.width / 2
            ry = self.rect.height / 2
            return (dx**2) / (rx**2) + (dy**2) / (ry**2) <= 1
        if self.hitbox == 'rect':
            return (mouse_pos[0] > self.pos[0]) and (mouse_pos[0] < self.pos[0] + self.width) and (mouse_pos[1] > self.pos[1]) and (mouse_pos[1] < self.pos[1] + self.height)
class ImgBasedButton:
    def __init__(self, pos, img, screen_obj):
        self.pos = pos
        self.img = img
        self.rendered_image = pygame.image.load(self.img)
        self.screen_obj = screen_obj
        self.width = self.rendered_image.get_width()
        self.height = self.rendered_image.get_height()
        self.origin = pygame.image.load(self.img)
    def draw(self):
        self.screen_obj.blit(self.rendered_image, self.pos)
    def is_on_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        return mouse_pos[0] >= self.pos[0] and mouse_pos[0] <= self.pos[0] + self.width and mouse_pos[1] >= self.pos[1] and mouse_pos[1] <= self.pos[1] + self.height
    def is_clicked(self):
        return self.is_on_hover() and any(pygame.mouse.get_pressed())
    def scale(self, factor):
        genislik, yukseklik = self.origin.get_size()
        new_width = int(genislik * factor)
        new_height = int(yukseklik * factor)
        # Always reload from the file only once
        if not hasattr(self, '_original_loaded'):
            self.origin = pygame.image.load(self.img).convert_alpha()
            self._original_loaded = True
        scaled_image = pygame.transform.scale(self.origin, (new_width, new_height))
        self.rendered_image = scaled_image
        self.width = new_width
        self.height = new_height
    def update(self):
        self.origin = pygame.image.load(self.img)
class Composter:
    def __init__(self, pos, screen_obj):
        self.img = pygame.image.load("composter.png")
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.pos = pos
        self.hitbox = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.screen = screen_obj
        self.all_coords = []
        self.mask = pygame.mask.from_surface(self.img)
        self.origin = self.img
    def draw(self):
        self.update()
        self.screen.blit(self.img, self.hitbox)
    def update(self):
        self.hitbox = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
    def scale(self, factor):
        genislik, yukseklik = self.origin.get_size()
        self.img = pygame.transform.scale(self.img, (int(genislik * factor), int(yukseklik * factor)))
        self.width *= factor
        self.height *= factor
        self.width = int(self.width)
        self.height = int(self.height)
        self.all_coords = []
        self.mask = pygame.mask.from_surface(self.img)
class Item:
    def __init__(self):
        self.pos = [random.randint(-20, 520), 0]
        self.type = random.choice(img_files)
        self.good = point_dict[self.type] > 0
        self.img = pygame.image.load(self.type)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.all_coords = []
        self.origin = self.img
        self.scale_number = 1
        self.mask =  pygame.mask.from_surface(self.img)
        self.caught = False
    def draw(self):
        screen.blit(self.img, self.pos)
    def scale(self, factor):
        genislik, yukseklik = self.origin.get_size()
        self.img = pygame.transform.scale(self.img, (int(genislik * factor), int(yukseklik * factor)))
        self.width *= factor
        self.height *= factor
        self.width = int(self.width)
        self.height = int(self.height)
        self.scale_number = factor
        self.mask = pygame.mask.from_surface(self.img)
    def has_overlap(self):
        return self.mask.overlap(composter.mask, (self.pos[0] - composter.pos[0], self.pos[1] - composter.pos[1]))
class TestItem(Item):
    def __init__(self):
        self.pos = [random.randint(-20, 520), 0]
        self.type = random.choice(img_test)
        self.good = point_dict[self.type] > 0
        self.img = pygame.image.load(self.type)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.all_coords = []
        self.origin = self.img
        self.scale_number = 1
        self.mask =  pygame.mask.from_surface(self.img)
        self.caught = False
class Counter:
    def __init__(self):
        self.font = pygame.font.SysFont("Comic Sans", 30)
        self.text = ""
    def render_point(self, points, pos):
        points = str(points)
        self.text = "Puan: " + points
        rendered = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(rendered, pos)
class Timer:
    def __init__(self):
        self.font = pygame.font.SysFont("Comic Sans", 30)
        self.text = ""
    def render_time(self, time_left, pos):
        minutes = f"{time_left // 60}"
        seconds = f"{time_left % 60}"
        if int(minutes) < 10:
            minutes = "0" + minutes
        if int(seconds) < 10:
            seconds = "0" + seconds
        self.text = " Kalan Zaman: " + minutes + ":" + seconds
        rendered = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(rendered, pos)
class Notification:
    def __init__(self, wait, *text, color=(255, 255, 255), outline_color=(0, 0, 0), outline_width=1):
        self.wait = wait
        self.color = color
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.x = 10
        self.y = 3000
        self.start = pygame.time.get_ticks()
        self.appeared = False
        self.texts = text
        self.frozen = not bool(len(self.texts))
    def draw(self):
        rect = pygame.rect.Rect(self.x, self.y, 580, 50)
        count = 0
        pygame.draw.rect(screen, self.color, rect, border_bottom_left_radius=10, border_bottom_right_radius=10, border_top_left_radius=10, border_top_right_radius=10)
        pygame.draw.rect(screen, self.outline_color, rect, width = self.outline_width, border_bottom_left_radius=10, border_bottom_right_radius=10, border_top_right_radius=10, border_top_left_radius=10)
        for text in self.texts:
            screen.blit(font.render(text, True, (0, 0, 0)), (self.x, self.y + (15 * self.texts.index(text))))
    def unfreeze(self):
        self.frozen=False
    def update(self):
        if not self.frozen:
            if not self.appeared:
                self.y -= 5
            if self.y <= 540:
                self.y = 540
                self.appeared = True
            if abs((pygame.time.get_ticks() - self.start) // 1000) >= self.wait:
                self.y += 5
            self.draw()
        if self.y > 3000:
            self.frozen = True
    def reset(self):
        self.color = (255, 255, 255)
        self.outline_color = (0,0,0)
        self.outline_width = -1
        self.x = 10
        self.y = 3000
        self.start = pygame.time.get_ticks()
        self.appeared = False
        self.texts = ()
        self.frozen = True
class Slide:
    def __init__(self, texts, images):
        self.texts = texts
        self.images = images
        self.img_dict = {}
        self.index = 0
        for text in texts:
            self.img_dict[text] = images[texts.index(text)]
    def draw(self):
        selected_text = self.texts[self.index]
        selected_image = self.img_dict[selected_text]
        screen.blit(font.render(selected_text, True, (0, 0, 0)), (10, 50))
        screen.blit(selected_image, (10, 100))
class SlideSwitcher:
    """
    Do a circle for every selected item for slide.
    """
    def __init__(self, start_pos, rad, slide: Slide):
        self.slide = slide
        self.pos = start_pos
        self.rad = rad
    def draw(self):
        len(self.slide.texts)
img_list = [pygame.Surface((10, 10)) for i in range(6)]
item: Item
slide = Slide(["Oynamak için 'Oyna' butonuna tıklayın", "İyi şeyleri yakalayıp kötü şeyleri yakalamayın.", "Kompost kutusunu sola ve sağa hareket ettirmek için okları kullanın.", "İyi şeyleri yakalayınca puan kazanır, kötü şeyler yakalayınca puan kaybedersiniz.", "Doğruluğunuzu test etmek için 'Test' düğmesine tıklayın.", "Hızlandırıcıları kullanmak için boşluk tuşuna basın."], img_list)
slide_switch_button_left = Button((15, 240), screen, font, 10, 10, 10, 10, "rect", 30, 100, "")
slide_switch_button_right = Button((555, 240), screen, font, 10, 10, 10, 10, "rect", 30, 100, "")
marketplace_button = Button((375, 337), screen, font, text = "Market", outline_width = 2, hitbox = "ellipse")
test_button = Button((75, 300), screen, font, text="Test", outline_width = 2, hitbox = 'ellipse')
play_button = Button((261, 300), screen, font, text="Oyna", outline_width = 2, hitbox = 'ellipse')
how_to_play_button = Button((450, 300), screen, font, text="Nasıl Oynanır?", outline_width = 2, width=150, hitbox = 'ellipse')
how_to_play_text1 = font.render('Oynamak için "Oyna" butonuna tıklayın. İyi şeyleri yakalayın, kötü', True, (0, 0, 0))
how_to_play_text2 = font.render(' şeyleri yakalamayın. Kompost kutusunu sola ve sağa hareket et-', True, (0, 0, 0))
how_to_play_text3 = font.render('tirmek için okları kullanın. Puan kazanacak ve kaybedeceksiniz.', True, (0, 0, 0))
how_to_play_text4 = font.render('Doğruluğunuzu test etmek için "Test" düğmesine tıklayın. Hızlan-', True, (0, 0, 0))
how_to_play_text5 = font.render("dırıcılarınızı kullanmak için boşluk tuşuna basın.", True, (0, 0, 0))
pause_button = ImgBasedButton((5, 45), "pause.png", screen)
pause_button.scale(5 / 128)
main_menu_composter2 = pygame.image.load("composter.png")
main_menu_composter = pygame.transform.scale(main_menu_composter2, (300, 300))
main_menu_composter_rect = main_menu_composter.get_rect(center=(width // 2, height // 4))
composter = Composter([270, 525], screen)
high_scores_button = Button((150, 350), screen, font, text="Yüksek Skorlar", outline_width = 2, hitbox = 'ellipse', width = 160)
exit_button = ImgBasedButton((5, 0), "arrow.png", screen)
speed_purchase = Button((245, 200), screen, font, 10, 10, 10, 10, "rect", 125, 25, "400")
composter.scale(75 / 2048)
exit_button.scale(15 / 512)
counter = Counter()
timer = Timer()
items = []
pause = False
notification = Notification(3)
notif_needed = {"color": (255, 255, 255), "outline_color": (0, 0, 0), "outline_width": 1, "text": ["Welcome to Crazy Composter!"]}
while run:
    for event in pygame.event.get():
        if event.type == 256:
            save()
            sys.exit()
    screen.fill((255, 255, 255))
    if in_main_menu:
        test_button.draw()
        play_button.draw()
        marketplace_button.draw()
        if notif_needed:
            if not notification.texts:
                notification.unfreeze()
                notification.color = notif_needed["color"]
                notification.outline_color = notif_needed["outline_color"]
                notification.outline_width = notif_needed["outline_width"]
                notification.texts = notif_needed["text"]
        if not notification.frozen:
            notification.update()
        else:
            notif_needed = False
        screen.blit(main_menu_composter, main_menu_composter_rect)
        how_to_play_button.draw()
        high_scores_button.draw()
        pygame.display.update()
        if marketplace_button.is_clicked():
            in_loop = True
            while in_loop:
                screen.fill((255, 255, 255))
                for event in pygame.event.get():
                    if event.type == 256:
                        save()
                        sys.exit()
                if exit_button.is_clicked():
                    in_loop = False
                exit_button.draw()
                coin_text = coin_text_font.render(str(money), True, (0, 0, 0))
                coin_rect = coin_text.get_rect()
                point_text = coin_text_font.render(str(points_2), True, (0, 0, 0))
                point_rect = point_text.get_rect()
                speed_text = coin_text_font.render(str(speed_boosts_left), True, (0, 0, 0))
                speed_rect = speed_text.get_rect()
                screen.blit(coin_text, (475, 25))
                coin_rect.topleft = (475, 25)
                screen.blit(coin_img, coin_rect.topright)
                point_rect.topleft = (475, 75)
                screen.blit(point_text, (475, 75))
                screen.blit(point_img, point_rect.topright)
                screen.blit(speed_text, (475, 125))
                speed_rect.topleft = (475, 125)
                screen.blit(speed_img, speed_rect.topright)
                screen.blit(speed_img, (245, 100))
                speed_purchase.draw()
                purch_rect = font.render(speed_purchase.text, True, (0, 0, 0)).get_rect()
                purch_rect.center = (307, 212)
                purch_rect.top -= 3
                screen.blit(pygame.transform.scale_by(coin_img, 0.68), purch_rect.topright)
                if speed_purchase.is_clicked():
                    if money >= 400:
                        money -= 400
                        speed_boosts_left += 1
                        while speed_purchase.is_clicked():
                            for event in pygame.event.get():
                                if event.type == 256:
                                    save()
                                    sys.exit()
                pygame.display.update()
        if high_scores_button.is_clicked():
            WFC = True
            h_s_text = font.render(f"Yüksek Skor: {fixed_max(scores)}", True, (0, 0, 0))
            h_p_text = font.render(f"Yüksek Yüzde: {fixed_max(percentages)}", True, (0, 0, 0))
            while WFC:
                for event in pygame.event.get():
                    if event.type == 256:
                        save()
                        sys.exit()

                screen.fill((255, 120, 0))
                screen.blit(h_s_text, (263, 300))
                screen.blit(h_p_text, (263, 263))

                exit_button.draw()
                if exit_button.is_clicked():
                    WFC = False
                    in_main_menu = True

                pygame.display.update()
        if how_to_play_button.is_clicked():
            in_main_menu = False
            while not exit_button.is_clicked():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        save()
                        sys.exit()
                screen.fill((255, 255, 255))
                keys = pygame.key.get_pressed()
                if slide_switch_button_right.is_clicked() and slide.index + 1 < len(slide.texts):
                    slide.index += 1
                    while slide_switch_button_right.is_clicked():
                        for event in pygame.event.get():
                            if event.type == 256:
                                save()
                                sys.exit()
                if slide_switch_button_left.is_clicked() and slide.index > 0:
                    slide.index -= 1
                    while slide_switch_button_left.is_clicked():
                        for event in pygame.event.get():
                            if event.type == 256:
                                save()
                                sys.exit()
                slide.draw()
                if slide.index != 0:
                    slide_switch_button_left.draw()
                if slide.index != len(slide.texts) - 1:
                    slide_switch_button_right.draw()
                exit_button.draw()
                pygame.display.update()
            in_main_menu = True
        if play_button.is_clicked():
            game = True
            points = 0
            ticks = 0
            start = pygame.time.get_ticks()
            time_paused = 0
            while game:
                ticks += 1
                for event in pygame.event.get():
                    if event.type == 256:
                        save()
                        sys.exit()
                    if event.type == POINT_GET:
                        points += event.point
                        if points < 0:
                            points = 0
                screen.fill((255, 255, 255))
                keys = pygame.key.get_pressed()
                boost_factor = 2 if speed_boost_activated else 1
                if keys[pygame.K_RIGHT]:
                    composter.pos[0] += boost_factor
                if keys[pygame.K_LEFT]:
                    composter.pos[0] -= boost_factor
                if keys[pygame.K_SPACE]:
                    if not speed_boost_activated:
                        if speed_boosts_left:
                            speed_boost_activated = True
                            speed_boosts_left -= 1
                if composter.pos[0] < 5:
                    composter.pos[0] = 5
                elif composter.pos[0] > 525:
                    composter.pos[0] = 525
                pause_button.draw()
                if pause_button.is_clicked():
                    pause = True
                    big_font = pygame.font.SysFont("Comic Sans", 60)
                    text = big_font.render("DURDURULDU", True, (0, 0, 0))
                    rect = text.get_rect(center=(300, 300))
                    pause_button.img = "start.png"
                    pause_button.update()
                    pause_button.scale(5 / 128)
                    while pause:
                        while pause_button.is_clicked():
                            for event in pygame.event.get():
                                if event.type == 256:
                                    save()
                                    sys.exit()
                            screen.fill((255, 255, 255))
                            screen.blit(text, rect)
                            pause_button.draw()
                            pygame.display.update()
                        for event in pygame.event.get():
                            if event.type == 256:
                                save()
                                sys.exit()
                        if pause_button.is_clicked():
                            pause_button.img = "pause.png"
                            pause_button.update()
                            pause_button.scale(5 / 128)
                            pause = False
                            while pause_button.is_clicked():
                                for event in pygame.event.get():
                                    if event.type == 256:
                                        save()
                                        sys.exit()
                            break
                        screen.fill((255, 255, 255))
                        screen.blit(text, rect)
                        pause_button.draw()
                        pygame.display.update()
                if ticks == 400:
                    items.append(Item())
                    ticks = 0
                for item in items:
                    if not item.scale == 9 / 160:
                        item.scale(9/160)
                    item.pos[1] += 1.5
                    if item.pos[1] > 550:
                        del items[items.index(item)]
                    if item.has_overlap():
                        if item.type == "coin.png":
                            money += 1
                        del items[items.index(item)]
                        pygame.event.post(pygame.event.Event(POINT_GET, {"point" : point_dict[item.type]}))
                    item.draw()
                composter.draw()
                counter.render_point(points, (50, 30))
                if 60 - ((pygame.time.get_ticks() - start) // 1000) == 0:
                    money += int((9 * points) / 2)
                    speed_boost_activated = False
                    points_2 += points
                    in_main_menu = True
                    scores.append(points)
                    high_score = str(max(scores))
                    high_score_text = font.render(f"Yüksek Skor: {high_score}", True, (0, 0, 0))
                    start2 = pygame.time.get_ticks()
                    waiting = True
                    score = font.render(f"Skor: {points}", True, (0, 0, 0))
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == 256:
                                save()
                                sys.exit()
                        screen.fill((64, 224, 208))
                        screen.blit(score, (300, 300))
                        screen.blit(high_score_text, (300, 337))
                        if (pygame.time.get_ticks() - start2) // 1000 == 5:
                            game = False
                            break
                        pygame.display.update()
                    waiting = False
                    break
                timer.render_time(60 - ((pygame.time.get_ticks() - start) // 1000), (325, 22))
                pygame.display.update()
                clock.tick(330)
        if test_button.is_clicked():
            game = True
            total_items = 0
            correct_items_caught = 0
            speed_boost_activated = False
            ticks = 0
            start = pygame.time.get_ticks()
            while game:
                ticks += 1
                for event in pygame.event.get():
                    if event.type == 256:
                        save()
                        sys.exit()
                screen.fill((255, 255, 255))
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RIGHT]:
                    composter.pos[0] += boost_factor
                if keys[pygame.K_LEFT]:
                    composter.pos[0] -= boost_factor
                if composter.pos[0] < 5:
                    composter.pos[0] = 5
                elif composter.pos[0] > 520:
                    composter.pos[0] = 520
                if keys[pygame.K_SPACE]:
                    if speed_boosts_left and not speed_boost_activated:
                        speed_boost_activated = True
                        speed_boosts_left -= 1
                composter.draw()
                boost_factor = 2 if speed_boost_activated else 1
                pause_button.draw()
                if pause_button.is_clicked():
                    pause = True
                    big_font = pygame.font.SysFont("Comic Sans", 60)
                    text = big_font.render("DURDURULDU", True, (0, 0, 0))
                    rect = text.get_rect(center=(300, 300))
                    pause_button.img = "start.png"
                    pause_button.update()
                    pause_button.scale(5 / 128)
                    while pause:
                        while pause_button.is_clicked():
                            for event in pygame.event.get():
                                if event.type == 256:
                                    save()
                                    sys.exit()
                            screen.fill((255, 255, 255))
                            screen.blit(text, rect)
                            pause_button.draw()
                            pygame.display.update()
                        for event in pygame.event.get():
                            if event.type == 256:
                                save()
                                sys.exit()
                        if pause_button.is_clicked():
                            pause_button.img = "pause.png"
                            pause_button.update()
                            pause_button.scale(5 / 128)
                            pause = False
                            while pause_button.is_clicked():
                                for event in pygame.event.get():
                                    if event.type == 256:
                                        save()
                                        sys.exit()
                            break
                        screen.fill((255, 255, 255))
                        screen.blit(text, rect)
                        pause_button.draw()
                        pygame.display.update()
                        clock.tick(330)
                if ticks == 400:
                    item = TestItem()
                    items_existed.append(item)
                    items.append(item)
                    total_items += 1
                    ticks = 0
                for item in items:
                    if not item.scale == 9 / 160:
                        item.scale(9/160)
                    item.pos[1] += 1.5
                    if item.pos[1] > 550:
                        del items[items.index(item)]
                    if item.has_overlap():
                        items[items.index(item)].caught = True
                        del items[items.index(item)]
                    item.draw()
                if 60 - ((pygame.time.get_ticks() - start) // 1000) == 0:
                    in_main_menu = True
                    for item in items_existed:
                        if item.caught:
                            if item.good:
                                correct_items_caught += 1
                        else:
                            if not item.good:
                                correct_items_caught += 1
                    score = (100 * correct_items_caught) // total_items
                    speed_boost_activated = False
                    percentages.append(score)
                    max_per = max(percentages)
                    max_per_text = font.render(f"Yüksek Yüzde: {max_per}", True, (0, 0, 0))
                    start2 = pygame.time.get_ticks()
                    waiting = True
                    score_text = font.render(f"Yüzde: {score}", True, (0, 0, 0))
                    items_existed = []
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == 256:
                                save()
                                sys.exit()
                        screen.fill((64, 224, 208))
                        screen.blit(score_text, (300, 300))
                        screen.blit(max_per_text, (300, 337))
                        if (pygame.time.get_ticks() - start2) // 1000 == 5:
                            game = False
                            break
                        pygame.display.update()
                    waiting = False
                    break
                timer.render_time(60 - ((pygame.time.get_ticks() - start) // 1000), (325, 22))
                pygame.display.update()
                clock.tick(330)
        test_button.draw()
        play_button.draw()
        how_to_play_button.draw()
    pygame.display.update()