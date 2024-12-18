import numpy as np
import os
from itertools import product
from cobamp.efm_enumeration.kshortest_efms import KShortestEFMAlgorithm
from cobamp.linear_systems.linear_systems import DualLinearSystem
from cobamp.mcs_enumeration.intervention_problem import *
import cobamp.efm_enumeration.kshortest_efm_properties as kp

os.chdir('/home/skapur/Workspaces/PyCharm/cobamp/examples/iAF1260_resources')

S = np.genfromtxt('iAF1260_comp_stoich.csv', delimiter=',')

with open('iAF1260_comp_exclusions.txt','r') as f:
	singles = [s.strip() for s in f.readlines()]

with open('iAF1260_comp_rxnames.txt','r') as f:
	rx_names = [s.strip() for s in f.readlines()]

with open('iAF1260_comp_metnames.txt','r') as f:
	met_names = [s.strip() for s in f.readlines()]

with open('iAF1260_comp_bound_map.txt','r') as f:
	bound_map = {k:[float(n) for n in v.split(',')]for k,v in dict([s.strip().split('=') for s in f.readlines()]).items()}

with open('iAF1260_comp_orx_map.txt','r') as f:
	orx_map = {k:[n for n in v.split(',')]for k,v in dict([s.strip().split('=') for s in f.readlines()]).items()}

irrev = np.where(np.array([bound_map[r][0] >= 0 for r in rx_names]))[0]
exclusions = [[rx_names.index([k for k,v in orx_map.items() if s in v][0])] for s in singles if s in list(chain(*orx_map.values()))]
biomass_index = rx_names.index('R_Ec_biomass_iAF1260_core_59p81M')
atpm_index = rx_names.index('R_ATPM')
glc_index = rx_names.index('R_EX_glc_e')

configuration = kp.KShortestProperties()
configuration[kp.K_SHORTEST_MPROPERTY_METHOD] = kp.K_SHORTEST_METHOD_POPULATE
configuration[kp.K_SHORTEST_OPROPERTY_MAXSIZE] = 1

problem = InterventionProblem(S)
T, b = problem.generate_target_matrix([
	DefaultFluxbound(0.0001, None, biomass_index),
	DefaultFluxbound(-20, None, glc_index),
	DefaultFluxbound(8.39, 8.39, atpm_index)])

dual_system = DualLinearSystem(S, irrev, T, b)

algorithm = KShortestEFMAlgorithm(configuration)

lethals = list(algorithm.enumerate(dual_system, exclusions))

def decode_solutions(solutions):
 """
 Args:
     solutions:
 """
	return list(chain(*[list(product(*[orx_map[rx_names[i]] for i in lethal.get_active_indicator_varids()])) for lethal in solutions]))

decoded = decode_solutions(lethals)

len(decoded)