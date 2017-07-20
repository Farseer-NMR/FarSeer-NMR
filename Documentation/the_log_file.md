Farseer-NMR outputs all the operations performed in real time to the `Terminal` window and, at the end of the calculations, to a text log file which follows [Markdown syntax](https://en.wikipedia.org/wiki/Markdown).

**Example of a farseer_log.md file:**

*******************************************************************************  
**LOG STARTED:** 2017/07/12 - 16:58:09 
*******************************************************************************  

*******************************************************************************  
### INITIATES FARSEER SET  
*******************************************************************************  
  
path: /home/user/Farseer-NMR/tutorial/Example1/spectra  
side chains: False  
FASTA starting residue: 1    

*******************************************************************************  
### READING INPUT FILES *.CSV*  
*******************************************************************************  
  
* /home/user/Farseer-NMR/tutorial/Example1/spectra/298/L1/0000.csv  
* /home/user/Farseer-NMR/tutorial/Example1/spectra/298/L1/0125.csv  
* /home/user/Farseer-NMR/tutorial/Example1/spectra/298/L1/0250.csv  
* /home/user/Farseer-NMR/tutorial/Example1/spectra/298/L1/0500.csv  
* /home/user/Farseer-NMR/tutorial/Example1/spectra/298/L1/1000.csv  
* /home/user/Farseer-NMR/tutorial/Example1/spectra/298/L1/2000.csv  
* /home/user/Farseer-NMR/tutorial/Example1/spectra/298/L1/4000.csv  
> All <.csv> files found - OK!  

*******************************************************************************  
### READING INPUT FILES *.FASTA*  
*******************************************************************************  
  
* /home/user/Farseer-NMR/tutorial/Example1/spectra/298/L1/pseq.fasta  
  * 1-MDAVEKNQFFELEQNPMCRGDSTMGLPVEMEECQINIQDKIDNPLQLNWTMNEVDQAGNFWKPNDSECSDRRYYPEIPSWCLSNMIEPCNMCMGMQHYEP-100  
> All <.fasta> files found - OK!  

*******************************************************************************  
### IDENTIFIED TITRATION VARIABLES  
*******************************************************************************  
  
* 1st titration variables (cond1): ['0000', '0125', '0250', '0500', '1000', '2000', '4000']
* 2nd titration variables (cond2): ['L1']
* 3rd titration variables (cond3): ['298']
  

*******************************************************************************  
### IDENTIFIES RESIDUE INFORMATION FROM ASSIGNMENT COLUMN  
*******************************************************************************  
  
**[298][L1][0000]** new columns inserted:  OK  | sidechains user setting: False | sidechains identified: False | SD count: 0  
**[298][L1][0125]** new columns inserted:  OK  | sidechains user setting: False | sidechains identified: False | SD count: 0  
**[298][L1][0250]** new columns inserted:  OK  | sidechains user setting: False | sidechains identified: False | SD count: 0  
**[298][L1][0500]** new columns inserted:  OK  | sidechains user setting: False | sidechains identified: False | SD count: 0  
**[298][L1][1000]** new columns inserted:  OK  | sidechains user setting: False | sidechains identified: False | SD count: 0  
**[298][L1][2000]** new columns inserted:  OK  | sidechains user setting: False | sidechains identified: False | SD count: 0  
**[298][L1][4000]** new columns inserted:  OK  | sidechains user setting: False | sidechains identified: False | SD count: 0  

*******************************************************************************  
### ADDS LOST RESIDUES BASED ON THE REFERENCE  
*******************************************************************************  
  
**[298][L1][0000]** vs. [298][L1][0000] | Target Initial Length :: 90 | Template Length :: 90 | Target final length :: 90  
**[298][L1][0125]** vs. [298][L1][0000] | Target Initial Length :: 89 | Template Length :: 90 | Target final length :: 90  
**[298][L1][0250]** vs. [298][L1][0000] | Target Initial Length :: 87 | Template Length :: 90 | Target final length :: 90  
**[298][L1][0500]** vs. [298][L1][0000] | Target Initial Length :: 86 | Template Length :: 90 | Target final length :: 90  
**[298][L1][1000]** vs. [298][L1][0000] | Target Initial Length :: 84 | Template Length :: 90 | Target final length :: 90  
**[298][L1][2000]** vs. [298][L1][0000] | Target Initial Length :: 83 | Template Length :: 90 | Target final length :: 90  
**[298][L1][4000]** vs. [298][L1][0000] | Target Initial Length :: 82 | Template Length :: 90 | Target final length :: 90  

*******************************************************************************  
### ADDS LOST RESIDUES BASED ON THE FASTA  
*******************************************************************************  
  
**[298][L1][0000]** vs. [298][L1][pseq] | Target Initial Length :: 90 | Template Length :: 100 | Target final length :: 100  
**[298][L1][0125]** vs. [298][L1][pseq] | Target Initial Length :: 90 | Template Length :: 100 | Target final length :: 100  
**[298][L1][0250]** vs. [298][L1][pseq] | Target Initial Length :: 90 | Template Length :: 100 | Target final length :: 100  
**[298][L1][0500]** vs. [298][L1][pseq] | Target Initial Length :: 90 | Template Length :: 100 | Target final length :: 100  
**[298][L1][1000]** vs. [298][L1][pseq] | Target Initial Length :: 90 | Template Length :: 100 | Target final length :: 100  
**[298][L1][2000]** vs. [298][L1][pseq] | Target Initial Length :: 90 | Template Length :: 100 | Target final length :: 100  
**[298][L1][4000]** vs. [298][L1][pseq] | Target Initial Length :: 90 | Template Length :: 100 | Target final length :: 100  

*******************************************************************************  
### ORGANIZING PEAKLIST COLUMNS' ORDER  
*******************************************************************************  
  
**[298][L1][0000]** Columns organized :: OK  
**[298][L1][0125]** Columns organized :: OK  
**[298][L1][0250]** Columns organized :: OK  
**[298][L1][0500]** Columns organized :: OK  
**[298][L1][1000]** Columns organized :: OK  
**[298][L1][2000]** Columns organized :: OK  
**[298][L1][4000]** Columns organized :: OK  

*******************************************************************************  
### INITIATING FARSEER CUBE  
*******************************************************************************  
  
> Created cube for all the backbone peaklists - OK!  

*******************************************************************************  
### GENERATING DICTIONARY OF TITRATIONS FOR COND1  
*******************************************************************************  
  
**Titration [298][L1]** with data points ['0000', '0125', '0250', '0500', '1000', '2000', '4000']  

*******************************************************************************  
### ANALYZING...   Backbone/Calculations/cond1/298/L1  
*******************************************************************************  
**Calculated** H1_delta  
**Calculated** N15_delta  
**Calculated** CSP  
**Calculated** Height_ratio  
**Calculated** Vol_ratio  
**Exported peaklist** Backbone/Calculations/cond1/298/L1/FullPeaklists/0000.tsv  
**Exported peaklist** Backbone/Calculations/cond1/298/L1/FullPeaklists/0125.tsv  
**Exported peaklist** Backbone/Calculations/cond1/298/L1/FullPeaklists/0250.tsv  
**Exported peaklist** Backbone/Calculations/cond1/298/L1/FullPeaklists/0500.tsv  
**Exported peaklist** Backbone/Calculations/cond1/298/L1/FullPeaklists/1000.tsv  
**Exported peaklist** Backbone/Calculations/cond1/298/L1/FullPeaklists/2000.tsv  
**Exported peaklist** Backbone/Calculations/cond1/298/L1/FullPeaklists/4000.tsv  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/H1_delta/0000_H1_delta.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/H1_delta/0125_H1_delta.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/H1_delta/0250_H1_delta.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/H1_delta/0500_H1_delta.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/H1_delta/1000_H1_delta.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/H1_delta/2000_H1_delta.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/H1_delta/4000_H1_delta.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/N15_delta/0000_N15_delta.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/N15_delta/0125_N15_delta.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/N15_delta/0250_N15_delta.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/N15_delta/0500_N15_delta.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/N15_delta/1000_N15_delta.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/N15_delta/2000_N15_delta.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/N15_delta/4000_N15_delta.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/CSP/0000_CSP.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/CSP/0125_CSP.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/CSP/0250_CSP.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/CSP/0500_CSP.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/CSP/1000_CSP.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/CSP/2000_CSP.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/CSP/4000_CSP.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/Height_ratio/0000_Height_ratio.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/Height_ratio/0125_Height_ratio.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/Height_ratio/0250_Height_ratio.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/Height_ratio/0500_Height_ratio.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/Height_ratio/1000_Height_ratio.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/Height_ratio/2000_Height_ratio.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/Height_ratio/4000_Height_ratio.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/Vol_ratio/0000_Vol_ratio.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/Vol_ratio/0125_Vol_ratio.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/Vol_ratio/0250_Vol_ratio.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/Vol_ratio/0500_Vol_ratio.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/Vol_ratio/1000_Vol_ratio.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/Vol_ratio/2000_Vol_ratio.att  
**Exported Chimera Att** Backbone/Calculations/cond1/298/L1/ChimeraAttributeFiles/Vol_ratio/4000_Vol_ratio.att  
**Plotting** bar_compacted for H1_delta...  
**Plot Saved** Backbone/Calculations/cond1/298/L1/TablesAndPlots/H1_delta/H1_delta_bar_compacted.png  
**Exported data table:** Backbone/Calculations/cond1/298/L1/TablesAndPlots/H1_delta/H1_delta.tsv  
**Plotting** bar_compacted for N15_delta...  
**Plot Saved** Backbone/Calculations/cond1/298/L1/TablesAndPlots/N15_delta/N15_delta_bar_compacted.png  
**Exported data table:** Backbone/Calculations/cond1/298/L1/TablesAndPlots/N15_delta/N15_delta.tsv  
**Plotting** bar_compacted for CSP...  
**Plot Saved** Backbone/Calculations/cond1/298/L1/TablesAndPlots/CSP/CSP_bar_compacted.png  
**Exported data table:** Backbone/Calculations/cond1/298/L1/TablesAndPlots/CSP/CSP.tsv  
**Plotting** bar_compacted for Height_ratio...  
**Plot Saved** Backbone/Calculations/cond1/298/L1/TablesAndPlots/Height_ratio/Height_ratio_bar_compacted.png  
**Exported data table:** Backbone/Calculations/cond1/298/L1/TablesAndPlots/Height_ratio/Height_ratio.tsv  
**Plotting** bar_compacted for Vol_ratio...  
**Plot Saved** Backbone/Calculations/cond1/298/L1/TablesAndPlots/Vol_ratio/Vol_ratio_bar_compacted.png  
**Exported data table:** Backbone/Calculations/cond1/298/L1/TablesAndPlots/Vol_ratio/Vol_ratio.tsv  
*******************************************************************************  
**LOG ENDED:** 2017/07/12 - 16:58:23 
*******************************************************************************  
