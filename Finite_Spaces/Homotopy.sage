from Finite_Spaces.General import *

#Homology
def homology(X):
	return X.order_complex().homology()

#Fundamental group
def fundamental_group(X):
	return X.order_complex().fundamental_group()

#Closed sets, open sets and neighborhoods.
def F(X, x):
	return X.subposet(X.order_filter([x]))

def U(X, x):
	return X.subposet(X.order_ideal([x]))

def C(X, x):
	elms=[y for y in X.list() if X.is_gequal(x,y) or X.is_gequal(y,x)]
	return X.subposet(elms)

def F_hat(X, x):
	elms=[y for y in X.list() if X.is_greater_than(y, x)]
	return X.subposet(elms)

def U_hat(X, x):
	elms=[y for y in X.list() if X.is_greater_than(x, y)]
	return X.subposet(elms)

def C_hat(X, x):
	elms=[y for y in X.list() if X.is_greater_than(x, y) or X.is_greater_than(y, x)]
	return X.subposet(elms)

#Reduction

def remove_point(X, x):
	elms=[y for y in X.list() if not y == x]
	return X.subposet(elms)

def remove_edge(X, e): #e = [e[0], e[1]]
	rels=[edge for edge in X.cover_relations() if not edge == e]
	return Poset((X.list(), rels))

#Homotopy Theory

def is_beat_point(X, x):
	return len(X.upper_covers(x)) == 1 or len(X.lower_covers(x)) == 1

def beat_points(X):
	return [x for x in X.list() if is_beat_point(X,x)]

def core(X): 
	for x in beat_points(X):
		X = remove_point(X, x)
		return core(X)
	return X

def is_contractible(X):
	if X.has_top() or X.has_bottom():
		return True
	return core(X).cardinality() == 1

#Simple Homotopy Theory

def is_weak_point(X, x):
	return (is_contractible(U_hat(X, x)) or is_contractible(F_hat(X, x)))

def weak_points(X):
	return [x for x in X.list() if is_weak_point(X, x)]

def weak_core(X):
	for x in weak_points(X):
		X = remove_point(X, x)
		return weak_core(X)
	return X

def minwcoreaux(X): 
	MX = X
	for x in weak_points(X): 
		S = remove_point(X, x)
		K = tuple(S.list()) 
		if not visitados.has_key(K): 
			visitados[K] = True 
			Y = minwcoreaux(S) 
			if Y.cardinality()< MX.cardinality(): MX = Y
	return MX

def min_weak_core(X): 
	global visitados 
	visitados = {} 
	return minwcoreaux(X) 

def is_collapsible_aux(X):
	if is_contractible(X):
		return True
	if non_collapsibles.has_key(tuple(X.list())):
		return False
	for x in weak_points(X): 
		S = remove_point(X,x) 
		if not non_collapsibles.has_key(tuple(S.list())):
			if is_collapsible(S):
				return True
			non_collapsibles[tuple(S.list())] = True
	return False

def is_collapsible(X): 
	global non_collapsibles 
	non_collapsibles = {} 
	return is_collapsible_aux(X) 

#Qc-reductions

def is_qc_reduction(X, a, b):
	return is_contractible(X.subposet(X.order_ideal([a, b])))

def is_qc_op_reduction(X, a, b):
	return is_contractible(X.subposet(X.order_filter([a, b])))


def qc_core(X):
	if len(X.maximal_elements()) == 1:
		return X
	for a in X.maximal_elements():
		for b in X.maximal_elements():
			if a != b and is_qc_reduction(X, a, b):
				X = quotient_poset(X, [a, b])
				return qc_core(X)
	return X

def qc_coresaux(X): 
	have_entered = False 
	for a in X.maximal_elements():
		for b in X.maximal_elements():
			if a != b and is_qc_reduction(X, a, b):
				have_entered = True 
				qc_coresaux(quotient_poset(X, [a, b]))
	if not have_entered and X not in qcC:
		qcC.append(X)

def qc_cores(X): 
	global qcC
	qcC = [] 
	qc_coresaux(X) 
	return qcC

