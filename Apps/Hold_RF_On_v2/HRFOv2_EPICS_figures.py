import numpy as np, time, sys
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import HRFOv2_EPICS_data
from decimal import *
import scipy
from scipy import stats

#from CASCADE_2_data import data_functions

class figures():
    #C2_data = CASCADE_2_data()

    def __init__(self):
        print('Initaited figures()')


    def individual_PV_plot(self, time, yaxis, ylabel, savename, PV_idx):
        '''
        Simple x-y plotter used to plot each individual PV values as a function of time.
        :param time: list
        :param yaxis: list
        :param ylabel: str
        :return:
        '''
        self.time = time
        self.yaxis = yaxis
        self.ylabel = ylabel
        self.savename = savename
        self.PV_idx = PV_idx
        self.savepath = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]
        self.savename = savename
        self.PV_idx = PV_idx

        plt.plot(time, yaxis, ls='-', lw=1.0, color='b')
        plt.scatter(time, yaxis, marker='o', s=3.0, c='r')
        # plt.ylabel(data[0]["meta"]["EGU"])
        plt.title(self.ylabel)
        plt.ylabel(self.ylabel)
        plt.xlabel("Time Since Epics Epoch")
        plt.savefig(self.savepath + "\\" + self.savename + f"_pv_{self.PV_idx}.png")
        plt.close('all')


    def subplots_x(self, pv_idx_list):
        '''
        Creates a figure of two vertically stacked subplots.
        Used for comparing two PV values
        :param pv_idx_0:
        :param pv_idx_1:
        :return:
        '''


        self.pv_idx_list = pv_idx_list
        self.N_PVs = len(self.pv_idx_list)

        if self.N_PVs > 6:
            print(f'More than 6 sublots selected in subplots_x().\nReduce number or amend function.')
            sys.exit()
        else:
            pass

        self.savepath = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]
        self.all_mod_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.all_mod_PVs]
        self.PV_TIME_DATA = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PV_TIME_DATA]
        self.PV_YAXIS_DATA = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PV_YAXIS_DATA]
        self.colours = ['r', 'g', 'b', 'c', 'darkorange', 'm']

        self.savename_idx_string = ''
        self.suptitle_string = ''
        fig, axs = plt.subplots(self.N_PVs)

        for idx, pv_idx in enumerate(self.pv_idx_list):
            self.savename_idx_string + '_' + str(pv_idx)
            self.suptitle_string + self.all_mod_PVs[pv_idx] + '\n'

            axs[idx].plot(self.PV_TIME_DATA[pv_idx], self.PV_YAXIS_DATA[pv_idx], ls='-', lw=1.0, color='b')
            axs[idx].scatter(self.PV_TIME_DATA[pv_idx], self.PV_YAXIS_DATA[pv_idx], marker='o', s=3.0, c='r')
            if idx < self.N_PVs-1:
                # make these tick labels invisible
                plt.setp(axs[idx].get_xticklabels(), visible=False)

        fig.suptitle(self.suptitle_string, fontsize=7)
        plt.savefig(self.savepath + f"\\_subplots_{self.savename_idx_string}.png")
        plt.close('all')

    def subplots_2(self, pv_idx_0, pv_idx_1):
        '''
        Creates a figure of two vertically stacked subplots.
        Used for comparing two PV values
        :param pv_idx_0:
        :param pv_idx_1:
        :return:
        '''


        self.pv_idx_0 = pv_idx_0
        self.pv_idx_1 = pv_idx_1
        self.savepath = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]
        self.all_mod_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.all_mod_PVs]
        self.PV_TIME_DATA = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PV_TIME_DATA]
        self.PV_YAXIS_DATA = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PV_YAXIS_DATA]

        fig, axs = plt.subplots(2)
        fig.suptitle(f'{self.all_mod_PVs[self.pv_idx_0]}\n{self.all_mod_PVs[self.pv_idx_1]}')
        axs[0].plot(self.PV_TIME_DATA[self.pv_idx_0], self.PV_YAXIS_DATA[self.pv_idx_0], ls='-', lw=1.0, color='b')
        axs[0].scatter(self.PV_TIME_DATA[self.pv_idx_0], self.PV_YAXIS_DATA[self.pv_idx_0], marker='o', s=3.0, c='r')
        # make these tick labels invisible
        plt.setp(axs[0].get_xticklabels(), visible=False)
        axs[1].plot(self.PV_TIME_DATA[self.pv_idx_1], self.PV_YAXIS_DATA[self.pv_idx_1], ls='-', lw=1.0, color='b')
        axs[1].scatter(self.PV_TIME_DATA[self.pv_idx_1], self.PV_YAXIS_DATA[self.pv_idx_1], marker='o', s=3.0, c='r')
        plt.savefig(self.savepath + f"\\_subplots_{self.pv_idx_0}_{self.pv_idx_1}.png")
        plt.close('all')

    def subplots_3(self, pv_idx_0, pv_idx_1, pv_idx_2):
        '''
        Creates a figure of three vertically stacked subplots.
        Used for comparing two PV values.
        :param pv_idx_0:
        :param pv_idx_1:
        :param pv_idx_2:
        :return:
        '''


        self.pv_idx_0 = pv_idx_0
        self.pv_idx_1 = pv_idx_1
        self.pv_idx_2 = pv_idx_2
        self.savepath = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]
        self.all_mod_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.all_mod_PVs]
        self.PV_TIME_DATA = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PV_TIME_DATA]
        self.PV_YAXIS_DATA = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PV_YAXIS_DATA]

        fig, axs = plt.subplots(3)
        fig.suptitle(f'{self.all_mod_PVs[self.pv_idx_0]}\n{self.all_mod_PVs[self.pv_idx_1]}')
        axs[0].plot(self.PV_TIME_DATA[self.pv_idx_0], self.PV_YAXIS_DATA[self.pv_idx_0], ls='-', lw=1.0, color='b')
        axs[0].scatter(self.PV_TIME_DATA[self.pv_idx_0], self.PV_YAXIS_DATA[self.pv_idx_0], marker='o', s=3.0, c='r')
        # make these tick labels invisible
        plt.setp(axs[0].get_xticklabels(), visible=False)
        axs[1].plot(self.PV_TIME_DATA[self.pv_idx_1], self.PV_YAXIS_DATA[self.pv_idx_1], ls='-', lw=1.0, color='b')
        axs[1].scatter(self.PV_TIME_DATA[self.pv_idx_1], self.PV_YAXIS_DATA[self.pv_idx_1], marker='o', s=3.0, c='r')
        # make these tick labels invisible
        plt.setp(axs[1].get_xticklabels(), visible=False)
        axs[2].plot(self.PV_TIME_DATA[self.pv_idx_2], self.PV_YAXIS_DATA[self.pv_idx_2], ls='-', lw=1.0, color='b')
        axs[2].scatter(self.PV_TIME_DATA[self.pv_idx_2], self.PV_YAXIS_DATA[self.pv_idx_2], marker='o', s=3.0, c='r')
        plt.savefig(self.savepath + f"\\_subplots_{self.pv_idx_0}_{self.pv_idx_1}_{self.pv_idx_2}.png")
        plt.close('all')


    def make_patch_spines_invisible(self, ax):
        '''
        Makes the patch and spines invisible for a multi y-axes plot.
        :param ax: the axis reqired.
        :return:
        '''

        ax.set_frame_on(True)
        ax.patch.set_visible(False)
        for sp in ax.spines.values():
            sp.set_visible(False)


    def triple_yaxis_plot(self, pv_idx_0, pv_idx_1, pv_idx_2):
        '''
        Creates a figure of three PV values on the same plot with 3 y-axes.
        Used for comparing two PV values.
        :param pv_idx_0:
        :param pv_idx_1:
        :param pv_idx_2:
        :return:
        '''
        self.pv_idx_0 = pv_idx_0
        self.pv_idx_1 = pv_idx_1
        self.pv_idx_2 = pv_idx_2

        fig, host = plt.subplots()
        fig.subplots_adjust(right=0.75)

        par1 = host.twinx()
        par2 = host.twinx()

        # Offset the right spine of par2.  The ticks and label have already been
        # placed on the right by twinx above.
        par2.spines["right"].set_position(("axes", 1.2))
        # Having been created by twinx, par2 has its frame off, so the line of its
        # detached spine is invisible.  First, activate the frame but make the patch
        # and spines invisible.
        self.make_patch_spines_invisible(par2)
        # Second, show the right spine.
        par2.spines["right"].set_visible(True)

        p1, = host.plot(self.PV_TIME_DATA[self.pv_idx_0], self.PV_YAXIS_DATA[self.pv_idx_0], ls='-', lw=1.0, color='r')
        # p1, = host.scatter(X_DATA[PV_idx_1], Y_DATA[PV_idx_1], marker='o', s=3.0, c='r')
        p2, = par1.plot(self.PV_TIME_DATA[self.pv_idx_1], self.PV_YAXIS_DATA[self.pv_idx_1], ls='-', lw=1.0, color='g')
        # p2, = par1.scatter(X_DATA[PV_idx_2], Y_DATA[PV_idx_2], marker='o', s=3.0, c='r')
        p3, = par2.plot(self.PV_TIME_DATA[self.pv_idx_2], self.PV_YAXIS_DATA[self.pv_idx_2], ls='-', lw=1.0, color='b')
        # p3, = par2.scatter(X_DATA[PV_idx_3], Y_DATA[PV_idx_3], marker='o', s=3.0, c='r')

        # host.set_xlim(0, 2)
        # host.set_ylim(0, 2)
        # par1.set_ylim(0, 4)
        # par2.set_ylim(1, 65)

        # host.set_xlabel("Distance")
        # host.set_ylabel("Density")
        # par1.set_ylabel("Temperature")
        # par2.set_ylabel("Velocity")

        host.yaxis.label.set_color(p1.get_color())
        par1.yaxis.label.set_color(p2.get_color())
        par2.yaxis.label.set_color(p3.get_color())

        tkw = dict(size=4, width=1.5)
        host.tick_params(axis='y', colors=p1.get_color(), **tkw)
        par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
        par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
        host.tick_params(axis='x', **tkw)

        lines = [p1, p2, p3]

        # host.legend(lines, [l.get_label() for l in lines])

        plt.savefig(self.savepath + f"\\_Multi_y_{self.pv_idx_0}_{self.pv_idx_1}_{self.pv_idx_2}.png")
        plt.close('all')


    def histogram(self, data, xaxis_name, xmax):
        '''
        Generic histogram plotter including mean & st. dev. calcs.
        :param data:
        :param xaxis_name:
        :param xmax:
        :return:
        '''
        # try:
        self.data = data
        self.xaxis_name = xaxis_name
        self.xmax = xmax
        self.savepath = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]

        self.data_reduced = [i for i in self.data if i <= self.xmax]
        self.savename = f'\\{xaxis_name}.png'
        min_data = min(self.data_reduced)
        max_data = max(self.data_reduced)

        mean_dev_L = np.mean(self.data_reduced)
        std_dev_L = np.std(self.data_reduced)
        nbin = int(np.sqrt(len(self.data_reduced)) * 5.0)
        #print('len(data) = {}\nnbin = {}\ndata = {}\nnumber of NaNs in data = {}\nmin_data = {}\nmax_data = {}\nmean_dev_L = {}\nstd_dev_L = {}'
        #      .format(len(data), nbin, data, len(nans_in_data), min(data), max(data), mean_dev_L, std_dev_L))

        #print(f'xmax = {self.xmax}')
        self.n, self.bedges, self.patches = plt.hist(self.data_reduced, bins=nbin, range=(min_data, max_data), histtype='step', color='k')

        self.midbin_vals = self.define_midbins_from_bedegs(self.bedges)
        self.peak_x_val, self.peak_y_val = self.find_top_x_peaks_histogram(self.n, self.bedges)

        plt.scatter(self.peak_x_val, self.peak_y_val, marker='x', s=50, c='r')

        plt.plot([mean_dev_L, mean_dev_L], [0.0, max(self.n)], lw=0.5, ls='--', color='r')
        plt.plot([mean_dev_L + std_dev_L, mean_dev_L + std_dev_L], [0.0, max(self.n)], lw=0.5, ls='--', color='g')
        plt.plot([mean_dev_L - std_dev_L, mean_dev_L - std_dev_L], [0.0, max(self.n)], lw=0.5, ls='--', color='g')
        plt.text(int(self.xmax*0.6), max(self.n) * 0.75, r'$\mu$'' = {}\n'r'$\sigma$'' = {}\nN = {}\n'
                 .format(mean_dev_L, std_dev_L, len(self.data_reduced)))
        #plt.xlim(0.0, self.xmax)
        #plt.ylim(0.0, 200.0)
        plt.xlabel(self.xaxis_name)
        plt.ylabel('N')
        plt.savefig(self.savepath + self.savename)
        plt.close('all')


        #self.midbin_vals = self.define_midbins_from_bedegs(self.bedges)

        # except:
        #     print(f'Unable to produce histogram of {self.xaxis_name}')
        #     pass

    def define_midbins_from_bedegs(self, bedges):
        '''
        From a list/array of histogram bin edges it s sometimes useful to know the mid-bin values
        :param bedges: a list/array of histogram bin-edge x-axis values
        :return: a list of histogram x-axis mid-bin values
        '''

        # print(f'type(self.bedges) = {type(self.bedges)}')

        # convert to list for ease of use
        if str(type(self.bedges)) == "<class 'numpy.ndarray'>":
            self.bedges = bedges.tolist()
        else:
            pass

        # print(f'type(self.bedges) = {type(self.bedges)}')

        self.midbin_vals = [((self.bedges[i+1] -self.bedges[i]) / 2.0) + self.bedges[i] for i in range(len(self.bedges)-1)]

        #print(f'\nIdiot Check:\n{self.bedges[0]}  {self.midbin_vals[0]}  {self.bedges[1]}\n')

        return self.midbin_vals


    def find_top_x_peaks_histogram(self,  bin_population, midbin_vals):
        '''
        The returns from pyplot.his() are used in this function to give the x-axis value of the the top X number of peaks,
        along with the number of members of that bin.
        eg. self.n, self.bedges, self.patches = plt.hist(self.data_reduced, bins=nbin, range=(min_data, max_data), histtype='step', color='k')
        :param n: Number of members of each bin.
        :param midbin_vals: a list of histogram x-axis mid-bin values.

        :return:
        '''


        #self.top_x = int(HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.X_HIGHEST_PEAKS_HIST])
        self.top_x = int(25)
        self.bin_population = bin_population
        self.midbin_vals = midbin_vals


        self.temp_bin_population = list(np.copy(bin_population))

        self.peak_x_val = []
        self.peak_y_val = []

        count = 0
        while self.top_x > count:

            # Define (new) max value in temp_bin_population list
            # and it's index in the original bin_population list
            # 2 lists are used because otherwise the indexing becomes irrelevant.
            max_val = max(self.temp_bin_population)
            max_idx = int(np.argwhere(self.bin_population == max_val)[-1])
            temp_max_idx = int(np.argwhere(self.temp_bin_population == max_val)[-1])

            # Append values to lists to be returned by the function
            self.peak_x_val.append(self.midbin_vals[max_idx])
            self.peak_y_val.append(self.bin_population[max_idx])

            # Remove the maximum value from the temp_bin_population list
            # so that the next highest value can be found by the max() function
            self.temp_bin_population.remove(self.temp_bin_population[temp_max_idx])

            print(count, f'\nmax_val = {max_val}\nmax_idx = {max_idx}\nlen(temp_bin_population) = {len(self.temp_bin_population)}')

            # Increase the count by 1 for the while loop to function
            count += 1

        print(f'\nself.peak_x_val = {self.peak_x_val}\nself.peak_y_val = {self.peak_y_val}\n')

        return self.peak_x_val, self.peak_y_val

    def Nmaxelements(self, list1, N):
        '''
        taken from the website "geeksforgeeks.org" available at:
        https://www.geeksforgeeks.org/python-program-to-find-n-largest-elements-from-a-list/
        Never used in this script but useful for future reference.
        ""
        :param list1:
        :param N:
        :return:
        '''
        final_list = []

        for i in range(0, N):
            max1 = 0

            for j in range(len(list1)):
                if list1[j] > max1:
                    max1 = list1[j]

            list1.remove(max1)
            final_list.append(max1)

        print(final_list)

        return final_list