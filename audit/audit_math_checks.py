#!/usr/bin/env python3
"""Independent, bounded mathematical checks. Does not execute repository code.
Run: python audit_math_checks.py. Numerical checks are not proofs of full theorems.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import permutations, combinations
import json
import mpmath as mp
import sympy as s
mp.mp.dps=90
out={}
# Pi examples: rational subtraction at 90 decimal digits.
out['pi_examples']={f'{p}/{q}':{'absolute_error':mp.nstr(abs(mp.pi-mp.mpf(p)/q),75),'q_squared_error':mp.nstr(q*q*abs(mp.pi-mp.mpf(p)/q),75),'beats_inverse_q_squared':bool(abs(mp.pi-mp.mpf(p)/q)<mp.mpf(1)/(q*q))} for p,q in [(22,7),(355,113)]}
# Four-row permanent proof, Eq.(4): exact covariance and identity for all
# centered integer rows with entries in {-2,-1,0,1,2}, paired with each other.
rows=[r for r in __import__('itertools').product(range(-2,3),repeat=4) if sum(r)==0]
ps=list(permutations(range(4)))
for g in rows:
 for h in rows:
  actual=F(sum(g[p[0]]*h[p[1]] for p in ps),24)
  expected=-F(sum(a*b for a,b in zip(g,h)),12)
  assert actual==expected
out['permanent_covariance']={'centered_rows':len(rows),'exact_row_pairs':len(rows)**2,'all_passed':True,'scope':'Only the uniform S4 covariance identity underlying the local p>4/3 calculation; not the full Thorp mixing theorem.'}
# Exact block algebra for affine maximal dimension-ten ODE.
A,B,D=s.symbols('A B D'); gam=s.Rational(12,11)
V=s.Matrix([A*(1+B-A),B*(9+A+gam*B*D-9*B),(11-D)*A-8*D+B*D*(1-D/11)])
corner={A:s.Rational(9,2),B:s.Rational(7,2),D:s.Rational(33,7)}
assert V.subs(corner)==s.zeros(3,1)
# All six faces checked by direct factorized expressions and the printed ranges.
faces={f'V{i+1}_{name}':str(s.factor(V[i].subs(var,value))) for i,var in enumerate((A,B,D)) for name,value in [('lower',0),('upper',corner[var])]}
# Re-derive Ddot from A,B,C logarithmic derivative system without assuming paper Eq.(16).
C=s.symbols('C'); Bdot=B*(9+A+gam*C-9*B); Cdot=C*(1+C-8*B)+11*A*B
assert s.simplify(((Cdot*B-C*Bdot)/B**2).subs(C,B*D)-V[2])==0
out['affine_maximal_ode']={'corner_equilibrium_exact':True,'D_equation_exact':True,'face_expressions':faces,'scope':'Lemma 4.1 change of variables and Lemma 4.2 invariant-box algebra; no full PDE formalization.'}
# Monge ansatz: center Coulomb Hessians and derivatives are rational.
# x=0,y=e1,z=-e1. h Hessian at e1 is diag(2,-1,-1); at 2e1 it is /8.
H=s.diag(2,-1,-1); M=(2*H).row_join(-H).col_join((-H).row_join(s.Rational(9,8)*H)); N=(-H).col_join(-H/8)
K=20; Q=M+K*s.eye(6); deriv=-Q.inv()*N
assert all(v>0 for v in Q.eigenvals())
assert deriv[:3,:].det()!=0 and deriv[3:,:].det()!=0
out['coulomb_local_branch']={'K':K,'positive_definite_exact':True,'DX_determinant':str(s.factor(deriv[:3,:].det())),'DZ_determinant':str(s.factor(deriv[3:,:].det())),'cost_at_center':'5/2','mixed_center_gap':str(2+1/s.sqrt(2)-s.Rational(5,2)),'scope':'Lemma 3.1 finite center algebra and Proposition 4.1 center gap only; local-to-global measure proof reviewed separately.'}
# Hadamard examples in exact cyclotomic fields: check Gram=6I and every
# permutation of alpha Fourier character vanishes for F6. Tao satisfies H^2 Gram=6I.
z=s.symbols('z')
def zero_root_sum(exponents,order):
 return s.rem(sum((z**(int(e)%order) for e in exponents),s.S.Zero),s.cyclotomic_poly(order,z),z)==0
def hadamard(E,order,mult=1):
 return all(zero_root_sum([mult*(E[i][k]-E[j][k]) for k in range(6)],order) for i in range(6) for j in range(i))
F6=[[i*j for j in range(6)] for i in range(6)]
assert hadamard(F6,6)
for S in combinations(range(6),3):
 alpha=[1 if i in S else -1 for i in range(6)]
 assert zero_root_sum([sum(alpha[i]*F6[i][k] for i in range(6)) for k in range(6)],6)
T=[[0 if i==0 or j==0 or i==j else (1 if (i-j)%5 in (1,4) else -1) for j in range(6)] for i in range(6)]
assert hadamard(T,3) and hadamard(T,3,2)
out['hadamard_examples']={'F6_gram_exact':True,'F6_twenty_alpha_characters_exact_zero':True,'Tao_gram_exact':True,'Tao_entrywise_square_gram_exact':True,'scope':'Explicit examples only, separate from the repository general exact certificate rerun.'}
out['limitations']='No finite sample verifies an asymptotic universal claim. No confirmed counterexample found in these bounded checks. No Lean build was attempted.'
print(json.dumps(out,ensure_ascii=False,indent=2))
