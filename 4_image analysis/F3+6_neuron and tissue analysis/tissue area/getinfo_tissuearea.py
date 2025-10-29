from tqdm.auto import tqdm
import os
import tifffile as tiff
import numpy as np
import matplotlib.pyplot as plt


class ImageData : 
    def __init__ (self, subdir):
        nfcellpose_paths = os.path.join(subdir, 'nf_cellpose/cellpose_masks')
        ib4cellpose_paths = os.path.join(subdir, 'ib4_cellpose/cellpose_masks')
        tissue_paths = os.path.join(subdir, 'nf_tissue/masks')

        self.tissue_area_L = []
        self.neuron_area_L = []
        self.ib4_area_L = []
        self.nf_anz_L = []
        self.ib4_anz_L = []

        
        for nfcp_filename, ib4cp_filename, tissue_filename in tqdm(zip(os.listdir(nfcellpose_paths), 
                                                        os.listdir(ib4cellpose_paths), os.listdir(tissue_paths))):
            nf_cp_labels = tiff.imread (os.path.join (nfcellpose_paths, nfcp_filename))
            ib4_cp_labels = tiff.imread (os.path.join (ib4cellpose_paths, ib4cp_filename))
            tissueM = plt.imread (os.path.join (tissue_paths, tissue_filename))
            nfM = (nf_cp_labels > 0) *1
            ib4M = (ib4_cp_labels > 0)*1

            ib4_anz , ib4_sizes = self.get_cellnum_sizes_cellpose (ib4_cp_labels)
            nf_anz , nf_sizes  = self.get_cellnum_sizes_cellpose (nf_cp_labels) 
          
            self.nf_anz_L.append (float(nf_anz))
            self.ib4_anz_L.append (float(ib4_anz))

            self.tissue_area_L.append (float(np.sum (tissueM)))
            self.neuron_area_L.append (float(np.sum (nfM)))
            self.ib4_area_L.append (float(np.sum (ib4M)))

            
                       

    def get_overlapM (self, mask1 , mask2):
        addM = (mask1 + mask2)
        overlapM = (addM ==2)*1
        return overlapM
    
    def get_cellnum_sizes_cellpose (self, cellpose):
        sizes = []
        filtered_label = np.zeros([cellpose.shape[0], cellpose.shape[1]])
        count = 1
        for i in range(cellpose.max()+1):
            if i > 0:
                cell = cellpose==i
                if cell.sum() > 150:
                    filtered_label[cell] = int(count)
                    count +=1
                    sizes.append (float (cell.sum()))
        return count, sizes
        