"""Illustrative checks of unique water-filling, potential, and fair unbounded waits."""
import math

vals=((1.,2.,3.),(3.,0.,1.),(0.,3.,2.))
budgets=(1.,1.2,1.3)
n=len(vals)
m=len(vals[0])

def agg(state):
    return tuple(sum(row[x] for row in state) for x in range(m))

def phi(z):
    d=agg(z)
    return -sum(a*math.log(a) for a in d if a)+sum(
        z[i][x]*math.log(vals[i][x]) for i in range(n) for x in range(m) if vals[i][x])

def update(z,i):
    d=agg(z)
    b=[d[x]-z[i][x] for x in range(m)]
    v=vals[i]
    hi=max((b[x]+budgets[i])/v[x] for x in range(m) if v[x])
    lo=0.
    for _ in range(48):
        t=(hi+lo)/2
        if sum(max(0.,t*v[x]-b[x]) for x in range(m) if v[x])<budgets[i]: lo=t
        else: hi=t
    return z[:i]+(tuple(max(0.,hi*v[x]-b[x]) if v[x] else 0.
                       for x in range(m)),)+z[i+1:]

def initialize():
    z=((0.,)*m,)*n
    for i in range(n): z=update(z,i)
    return z

def run(schedule,z):
    last=phi(z)
    for i in schedule:
        z=update(z,i)
        p=phi(z)
        assert p>=last-1e-11
        last=p
    return z

z=initialize()
reference=run((0,1,2)*200,z)
schedule=(i for k in range(1,75) for i in list((0,1)*k)+[2])
current=run(schedule,z)
for i in range(n):
    assert max(abs(a-b) for a,b in zip(current[i],update(current,i)[i]))<1e-9
assert max(abs(a-b) for a,b in zip(agg(current),agg(reference)))<1e-9
print("Potential monotonicity and agreement under 74 increasing-gap schedule blocks checked.")
