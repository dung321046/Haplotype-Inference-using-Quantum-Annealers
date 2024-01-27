import os
import random

from utils import *


def gen_g(h1, h2):
    ans = ''
    for i in range(len(h1)):
        if h1[i] == '1' and h2[i] == '1':
            ans += '1'
        elif h1[i] == '0' and h2[i] == '0':
            ans += '0'
        else:
            ans += '2'
    return ans


def create_haplotype(g):
    h1 = ''
    h2 = ''
    for gi in g:
        if gi == '0':
            h1 += '0'
            h2 += '0'
        elif gi == '1':
            h1 += '0'
            h2 += '0'
        else:
            if random.random() > 0.5:
                h1 += '0'
                h2 += '1'
            else:
                h1 += '1'
                h2 += '0'
    return h1, h2


def create_haplotype_from_2gen(g1, g2):
    h1 = ''
    h2 = ''
    hm = ''
    for i in range(len(g1)):
        p1 = int(g1[i])
        p2 = int(g2[i])
        if p1 + p2 == 1:
            return "", "", ""
        if p1 == p2 and p1 < 2:
            h1 += g1[i]
            h2 += g1[i]
            hm += g1[i]
        elif p1 == 2:
            if p2 < 2:
                h1 += str(1 - p2)
                h2 += g2[i]
                hm += g2[i]
            else:
                if random.random() > 0.5:
                    h1 += '0'
                    hm += '1'
                    h2 += '0'
                else:
                    h1 += '1'
                    h2 += '1'
                    hm += '0'
        elif p2 == 2 and p1 < 2:
            h1 += g1[i]
            h2 += str(1 - p1)
            hm += g1[i]
        else:
            print("ERRORRR", file=sys.stderr)
    return h1, h2, hm


def gen_genotype_set(density, hsample, rr):
    gs = set()
    for i in range(1, rr):
        for j in range(i):
            if random.random() > density:
                g = gen_g(hsample[i], hsample[j])
                gs.add(g)
    return list(gs)


def associate(h, g):
    for i, hi in enumerate(h):
        if int(g[i]) < 2 and g[i] != hi:
            return False
    return True


def find_h(h, g):
    h2 = ''
    for i, hi in enumerate(h):
        if int(g[i]) == 2:
            h2 += str(1 - int(hi))
        else:
            if g[i] != hi:
                return False, h2
            h2 += hi
    return True, h2


def single_relation(h, t, gs):
    for i in range(len(gs)):
        if i != t:
            b, ch = find_h(h, gs[i])
            if b:
                return False, ch
    return True, "Invalid"


def gen_all(hap, seql, cur):
    if len(cur) == seql:
        hap.add(cur)
        return
    gen_all(hap, seql, cur + "0")
    gen_all(hap, seql, cur + "1")


random.seed(1)
sys.stdin = open('Data/HapSet.inp', 'r')
TT = 0
dataset_folder = "Data/Data/"
if not os.path.exists(dataset_folder):
    os.mkdir(dataset_folder)
while TT < 20:
    s = input()
    if not re.search("segsites", s):
        continue
    input()
    hsample = set()
    while True:
        s = input()
        if s == "":
            break
        hsample.add(s)
    hsample = list(hsample)
    seql = len(hsample[0])
    init_size = len(hsample)
    sys.stdout = sys.__stdout__
    print(len(hsample))
    gs = []
    cnt = 0
    while len(gs) < init_size or len(gs) >= 2 * init_size:
        density = random.uniform(0.6, 0.99)
        gs = gen_genotype_set(density, hsample, init_size)
    n = len(gs)
    hsample = set()
    gen_all(hsample, seql, "")
    hsample = list(hsample)
    hpairs = create_pairs_fast(hsample, n, len(hsample), seql, gs)
    filename = dataset_folder + str(TT).zfill(2) + "Gen" + str(n) + "Hap" + str(len(hsample)) + ".txt"
    sys.stdout = open(filename, 'w')
    print(n, seql)
    for g in gs:
        print(g)
    print()
    print()
    print(len(hsample))
    for h in hsample:
        print(h)
    sys.stdout.close()
    TT += 1
