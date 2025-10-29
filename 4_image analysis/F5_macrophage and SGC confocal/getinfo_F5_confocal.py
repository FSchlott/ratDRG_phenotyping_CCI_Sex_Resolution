import matplotlib.pyplot as plt
import numpy as np
from skimage import segmentation, measure 
from skimage.morphology import binary_dilation, binary_erosion, disk
from tqdm.auto import tqdm
import tifffile as tiff
import os

class ImageData : 
    def __init__ (self, subdir): 
        nfmask_paths = os.path.join(subdir, 'nf_pred/masks')
        iba1mask_paths = os.path.join(subdir, 'iba1_pred/masks')
        fabp7mask_paths = os.path.join(subdir, 'fabp7_pred/masks')
        nfcellpose_paths = os.path.join(subdir, 'nf_cellpose/cellpose_masks')  
         
        self.edges_pct_iba1_L = []
        self.inv_pct_iba1_L = [] 
        self.dil1_pct_iba1_L = []
        self.dil2_pct_iba1_L = []
        self.edges_pct_fabp7_L = []
        self.inv_pct_fabp7_L = [] 
        self.dil1_pct_fabp7_L = []
        self.dil2_pct_fabp7_L = []
        
        self.nf_anz_L = []
        self.nf_px_L = []
        self.iba1_anz_L = []
        self.iba1_px_L = []
        self.fabp7_anz_L = []
        self.fabp7_px_L = []

        self.ov_iba1_fabp7_L = []
        self.ov_iba1_per_fabp7_L = []


        for nfM_filename , fabp7M_filename , iba1M_filename, nfcp_filename in tqdm(zip(os.listdir(nfmask_paths), 
                                            os.listdir(fabp7mask_paths), [fn for fn in os.listdir(iba1mask_paths) if fn.endswith ("png")], 
                                            os.listdir(nfcellpose_paths))):
                                     
            nfM = plt.imread (os.path.join (nfmask_paths, nfM_filename))
            fabp7M = plt.imread (os.path.join (fabp7mask_paths, fabp7M_filename))
            iba1M = plt.imread (os.path.join (iba1mask_paths, iba1M_filename))
            nf_cp_labels = tiff.imread (os.path.join (nfcellpose_paths, nfcp_filename))

            
            iba1_anz, iba1_px = self.get_nonN_numbers (iba1M)
            fabp7_anz, fabp7_px = self.get_nonN_numbers (fabp7M) 
            ov_iba1_fabp7, ov_iba1_per_fabp7 = self.get_iba1_fabp7_ov (iba1M, fabp7M)
            nf_filtered_labels, nf_sizes, nf_anz = self.get_cellnum_sizes_cellpose (nf_cp_labels) 

            edges_pct_fabp7, inv_pct_fabp7, dil1_pct_fabp7, dil2_pct_fabp7 = self.get_circles_pct (nf_filtered_labels, fabp7M)
            edges_pct_iba1, inv_pct_iba1, dil1_pct_iba1, dil2_pct_iba1 = self.get_circles_pct (nf_filtered_labels, iba1M)
            
            
            self.iba1_anz_L.append (float(iba1_anz))
            self.iba1_px_L.append (float (iba1_px))
            self.fabp7_anz_L.append (float(fabp7_anz))
            self.fabp7_px_L.append (float (fabp7_px))
            self.nf_px_L.append (nf_sizes)
            self.nf_anz_L.append (float(nf_anz))

            self.ov_iba1_fabp7_L.append (float(ov_iba1_fabp7))
            self.ov_iba1_per_fabp7_L.append (float(ov_iba1_per_fabp7))

            self.edges_pct_iba1_L.append (edges_pct_iba1)
            self.dil1_pct_iba1_L.append (inv_pct_iba1)
            self.inv_pct_iba1_L.append (dil1_pct_iba1) 
            self.dil2_pct_iba1_L.append (dil2_pct_iba1)

            self.edges_pct_fabp7_L.append (edges_pct_fabp7)
            self.inv_pct_fabp7_L.append (inv_pct_fabp7) 
            self.dil1_pct_fabp7_L.append (dil1_pct_fabp7)
            self.dil2_pct_fabp7_L.append (dil2_pct_fabp7)
            

    #for neurons (here nf)
    def get_cellnum_sizes_cellpose (self, cellpose):
        sizes = []
        filtered_label = np.zeros([cellpose.shape[0], cellpose.shape[1]])
        count = 1
        for i in range(cellpose.max()+1):
            if i > 0:
                cell = cellpose==i
                if cell.sum() > 800:
                    filtered_label[cell] = int(count)
                    count +=1
                    sizes.append (float (cell.sum()))
        return np.uint16 (filtered_label), sizes, count
    
    #for non-neuronal cells
    def get_nonN_numbers (self, qM):
        labels , anz = measure.label (qM , return_num = True )  
        qsum = np.sum (qM)
        return anz , qsum
    
    #generates an overlap of Iba1 and Fabp7 and the percentage of the fabp7 label that is also iba1 positive (cell overlap)
    def get_iba1_fabp7_ov (self, iba1M, fabp7M):
        addM = iba1M + fabp7M
        overlap = (addM == 2)*1
        ov = np.sum (overlap) 
        ov_per_fabp7 = np.sum (overlap) / np.sum (fabp7M)
        return ov, ov_per_fabp7

    #overlap of the non-neuronal cells with the circular rings around the cells
    def get_OL_pct (self, circ, cellM):
        circ_px = np.sum (circ)
        OL = ((circ + cellM)==2)*1
        OL_px = OL.sum ()
        OL_pct = (OL_px/circ_px)*100
        return OL_pct
    
    #overlap of the non-neuronal cells with the neuron border, and rings inverted or outwards from it
    def get_circles_pct (self, n_label, cellM):
        inv_pct_L = []
        dil1_pct_L = []
        dil2_pct_L = []
        edges_pct_L = []
    
        for i in range (1, n_label.max()+1):
            neuron = (n_label==i)*1
            neuron_inv = (binary_erosion (neuron, disk (10)))*1
            neuron_dil1 = (binary_dilation (neuron, disk (10)))*1
            neuron_dil2 = (binary_dilation (neuron_dil1, disk (10)))*1
        
            inv = neuron - neuron_inv
            dil1 = neuron_dil1 - neuron
            dil2 = neuron_dil2 - neuron_dil1
            edges = (segmentation.find_boundaries (neuron, mode = "thick"))*1

            inv_pct = self.get_OL_pct (inv, cellM)
            dil1_pct = self.get_OL_pct (dil1, cellM)
            dil2_pct = self.get_OL_pct (dil2, cellM)
            edges_pct = self.get_OL_pct (edges, cellM)

            inv_pct_L.append (float (inv_pct))
            dil1_pct_L.append (float (dil1_pct))
            dil2_pct_L.append (float (dil2_pct))
            edges_pct_L.append (float (edges_pct))
        
        return edges_pct_L, inv_pct_L, dil1_pct_L, dil2_pct_L

