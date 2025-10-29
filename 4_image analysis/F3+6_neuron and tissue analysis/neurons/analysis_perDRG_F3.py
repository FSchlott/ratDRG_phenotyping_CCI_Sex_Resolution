import numpy as np

class GroupData:
    def __init__ (self, results_file , drg_side):
        self.results_file = results_file
        self.drg_side = drg_side

        self.name = "cci" + drg_side

        self.get_means_for_allrats ()

    def get_means_for_allrats (self):
        self.paths = []
        self.atf3_per_nf_allrats = [] 
        self.atf3_per_ib4_allrats = []
        self.ib4_per_nf_allrats = []
        self.ib4_per_atf3_allrats = []
        self.nf_anz_allrats = []
        self.atf3_anz_allrats = []        
        self.ib4_anz_allrats = []

        for drg in self.results_file:
            if self.drg_side in drg["group"]:
                self.get_means_perdrg (drg)
  
    def get_means_perdrg (self, drg): 
        self.paths.append (drg["path"])
        self.atf3_per_nf_allrats.append (np.mean(drg ["atf3_per_nf"]))
        self.atf3_per_ib4_allrats.append (np.mean (drg ["atf3_per_ib4"]))
        self.ib4_per_nf_allrats.append (np.mean (drg ["ib4_per_nf"]))
        self.ib4_per_atf3_allrats.append (np.mean (drg ["ib4_per_atf3"]))
        self.nf_anz_allrats.append (np.mean (drg ["nf_anz"]))
        self.ib4_anz_allrats.append (np.mean (drg ["ib4_anz"]))
        self.atf3_anz_allrats.append (np.mean (drg ["atf3_anz"]))


