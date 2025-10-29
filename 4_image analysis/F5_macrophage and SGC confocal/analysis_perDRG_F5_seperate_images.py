import numpy as np

class GroupData:
    def __init__ (self, results_file , drg_side):
        self.results_file = results_file
        self.drg_side = drg_side

        self.name = "cci" + drg_side

        self.get_means_for_allrats ()

    def get_means_for_allrats (self):
        self.paths = []
        self.edges_pct_iba1_allrats = [] 
        self.inv_pct_iba1_allrats = []
        self.dil1_pct_iba1_allrats = []
        self.dil2_pct_iba1_allrats = []
        self.edges_pct_fabp7_allrats = [] 
        self.inv_pct_fabp7_allrats = []
        self.dil1_pct_fabp7_allrats = []
        self.dil2_pct_fabp7_allrats = []
        self.img_pct_iba1_allrats = []
        self.img_pct_fabp7_allrats = []

    
        self.nf_anz_permm2_allrats = []
        self.iba1_anz_permm2_allrats = []
        self.fabp7_anz_permm2_allrats = []
    
        self.nf_um_sc_allrats = []
        self.iba1_vol_per_anz_allrats = []
        self.fabp7_vol_per_anz_allrats = []

        self.img_pct_ov_iba1_fabp7_allrats = []

        #drg indicates the dictionary, group the side IL/CL  
        for drg in self.results_file:
            if self.drg_side in drg["group"]:
                self.get_means_perdrg (drg)

    def get_means_perdrg (self, drg): 
        nf_sc_um_L = []
        iba1_um_L = []
        iba1_vol_per_anz_L = []
        fabp7_um_L = []
        fabp7_vol_per_anz_L = []

        ov_iba1_fabp7_um_L = []
        ov_iba1_per_fabp7_um_L = []

        nf_anz_permm2_L = []
        iba1_anz_permm2_L = []
        fabp7_anz_permm2_L = []

        #calculates volume per cell and numbers per area 
        for nf_sc_px, nf_anz, iba1_anz , iba1_px, fabp7_anz, fabp7_px, ov_iba1_fabp7, ov_iba1_per_fabp7 in zip (
                        drg ["nf_px"], drg ["nf_anz"], drg ["iba1_anz"], drg ["iba1_px"], 
                        drg ["fabp7_anz"], drg ["fabp7_px"], drg ["ov_iba1_fabp7"],
                        drg ["ov_iba1_per_fabp7"]):
            
            iba1_um = iba1_px * 0.0428 #px to um2
            fabp7_um = fabp7_px * 0.0428

            nf_sc_um_L.append ([i * 0.0428 for i in nf_sc_px])
            iba1_um_L.append (iba1_um)
            fabp7_um_L.append (fabp7_um)
            ov_iba1_fabp7_um_L.append (ov_iba1_fabp7 * 0.0428)
            ov_iba1_per_fabp7_um_L.append (ov_iba1_per_fabp7 * 0.0428)

            #number per image; 1 img = 0.044931 mm^2
            nf_anz_permm2_L.append (nf_anz / 0.0449)
            iba1_anz_permm2_L.append (iba1_anz / 0.0449)
            fabp7_anz_permm2_L.append (fabp7_anz / 0.0449)

            if iba1_anz > 0 : 
                iba1_vol_per_anz = iba1_um / iba1_anz
            else:
                iba1_vol_per_anz = 0
            if fabp7_anz > 0:
                fabp7_vol_per_anz = fabp7_um / fabp7_anz
            else:
                fabp7_vol_per_anz = 0

            iba1_vol_per_anz_L.append (iba1_vol_per_anz)
            fabp7_vol_per_anz_L.append (fabp7_vol_per_anz)

        self.paths.append (drg["path"])
        self.edges_pct_iba1_allrats.append (self.get_list_mean (drg ["edges_pct_iba1"])) 
        self.inv_pct_iba1_allrats.append (self.get_list_mean (drg ["inv_pct_iba1"]))
        self.dil1_pct_iba1_allrats.append (self.get_list_mean (drg ["dil1_pct_iba1"]))
        self.dil2_pct_iba1_allrats.append (self.get_list_mean (drg ["dil2_pct_iba1"]))
        self.edges_pct_fabp7_allrats.append (self.get_list_mean (drg ["edges_pct_fabp7"])) 
        self.inv_pct_fabp7_allrats.append (self.get_list_mean (drg ["inv_pct_fabp7"]))
        self.dil1_pct_fabp7_allrats.append (self.get_list_mean (drg ["dil1_pct_fabp7"]))
        self.dil2_pct_fabp7_allrats.append (self.get_list_mean (drg ["dil2_pct_fabp7"]))

        self.img_pct_iba1_allrats.append ([(i/44931.28)*100 for i in iba1_um_L])
        self.img_pct_fabp7_allrats.append ([(i/44931.28)*100 for i in fabp7_um_L])
        self.img_pct_ov_iba1_fabp7_allrats.append ([(i/44931.28)*100 for i in ov_iba1_fabp7_um_L])

        self.nf_anz_permm2_allrats.append (np.mean (nf_anz_permm2_L))
        self.iba1_anz_permm2_allrats.append (np.mean (iba1_anz_permm2_L))
        self.fabp7_anz_permm2_allrats.append (np.mean (fabp7_anz_permm2_L))
        self.nf_um_sc_allrats.append (np.mean (self.get_list_mean (nf_sc_um_L)))
        self.iba1_vol_per_anz_allrats.append (np.mean (iba1_vol_per_anz_L)) 
        self.fabp7_vol_per_anz_allrats.append (np.mean (fabp7_vol_per_anz_L))
        

    def get_list_mean (self, drgfeature):
        L_mean = []
        for L in drgfeature: 
                L_mean.append (np.mean (L))
        return L_mean