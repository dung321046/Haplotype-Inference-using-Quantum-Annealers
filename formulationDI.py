from collections import defaultdict

from utils import *


def formulate(gsize, hsize, hpairs):
    constraint_set = []
    OFFSET = 0
    vname2idx = dict()
    Q = defaultdict(int)
    A = 2
    for i in range(hsize):
        vname2idx[x_name(i)] = i
        Q[(i, i)] += 1
    for i in range(gsize):
        for (u, v) in hpairs[i]:
            name = p_name(u, v)
            vname2idx[name] = len(vname2idx)
            x_u, x_v, x_uv = vname2idx[x_name(u)], vname2idx[x_name(v)], vname2idx[name]
            constraint_set.append(["x,y>=z", x_name(u), x_name(v), name])
            Q[(x_uv, x_uv)] += 2 * A
            Q[(x_uv, x_u)] -= A
            Q[(x_uv, x_v)] -= A
    B = 2
    for K in range(gsize):
        idx = [-1]
        names = ["sum" + str(K), 1]
        for (u, v) in hpairs[K]:
            names.append(p_name(u, v))
            idx.append(vname2idx[p_name(u, v)])
        constraint_set.append(names)
        # Formulation for  B * (1 - p_K0 - ... - p_{Kt}) ^ 2
        # 2 u v
        for i in range(len(idx)):
            for j in range(i):
                if idx[j] == -1:
                    Q[(idx[i], idx[i])] -= B
                else:
                    Q[(idx[i], idx[j])] += 2 * B
        OFFSET += B
    return OFFSET, Q, vname2idx, constraint_set


if __name__ == "__main__":
    import neal
    import time

    files = ['Data/Geno4Len5.txt']
    for filename in files:
        gsize, glen, g, hsize, h = read_data(filename)
        hpairs = create_pairs(h, gsize, hsize, glen, g)
        OFFSET, Q, vname2idx, constraint_set = formulate(gsize, hsize, hpairs)
        start = time.time()
        sampler = neal.SimulatedAnnealingSampler()
        print("#Var-#NoneZ:", len(vname2idx), '-', len(Q))
        response = sampler.sample_qubo(Q, num_reads=100, sweeps=1000)
        best = 1000000
        best_response = []
        for run in response.data():
            if run.energy < best:
                best_response.append(run)
                best = run.energy
            elif run.energy == best:
                best_response.append(run)
        for rid, r in enumerate(best_response[:10]):
            objv = 0
            for i in range(hsize):
                if r.sample[vname2idx[x_name(i)]] == 1:
                    objv += 1
            print("run:", rid, " Obj:", objv, "Energy:", r.energy + OFFSET)
            check_constraint(constraint_set, r, vname2idx)
        end = time.time()
        print("Time running", end - start)
        sys.stdout = open(filename[:-3] + "out", 'w')
        for r in best_response[:1]:
            objv = 0
            for i in range(hsize):
                if r.sample[vname2idx[x_name(i)]] == 1:
                    objv += 1
                    print("1")
                else:
                    print("0")
            print("Objective:", objv)
