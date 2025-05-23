import numpy as np
import ase
from scipy.constants import Boltzmann, pi, elementary_charge, hbar

atomic_num_dict = ase.atom.atomic_numbers
atomic_num_dict_r = dict(zip(atomic_num_dict.values(), atomic_num_dict.keys()))