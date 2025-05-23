from typing import List, Callable
from dargs import dargs, Argument, Variant, ArgumentEncoder
import logging

log = logging.getLogger(__name__)

def normalize_run(data):

    run_op = run_options()
    data = run_op.normalize_value(data)
    run_op.check_value(data, strict=True)
    
    return data

def run_options():
    doc_task = "the task to run, includes: band, dos, pdos, FS2D, FS3D, ifermi"
    doc_structure = "the structure to run the task"
    doc_device = "The device to run the calculation, choose among `cpu` and `cuda[:int]`, Default: None. default None means to use the device seeting in the model ckpt file."
    doc_dtype = """The digital number's precision, choose among: 
                    Default: None,
                        - `float32`: indicating torch.float32
                        - `float64`: indicating torch.float64
                    default None means to use the device seeting in the model ckpt file.
                """
 
    args = [
        Argument("task_options", dict, sub_fields=[], optional=True, sub_variants=[task_options()], doc = doc_task),
        Argument("structure", [str,None], optional=True, default=None, doc = doc_structure),
        Argument("device", [str,None], optional = True, default=None, doc = doc_device),
        Argument("dtype", [str,None], optional = True, default=None, doc = doc_dtype),
        AtomicData_options_sub()
    ]
    return Argument("run_op", dict, args)

def task_options():
    doc_task = '''The string define the task  includes: 
                    - `ac_cond`: for ac optical conductivity.
                '''

    return Variant("task", [
            Argument("ac_cond", dict, ac_cond()),
        ],optional=False, doc=doc_task)
        
def ac_cond():
    doc_emax = ""
    doc_num_omega = ""
    doc_mesh_grid = ""
    doc_nk_per_loop = ""
    doc_delta = ""
    doc_e_fermi = ""
    doc_valence_e = ""
    doc_gap_corr = ""
    doc_T = ""
    doc_direction = ""
    doc_g_s = ""

    argu = [
        Argument("emax", float, optional=False, default=10, doc=doc_emax),
        Argument("num_omega", int, optional=False, default=1000, doc=doc_num_omega),
        Argument("mesh_grid", list, optional=False, default=[1,1,1], doc=doc_mesh_grid),
        Argument("nk_per_loop", [int, None], optional=True, default=None, doc=doc_nk_per_loop),
        Argument("delta", float, optional=False, default=0.03, doc=doc_delta),
        Argument("e_fermi", [float, int, None], optional=False, doc=doc_e_fermi),
        Argument("valence_e", [dict, None], optional=True, default=None, doc=doc_valence_e),
        Argument("gap_corr", float, optional=False, default=0, doc=doc_gap_corr),
        Argument("T", [float, int], optional=False, default=300, doc=doc_T),
        Argument("direction", str, optional=False, default="xx", doc=doc_direction),
        Argument("g_s", int, optional=False, default=2, doc=doc_g_s)
        ]

    return argu