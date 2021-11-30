import numpy as np, time, sys, os
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d.axes3d import Axes3D
import HRFOv2_EPICS_data
from decimal import *
import scipy
from scipy import stats

#from HRFOv2_EPICS_reader import reader

class figures():




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
        self.time = np.array(time)
        self.yaxis = np.array(yaxis)
        self.ylabel = ylabel
        self.savename = savename
        self.PV_idx = PV_idx
        self.savepath = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]
        self.savename = savename
        self.PV_idx = PV_idx


        #print(f'\n\n{self.savepath}\\{self.savename}_pv_{self.PV_idx}.png')

        plt.step(self.time, self.yaxis, color='b', where='post')
        plt.scatter(self.time, self.yaxis, marker='o', s=3.0, c='r')
        #plt.plot(self.time, self.yaxis, ls='-', lw=1.0, color='b')

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

        print(f'len(self.PV_TIME_DATA[self.pv_idx_0]) = {len(self.PV_TIME_DATA[self.pv_idx_0])}\n'
              f'len(self.PV_YAXIS_DATA[self.pv_idx_0]) = {len(self.PV_YAXIS_DATA[self.pv_idx_0])}')

        print(f'len(self.PV_TIME_DATA[self.pv_idx_1]) = {len(self.PV_TIME_DATA[self.pv_idx_1])}\n'
              f'len(self.PV_YAXIS_DATA[self.pv_idx_1]) = {len(self.PV_YAXIS_DATA[self.pv_idx_1])}\n\n')


        # for index in range(len(self.PV_TIME_DATA)):
        #     print(f'len(self.PV_TIME_DATA[self.pv_idx_{index}]) = {len(self.PV_TIME_DATA[index])}\n'
        #           f'len(self.PV_YAXIS_DATA[self.pv_idx_{index}]) = {len(self.PV_YAXIS_DATA[index])}\n')
        #
        # input()

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

    def histogram_nbin(self, data, xaxis_name, xmax, nbin):
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
        self.nbin = int(nbin)
        self.savepath = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]

        self.data_reduced = [i for i in self.data if i <= self.xmax]
        self.savename = f'\\{xaxis_name}.png'
        min_data = min(self.data_reduced)
        max_data = max(self.data_reduced)

        mean_dev_L = np.mean(self.data_reduced)
        std_dev_L = np.std(self.data_reduced)
        #nbin = int(np.sqrt(len(self.data_reduced)) * 5.0)
        #print('len(data) = {}\nnbin = {}\ndata = {}\nnumber of NaNs in data = {}\nmin_data = {}\nmax_data = {}\nmean_dev_L = {}\nstd_dev_L = {}'
        #      .format(len(data), nbin, data, len(nans_in_data), min(data), max(data), mean_dev_L, std_dev_L))

        #print(f'xmax = {self.xmax}')
        self.n, self.bedges, self.patches = plt.hist(self.data_reduced, bins=self.nbin, range=(min_data, max_data), histtype='step', color='k')

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

    def barchart_FaultLog(self):
        '''
        Takes the fault log in one-hot coded version and creates a histogram of occurances
        :return:
        '''
        self.savepath =  HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]
        self.full_buffers = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.full_buffers]
        self.fault_log_to_index_dict = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.fault_log_to_index_dict]
        self.savename = f'\\histogram_FaultLog_occurances.png'
        self.full_buffers_one_hot = [self.fault_log_to_index_dict[j] for i in self.full_buffers for j in i]
        self.full_buffers_one_hot_classes = list(set(self.full_buffers_one_hot))
        print(self.full_buffers_one_hot_classes)
        self.fault_population = [0]*len(self.fault_log_to_index_dict)

        self.date_from = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.date_from]
        self.time_from = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.time_from]
        self.date_to = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.date_to]
        self.time_to = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.time_to]
        for i in self.full_buffers_one_hot:
            #print(i)
            self.fault_population[i] += 1

        print(f'self.fault_population = {self.fault_population}')

        plt.bar(range(len(self.fault_log_to_index_dict)), self.fault_population, 1., color='white', align='center', edgecolor='k')
        new_labels = range(len(self.fault_log_to_index_dict))
        plt.xticks(new_labels)

        legend_0 = mpatches.Patch(label=f'0: Cavity Interlock ({self.fault_population[0]})')
        legend_1 = mpatches.Patch(label=f'1: General Interlock ({self.fault_population[1]})')
        legend_2 = mpatches.Patch(label=f'2: Hold RF (Con) Engaged ({self.fault_population[2]})')
        legend_3 = mpatches.Patch(label=f'3: Hold RF Deactivated ({self.fault_population[3]})')
        legend_4 = mpatches.Patch(label=f'4: Hold RF Engaged ({self.fault_population[4]})')
        legend_5 = mpatches.Patch(label=f'5: Hold RF On had to STOP ({self.fault_population[5]})')
        legend_6 = mpatches.Patch(label=f'6: Libera: General Interlock ({self.fault_population[6]})')
        legend_7 = mpatches.Patch(label=f'7: LLRF:Channel 1 ({self.fault_population[7]})')
        legend_8 = mpatches.Patch(label=f'8: LLRF:Channel 2 ({self.fault_population[8]})')
        legend_9 = mpatches.Patch(label=f'9: LLRF:Channel 3 ({self.fault_population[9]})')
        legend_10 = mpatches.Patch(label=f'10: LLRF:Channel 4 ({self.fault_population[10]})')
        legend_11 = mpatches.Patch(label=f'11: LLRF:Channel 5 ({self.fault_population[11]})')
        legend_12 = mpatches.Patch(label=f'12: LLRF:Channel 6 ({self.fault_population[12]})')
        legend_13 = mpatches.Patch(label=f'13: Mod is OFF ({self.fault_population[13]})')
        legend_14 = mpatches.Patch(label=f'14: Mod:HV Not On ({self.fault_population[14]})')
        legend_15 = mpatches.Patch(label=f'15: Mod:HvPs\Ps1\IGBT int. ({self.fault_population[15]})')
        legend_16 = mpatches.Patch(label=f'16: Mod:Pt\\Cool\\Klystron Body Flow int. ({self.fault_population[16]})')
        legend_17 = mpatches.Patch(label=f'17: Mod:Pt\\Cool\\Tank Flow int. ({self.fault_population[17]})')
        legend_18 = mpatches.Patch(label=f'18: Mod:Pt\\Diag\\CT read int. ({self.fault_population[18]})')
        legend_19 = mpatches.Patch(label=f'19: Mod:Pt\\FilPs\\Volt int. ({self.fault_population[19]})')
        legend_20 = mpatches.Patch(label=f'20: Mod:Pt\Diag\CT arc int. ({self.fault_population[20]})')
        legend_21 = mpatches.Patch(label=f'21: Mod:RF Not On ({self.fault_population[21]})')
        legend_22 = mpatches.Patch(label=f'22: Mod:Sys\\Cool\\Solenoid Flow int. ({self.fault_population[22]})')
        legend_23 = mpatches.Patch(label=f'23: Mod:Sys\ExtCom\Communication int. ({self.fault_population[23]})')
        legend_24 = mpatches.Patch(label=f'24: Mod:Sys\HwCtr\Hv interlock 1. ({self.fault_population[24]})')
        legend_25 = mpatches.Patch(label=f'25: Mod:Sys\HwCtr\Hv interlock 2. ({self.fault_population[25]})')
        legend_26 = mpatches.Patch(label=f'26: RF Enable Interlock ({self.fault_population[26]})')
        legend_27 = mpatches.Patch(label=f'27: Switched Modulator OFF. ({self.fault_population[27]})')

        _HANDLES = [legend_0,
                    legend_1,
                    legend_2,
                    legend_3,
                    legend_4,
                    legend_5,
                    legend_6,
                    legend_7,
                    legend_8,
                    legend_9,
                    legend_10,
                    legend_11,
                    legend_12,
                    legend_13,
                    legend_14,
                    legend_15,
                    legend_16,
                    legend_17,
                    legend_18,
                    legend_19,
                    legend_20,
                    legend_21,
                    legend_22,
                    legend_23,
                    legend_24,
                    legend_25,
                    legend_26,
                    legend_27]

        plt.legend(handles=_HANDLES, fontsize=6, loc=1)
        plt.title(f'From {self.date_from} {self.time_from} to {self.date_to} {self.time_to}')
        plt.xlabel('Hold RF On Fault Log')
        plt.ylabel('N')
        plt.savefig(self.savepath + self.savename)
        plt.close('all')

    def barchart_FaultLog_simplified(self):
        '''
        Takes the fault log in one-hot coded version and creates a histogram of occurances
        :return:
        '''
        self.savepath =  HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]
        #self.full_buffers = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.full_buffers]
        self.buffer_entries = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.buffer_entries]
        self.fault_log_to_index_dict = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.fault_log_to_index_dict]
        self.savename = f'\\histogram_FaultLog_occurances_simplified.png'
        self.full_buffers_one_hot = [self.fault_log_to_index_dict[i] for i in self.buffer_entries]
        self.full_buffers_one_hot_classes = list(set(self.full_buffers_one_hot))
        print(self.full_buffers_one_hot_classes)
        self.fault_population = [0]*len(self.fault_log_to_index_dict)

        self.date_from = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.date_from]
        self.time_from = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.time_from]
        self.date_to = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.date_to]
        self.time_to = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.time_to]

        for i in self.full_buffers_one_hot:
            #print(i)
            self.fault_population[i] += 1

        self.population_total = np.sum(self.fault_population)
        print(f'self.fault_population = {self.fault_population}\n'
              f'self.population_total = {self.population_total}')


        plt.bar(range(len(self.fault_log_to_index_dict)), self.fault_population, 1., color='white', align='center', edgecolor='k')
        new_labels = range(len(self.fault_log_to_index_dict))
        plt.xticks(new_labels)

        legend_0 = mpatches.Patch(label=f'0: Cavity Interlock ({self.fault_population[0]})')
        legend_1 = mpatches.Patch(label=f'1: General Interlock ({self.fault_population[1]})')
        legend_2 = mpatches.Patch(label=f'2: Hold RF (Con) Engaged ({self.fault_population[2]})')
        legend_3 = mpatches.Patch(label=f'3: Hold RF Deactivated ({self.fault_population[3]})')
        legend_4 = mpatches.Patch(label=f'4: Hold RF Engaged ({self.fault_population[4]})')
        legend_5 = mpatches.Patch(label=f'5: Hold RF On had to STOP ({self.fault_population[5]})')
        legend_6 = mpatches.Patch(label=f'6: Libera: General Interlock ({self.fault_population[6]})')
        legend_7 = mpatches.Patch(label=f'7: LLRF:Channel 1 ({self.fault_population[7]})')
        legend_8 = mpatches.Patch(label=f'8: LLRF:Channel 2 ({self.fault_population[8]})')
        legend_9 = mpatches.Patch(label=f'9: LLRF:Channel 3 ({self.fault_population[9]})')
        legend_10 = mpatches.Patch(label=f'10: LLRF:Channel 4 ({self.fault_population[10]})')
        legend_11 = mpatches.Patch(label=f'11: LLRF:Channel 5 ({self.fault_population[11]})')
        legend_12 = mpatches.Patch(label=f'12: LLRF:Channel 6 ({self.fault_population[12]})')
        legend_13 = mpatches.Patch(label=f'13: Mod is OFF ({self.fault_population[13]})')
        legend_14 = mpatches.Patch(label=f'14: Mod:HV Not On ({self.fault_population[14]})')
        legend_15 = mpatches.Patch(label=f'15: Mod:HvPs\Ps1\IGBT int. ({self.fault_population[15]})')
        legend_16 = mpatches.Patch(label=f'16: Mod:Pt\\Cool\\Klystron Body Flow int. ({self.fault_population[16]})')
        legend_17 = mpatches.Patch(label=f'17: Mod:Pt\\Cool\\Tank Flow int. ({self.fault_population[17]})')
        legend_18 = mpatches.Patch(label=f'18: Mod:Pt\\Diag\\CT read int. ({self.fault_population[18]})')
        legend_19 = mpatches.Patch(label=f'19: Mod:Pt\\FilPs\\Volt int. ({self.fault_population[19]})')
        legend_20 = mpatches.Patch(label=f'20: Mod:Pt\Diag\CT arc int. ({self.fault_population[20]})')
        legend_21 = mpatches.Patch(label=f'21: Mod:RF Not On ({self.fault_population[21]})')
        legend_22 = mpatches.Patch(label=f'22: Mod:Sys\\Cool\\Solenoid Flow int. ({self.fault_population[22]})')
        legend_23 = mpatches.Patch(label=f'23: Mod:Sys\ExtCom\Communication int. ({self.fault_population[23]})')
        legend_24 = mpatches.Patch(label=f'24: Mod:Sys\HwCtr\Hv interlock 1. ({self.fault_population[24]})')
        legend_25 = mpatches.Patch(label=f'25: Mod:Sys\HwCtr\Hv interlock 2. ({self.fault_population[25]})')
        legend_26 = mpatches.Patch(label=f'26: RF Enable Interlock ({self.fault_population[26]})')
        legend_27 = mpatches.Patch(label=f'27: Switched Modulator OFF. ({self.fault_population[27]})')

        _HANDLES = [legend_0,
                    legend_1,
                    legend_2,
                    legend_3,
                    legend_4,
                    legend_5,
                    legend_6,
                    legend_7,
                    legend_8,
                    legend_9,
                    legend_10,
                    legend_11,
                    legend_12,
                    legend_13,
                    legend_14,
                    legend_15,
                    legend_16,
                    legend_17,
                    legend_18,
                    legend_19,
                    legend_20,
                    legend_21,
                    legend_22,
                    legend_23,
                    legend_24,
                    legend_25,
                    legend_26,
                    legend_26]

        plt.legend(handles=_HANDLES, fontsize=6, loc=1)

        plt.title(f'From    {self.date_from} {self.time_from}\nto         {self.date_to} {self.time_to}')
        plt.xlabel('Hold RF On Fault Log')
        plt.ylabel('N')
        plt.savefig(self.savepath + self.savename)
        plt.close('all')

        # for l_idx, l in enumerate(HANDLES):
        #     print(f'{l_idx} {str(l)} {self.fault_population[l_idx]}')

    def barchart_FaultLog_quick_check(self, EPICS_datetime_from, EPICS_datetime_now):
        '''
        Takes the fault log in one-hot coded version and creates a histogram of occurances
        :return:
        '''
        self.EPICS_datetime_from = EPICS_datetime_from
        self.EPICS_datetime_now = EPICS_datetime_now
        self.savepath =  HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]
        #self.full_buffers = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.full_buffers]
        self.buffer_entries_quick_check = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.buffer_entries_quick_check]
        self.fault_log_to_index_dict = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.fault_log_to_index_dict]
        self.savename = f'\\histogram_FaultLog_occurances_quick_check.png'
        self.full_buffers_one_hot = [self.fault_log_to_index_dict[i] for i in self.buffer_entries_quick_check]
        self.full_buffers_one_hot_classes = list(set(self.full_buffers_one_hot))
        self.buffer_entries_quick_check_classes = list(set(self.buffer_entries_quick_check))
        print(self.full_buffers_one_hot_classes)
        print('\n\n')
        for idx, i in enumerate(self.buffer_entries_quick_check_classes):
            print(i)#, self.full_buffers_one_hot_classes[idx])

        #input()
        print('\n\n')

        self.fault_population = [0]*len(self.fault_log_to_index_dict)

        self.date_from = str(self.EPICS_datetime_from)[:10]
        self.time_from = str(self.EPICS_datetime_from)[11:]
        self.date_to = str(self.EPICS_datetime_now)[:10]
        self.time_to = str(self.EPICS_datetime_now)[11:]

        for i in self.full_buffers_one_hot:
            #print(i)
            self.fault_population[i] += 1

        self.population_total = np.sum(self.fault_population)
        print(f'self.fault_population = {self.fault_population}\n'
              f'self.population_total = {self.population_total}')


        plt.bar(range(len(self.fault_log_to_index_dict)), self.fault_population, 1., color='white', align='center', edgecolor='k')
        new_labels = range(len(self.fault_log_to_index_dict))
        plt.xticks(new_labels)

        legend_0 = mpatches.Patch(label=f'0: Cavity Interlock ({self.fault_population[0]})')
        legend_1 = mpatches.Patch(label=f'1: General Interlock ({self.fault_population[1]})')
        legend_2 = mpatches.Patch(label=f'2: Hold RF (Con) Engaged ({self.fault_population[2]})')
        legend_3 = mpatches.Patch(label=f'3: Hold RF Deactivated ({self.fault_population[3]})')
        legend_4 = mpatches.Patch(label=f'4: Hold RF Engaged ({self.fault_population[4]})')
        legend_5 = mpatches.Patch(label=f'5: Hold RF On had to STOP ({self.fault_population[5]})')
        legend_6 = mpatches.Patch(label=f'6: Libera: General Interlock ({self.fault_population[6]})')
        legend_7 = mpatches.Patch(label=f'7: LLRF:Channel 1 ({self.fault_population[7]})')
        legend_8 = mpatches.Patch(label=f'8: LLRF:Channel 2 ({self.fault_population[8]})')
        legend_9 = mpatches.Patch(label=f'9: LLRF:Channel 3 ({self.fault_population[9]})')
        legend_10 = mpatches.Patch(label=f'10: LLRF:Channel 4 ({self.fault_population[10]})')
        legend_11 = mpatches.Patch(label=f'11: LLRF:Channel 5 ({self.fault_population[11]})')
        legend_12 = mpatches.Patch(label=f'12: LLRF:Channel 6 ({self.fault_population[12]})')
        legend_13 = mpatches.Patch(label=f'13: Mod is OFF ({self.fault_population[13]})')
        legend_14 = mpatches.Patch(label=f'14: Mod:HV Not On ({self.fault_population[14]})')
        legend_15 = mpatches.Patch(label=f'15: Mod:HvPs\Ps1\IGBT int. ({self.fault_population[15]})')
        legend_16 = mpatches.Patch(label=f'16: Mod:Pt\\Cool\\Klystron Body Flow int. ({self.fault_population[16]})')
        legend_17 = mpatches.Patch(label=f'17: Mod:Pt\\Cool\\Tank Flow int. ({self.fault_population[17]})')
        legend_18 = mpatches.Patch(label=f'18: Mod:Pt\\Diag\\CT read int. ({self.fault_population[18]})')
        legend_19 = mpatches.Patch(label=f'19: Mod:Pt\\FilPs\\Volt int. ({self.fault_population[19]})')
        legend_20 = mpatches.Patch(label=f'20: Mod:Pt\Diag\CT arc int. ({self.fault_population[20]})')
        legend_21 = mpatches.Patch(label=f'21: Mod:RF Not On ({self.fault_population[21]})')
        legend_22 = mpatches.Patch(label=f'22: Mod:Sys\\Cool\\Solenoid Flow int. ({self.fault_population[22]})')
        legend_23 = mpatches.Patch(label=f'23: Mod:Sys\ExtCom\Communication int. ({self.fault_population[23]})')
        legend_24 = mpatches.Patch(label=f'24: Mod:Sys\HwCtr\Hv interlock 1. ({self.fault_population[24]})')
        legend_25 = mpatches.Patch(label=f'25: Mod:Sys\HwCtr\Hv interlock 2. ({self.fault_population[25]})')
        legend_26 = mpatches.Patch(label=f'26: RF Enable Interlock ({self.fault_population[26]})')
        legend_27 = mpatches.Patch(label=f'27: Switched Modulator OFF. ({self.fault_population[27]})')

        _HANDLES = [legend_0,
                    legend_1,
                    legend_2,
                    legend_3,
                    legend_4,
                    legend_5,
                    legend_6,
                    legend_7,
                    legend_8,
                    legend_9,
                    legend_10,
                    legend_11,
                    legend_12,
                    legend_13,
                    legend_14,
                    legend_15,
                    legend_16,
                    legend_17,
                    legend_18,
                    legend_19,
                    legend_20,
                    legend_21,
                    legend_22,
                    legend_23,
                    legend_24,
                    legend_25,
                    legend_26,
                    legend_27]

        plt.legend(handles=_HANDLES, fontsize=5, loc=0)

        plt.title(f'From    {self.date_from} {self.time_from}\nto         {self.date_to} {self.time_to}')
        plt.xlabel('Hold RF On Fault Log')
        plt.ylabel('N')
        plt.savefig(self.savepath + self.savename)
        plt.close('all')


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

    def find_top_x_peaks_histogram(self, bin_population, midbin_vals):
        '''
        The returns from pyplot.his() are used in this function to give the x-axis value of the the top X number of peaks,
		along with the number of members of that bin.
		eg. self.n, self.bedges, self.patches = plt.hist(self.data_reduced, bins=nbin, range=(min_data, max_data), histtype='step', color='k')
		:param n: Number of members of each bin.
		:param midbin_vals: a list of histogram x-axis mid-bin values.
		:return: peak_x_val, peak_y_val
		'''
        self.top_x = int(HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.X_HIGHEST_PEAKS_HIST])
        # Bypass the config value of top_x if not reading in the PVs
        # self.top_x = int(25)
        self.bin_population = bin_population
        self.midbin_vals = np.array(midbin_vals)
        self.peak_x_val = []
        self.peak_y_val = []

        count = 0
        while self.top_x > count:
            #print(f'\ncount = {count}')
            bin_population_top_idxs = self.bin_population.argsort()[-self.top_x:][::-1]
            self.peak_x_val.append(self.midbin_vals[bin_population_top_idxs[count]])
            self.peak_y_val.append(self.bin_population[bin_population_top_idxs[count]])
            count += 1

        print(f'\nself.peak_x_val = {self.peak_x_val}\nself.peak_y_val = {self.peak_y_val}\n')

        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.hist_peak_x_vals] = self.peak_x_val
        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.hist_peak_y_vals] = self.peak_y_val

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

    def handle_group_subplots(self, unique_group_idx, pv_idx_list, xaxis='index', individual_index=False):
        '''
        wrapper function that creates a floder for each unique group index
        then calls unique_group_all_subplots_x() and unique_group_individual_subplots_x()
        :param unique_group_idx:
        :param pv_idx_list:
        :param xaxis: 'time', 'index' or 'both'
        :param individual_index: turn plotting unique_group_individual_subplots_x(xaxis='index') on or off (True or False)
        :return:
        '''

        self.unique_group_idx = int(unique_group_idx)
        self.pv_idx_list = pv_idx_list
        self.xaxis = xaxis
        self.individual_index = individual_index
        self.foldername = f'\\UniqueGroup_{self.unique_group_idx}'

        self.create_folder_UniqueGroup_number(self.foldername)

        if self.xaxis == 'time':
            self.unique_group_all_subplots_x(self.unique_group_idx, self.pv_idx_list, self.foldername, xaxis='time')
            self.unique_group_individual_subplots_x(self.unique_group_idx, self.pv_idx_list, self.foldername, xaxis='time')

        elif self.xaxis == 'index':
            self.unique_group_all_subplots_x(self.unique_group_idx, self.pv_idx_list, self.foldername, xaxis='index')
            if self.individual_index == True:
                self.unique_group_individual_subplots_x(self.unique_group_idx, self.pv_idx_list, self.foldername, xaxis='index')
            else:
                pass

        elif self.xaxis == 'both':
            self.unique_group_all_subplots_x(self.unique_group_idx, self.pv_idx_list, self.foldername, xaxis='time')
            self.unique_group_individual_subplots_x(self.unique_group_idx, self.pv_idx_list, self.foldername, xaxis='time')

            self.unique_group_all_subplots_x(self.unique_group_idx, self.pv_idx_list, self.foldername, xaxis='index')
            if self.individual_index == True:
                self.unique_group_individual_subplots_x(self.unique_group_idx, self.pv_idx_list, self.foldername,xaxis='index')
            else:
                pass

        else:
            print(f'3rd arguement in unique_group_subplots_x() need to be either "time" or "index"\n'
                  f'Currently it is "{self.xaxis}"')
            sys.exit()

    def create_folder_UniqueGroup_number(self, foldername):
        '''
        Creates a folder in the savepath folder with a name based on the time range entered into the config yaml
        useful for storing data
        :return:
        '''
        #df = data_functions()
        #df.create_folder_named_date_time_from_to()

        self.directory = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]

        self.foldername = foldername

        self.path = r'{}\{}'.format(self.directory, self.foldername)  # path to be created

        print('directory = {}\npath = {}'.format(self.directory, self.path))

        try:
            os.makedirs(self.path)
            print(f'\nNew "{self.foldername}" folder created.\n')
        except OSError:
            try:
                folder_test = self.path
                print(f'\n"{self.foldername}" folder already exists.')
            except:
                print(f'\n...Problem with setting up "{self.foldername}" folder.')
                sys.exit()


    def unique_group_all_subplots_x(self, unique_group_idx, pv_idx_list, foldername, xaxis='index'):
        '''

        *** NB - Just for "standby --> standby" groups NOT "delta_time" yet ***

        Creates a figure of X number vertically stacked PV subplots with modulator state at the bottom
        and ONE member of the unique group plotted in each PV subplot.
        :param pv_idx_list: a list of all PVs required with mod state (usually index 0) at the end of the list.
        :return:
        '''

        self.unique_group_idx = int(unique_group_idx)
        self.pv_idx_list = pv_idx_list
        self.foldername = foldername
        self.xaxis = xaxis
        self.N_PVs = len(self.pv_idx_list)

        if self.N_PVs > 9:
            print(f'\n\nMore than 9 sublots selected in subplots_x() function.\nReduce number or amend function.')
            sys.exit()
        else:
            pass

        self.savepath = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]
        self.all_mod_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.all_mod_PVs]
        self.PV_TIME_DATA = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PV_TIME_DATA]
        self.PV_YAXIS_DATA = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PV_YAXIS_DATA]
        self.unique_group_start_times_standby = HRFOv2_EPICS_data.values[
            HRFOv2_EPICS_data.unique_group_start_times_standby]
        self.unique_group_end_times_standby = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.unique_group_end_times_standby]
        self.unique_group_member_indices = HRFOv2_EPICS_data.values[
            HRFOv2_EPICS_data.unique_group_member_indices_standby]
        self.mod_StateRead_time = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.mod_StateRead_time]
        self.mod_StateRead_yaxis = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.mod_StateRead_yaxis]
        self.mod_StateRead_plot_index = self.N_PVs + 1
        self.plus_minus_time_buffer = 1.0
        self.mod_state_time = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.mod_StateRead_time]
        self.idx_pv_dict = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.idx_pv_dict]
        self.time_0 = self.mod_state_time[0]
        self.delta_time = (max(self.unique_group_end_times_standby[self.unique_group_idx]) - min(self.unique_group_start_times_standby[self.unique_group_idx]))
        self.end_time = self.time_0 + self.delta_time
        self.colours = ['r', 'g', 'b', 'c', 'darkorange', 'm', 'k', 'gray', 'brown']
        self.savename_idx_string = ''
        self.suptitle_string = ''
        fig, axs = plt.subplots(self.N_PVs + 1)

        TIME_min = []
        TIME_max = []

        save_pvs = ''
        for s in self.pv_idx_list:
            save_pvs += f'-{str(s)}'

        # Open text file
        txt_file_name = self.savepath + self.foldername + f"\\PVs{str(save_pvs)}_UniqueGroup{self.unique_group_idx}_{self.xaxis}.txt"
        text_file_obj = open(txt_file_name, 'w')


        fs = 6  # title fontsize
        for idx, pv_idx in enumerate(self.pv_idx_list):
            self.savename_idx_string + '_' + str(pv_idx)
            self.suptitle_string + self.all_mod_PVs[pv_idx] + '\n'

            pv_name = str(self.idx_pv_dict[str(pv_idx)])

            axs[idx].set_title(f'{pv_name} [{pv_idx}]', size=fs, loc='right', y=0.75) #  , fontsize=fs)



            for g_idx, g in enumerate(self.unique_group_member_indices[self.unique_group_idx]):

                # Write to text file
                if xaxis == 'time':
                    text_file_obj.write(f'\n\n{pv_name} [{str(pv_idx)}]\nUnique Group Member Index #{str(g_idx)}\nTime (s)\tValue\n')

                if xaxis == 'index':
                    text_file_obj.write(f'\n\n{pv_name} [{str(pv_idx)}]\nUnique Group Member Index #{str(g_idx)}\nIndex\tValue\n')

                time_min_raw = self.unique_group_start_times_standby[self.unique_group_idx][g_idx]

                time_min = time_min_raw - self.plus_minus_time_buffer
                time_max_raw = self.unique_group_end_times_standby[self.unique_group_idx][
                                   g_idx] + self.plus_minus_time_buffer
                time_max = time_max_raw + self.plus_minus_time_buffer

                TIME_min.append(time_min)
                TIME_max.append(time_max)

                mod_time_0 = self.mod_StateRead_time[self.unique_group_member_indices[self.unique_group_idx][g_idx][0]]

                temp_time = [self.PV_TIME_DATA[pv_idx][i] for i in range(len(self.PV_TIME_DATA[pv_idx])) if
                             self.PV_TIME_DATA[pv_idx][i] > time_min and self.PV_TIME_DATA[pv_idx][i] < time_max]
                zeroed_time = [i - mod_time_0 for i in temp_time]
                temp_yaxis = [self.PV_YAXIS_DATA[pv_idx][i] for i in range(len(self.PV_YAXIS_DATA[pv_idx])) if
                              self.PV_TIME_DATA[pv_idx][i] > time_min and self.PV_TIME_DATA[pv_idx][i] < time_max]


                if self.xaxis == 'time':

                    axs[idx].step(zeroed_time, temp_yaxis, color='b', where='post')
                    axs[idx].scatter(zeroed_time, temp_yaxis, marker='o', s=3.0, c='r')

                    # Write to text file
                    for txt_idx in range(len(zeroed_time)):
                        text_file_obj.write(str(zeroed_time[txt_idx]) + '\t' + str(temp_yaxis[txt_idx]) + '\n')


                elif self.xaxis == 'index':

                    axs[idx].step(range(len(zeroed_time)), temp_yaxis, color='b', where='post')
                    axs[idx].scatter(range(len(zeroed_time)), temp_yaxis, marker='o', s=3.0, c='r')

                    # Write to text file
                    for txt_idx in range(len(zeroed_time)):
                        text_file_obj.write(str(txt_idx) + '\t' + str(temp_yaxis[txt_idx]) + '\n')


                else:
                    print(f'3rd arguement in unique_group_subplots_x() need to be either "time" or "index"\n'
                          f'Currently it is "{self.xaxis}"')
                    sys.exit()

                # make these tick labels invisible
                plt.setp(axs[idx].get_xticklabels(), visible=False)


        axs[self.mod_StateRead_plot_index - 1].set_title('CLA-GUNS-HRF-MOD-01:Sys:StateRead', size=fs, loc='right', y=0.75) # , fontsize=fs)



        for t_idx, t in enumerate(self.unique_group_member_indices[self.unique_group_idx]):

            if self.xaxis == 'time':
                text_file_obj.write(f'\n\nModulator States\nUnique Group Member Index #{str(t_idx)}\nTime (s)\tState Number\n')

            if self.xaxis == 'index':
                text_file_obj.write(f'\n\nModulator States\nUnique Group Member Index #{str(t_idx)}\nIndex\tState Number\n')

            time_min = TIME_min[t_idx]
            time_min_raw = TIME_min[t_idx] + self.plus_minus_time_buffer
            time_max = TIME_max[t_idx]
            time_max_raw = TIME_max[t_idx] - self.plus_minus_time_buffer

            # Plot the modulator state on the bottom panel:
            mod_temp_time = [self.mod_StateRead_time[i] for i in range(len(self.mod_StateRead_time)) if
                             self.mod_StateRead_time[i] > time_min and self.mod_StateRead_time[i] < time_max]

            zeroed_mod_time = [i - mod_temp_time[0] for i in mod_temp_time]

            mod_temp_yaxis = [self.mod_StateRead_yaxis[i] for i in range(len(self.mod_StateRead_yaxis)) if
                              self.mod_StateRead_time[i] > time_min and self.mod_StateRead_time[i] < time_max]

            if self.xaxis == 'time':

                axs[self.mod_StateRead_plot_index - 1].step(zeroed_mod_time, mod_temp_yaxis, color='b', where='post')
                axs[self.mod_StateRead_plot_index - 1].scatter(zeroed_mod_time, mod_temp_yaxis, marker='o', s=3.0,
                                                               c='r')

                # Write to text file
                for txt_idx in range(len(zeroed_mod_time)):
                    text_file_obj.write(str(zeroed_mod_time[txt_idx]) + '\t' + str(mod_temp_yaxis[txt_idx]) + '\n')

            elif self.xaxis == 'index':

                axs[self.mod_StateRead_plot_index - 1].step(range(len(zeroed_mod_time)), mod_temp_yaxis, color='b', where='post')

                axs[self.mod_StateRead_plot_index - 1].scatter(range(len(zeroed_mod_time)), mod_temp_yaxis, marker='o',
                                                               s=3.0, c='r')

                # Write to text file
                for txt_idx in range(len(zeroed_mod_time)):
                    text_file_obj.write(str(txt_idx) + '\t' + str(mod_temp_yaxis[txt_idx]) + '\n')


            else:
                print(f'3rd arguement in unique_group_subplots_x() need to be either "time" or "index"\n'
                      f'Currently it is "{self.xaxis}"')
                sys.exit()

        if self.xaxis == 'time':
            plt.xlabel("Time Elapsed Since ModState == 'Standby' (s)")
        elif self.xaxis == 'index':
            plt.xlabel("Index Number")
        else:
            pass

        save_pvs = ''
        for s in self.pv_idx_list:
            save_pvs += f'-{str(s)}'
        print(f'self.savepath = {self.savepath}\n'
              f'self.foldername = {self.foldername}\n'
              f'self.unique_group_idx = {self.unique_group_idx}\n'
              f'self.xaxis = {self.xaxis}\n'
              f'save_pvs = {save_pvs}\n'
              )

        plt.savefig(
            self.savepath + self.foldername + f"\\PVs{str(save_pvs)}_UniqueGroup{self.unique_group_idx}_AllGroups_{self.xaxis}.png")
        plt.close('all')

        # Close text file
        text_file_obj.close()

    def unique_group_individual_subplots_x(self, unique_group_idx, pv_idx_list, foldername, xaxis='time'):
        '''

        *** NB - Just for "standby --> standby" groups NOT "delta_time" yet ***

        Creates a figure of X number vertically stacked PV subplots with modulator state at the bottom
        and ONE member of the unique group plotted in each PV subplot.
        :param pv_idx_list: a list of all PVs required with mod state (usually index 0) at the end of the list.
        :return:
        '''

        self.unique_group_idx = int(unique_group_idx)
        self.pv_idx_list = pv_idx_list
        self.foldername = foldername
        self.xaxis = xaxis
        self.N_PVs = len(self.pv_idx_list)

        if self.N_PVs > 9:
            print(f'\n\nMore than 9 sublots selected in subplots_x() function.\nReduce number or amend function.')
            sys.exit()
        else:
            pass

        self.savepath = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]
        self.all_mod_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.all_mod_PVs]
        self.PV_TIME_DATA = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PV_TIME_DATA]
        self.PV_YAXIS_DATA = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PV_YAXIS_DATA]
        # self.unique_groups_standby = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.unique_groups_standby]
        self.unique_group_start_times_standby = HRFOv2_EPICS_data.values[
            HRFOv2_EPICS_data.unique_group_start_times_standby]
        self.unique_group_end_times_standby = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.unique_group_end_times_standby]
        # self.unique_groups_population_standby = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.unique_groups_population_standby]
        self.unique_group_member_indices = HRFOv2_EPICS_data.values[
            HRFOv2_EPICS_data.unique_group_member_indices_standby]

        self.mod_StateRead_time = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.mod_StateRead_time]
        self.mod_StateRead_yaxis = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.mod_StateRead_yaxis]
        self.mod_StateRead_plot_index = self.N_PVs + 1

        self.idx_pv_dict = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.idx_pv_dict]

        self.plus_minus_time_buffer = 1.0

        self.mod_state_time = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.mod_StateRead_time]

        self.time_0 = self.mod_state_time[0]
        self.delta_time = (max(self.unique_group_end_times_standby[self.unique_group_idx]) - min(self.unique_group_start_times_standby[self.unique_group_idx]))
        self.end_time = self.time_0 + self.delta_time

        # print(f'self.time_0 = {self.time_0}\n'
        #       f'self.delta_time = {self.delta_time}\n'
        #       f'self.end_time = {self.end_time}')

        # self.PV_TIME_zeroed = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PV_TIME_zeroed]

        self.colours = ['r', 'g', 'b', 'c', 'darkorange', 'm', 'k', 'gray', 'brown']

        self.savename_idx_string = ''
        self.suptitle_string = ''

        # TODO: set up x-axis so start of each group = (0s - delta time) and end = (0s + delta time)
        #  maybe start - 20s and end + 20s to capture context
        #  then for each PV subplot cycle over each unique group member and plot x and y.
        # ~~~~~~~~~~~~~~~~~~~~~~ MESS !! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        save_pvs = ''
        for s in self.pv_idx_list:
            save_pvs += f'-{str(s)}'
        print(f'save_pvs = {save_pvs}')

        fs = 6  # title fontsize

        for g_idx, g in enumerate(self.unique_group_member_indices[self.unique_group_idx]):

            # self.savename_idx_string + '_' + str(pv_idx)
            # self.suptitle_string + self.all_mod_PVs[pv_idx] + '\n'

            fig, axs = plt.subplots(self.N_PVs + 1)

            axs[self.mod_StateRead_plot_index - 1].set_title('CLA-GUNS-HRF-MOD-01:Sys:StateRead', size=fs, loc='right',
                                                             y=0.75)  # , fontsize=fs)

            TIME_min = []
            TIME_max = []

            for idx, pv_idx in enumerate(self.pv_idx_list):

                # print(f'self.unique_group_member_indices[self.unique_group_idx] = {self.unique_group_member_indices[self.unique_group_idx]}')

                # print(f'self.unique_group_start_times_standby[g_idx] = {self.unique_group_start_times_standby[g_idx] }')

                #if idx == 0:
                pv_name = str(self.idx_pv_dict[str(pv_idx)])

                axs[idx].set_title(pv_name, size=fs, loc='right', y=0.75)  # , fontsize=fs)


                time_min_raw = self.unique_group_start_times_standby[self.unique_group_idx][g_idx]
                #print(f'time_min_raw = {time_min_raw}')
                time_min = time_min_raw - self.plus_minus_time_buffer
                time_max_raw = self.unique_group_end_times_standby[self.unique_group_idx][
                                   g_idx] + self.plus_minus_time_buffer
                time_max = time_max_raw + self.plus_minus_time_buffer

                TIME_min.append(time_min)
                TIME_max.append(time_max)

                # mod_time_0 = [self.mod_StateRead_time[i] for i in range(len(self.mod_StateRead_time)) if
                #               self.mod_StateRead_time[i] > time_min and self.mod_StateRead_time[i] < time_max][0]

                mod_time_0 = self.mod_StateRead_time[self.unique_group_member_indices[self.unique_group_idx][g_idx][0]]

                temp_time = [self.PV_TIME_DATA[pv_idx][i] for i in range(len(self.PV_TIME_DATA[pv_idx])) if
                             self.PV_TIME_DATA[pv_idx][i] > time_min and self.PV_TIME_DATA[pv_idx][i] < time_max]
                zeroed_time = [i - mod_time_0 for i in temp_time]
                temp_yaxis = [self.PV_YAXIS_DATA[pv_idx][i] for i in range(len(self.PV_YAXIS_DATA[pv_idx])) if
                              self.PV_TIME_DATA[pv_idx][i] > time_min and self.PV_TIME_DATA[pv_idx][i] < time_max]

                # yaxis = self.PV_TIME_zeroed[self.unique_group_idx]

                # print(f'{g_idx}: len(temp_time) = {temp_time}\n'
                #       f'{g_idx}: len(temp_yaxis) = {temp_yaxis}')

                if self.xaxis == 'time':

                    axs[idx].step(zeroed_time, temp_yaxis, color='b', where='post')
                    axs[idx].scatter(zeroed_time, temp_yaxis, marker='o', s=3.0, c='r')


                elif self.xaxis == 'index':

                    axs[idx].step(range(len(zeroed_time)), temp_yaxiscolor='b', where='post')
                    axs[idx].scatter(range(len(zeroed_time)), temp_yaxis, marker='o', s=3.0, c='r')




                else:
                    print(f'3rd arguement in unique_group_subplots_x() need to be either "time" or "index"\n'
                          f'Currently it is "{self.xaxis}"')
                    sys.exit()

                # make these tick labels invisible
                plt.setp(axs[idx].get_xticklabels(), visible=False)

            # for ug_idx, ug in enumerate(self.unique_group_member_indices):

            # print(f'len(axs) = {len(axs)}\n'
            #       f'self.mod_StateRead_plot_index] = {self.mod_StateRead_plot_index}')

            for t_idx, t in enumerate(TIME_min):

                time_min = TIME_min[t_idx]
                time_min_raw = TIME_min[t_idx] + self.plus_minus_time_buffer
                time_max = TIME_max[t_idx]
                time_max_raw = TIME_max[t_idx] - self.plus_minus_time_buffer

                # lastly plot the modulator state on the bottom panel:

                mod_temp_time = [self.mod_StateRead_time[i] for i in range(len(self.mod_StateRead_time)) if
                                 self.mod_StateRead_time[i] > time_min and self.mod_StateRead_time[i] < time_max]

                zeroed_mod_time = [i - mod_temp_time[0] for i in mod_temp_time]

                mod_temp_yaxis = [self.mod_StateRead_yaxis[i] for i in range(len(self.mod_StateRead_yaxis)) if
                                  self.mod_StateRead_time[i] > time_min and self.mod_StateRead_time[i] < time_max]

                if self.xaxis == 'time':

                    axs[self.mod_StateRead_plot_index - 1].step(zeroed_mod_time, mod_temp_yaxis, color='b', where='post')
                    axs[self.mod_StateRead_plot_index - 1].scatter(zeroed_mod_time, mod_temp_yaxis, marker='o', s=3.0,
                                                                   c='r')

                    for xy in zip(zeroed_mod_time, mod_temp_yaxis):
                        y = xy[1]
                        axs[self.mod_StateRead_plot_index - 1].annotate(f'{y}', xy=xy, textcoords='data')


                elif self.xaxis == 'index':

                    axs[self.mod_StateRead_plot_index - 1].step(range(len(zeroed_mod_time)), mod_temp_yaxis, where='post',
                                                                color='b')
                    axs[self.mod_StateRead_plot_index - 1].scatter(range(len(zeroed_mod_time)), mod_temp_yaxis, marker='o',
                                                                   s=3.0, c='r')

                    for xy in zip(range(len(zeroed_mod_time)), mod_temp_yaxis):
                        y = xy[1]
                        axs[self.mod_StateRead_plot_index - 1].annotate(f'{y}', xy=xy, textcoords='data')

                else:
                    print(f'3rd arguement in unique_group_subplots_x() need to be either "time" or "index"\n'
                          f'Currently it is "{self.xaxis}"')
                    sys.exit()

            if self.xaxis == 'time':
                plt.xlabel("Time Elapsed Since ModState == 'Standby' (s)")
            elif self.xaxis == 'index':
                plt.xlabel("Index Number")
            else:
                pass

            plt.savefig(self.savepath + self.foldername + f"\\PVs{str(save_pvs)}_UniqueGroup{self.unique_group_idx}_GroupMember{g_idx}_{self.xaxis}.png")
            plt.close('all')


    def overplot_HV_PV_data(self, time_list, yaxis_list, pv_name, savepath, savename, pv_idx):
        '''
        Overplots all data in a list of lists for one PV for every HV interlock window.
        We are looking for correlations or just patterns in general.
        :param time_list: list of lists of time data for this PV in this HV interlock window
        :param yaxis_list: list of lists of y-axis data for this PV in this HV interlock window
        :param pv_name: Name of this PV
        :param savepath: amended savepath; save in 'HV_interlock_PV_overplots' folder within savepath
        :param savename: savename, usualy PV name
        :param pv_idx: index of PV as set by the order of the list in the cnfig .yaml
        :return: saved overplots
        '''
        self.time_list = time_list
        self.yaxis_list = yaxis_list
        self.pv_name = pv_name
        self.savepath = savepath
        self.savename = savename
        self.pv_idx = pv_idx

        print(f'savepath = {savepath}')

        for idx, time_data in enumerate(self.time_list):
            plt.step(time_data, self.yaxis_list[idx], color='b', where='post')
            plt.scatter(time_data, self.yaxis_list[idx], marker='o', s=3.0, c='r')

        plt.title(self.pv_name)
        plt.ylabel(self.pv_name)
        plt.xlabel("Time Since Epics Epoch")
        plt.savefig(f"{self.savepath}\\{self.savename}_pv_{self.pv_idx}.png")
        plt.close('all')


    def subplot_HV_PV_data(self, time_vector, yaxis_list_of_lists, HV_time, Bespoke_savepath, savename):
        '''
        Takes one HV interlock window and creates subplots of all PVs of interest for that period
        :param time_vector: list of normalised time
        :param yaxis_list_of_lists: list of lists of each subplot y-axis data
        :param HV_time: EPICS formatted time as plot name, also acts as savename
        :param Bespoke_savepath:
        :return:
        '''
        self.time_vector = time_vector
        self.yaxis_list_of_lists = yaxis_list_of_lists
        self.HV_time = HV_time
        self.savepath = Bespoke_savepath
        self.savename = savename
        self.plot_title = f'{self.savename[:10]} {self.savename[11:13]}:{self.savename[13:15]}:{self.savename[15:17]}.{self.savename[17:19]} '
        self.HV_interlock_comparison_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.HV_interlock_comparison_PVs]
        self.interlock_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.interlock_PVs]
        self.delta_time_before_seconds = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.HV_interlock_window_seconds_before]
        self.delta_time_after_seconds = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.HV_interlock_window_seconds_after]
        self.n_subplots = len(self.yaxis_list_of_lists)

        print(f'self.time_vector[0] = {self.time_vector[0]}\n'
              f'self.savename = {self.savename}\n'
              f'self.HV_time = {self.HV_time}')
        #input()

        fig, axes = plt.subplots(self.n_subplots, 1, dpi=125)

        #fig, axes = plt.subplots(12, 1, dpi=180)
        fig.suptitle(str(self.plot_title))

        for idx in range(self.n_subplots):
            # print(f'min = {float(np.amin(self.yaxis_list_of_lists[idx]))}\n'
            #       f'max = { float(np.amax(self.yaxis_list_of_lists[idx]))}')
            axes[idx].step(self.time_vector[idx], self.yaxis_list_of_lists[idx], where='post', lw=1.2, color='mediumblue')
            axes[idx].scatter(self.time_vector[idx], self.yaxis_list_of_lists[idx], marker='o', s=1.0, c='r')
            if type(self.yaxis_list_of_lists[idx][0]) == str:
                pass
            else:
                axes[idx].vlines(0.0, float(np.amin(self.yaxis_list_of_lists[idx])), float(np.amax(self.yaxis_list_of_lists[idx])), lw=0.6, ls='--', color='r')
            axes[idx].set_xlim(-self.delta_time_before_seconds, self.delta_time_after_seconds)
            if self.HV_interlock_comparison_PVs[idx] == "CLA-GUNS-HRF-MOD-01:Sys:StateRead" or self.HV_interlock_comparison_PVs[idx] == "CLA-GUNS-HRF-MOD-01:Sys:StateSet":
                for xy_idx, xy in enumerate(zip(self.time_vector[idx], self.yaxis_list_of_lists[idx])):  # <--
                    axes[idx].annotate('%s' % self.yaxis_list_of_lists[idx][xy_idx], xy=xy, textcoords='data', fontsize=7.)

            if self.HV_interlock_comparison_PVs[idx] in self.interlock_PVs:
                self.interlock_PVs_unique_labels = list(set(self.yaxis_list_of_lists[idx]))
                axes[idx].text(0.8, 0.9,
                               self.interlock_PVs_unique_labels,
                               ha='center', va='center',
                               transform=axes[idx].transAxes,
                               fontsize=6.)

            # print PV name on each subplot
            axes[idx].text(0.25, 0.6,
                           self.HV_interlock_comparison_PVs[idx],
                           ha='center', va='center',
                           transform=axes[idx].transAxes,
                           fontsize=6.)

            # remove x- and y-axis ticks from each subplot
            # apart from the x-axis ticks on the last subplot
            if str(idx) == str(self.n_subplots-1):
                #axes[idx].set_yticks([])
                pass
            else:
                axes[idx].set_xticks([])
                #axes[idx].set_yticks([])

        plt.xlabel('Time relative to HV interlock log timestamp (s)')
        plt.savefig(f'{self.savepath}\\{savename}.png')
        plt.close('all')
        
    def subplot_chosen_PV_data(self, time_vector, yaxis_list_of_lists, chosen_time, Bespoke_savepath, savename):
        '''
        Takes one chosen interlock window and creates subplots of all PVs of interest for that period
        :param time_vector: list of normalised time
        :param yaxis_list_of_lists: list of lists of each subplot y-axis data
        :param chosen_time: EPICS formatted time as plot name, also acts as savename
        :param Bespoke_savepath:
        :return:
        '''
        self.time_vector = time_vector
        self.yaxis_list_of_lists = yaxis_list_of_lists
        self.chosen_time = chosen_time
        self.savepath = Bespoke_savepath
        self.savename = savename
        self.plot_title = f'{self.savename[:10]} {self.savename[11:13]}:{self.savename[13:15]}:{self.savename[15:17]}.{self.savename[17:19]} '
        self.chosen_interlock_comparison_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.chosen_interlock_comparison_PVs]
        self.interlock_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.interlock_PVs]
        self.delta_time_before_seconds = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.chosen_interlock_window_seconds_before]
        self.delta_time_after_seconds = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.chosen_interlock_window_seconds_after]
        self.n_subplots = len(self.yaxis_list_of_lists)

        print(f'self.time_vector[0] = {self.time_vector[0]}\n'
              f'self.savename = {self.savename}\n'
              f'self.chosen_time = {self.chosen_time}')
        #input()

        fig, axes = plt.subplots(self.n_subplots, 1, dpi=125)

        #fig, axes = plt.subplots(12, 1, dpi=180)
        fig.suptitle(str(self.plot_title))

        for idx in range(self.n_subplots):
            # print(f'min = {float(np.amin(self.yaxis_list_of_lists[idx]))}\n'
            #       f'max = { float(np.amax(self.yaxis_list_of_lists[idx]))}')
            axes[idx].step(self.time_vector[idx], self.yaxis_list_of_lists[idx], where='post', lw=1.2, color='mediumblue')
            axes[idx].scatter(self.time_vector[idx], self.yaxis_list_of_lists[idx], marker='o', s=1.0, c='r')
            print(f'self.yaxis_list_of_lists[idx] = {self.yaxis_list_of_lists[idx]}')
            if type(self.yaxis_list_of_lists[idx][0]) == str:
                pass
            else:
                axes[idx].vlines(0.0, float(np.amin(self.yaxis_list_of_lists[idx])), float(np.amax(self.yaxis_list_of_lists[idx])), lw=0.6, ls='--', color='r')
            axes[idx].set_xlim(-self.delta_time_before_seconds, self.delta_time_after_seconds)
            if self.chosen_interlock_comparison_PVs[idx] == "CLA-GUNS-HRF-MOD-01:Sys:StateRead" or self.chosen_interlock_comparison_PVs[idx] == "CLA-GUNS-HRF-MOD-01:Sys:StateSet":
                for xy_idx, xy in enumerate(zip(self.time_vector[idx], self.yaxis_list_of_lists[idx])):  # <--
                    axes[idx].annotate('%s' % self.yaxis_list_of_lists[idx][xy_idx], xy=xy, textcoords='data', fontsize=7.)

            if self.chosen_interlock_comparison_PVs[idx] == "CLA-GUNS-RFHOLD:FaultLog":
                for xy_idx, xy in enumerate(zip(self.time_vector[idx], self.yaxis_list_of_lists[idx])):  # <--
                    axes[idx].annotate('%s' % self.yaxis_list_of_lists[idx][xy_idx], xy=xy, textcoords='data', fontsize=7.)


            if self.chosen_interlock_comparison_PVs[idx] in self.interlock_PVs:
                self.interlock_PVs_unique_labels = list(set(self.yaxis_list_of_lists[idx]))
                axes[idx].text(0.8, 0.9,
                               self.interlock_PVs_unique_labels,
                               ha='center', va='center',
                               transform=axes[idx].transAxes,
                               fontsize=6.)

            # print PV name on each subplot
            axes[idx].text(0.25, 0.6,
                           self.chosen_interlock_comparison_PVs[idx],
                           ha='center', va='center',
                           transform=axes[idx].transAxes,
                           fontsize=6.)

            # remove x- and y-axis ticks from each subplot
            # apart from the x-axis ticks on the last subplot
            if str(idx) == str(self.n_subplots-1):
                #axes[idx].set_yticks([])
                pass
            else:
                axes[idx].set_xticks([])
                #axes[idx].set_yticks([])

        plt.xlabel('Time relative to chosen interlock log timestamp (s)')
        plt.savefig(f'{self.savepath}\\{savename}.png')
        plt.close('all')