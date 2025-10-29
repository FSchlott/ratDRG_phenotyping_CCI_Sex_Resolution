import numpy as np

class GroupData:
    def __init__ (self, results_file , drg_side):
        self.results_file = results_file
        self.drg_side = drg_side

        self.name = "cci" + drg_side

        self.get_lists_for_allrats ()

    def get_lists_for_allrats (self):
        
        self.paths = []
        self.nf_anz_allrats = []       
        self.ib4_anz_allrats = []
        self.tissuearea_px_allrats = []
        self.neuronarea_px_allrats = []
        self.ib4area_px_allrats = []

        self.tissuearea_mm2_allrats = []
        self.neuronarea_mm2_allrats = []
        self.ib4area_mm2_allrats = []

        self.nf_anz_sum_allrats = []       
        self.ib4_anz_sum_allrats = []
        self.tissuearea_mm2_sum_allrats = []
        self.neuronarea_mm2_sum_allrats = []
        self.ib4area_mm2_sum_allrats = []

        self.anz_slices_allrats = []
        self.neuronarea_per_tissue = []
        self.neuronnumber_per_tissue = []
        self.ib4area_per_tissue = []
        self.ib4number_per_tissue = []
        self.ib4number_per_nfnumber = []

        for drg in self.results_file:
            if self.drg_side in drg["group"]:
                self.get_data_perdrg (drg)
  
    def get_data_perdrg (self, drg): 
        self.paths.append (drg["path"])
        self.nf_anz_allrats.append (drg ["nf_anz"])
        self.ib4_anz_allrats.append (drg ["ib4_anz"])
        self.tissuearea_px_allrats.append (drg ["tissue_area_px"])
        self.neuronarea_px_allrats.append (drg ["neuron_area_px"])
        self.ib4area_px_allrats.append (drg ["ib4_area_px"])

        tissuearea_mm2 = [i*0.00000082447 for i in drg ["tissue_area_px"]]
        neuronarea_mm2 = [i*0.00000082447 for i in drg ["neuron_area_px"]]
        ib4area_mm2 = [i*0.00000082447 for i in drg ["ib4_area_px"]]
        self.tissuearea_mm2_allrats.append (np.mean (tissuearea_mm2))
        self.neuronarea_mm2_allrats.append (np.mean (neuronarea_mm2))
        self.ib4area_mm2_allrats.append (np.mean (ib4area_mm2))

        self.nf_anz_sum_allrats.append (np.sum (drg ["nf_anz"]))
        self.ib4_anz_sum_allrats.append (np.sum (drg ["ib4_anz"]))
        self.tissuearea_mm2_sum_allrats.append (np.sum (tissuearea_mm2))
        self.neuronarea_mm2_sum_allrats.append (np.sum (neuronarea_mm2))
        self.ib4area_mm2_sum_allrats.append (np.sum (ib4area_mm2))  

        self.anz_slices_allrats.append (len(drg ["nf_anz"]))
        self.neuronarea_per_tissue.append ((np.sum (neuronarea_mm2)) / (np.sum (tissuearea_mm2)))
        self.neuronnumber_per_tissue.append ((np.sum (drg ["nf_anz"])) / (np.sum (tissuearea_mm2)))
        self.ib4area_per_tissue.append ((np.sum (ib4area_mm2)) / (np.sum (tissuearea_mm2)))
        self.ib4number_per_tissue.append ((np.sum (drg ["ib4_anz"])) / (np.sum (tissuearea_mm2)))
        self.ib4number_per_nfnumber.append ((np.sum (drg ["ib4_anz"])) /(np.sum (drg ["nf_anz"])))
        

        


