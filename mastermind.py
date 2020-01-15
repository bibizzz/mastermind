from __future__ import division
import random
import math
import operator

#to do
# better sorting of best guesses (add entropy and if move is in set)
# add an automatic resolution of all codes with the best guess (or random guess)
# sort by number of colors, patterns the set


class Game:
    def __init__(self, places=4, colors=6):
        self.places = places
        self.colors = colors
        self.guess_list = list()
        self.resp_list = list()
        self.set_list = list()
        self.set_list.append(Set(places, colors))
        self.cur_move = 0

    def play(self, guess, response):
        cur_guess = Guess(guess)
        self.guess_list.append(Guess(guess))
        self.resp_list.append(response)
        self.set_list.append(set_list[-1].new_set(cur_guess, response))


class Guess:

    def __init__(self, number):
        self.number = number
        self.string = str(number)
        self.places = len(self.string)
        self.ent = 0
        self.distribution = {}

    def response(self, code):
        if len(code) != len(self.string):
            return -1
        else:
            black = white = 0
            to_be_tested = list(range(0, len(code)))
            for i in range(0, len(code)):
                if code[i] == self.string[i]:
                    black += 1
                    to_be_tested.remove(i)
            to_be_tested_black = list(to_be_tested)
            for i in to_be_tested_black:
#                print("i:" +str(i))
#                print(self.string[i])
                for j in to_be_tested:
#                    print("j:" +str(j))
#                    print(code[j])
                    if code[j] == self.string[i]:
                        white += 1
                        to_be_tested.remove(j)
#                        print(to_be_tested)
                        break
        return (black, white)

    def proba(self, set):
        occ = {}
        for elt in set.positions:
            rep = Guess(elt).response(self.number)
            if rep in occ.keys():
                occ[rep] += 1
            else:
                occ[rep] = 1
        self.distribution = occ
        return sorted(occ.items(), key=operator.itemgetter(0))

    def entropy(self):
        if self.distribution == {}:
            self.ent = 0
        card = sum(self.distribution.values())
        #print(card)
        ent = 0
        #print(self.distribution)
        for nb in self.distribution.values():
            if nb != 0 and card != 0:
                #print(nb)
                p = nb / card
                ent += p * math.log(p)
        self.ent = - ent


def get_dict_max(dicti):
    max = 0
    max_elt = (-1, -1)
    for key, elt in dicti.items():
        if elt >= max:
            max = elt
            max_elt = key
    return max_elt, max


def get_dict_min(dicti):
    min = 1000000000
    min_elt = (-1, -1)
    for key, elt in dicti.items():
        if elt <= min:
            min = elt
            min_elt = key
    return min_elt, min


class Code:

    def __init__(self, places, colours):
        self.code_s = ""
        for i in range(0, places):
            r = str(random.randint(0, colours - 1))
            self.code_s += r
        print(self.code_s)


class Set:
    def __init__(self, places, colours):
        self.cardinal = 0 #math.pow(colours, places)
        self.positions = [] # self.ret_set(places, colours)
        self.places = places
        self.colours = colours
    
    def ret_set(self, places, colours):
        if places == 1:
            ret = list()
            for i in range(0, colours):
                ret.append(str(i))
            return ret
        else:
            ret = list()
            for i in range(0, colours):
                for e in self.ret_set(places - 1, colours):
                    ret.append(e + str(i))
            return ret

    def beginning_set(self):
        self.cardinal = math.pow(self.colours, self.places)
        self.positions = self.ret_set(self.places, self.colours)

    def new_set(self, code, response):
        ret_elt = list()
        for elt in self.positions:
            if Guess(code).response(elt) == response:
                ret_elt.append(elt)
        ret = Set(self.places, self.colours)
        ret.positions = ret_elt
        ret.cardinal = len(ret_elt)
        return ret

    def response_set(self, code, response):
        for elt in self.positions:
            if Guess(code).response(elt) != response:
                self.positions.remove(elt)
                self.cardinal -= 1

    def proba_colour(self, c):
        count = 0
        for pos in self.positions:
            for cc in pos:
                if cc == c:
                    count += 1
                    break
        return count * 100. / self.cardinal

    def distrib_colour(self):
        col_d = [0] * self.colours
        for col in range(0, self.colours):
            for pos in self.positions:
                for cc in pos:
                    if cc == str(col):
                        col_d[col] += 1
                        break
            col_d[col] = col_d[col] * 100. / self.cardinal
        return col_d

    def distrib_col_pos(self, posi):
        col_d = [0] * self.colours
        for col in range(0, self.colours):
            for pos in self.positions:
                if str(col) == pos[posi]:
                    col_d[col] += 1
            col_d[col] = col_d[col] * 100. / self.cardinal
        return col_d

colours = 6
places = 4

starting_set = Set(places, colours)
s = Set(places, colours)
s.beginning_set()
g = Guess("0123")
g.proba(s)
g.entropy()
print(g.ent)
print(s.distrib_colour())
print(Guess("0123").response("1000"))


def best_guess(test_set):
    ret_f = {}
    for g in Set(places, colours).positions:
        f = Guess(g)
        f.proba(test_set)
        m = get_dict_max(f.distribution)
        ret_f[g] = m[1]
    ret_s = sorted(ret_f.items(), key=operator.itemgetter(1))
    return ret_s

def save_bg(filename, list):
    f = open(filename + '.csv', 'w')
    for el1 in list:
        for el2 in el1:
             f.write(str(el2) + ';')
        f.write("\n")
    f.close()

if 0:
    ret_f = {}
    for g in starting_set.positions:
        f = Guess(g)
        p = f.proba(starting_set.positions)
        m = get_dict_max(p)
        print(g)
        print(m)
        ret_f[g] = m[1]

    print(ret_f)
    print("Resultats")
    print(get_dict_min(ret_f))
