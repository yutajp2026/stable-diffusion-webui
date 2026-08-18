import os
import sys
import types
import importlib.util
from modules.paths_internal import models_path, script_path, data_path, extensions_dir, extensions_builtin_dir, cwd  # noqa: F401

import modules.safe  # noqa: F401


def ensure_taming_stub():
    """Provide a minimal taming namespace for legacy SD imports when the optional package is absent."""
    if 'taming' in sys.modules:
        return

    taming = types.ModuleType('taming')
    taming.__path__ = []
    sys.modules['taming'] = taming

    modules_pkg = types.ModuleType('taming.modules')
    modules_pkg.__path__ = []
    sys.modules['taming.modules'] = modules_pkg

    losses_pkg = types.ModuleType('taming.modules.losses')
    losses_pkg.__path__ = []
    sys.modules['taming.modules.losses'] = losses_pkg

    vqvae_pkg = types.ModuleType('taming.modules.vqvae')
    vqvae_pkg.__path__ = []
    sys.modules['taming.modules.vqvae'] = vqvae_pkg

    vendored_quantize = os.path.join(script_path, 'extensions-builtin/LDSR/vqvae_quantize.py')
    if os.path.exists(vendored_quantize):
        spec = importlib.util.spec_from_file_location('taming.modules.vqvae.quantize', vendored_quantize)
        quantize_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(quantize_mod)
        sys.modules['taming.modules.vqvae.quantize'] = quantize_mod
    else:
        quantize_mod = types.ModuleType('taming.modules.vqvae.quantize')
        quantize_mod.__all__ = []
        sys.modules['taming.modules.vqvae.quantize'] = quantize_mod

    lpips = types.ModuleType('taming.modules.losses.lpips')
    lpips.LPIPS = None
    sys.modules['taming.modules.losses.lpips'] = lpips

    vqvae_pkg.quantize = sys.modules['taming.modules.vqvae.quantize']
    vqvae_pkg.VectorQuantizer2 = getattr(sys.modules['taming.modules.vqvae.quantize'], 'VectorQuantizer2', None)


def mute_sdxl_imports():
    """create fake modules that SDXL wants to import but doesn't actually use for our purposes"""

    ensure_taming_stub()

    class Dummy:
        pass

    module = Dummy()
    module.LPIPS = None
    sys.modules['taming.modules.losses.lpips'] = module

    module = Dummy()
    module.StableDataModuleFromConfig = None
    sys.modules['sgm.data'] = module


# data_path = cmd_opts_pre.data
sys.path.insert(0, script_path)

# search for directory of stable diffusion in following places
sd_path = None
possible_sd_paths = [os.path.join(script_path, 'repositories/stable-diffusion-stability-ai'), '.', os.path.dirname(script_path)]
for possible_sd_path in possible_sd_paths:
    if os.path.exists(os.path.join(possible_sd_path, 'ldm/models/diffusion/ddpm.py')):
        sd_path = os.path.abspath(possible_sd_path)
        break

assert sd_path is not None, f"Couldn't find Stable Diffusion in any of: {possible_sd_paths}"

mute_sdxl_imports()

path_dirs = [
    (sd_path, 'ldm', 'Stable Diffusion', []),
    (os.path.join(sd_path, '../generative-models'), 'sgm', 'Stable Diffusion XL', ["sgm"]),
    (os.path.join(sd_path, '../BLIP'), 'models/blip.py', 'BLIP', []),
    (os.path.join(sd_path, '../k-diffusion'), 'k_diffusion/sampling.py', 'k_diffusion', ["atstart"]),
]

paths = {}

for d, must_exist, what, options in path_dirs:
    must_exist_path = os.path.abspath(os.path.join(script_path, d, must_exist))
    if not os.path.exists(must_exist_path):
        print(f"Warning: {what} not found at path {must_exist_path}", file=sys.stderr)
    else:
        d = os.path.abspath(d)
        if "atstart" in options:
            sys.path.insert(0, d)
        elif "sgm" in options:
            # Stable Diffusion XL repo has scripts dir with __init__.py in it which ruins every extension's scripts dir, so we
            # import sgm and remove it from sys.path so that when a script imports scripts.something, it doesbn't use sgm's scripts dir.

            sys.path.insert(0, d)
            import sgm  # noqa: F401
            sys.path.pop(0)
        else:
            sys.path.append(d)
        paths[what] = d
