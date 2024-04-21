import numpy as np
from material import *
from glass import *
import json

class Layer():
    """ Coating Layer

    """
    def __init__(self, mat=None, t=0.0) -> None:
        self.thickness = t
        self.material  = mat
        self.theta     = complex(0.0,0.0) # angle in radian

    def delta(self, wavelength:float):
        N = self.material.complex_refractive_index(wavelength)
        return 2*np.pi*N*self.thickness*np.cos(self.theta)/wavelength

    def eta(self, polarize:str, wavelength:float):
        N = self.material.complex_refractive_index(wavelength)
        if polarize == 'p':
            return N/np.cos(self.theta)
        elif polarize == 's':
            return N*np.cos(self.theta)
        else:
            raise ValueError("Polalization must be 'p' or 's'")
        
    def characteristic_matrix(self, polarize:str, wavelength:float):
        i = 0 + 1j
        eta = self.eta(polarize, wavelength)
        delta = self.delta(wavelength)
        M = np.zeros([2,2], dtype=complex)
        M[0][0] = np.cos(delta)
        M[0][1] = i*np.sin(delta)/eta
        M[1][0] = i*eta*np.sin(delta)
        M[1][1] = np.cos(delta)
        return M


class Substrate:
    def __init__(self) -> None:
        self.theta = complex(0.0, 0.0) #angle in radian
        self.material:Glass = None

class LayerStackModel:
    """ Layer stack model
        Air, 0, 1, 2 ... ,n, Substrate 
    """
    
    def __init__(self) -> None:
        self.substrate       = Substrate()
        self.ambient         = Air()
        self.layers          = []
        self.__wavelength:float     = 0.55
        self.__incident_angle:float = 0.0

    def __str__(self):
        txt = "Angle: " + str(self.incident_angle) + "\n"
        txt += "Substrate: " + self.substrate.name + "\n"
        txt += "Material" + "\t" + "Thickness" + "\n"
        for layer in self.layers:
            txt += layer.material.name + "\t" + str(layer.thickness) + "\n"

        return txt
    
    @property
    def wavelength(self):
        return self.__wavelength
    
    @wavelength.setter
    def wavelength(self, lambdamicron:float):
        self.__wavelength = lambdamicron
        self.update()

    @property
    def incident_angle(self):
        return self.__incident_angle
    
    @incident_angle.setter
    def incident_angle(self, angle_in_radian:float):
        self.__incident_angle = angle_in_radian
        self.update()

    @property
    def number_of_layers(self):
        return len(self.layers)
    
    def load_json(self, json_file_path:str):
        pass
    
    def save_as_json(self, json_file_path:str):
        with open(json_file_path, 'w') as f:
            json.dump(self, f, indent=4)

    def set_layers(self, material_and_thickness:list):
        self.layers.clear
        for mat,t in material_and_thickness:
            self.layers.append(Layer(mat, t))

        self.update()
    
    def update(self):
        wavelength = self.__wavelength
        sin_theta_i = np.sin(self.__incident_angle)
        ni = self.ambient.complex_refractive_index(wavelength)
        for current_layer in self.layers:
            nr = current_layer.material.complex_refractive_index(wavelength)
            sin_theta_r = (ni/nr)*sin_theta_i
            current_layer.theta = np.arcsin(sin_theta_r)
            sin_theta_i = sin_theta_r
            ni = nr
        
        # substrate
        last_layer_sin_theta = sin_theta_r
        nr = self.substrate.material.complex_refractive_index(wavelength)
        subs_sin_theta = (ni/nr)*last_layer_sin_theta
        self.substrate.theta = np.arcsin(subs_sin_theta)
        

    def characteristic_matrix(self, polarize:str):
        wavelength = self.__wavelength
        M = np.eye(2,2)
        for layer in self.layers:
            Mr = layer.characteristic_matrix(polarize, wavelength)
            M = M @ Mr
        return M

    def amplitude_coefficients(self, polarize:str):
        M = self.characteristic_matrix(polarize)
        Nsubs = self.substrate.material.complex_refractive_index(self.wavelength)
        eta_subs = Nsubs
        if polarize == 'p':
            eta_subs = Nsubs/np.cos(self.__incident_angle)
        elif polarize == 's':
            eta_subs = Nsubs * np.cos(self.__incident_angle)
        S = np.array([1, eta_subs])
        BC = M @ S
        B = BC[0]
        C = BC[1]

        Namb = self.ambient.complex_refractive_index(self.wavelength)
        eta_amb = Namb
        if polarize == 'p':
            eta_amb = Namb / np.cos(self.__incident_angle)
        elif polarize == 's':
            eta_amb = Namb * np.cos(self.__incident_angle)

        rho = (eta_amb*B - C) / (eta_amb*B + C)
        tau = (2*eta_amb) / (eta_amb*B + C)
        return rho, tau
    
    def reflection(self, polarize:str) -> float:
        rho, tau = self.amplitude_coefficients(polarize)
        R = rho * rho.conjugate()
        return R.real

    def transmittance(self, polarize:str) -> float:
        rho, tau = self.amplitude_coefficients(polarize)
        Namb = self.ambient.complex_refractive_index(self.wavelength)
        Nsubs = self.substrate.complex_refractive_index(self.wavelength)
        T = (Nsubs/Namb)*tau*tau.conjugate()
        return T.real


    

