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

LEFT = 1
RIGHT = 2
TOP = 3
BOTTOM = 4    

def collide(a, b, mirror=True):
    if not a or not b:
        return []
    xa, ya, wa, ha = a
    xb, yb, wb, hb = b
    if xa + wa < xb or ya + ha < yb or xb + wb < xa or yb + hb < ya:
        return []
    ra = pygame.Rect(*a)
    rb = pygame.Rect(*b)
    if not ra.colliderect(rb):
        return []
    if xa < xb and ya < yb:
        if xb - xa < yb - ya:
            return [BOTTOM, TOP]
        else:
            return [RIGHT, LEFT]
    elif xa < xb:
        return [RIGHT, LEFT]
    elif ya < yb:
        return [BOTTOM, TOP]
    elif xa + wa > xb + wb and ya + ha > yb + hb:
        if (xb + wb - (xa - wa)) > (yb + hb - (ya + ha)):
            return [BOTTOM, TOP]
        else:
            return [LEFT, RIGHT]
    elif xa + wa > xb + wb:
        return [LEFT, RIGHT]
    else:
        return [TOP, BOTTOM]
        
def to_name(coll):
    if not coll:
        return "None"
    m = {LEFT: "left", RIGHT: "right", TOP: "top", BOTTOM: "bottom"}
    return map(lambda c: m[c], coll)
        
    

class Game(object):
    def __init__(self):
        self.objects = []
        self.obj_ids = {}
        self.current_zoom = 1
        self.anchor = (0,0)
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
    def update(self, screen, left, right, space, click, (x,y)):
        for o in self.objects:
            o.update(self, screen, left, right, space, click, (self.anchor[0] + x, self.anchor[0]+y))
        bbs = map(lambda o: [o, o.get_bb()], self.objects)
        for i,b in enumerate(bbs):
            for b1 in bbs[i+1:]:
                overlap = collide(b[1], b1[1])
                if overlap:
                    b[0].collide(b1[0], self, screen, overlap[0])
                    b1[0].collide(b[0], self, screen, overlap[1])
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
    def toscreenx(self, x):
        return (x-self.anchor[0])*self.current_zoom
    def toscreeny(self, y):
        return (y-self.anchor[1])*self.current_zoom

RULE_DIR = "rules"

class GameObject:
    def __init__(self, name, game):
        self.update_code = brainfuck.get_content(os.path.join(RULE_DIR, name + ".update"))
        self.bounding_box = brainfuck.get_content(os.path.join(RULE_DIR, name + ".bb"))
        self.collide_code = brainfuck.get_content(os.path.join(RULE_DIR, name + ".col"))
        init_code = brainfuck.get_content(os.path.join(RULE_DIR, name + ".init"))
        self.t = time.time()
        sp = make_spawn(game)
        sd = make_set_data(game)
        gd = make_get_data(game)
        gl = make_get_data_len(game)
        dz = make_dozoom(game)
        sz = make_set_zoom(game)
        self.name = name
        self.data = brainfuck.call_bf(init_code, [], locals(), globals())
    def update(self, game, screen, left, right, space, click, (x,y)):
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
            pygame.draw.rect(screen, (r,g,b), pygame.Rect(game.toscreenx(x),game.toscreeny(y),game.zoom(w),game.zoom(h)), width)
        def txt(*args):
            size = args[0]
            r,g,b = args[1:4]
            x,y = args[4:6]
            txt = "".join(map(chr, args[6:-1]))
            font = pygame.font.Font(None, size)
            text = font.render(txt, 1, (r,g,b))
            screen.blit(text, (game.toscreen(x),game.toscreen(y)))
        def p(*args):
            print args
        t1 = time.time()
        self.data = brainfuck.call_bf(self.update_code, [t1-self.t, left, right, space, 0, 0, 0] + self.data, locals(), globals())
        self.t = t1
    def get_bb(self):
        result = brainfuck.call_bf(self.bounding_box, self.data[:], locals(), globals())
        return result
    def collide(self, other, game, screen, overlap):
        if not self.collide_code: return
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
        self.data = brainfuck.call_bf(self.collide_code, [overlap, 0] + self.data + [0, other.id] + other.data, locals(), globals())
    

def test_coll(a,b):
    print a, b, to_name(collide(a,b))
    
if __name__ == "__main__":
    test_coll((0,0,10,10), (20,20,10,10))
    test_coll((0,0,10,10), (5,5,12,7))
    test_coll((10,10,10,10), (11,12,15,12))
    test_coll((10,10,10,10), (11,12,12,15))