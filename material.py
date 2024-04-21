import numpy as np
from scipy import interpolate


class Material:
    """Material for optical thin film

    This class defines materials for optical thin film layer.
    Both dielectric and metaic materials are accepted.

    Attributes:
        name(str): material name
        MATE_data(list): Zemax MATE style data of N=n+ik list for every wavelength.    

    """

    def __init__(self) -> None:
        self.name = ''
        self.mate_data = []
        self.interp = None
    
    def __str__(self):
        txt = "MATE\t" + self.name + "\n"
        for data in self.mate_data:
            txt += str(data[0]) + "\t" + str(data[1]) + "\t" + str(data[2])
            txt += "\n"
        return txt

    def update(self):
        """ create complex refractive index interpolation function
        """
        if len(self.mate_data) > 2:
            lambda_list = [w for w,n,k in self.mate_data]
            value_list  = [[n,k] for w,n,k in self.mate_data]
            self.interp = interpolate.PchipInterpolator(lambda_list, value_list, axis=0)
        else:
            self.interp = None

    def complex_refractive_index(self, wavelength):
        """ Computes complex refractive index for the given wavelength

        Values are interpolated from MATE data    

        """
        if self.interp is None:
            n = self.mate_data[0][0]
            k = self.mate_data[0][1]
        else:
            nk_interp = self.interp(wavelength)
            n = nk_interp[0]
            k = nk_interp[1]
        
        return complex(n, k)
    

class MaterialLibrary:
    """ Material library

    This class manages materials for thin films.
    The materials are defined in MATE format that is used in Zemax.
    """
    def __init__(self, dat_file_path:str ="") -> None:
        self.materials = []
        if dat_file_path != "":
            self.load_dat_file(dat_file_path)

    def get_material_name_list(self) -> list:
        """
        Returns material name list
        """
        names = []
        for m in self.materials:
            names.append(m.name)
        return names

    def find_material(self, name):
        """ Find and get material object from the given name
        """
        for m in self.materials:
            if name == m.name:
                return m
        
        print("Not found material: " + name)
        return None

    def load_dat_file(self, filepath:str) -> None:
        """ Load .DAT file and obtain material data

        Args:
            filepath(str): DAT file path
        """
        self.materials.clear

        f = open(filepath, 'r')
        lines = f.readlines()
        num_lines = len(lines)
        
        i = 0
        while i < num_lines:
            line = lines[i].strip()
            if line.startswith('MATE'):
                self.materials.append(Material())
                self.materials[-1].name = line.lstrip('MATE').strip()
                #print(self.materials[-1].name)
                i += 1
                while True:
                    line = lines[i]
                    lineparts = line.rstrip().split()
                    if len(lineparts) == 3:
                        w = float(lineparts[0])
                        n = float(lineparts[1])
                        k = float(lineparts[2])
                        self.materials[-1].mate_data.append([w,n,k])
                        i += 1
                    else:
                        break
            i += 1
        
        # update all materials
        for m in self.materials:
            m.update()

