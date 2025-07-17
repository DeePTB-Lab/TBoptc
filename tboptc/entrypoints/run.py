import os
import logging
import json
from typing import Optional
from pathlib import Path
from tboptc.utils.loggers import set_log_handles
from tboptc.utils.argcheck import normalize_run
from tboptc.utils.tools import j_loader
from tboptc.utils.tools import j_must_have
from tboptc.calc.optical_cond import AcCond


log = logging.getLogger(__name__)

def run(
        INPUT: str,
        init_model: str,
        structure: str,
        output: str,
        log_level: int,
        log_path: Optional[str],
        **kwargs
        ):

    run_opt = {
        "init_model":init_model,
        "structure":structure,
        "log_path": log_path,
        "log_level": log_level,
    }

    if output:
        Path(output).parent.mkdir(exist_ok=True, parents=True)
        Path(output).mkdir(exist_ok=True, parents=True)
        results_path = os.path.join(str(output), "results")
        Path(results_path).mkdir(exist_ok=True, parents=True)
        if not log_path:
            log_path = os.path.join(str(output), "log/log.txt")
        Path(log_path).parent.mkdir(exist_ok=True, parents=True)

        run_opt.update({
                        "output": str(Path(output).absolute()),
                        "results_path": str(Path(results_path).absolute()),
                        "log_path": str(Path(log_path).absolute())
                    })

    set_log_handles(log_level, Path(log_path) if log_path else None)

    jdata = j_loader(INPUT)
    jdata = normalize_run(jdata)

    task_options = j_must_have(jdata, "task_options")
    task = task_options["task"]
    results_path = run_opt.get("results_path", None)

    in_common_options = {}
    if jdata.get("device", None):
        in_common_options.update({"device": jdata["device"]})
    
    if jdata.get("dtype", None):
        in_common_options.update({"dtype": jdata["dtype"]})

    model = build_model(checkpoint=init_model, common_options=in_common_options)
    
    if  run_opt['structure'] is None:
        log.warning(msg="Warning! structure is not set in run option, read from input config file.")
        structure = j_must_have(jdata, "structure")
        run_opt.update({"structure":structure})

    struct_file = run_opt["structure"]


    if task == 'ac_cond':
        accondcal = AcCond(model=model, results_path=results_path)
        
        accondcal.get_accond(struct=struct_file, 
                                AtomicData_options=jdata.get('AtomicData_options',None),
                                pbc = jdata['task_options'].get('pbc',None),
                                emax=jdata['task_options'].get('emax'),
                                num_omega=jdata['task_options'].get('num_omega',1000),
                                mesh_grid=jdata['task_options'].get('mesh_grid',[1,1,1]),
                                nk_per_loop=jdata['task_options'].get('nk_per_loop',None),
                                delta=jdata['task_options'].get('delta',0.03),
                                e_fermi=jdata['task_options'].get('e_fermi',0),
                                valence_e=jdata['task_options'].get('valence_e',None),
                                gap_corr=jdata['task_options'].get('gap_corr',0),
                                T=jdata['task_options'].get('T',300),
                                direction=jdata['task_options'].get('direction','xx'),
                                g_s=jdata['task_options'].get('g_s',2)
                            )
        accondcal.accond_plot()
        log.info(msg='ac optical conductivity calculation successfully completed.')

    else:
        log.error(msg="Warning! task is not set in run option, read from input config file.")
        raise NotImplementedError