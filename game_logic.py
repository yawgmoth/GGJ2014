import brainfuck
import time
import pygame
import os

LEVEL_DIR = "levels"

def make_spawn(game):
    def spawn(*name):
        id = name[0]
        name = "".join(map(chr, name[1:]))
        if os.path.exists(os.path.join(RULE_DIR, name + ".update")):
            obj = GameObject(name, game)
            game.spawn(id, obj)
        return -1
    return spawn
    
def make_set_data(game):
    def set_data(*args):
        id = args[0]
        game.set_data(id, args[1:])
        return 0
    return set_data
    
def make_get_data(game):
    def get_data(*args):
        id = args[0]
        i = args[1]
        return game.get_data(id, i)
    return get_data
    
def make_get_data_len(game):
    def get_data_len(*args):
        id = args[0]
        return game.get_data_len(id, i)
    return get_data_len
    
def make_dozoom(game):
    def dozoom(*args):
        game.dozoom(args[0])
    return dozoom
    
def make_set_zoom(game):
    def set_zoom(*args):
        game.set_zoom(args[0])
    return set_zoom
    
def collide(a, b):
    return False

class Game(object):
    def __init__(self):
        self.objects = []
        self.obj_ids = {}
        self.current_zoom = 1
    def load_level(self, level):
        fname = os.path.join(LEVEL_DIR, level + ".lvl")
        if not os.path.exists(fname):
            return None
        self.objects = []
        sp = make_spawn(self)
        sd = make_set_data(self)
        gd = make_get_data(self)
        gl = make_get_data_len(self)
        dz = make_dozoom(self)
        sz = make_set_zoom(self)
        brainfuck.call_bf(brainfuck.get_content(fname), [], locals(), globals())
    def update(self, screen, left, right, space):
        for o in self.objects:
            o.update(self, screen, left, right, space)
        bbs = map(lambda o: [o, o.get_bb()], self.objects)
        for i,b in enumerate(bbs):
            for b1 in bbs[i+1:]:
                if collide(b[1], b1[1]):
                    b[0].collide(b1[0], self, screen)
                    b1[0].collide(b[0], self, screen)
    def spawn(self, id, what):
        self.objects.append(what)
        what.id = id
        self.obj_ids[id] = what
    def set_data(self, id, data):
        self.obj_ids[id].data = data
    def get_data(self, id, i):
        return self.obj_ids[id].data[i]
    def get_data_len(self, id):
        return len(self.obj_ids[id].data)
    def zoom(self, v):
        return v*self.current_zoom
    def dozoom(self, f):
        self.current_zoom *= f
    def set_zoom(self, z):
        self.current_zoom = z

RULE_DIR = "rules"

class GameObject:
    def __init__(self, name, game):
        self.update_code = brainfuck.get_content(os.path.join(RULE_DIR, name + ".update"))
        self.bounding_box = brainfuck.get_content(os.path.join(RULE_DIR, name + ".bb"))
        self.collide = brainfuck.get_content(os.path.join(RULE_DIR, name + ".col"))
        init_code = brainfuck.get_content(os.path.join(RULE_DIR, name + ".init"))
        self.t = time.time()
        sp = make_spawn(game)
        sd = make_set_data(game)
        gd = make_get_data(game)
        gl = make_get_data_len(game)
        dz = make_dozoom(game)
        sz = make_set_zoom(game)
        self.data = brainfuck.call_bf(init_code, [], locals(), globals())
    def update(self, game, screen, left, right, space):
        
        sp = make_spawn(game)
        sd = make_set_data(game)
        gd = make_get_data(game)
        gl = make_get_data_len(game)
        dz = make_dozoom(game)
        sz = make_set_zoom(game)
        def dr(*args):
            r,g,b = args[:3]
            x,y,w,h = args[3:7]
            width = args[7]
            pygame.draw.rect(screen, (r,g,b), pygame.Rect(game.zoom(x),game.zoom(y),game.zoom(w),game.zoom(h)), width)
        def txt(*args):
            size = args[0]
            r,g,b = args[1:4]
            x,y = args[4:6]
            txt = "".join(map(chr, args[6:-1]))
            font = pygame.font.Font(None, size)
            text = font.render(txt, 1, (r,g,b))
            screen.blit(text, (game.zoom(x),game.zoom(y)))
        def p(*args):
            print args
        t1 = time.time()
        self.data = brainfuck.call_bf(self.update_code, [t1-self.t, left, right, space, 0, 0, 0] + self.data, locals(), globals())
        self.t = t1
    def get_bb(self):
        return brainfuck.call_bf(self.bounding_box, self.data, locals(), globals())
    def collide(self, other, game, screen):
        sp = make_spawn(game)
        sd = make_set_data(game)
        gd = make_get_data(game)
        gl = make_get_data_len(game)
        dz = make_dozoom(game)
        sz = make_set_zoom(game)
        def dr(*args):
            r,g,b = args[:3]
            x,y,w,h = args[3:7]
            width = args[7]
            pygame.draw.rect(screen, (r,g,b), pygame.Rect(game.zoom(x),game.zoom(y),game.zoom(w),game.zoom(h)), width)
        def txt(*args):
            size = args[0]
            r,g,b = args[1:4]
            x,y = args[4:6]
            txt = "".join(map(chr, args[6:-1]))
            font = pygame.font.Font(None, size)
            text = font.render(txt, 1, (r,g,b))
            screen.blit(text, (game.zoom(x),game.zoom(y)))
        def p(*args):
            print args
        self.data = brainfuck.call_bf(self.update_code, self.data + [0, other.id] + other.data, locals(), globals())
    

