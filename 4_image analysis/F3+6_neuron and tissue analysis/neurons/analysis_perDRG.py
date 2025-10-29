import numpy as np

class GroupData:
    def __init__ (self, results_file , drg_side):
        self.results_file = results_file
        self.drg_side = drg_side

        self.name = "cci" + drg_side

        self.get_means_for_allrats ()

    def get_means_for_allrats (self):
        self.paths = []
        self.ib4_per_nf_allrats = []
        self.ib4oL_per_nf_allrats = []
        self.nf_anz_allrats = []        
        self.ib4_anz_allrats = []

        for drg in self.results_file:
            if self.drg_side in drg["group"]:
                self.get_means_perdrg (drg)
  
    def get_means_perdrg (self, drg): 
        self.paths.append (drg["path"])
        self.ib4_per_nf_allrats.append (np.mean (drg ["ib4_per_nf"]))
        self.ib4oL_per_nf_allrats.append (np.mean (drg ["ib4oL_per_nf"]))
        self.nf_anz_allrats.append (np.mean (drg ["nf_anz"]))
        self.ib4_anz_allrats.append (np.mean (drg ["ib4_anz"]))


