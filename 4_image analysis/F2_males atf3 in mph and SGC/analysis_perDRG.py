import numpy as np

class GroupData:
    def __init__ (self, results_file , drg_side , anz_rats ):
        self.results_file = results_file
        self.drg_side = drg_side

        self.name = "w5cci" + drg_side

        self.get_means_for_allrats (anz_rats)

    def get_means_for_allrats (self, anz_rats):
        self.paths = []
        self.iba1_borders_n_allrats = [] 
        self.iba1_borders_atf3_allrats = []
        self.iba1_borders_atf3_neg_allrats = []
        self.gs_borders_n_allrats = [] 
        self.gs_borders_atf3_allrats = []
        self.gs_borders_atf3_neg_allrats = []

        self.iba1_neuronratio_borders_n_allrats = [] 
        self.iba1_neuronratio_borders_atf3_allrats = []
        self.iba1_neuronratio_borders_atf3_neg_allrats = []
        self.gs_neuronratio_borders_n_allrats = [] 
        self.gs_neuronratio_borders_atf3_allrats = []
        self.gs_neuronratio_borders_atf3_neg_allrats = []
        
        self.gs_iba1_proximity_allrats = []

        self.n_anz_allrats = []
        self.atf3_anz_allrats = []
        self.atf3_neg_anz_allrats = []
        self.n_sizes_allrats = []
        self.atf3_sizes_allrats = []
        self.atf3_neg_sizes_allrats = []

          
        for n in range (anz_rats):
            rat = "R"+str(n+1)
            for i, drg in enumerate (self.results_file):
                if self.drg_side in drg["group"] and rat in self.results_file[i]['path']:
                    self.get_means_perdrg (drg)

       
    def get_means_perdrg (self, drg): 

        self.paths.append (drg["path"])
        self.iba1_borders_n_allrats.append (np.nanmean (self.get_borderratio_mean (drg ["iba1_borders_n"]))) 
        self.iba1_borders_atf3_allrats.append (np.nanmean (self.get_borderratio_mean (drg ["iba1_borders_atf3"])))
        self.iba1_borders_atf3_neg_allrats.append (np.nanmean (self.get_borderratio_mean (drg ["iba1_borders_atf3_neg"])))
        self.gs_borders_n_allrats.append (np.nanmean (self.get_borderratio_mean (drg ["gs_borders_n"]))) 
        self.gs_borders_atf3_allrats.append (np.nanmean (self.get_borderratio_mean (drg ["gs_borders_atf3"])))
        self.gs_borders_atf3_neg_allrats.append (np.nanmean (self.get_borderratio_mean (drg ["gs_borders_atf3_neg"])))

        self.iba1_neuronratio_borders_n_allrats.append (np.nanmean(self.get_neuronratio (drg ["iba1_borders_n"],drg["n_anz"])))
        self.iba1_neuronratio_borders_atf3_allrats.append (np.nanmean(self.get_neuronratio (drg ["iba1_borders_atf3"],drg["atf3_anz"])))
        self.iba1_neuronratio_borders_atf3_neg_allrats.append (np.nanmean(self.get_neuronratio (drg ["iba1_borders_atf3_neg"],drg["atf3_neg_anz"])))
        self.gs_neuronratio_borders_n_allrats.append (np.nanmean(self.get_neuronratio (drg ["gs_borders_n"],drg["n_anz"])))
        self.gs_neuronratio_borders_atf3_allrats.append (np.nanmean(self.get_neuronratio (drg ["gs_borders_atf3"],drg["atf3_anz"])))
        self.gs_neuronratio_borders_atf3_neg_allrats.append (np.nanmean(self.get_neuronratio (drg ["gs_borders_atf3_neg"],drg["atf3_neg_anz"])))

        self.gs_iba1_proximity_allrats.append (np.mean(drg ["gs_iba1_proximity"]))

        self.n_anz_allrats.append (np.mean(drg ["n_anz"]))
        self.atf3_anz_allrats.append (np.mean(drg ["atf3_anz"]))
        self.atf3_neg_anz_allrats.append (np.mean(drg ["atf3_neg_anz"]))

        self.n_sizes_allrats.append (np.nanmean (self.get_sizes_mean (drg ["n_sizes"])))
        self.atf3_sizes_allrats.append (np.nanmean (self.get_sizes_mean (drg ["atf3_sizes"])))
        self.atf3_neg_sizes_allrats.append (np.nanmean (self.get_sizes_mean (drg ["atf3_neg_sizes"])))
    

    def get_neuronratio (self , drgfeature_borders , drgfeature_anz ):
        ringratio_L = []
        for ring_touched, n_anz in zip (drgfeature_borders, drgfeature_anz):
            number_of_rings = len([i for i in ring_touched if i>0])
            if number_of_rings == 0:
                ringratio_L.append (0)
            else: 
                ratio_iba1_all = (number_of_rings/n_anz)*100
                ringratio_L.append (ratio_iba1_all)
        return  ringratio_L
        
    def get_borderratio_mean (self, drgfeature_borders):
        borderratio_mean = []
        for borderratios in drgfeature_borders:
            borderratios = borderratios *100
            borderratio_mean.append (np.mean (borderratios))
        return borderratio_mean

    def get_sizes_mean (self, drgfeature_sizes):
        sizes_mean = []
        for sizes in drgfeature_sizes: 
                sizes_mean.append (np.mean (sizes))
        return sizes_mean