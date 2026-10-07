"""Independent exact checks of the geometry proposed for episode158.
Does not import or execute renderer/repository code.
"""
from itertools import product, combinations
from pathlib import Path
import json
import sympy as s
r=s.Rational(2,5); basis=s.Matrix([[s.sqrt(3)*r,s.sqrt(3)*r/2],[0,3*r/2]])
a,b=s.symbols('a b', integer=True)
norm2=s.simplify((basis*s.Matrix([a,b])).dot(basis*s.Matrix([a,b])))
assert s.simplify(norm2-3*r*r*(a*a+a*b+b*b))==0
# Color difference zero => a+3b=7k. Positive norm integer divisible by7.
k=s.symbols('k',integer=True)
assert s.rem(((a*a+a*b+b*b).subs(a,7*k-3*b)).expand(),s.Integer(7),k)==0 # all coefficients divisible by7
lower=(s.sqrt(21)-2)*r
assert lower>1
# Pointy-top hexagon (vertices at 30+60k degrees) has nearest-neighbor distance sqrt3*r.
verts=[s.Matrix([r*s.cos(s.pi/6+j*s.pi/3),r*s.sin(s.pi/6+j*s.pi/3)]) for j in range(6)]
assert max(s.simplify((u-v).dot(u-v)) for u in verts for v in verts)==4*r*r
# Moser spindle: two unit diamonds rotated +/- theta/2, sin(theta/2)=1/(2sqrt3).
sh=1/(2*s.sqrt(3)); ch=s.sqrt(11)/(2*s.sqrt(3))
rot=s.Matrix([[ch,-sh],[sh,ch]])
base=[s.Matrix([0,0]),s.Matrix([s.sqrt(3)/2,s.Rational(1,2)]),s.Matrix([s.sqrt(3)/2,-s.Rational(1,2)]),s.Matrix([s.sqrt(3),0])]
V=[base[0]]+[rot*v for v in base[1:]]+[rot.T*v for v in base[1:]]
E=[(0,1),(0,2),(1,2),(1,3),(2,3),(0,4),(0,5),(4,5),(4,6),(5,6),(3,6)]
for i,j in E: assert s.simplify((V[i]-V[j]).dot(V[i]-V[j]))==1
assert all(s.simplify((V[i]-V[j]).dot(V[i]-V[j]))>0 for i,j in combinations(range(7),2))
actual=[(i,j) for i,j in combinations(range(7),2) if s.simplify((V[i]-V[j]).dot(V[i]-V[j]))==1]
assert set(actual)==set(E)
colors={}
for count in (3,4):
 solutions=[c for c in product(range(count),repeat=7) if all(c[i]!=c[j] for i,j in E)]
 colors[str(count)]={'count':len(solutions),'example':solutions[0] if solutions else None}
assert colors['3']['count']==0 and colors['4']['count']>0
out={'hexagon_radius':str(r),'max_same_tile_distance':str(2*r),'lattice_norm_squared':str(norm2),'same_color_rule':'(a+3b) mod7','same_color_norm_divisibility':str(s.expand((a*a+a*b+b*b).subs(a,7*k-3*b))),'closest_same_color_indices':[[1,2],[-3,1]],'minimum_distinct_same_color_point_distance_lower_bound':str(lower),'bound_decimal':float(lower),'Moser_vertices':[[str(s.simplify(x)) for x in v] for v in V],'Moser_edges':E,'all_11_edges_exact_unit':True,'no_additional_unit_edges':True,'color_enumeration':colors,'scope':'Checks the educational constructions only. Does not verify the new five-color lower bound or its arbitrary-to-weak-measurable transfer.'}
print(json.dumps(out,indent=2,ensure_ascii=False))
