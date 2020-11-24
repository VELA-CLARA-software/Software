import numpy as np, sys, os
import matplotlib.pyplot as plt
from config import config
from src.data.rf_conditioning_logger import rf_conditioning_logger as logger
#from src.data import config
from src.data.rf_conditioning_data import rf_conditioning_data



class binning(object):
    '''
    This class handles all binning functions
    '''



    def initial_bin(self):


        '''This reads in the data from the amp_power log and bins all available data.
        The power values are already mean so need multiplying by the # of pulses, summing then dividing by the total number of pulses
        to get the genuine mean.
        We also update the binned_amp_vs_kfpow dictionary directly here rather than returning values.
        '''

        rcd = rf_conditioning_data


        # TODO AJG: Remove x, y, bin width etc from initial_bin() as it happens first in the reduce_amp_power_log_data() function.

        # cycle through amp_vs_kfpow_running_stat to populate amp_sp, kfpwr and number-of-pulses lists
        amp_sp_raw = []
        num_pulses_prebin = []
        mean_kfpwr_raw = []

        for key in rcd.amp_vs_kfpow_running_stat.keys():
            amp_sp_raw.append(key)
            num_pulses_prebin.append(rcd.amp_vs_kfpow_running_stat[key][0])
            mean_kfpwr_raw.append(rcd.amp_vs_kfpow_running_stat[key][1])
            print("init_bin set_up data = ", amp_sp_raw[-1], num_pulses_prebin[-1], mean_kfpwr_raw[-1])

        #print('mean_kfpwr_raw = {}'.format(mean_kfpwr_raw))

        # Call in config parameters
        bin_width = config.raw_config_data['BIN_WIDTH']
        max_pow = config.raw_config_data['MAX_POW']
        min_amp = config.raw_config_data['MIN_AMP']
        max_amp = config.raw_config_data['MAX_AMP']

        print('bin_width = {}\nmax_pow = {}\nmin_amp = {}\nmax_amp = {}'.format(bin_width, max_pow, min_amp, max_amp))

        # add the max values of amp sp and KFPower from config, this ensures bins are created ahead of the data
        amp_sp_raw.append(max_amp)
        mean_kfpwr_raw.append(max_pow)


        # Create list of bin edges starting at min_amp and ending at max_amp (max_amp now last element of x list)
        bedges = list(np.arange(int(min_amp), int(max_amp), bin_width))  # Not happy with np.arange.tolist() but it works!?!


        # create arrays of zeros of length len(bedges)-1 ready to be populated by the main calculator
        bin_mean =  np.zeros(len(bedges) - 1)
        bin_pop = np.zeros(len(bedges) - 1)
        bin_std = np.zeros(len(bedges) - 1)
        bin_pulses = np.zeros(len(bedges) - 1)

        # Create list of empty lists ready to be populated by all the raw kfpwr data sorted by bins
        bin_all_data = [ [] for _ in range(len(bedges) - 1) ]

        # MAIN CALCULATOR: cycle over data and assign it to bins
        for i in range(0, len(amp_sp_raw)):
            for j in range(0, len(bin_mean)):
                if amp_sp_raw[i] >= bedges[j] and amp_sp_raw[i] < bedges[j + 1]:
                    # multiply the number of pulses by the mean kfpowr to get the product (used in MEAN_EQN)
                    bin_pulse_x_mean =  num_pulses_prebin[i] * mean_kfpwr_raw[i]
                    # Define the new total number of pulses in the bin (used in MEAN_EQN)
                    bin_pulses_new = (bin_pulses[j] +  num_pulses_prebin[i])
                    # MEAN_EQN:
                    bin_mean[j] = ((bin_mean[j] * bin_pulses[j]) + (bin_pulse_x_mean)) / bin_pulses_new
                    # Update the total number of pulses in the bin with new value
                    bin_pulses[j] = bin_pulses_new
                    # Add one to bin population
                    bin_pop[j] += 1.0
                    # Add datapoint to data_binned dictionary
                    bin_all_data[j].append(mean_kfpwr_raw[i])
                    # Calculate the standard deviation of the data in each bin (needs to be weighted properly)
                    bin_std[j] = np.std(bin_all_data[j])



        #print('X = {}\nbin_mean = {}\nbin_pulses = {}\nbin_pop = {}\ndata_binned = {}\nbin_error = {}'.format(X[0:10], bin_mean[0:10],
        # bin_pulses[0:10], bin_pop[0:10],data_binned, bin_std[0:10]))

        # The amp sp value in the middle of each bin
        BIN_X = [k + bin_width / 2.0 for k in bedges[:-1]]

        # a list of all possible am sp values between zero and the maximum data point + 1 bin width
        All_amp_sp = range(int(amp_sp_raw[-1] + bin_width ))



        # Update binned_amp_vs_kfpow dictionary
        rcd.binned_amp_vs_kfpow[rcd.BIN_edges] = bedges
        rcd.binned_amp_vs_kfpow[rcd.BIN_X] = BIN_X
        rcd.binned_amp_vs_kfpow[rcd.BIN_mean] = bin_mean
        rcd.binned_amp_vs_kfpow[rcd.BIN_pop] = bin_pop
        rcd.binned_amp_vs_kfpow[rcd.BIN_std] = bin_std
        rcd.binned_amp_vs_kfpow[rcd.BIN_pulses] = bin_pulses
        rcd.binned_amp_vs_kfpow[rcd.BIN_all_data] = bin_all_data






    def update_binned_data(self):
        '''
        This function reads in the latest amp_sp - kfpow values as well as the output from
        initial_bin() or the previous dynamic_bin().

        Finds the relevant bin for the new amp_sp value and updates BIN_pop & BIN_mean in that bin.
        updates the binning dictionary with new values.
        '''


        rcd = rf_conditioning_data

        # Number of standard deviations used to define upper and lower limits of acceptance power range
        N_std = 3.0

        # Acquire latest amp_sp, mean_kfpwr & number of pulses at amp_sp:
        new_kfp_pulses_list = rcd.amp_vs_kfpow_running_stat[rcd.values[rcd.amp_sp]]
        new_amp = rcd.values[rcd.amp_sp]
        new_kfp = new_kfp_pulses_list[1]
        new_pulses = new_kfp_pulses_list[0]

        # Collate new data into newdata list
        newdata = [new_amp, new_kfp, new_pulses]

        # Call in data from binned_amp_vs_kfpow distionary already populated by initial_bin() ind subsequently here.
        bin_mean = rcd.binned_amp_vs_kfpow[rcd.BIN_mean]
        bedges = rcd.binned_amp_vs_kfpow[rcd.BIN_edges]
        bin_pop = rcd.binned_amp_vs_kfpow[rcd.BIN_pop]
        bin_pulses = rcd.binned_amp_vs_kfpow[rcd.BIN_pulses]
        BIN_X = rcd.binned_amp_vs_kfpow[rcd.BIN_X]
        bin_std = rcd.binned_amp_vs_kfpow[rcd.BIN_std]
        bin_all_data = rcd.binned_amp_vs_kfpow[rcd.BIN_all_data]

        # Cycle through bin edges until the x-axis (amp_sp) data sits between current and next bin edge.
        for i in range(int(len(bin_mean))):
            if newdata[0] >= bedges[i] and newdata[0] < bedges[i + 1]:
                # Check if new power is within x standard deviations of bin mean
                upper_limit = bin_mean[i] + (N_std * bin_std[i])
                lower_limit = bin_mean[i] - (N_std * bin_std[i])
                if newdata[1] > lower_limit and newdata[1] < upper_limit:
                    # multiply the number of pulses by the mean kfpowr to get the product (used in MEAN_EQN)
                    bin_pulse_x_mean = newdata[1] * newdata[2]
                    # Define the new total number of pulses in the bin (used in MEAN_EQN)
                    bin_pulses_new = (bin_pulses[i] + newdata[2])
                    # MEAN_EQN:
                    bin_mean[i] = ((bin_mean[i] * bin_pulses[i]) + (bin_pulse_x_mean)) / bin_pulses_new
                    # Update the total number of pulses in the bin with new value
                    bin_pulses[i] = bin_pulses_new
                    # Add one to bin population
                    bin_pop[i] += 1.0
                    # append the power to the correct ith bin list
                    bin_all_data[i].append(newdata[1])
                    # recalculate standard deviation in ith bin
                    bin_std[i] = np.std(bin_all_data[i])
                    # Once found no need to continue, so break.

                    break
                else:
                    pass
            else:
                pass

            # Update dictionary with new values
            rf_conditioning_data.binned_amp_vs_kfpow[rcd.BIN_mean] = bin_mean
            rf_conditioning_data.binned_amp_vs_kfpow[rcd.BIN_pop] = bin_pop
            rf_conditioning_data.binned_amp_vs_kfpow[rcd.BIN_pulses] = bin_pulses
            rcd.binned_amp_vs_kfpow[rcd.BIN_std] = bin_std
            rcd.binned_amp_vs_kfpow[rcd.BIN_all_data] = bin_all_data




            '''
            bin_plots_path = r'C:\Users\dlerlp\Documents\RF_Conditioning_20200720'
            plt.scatter(newdata[0], newdata[0], c='g', s=35, marker='x', label='Data', zorder=1)
            plt.scatter(BIN_X_dyn, BIN_mean, c='r', s=25, marker='x', label='Binned Mean', zorder=0)
            plt.xlabel('Set Point')
            plt.ylabel('Power (MW)')
            plt.legend()
            plt.grid(True)
            plt.savefig(bin_plots_path + r'\Dynamic_Binning_Plot.png')
            plt.close('all')
            '''
