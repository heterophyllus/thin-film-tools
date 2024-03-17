from model import *


class ThinfilmProject:
    def __init__(self) -> None:

        self.material_lib = MaterialLibrary()
        self.material_lib.load_dat_file("./dat/COATING.dat")
        self.glass_lib = GlassLibrary()
        self.glass_lib.load_agf("./agf/OHARA.agf")

        self.layer_stack_model = LayerStackModel()




        