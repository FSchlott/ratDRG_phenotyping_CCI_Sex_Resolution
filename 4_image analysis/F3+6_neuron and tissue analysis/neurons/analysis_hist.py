
import numpy as np


class GroupData:
    def __init__ (self, results_file , drg_side):
        self.results_file = results_file
        self.drg_side = drg_side

        self.name = "cci" + drg_side

        self.get_numbers_from_allrats ()


    def get_numbers_from_allrats (self):
        self.paths = []
        self.nf_sizecounts_allrats = []
        self.binsizes = None
        self.ib4_sizecounts_allrats = []
 
        for drg in self.results_file:
            if self.drg_side in drg["group"]:
                self.get_numbers_perdrg (drg)

    # collect data per DRG from all images  
    def get_numbers_perdrg (self, drg): #see get_means_for_allrats
        self.paths.append (drg["path"])
        nf_sizecounts , ib4_sizecounts , binsizes = self.get_hist_data (drg)

        self.nf_sizecounts_allrats.append (np.mean(nf_sizecounts, axis = 0).tolist())
        self.binsizes = binsizes
        self.ib4_sizecounts_allrats.append (np.mean(ib4_sizecounts, axis = 0).tolist())
        

    def get_hist_data (self, drg):
        nf_sizecounts = []
        ib4_sizecounts = []

        for nf_sizes_px, nf_anz , ib4_sizes_px  in zip (drg ["nf_sizes"], drg ["nf_anz"], drg ["ib4_sizes"] ):
            if nf_anz > 0:
                #sizes in um from px --> 1 px 0.814um2
                nf_sizes = np.array(nf_sizes_px)*0.814
                nf_sizes [nf_sizes>3000] = 3000
                ib4_sizes = np.array(ib4_sizes_px)*0.814
                ib4_sizes [ib4_sizes>3000] = 3000

                nf_counts, bins = np.histogram (nf_sizes, bins = 15 , range = (0, 3000))
                ib4_counts, bins = np.histogram (ib4_sizes, bins = 15 , range = (0, 3000))

                nf_counts_percent = nf_counts/nf_counts.sum()*100
                ib4_counts_percent = ib4_counts/nf_counts.sum()*100
                
                nf_sizecounts.append(nf_counts_percent.tolist())
                ib4_sizecounts.append(ib4_counts_percent.tolist())
                
        return nf_sizecounts , ib4_sizecounts  , bins
