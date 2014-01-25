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

class Game(object):
    def __init__(self):
        self.objects = []
        self.obj_ids = {}
    def load_level(self, level):
        fname = os.path.join(LEVEL_DIR, level + ".lvl")
        if not os.path.exists(fname):
            return None
        self.objects = []
        sp = make_spawn(self)
        sd = make_set_data(self)
        gd = make_get_data(self)
        gl = make_get_data_len(self)
        brainfuck.call_bf(brainfuck.get_content(fname), [], locals(), globals())
    def update(self, screen):
        for o in self.objects:
            o.update(self, screen)
    def spawn(self, id, what):
        self.objects.append(what)
        self.obj_ids[id] = what
    def set_data(self, id, data):
        self.obj_ids[id].data = data
    def get_data(self, id, i):
        return self.obj_ids[id].data[i]
    def get_data_len(self, id):
        return len(self.obj_ids[id].data)

RULE_DIR = "rules"

class GameObject:
    def __init__(self, name, game):
        self.update_code = brainfuck.get_content(os.path.join(RULE_DIR, name + ".update"))
        init_code = brainfuck.get_content(os.path.join(RULE_DIR, name + ".init"))
        self.t = time.time()
        sp = make_spawn(game)
        sd = make_set_data(game)
        gd = make_get_data(game)
        gl = make_get_data_len(game)
        self.data = brainfuck.call_bf(init_code, [], locals(), globals())
    def update(self, game, screen):
        t1 = time.time()
        objects = []
        sp = make_spawn(game)
        sd = make_set_data(game)
        gd = make_get_data(game)
        gl = make_get_data_len(game)
        def dr(*args):
            r,g,b = args[:3]
            x,y,w,h = args[3:7]
            width = args[7]
            pygame.draw.rect(screen, (r,g,b), pygame.Rect(x,y,w,h), width)
        self.data = brainfuck.call_bf(self.update_code, [t1-self.t] + self.data, locals(), globals())
        self.t = t1
    

