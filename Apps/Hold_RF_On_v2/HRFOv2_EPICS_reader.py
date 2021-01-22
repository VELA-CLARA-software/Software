'''
Python 3:
https://www.python.org/downloads/windows/
Pycharm:
https://www.jetbrains.com/pycharm/download/#section=windows
Github:
https://git-scm.com/download/win
'''

savepath = r"C:\Users\zup98752\OneDrive - Science and Technology Facilities Council\Hold_RF_On\Python\Analysis"

import json
import requests
import matplotlib.pyplot as plt

#Define the PV
pv_name = 'CLA-GUNS-HRF-MOD-01:Sys:StateRead'
#pv_name = "CLA-S01-DIA-WCM-01:Q"

#Define the from and to times
time_from = "2021-01-19T10:00:00.00Z"
time_to = "2021-01-21T14:00:00.00Z"

url = "http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv="+pv_name+"&from="+time_from+"&to="+time_to
print(url)

r = requests.get(url)
data = r.json()

yaxis = []
time = []
for event in data[0]["data"] :
    time.append(event["secs"]+event["nanos"]*1E-9)
    yaxis.append(event["val"])

print(data[0]["meta"])

savename = data[0]["meta"]['name'][0:19]
print(savepath + "\\" + savename + r".png")

plt.plot(time,yaxis)
#plt.ylabel(data[0]["meta"]["EGU"])
plt.ylabel(data[0]["meta"]['name'])
plt.xlabel("Time Since Epics Epoch")
plt.savefig(savepath + "\\" + savename + r".png")
plt.close('all')

all_mod_PVs = [	"CLA-GUNS-HRF-MOD-01:HvPs:HvPs1:CurrRead",
	"CLA-GUNS-HRF-MOD-01:HvPs:HvPs1:TrigCountRead",
	"CLA-GUNS-HRF-MOD-01:HvPs:HvPs1:VoltRead",
	"CLA-GUNS-HRF-MOD-01:HvPs:HvPs2:CurrRead",
	"CLA-GUNS-HRF-MOD-01:HvPs:HvPs2:VoltRead",
	"CLA-GUNS-HRF-MOD-01:HvPs:HvPs3:CurrRead"	,
	"CLA-GUNS-HRF-MOD-01:HvPs:HvPs3:VoltRead"	,
	"CLA-GUNS-HRF-MOD-01:Pt:Diag:CtArc"	,
	"CLA-GUNS-HRF-MOD-01:Pt:Diag:CtRead"	,
	"CLA-GUNS-HRF-MOD-01:Pt:Diag:CvdArc"	,
	"CLA-GUNS-HRF-MOD-01:Pt:Diag:CvdRead"	,
	"CLA-GUNS-HRF-MOD-01:Pt:Diag:PlswthFwhmRead"	,
	"CLA-GUNS-HRF-MOD-01:Pt:Diag:PlswthRead"	,
	"CLA-GUNS-HRF-MOD-01:Pt:Diag:PowRead"	,
	"CLA-GUNS-HRF-MOD-01:Pt:Diag:PrfRead"	,
	"CLA-GUNS-HRF-MOD-01:Pt:FilPs:CurrRead"	,
	"CLA-GUNS-HRF-MOD-01:Pt:FilPs:VoltRead"	,
	"CLA-GUNS-HRF-MOD-01:Rf:Cool:BodyOutletTemp"	,
	"CLA-GUNS-HRF-MOD-01:Rf:Cool:KlystLimit"	,
	"CLA-GUNS-HRF-MOD-01:Rf:Cool:KlystPower"	,
	"CLA-GUNS-HRF-MOD-01:Rf:Ionp:PresRead1"	,
	"CLA-GUNS-HRF-MOD-01:Rf:MagPs1:CurrRead"	,
	"CLA-GUNS-HRF-MOD-01:Rf:MagPs1:VoltRead"	,
	"CLA-GUNS-HRF-MOD-01:Rf:MagPs2:CurrRead"	,
	"CLA-GUNS-HRF-MOD-01:Rf:MagPs2:VoltRead"	,
	"CLA-GUNS-HRF-MOD-01:Rf:MagPs3:CurrRead"	,
	"CLA-GUNS-HRF-MOD-01:Rf:MagPs3:VoltRead"	,
	"CLA-GUNS-HRF-MOD-01:Rf:MagPs4:CurrRead"	,
	"CLA-GUNS-HRF-MOD-01:Rf:MagPs4:VoltRead"	,
	"CLA-GUNS-HRF-MOD-01:Sys:ErrorRead.SVAL"	,
	"CLA-GUNS-HRF-MOD-01:Sys:ExtComm:AccessLevel"	,
	"CLA-GUNS-HRF-MOD-01:Sys:HvHoursRead"	,
	"CLA-GUNS-HRF-MOD-01:Sys:INTLK1"	,
	"CLA-GUNS-HRF-MOD-01:Sys:INTLK2"	,
	"CLA-GUNS-HRF-MOD-01:Sys:INTLK3"	,
	"CLA-GUNS-HRF-MOD-01:Sys:INTLK4"	,
	"CLA-GUNS-HRF-MOD-01:Sys:INTLK5"	,
	"CLA-GUNS-HRF-MOD-01:Sys:OffHoursRead"	,
	"CLA-GUNS-HRF-MOD-01:Sys:RemainingTime"	,
	"CLA-GUNS-HRF-MOD-01:Sys:StandbyHoursRead"	,
	"CLA-GUNS-HRF-MOD-01:Sys:StateRead"	,
	"CLA-GUNS-HRF-MOD-01:Sys:StateSet"	,
	"CLA-GUNS-HRF-MOD-01:Sys:Trig:PlswthSet"	,
	"CLA-GUNS-HRF-MOD-01:Sys:Trig:PrfSet"	,
	"CLA-GUNS-HRF-MOD-01:Sys:TrigHoursRead"	]

opaque_PVs_name = []
opaque_PVs_index = []
X_DATA = []
Y_DATA = []
for pv_idx, pv_name in enumerate(all_mod_PVs):

    print('\n', pv_idx)
    url = "http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=" + pv_name + "&from=" + time_from + "&to=" + time_to
    print(url)
    try:
        r = requests.get(url)
        data = r.json()

        yaxis = []
        time = []
        for event in data[0]["data"]:
            time.append(event["secs"] + event["nanos"] * 1E-9)
            yaxis.append(event["val"])

        X_DATA.append(time)
        Y_DATA.append(yaxis)

        print(data[0]["meta"])

        savename = data[0]["meta"]['name'][0:19]
        print(savepath + "\\" + savename + r".png")

        plt.plot(time, yaxis, ls='-', lw=1.0, color='b')
        plt.scatter(time, yaxis, marker='o', s=3.0, c='r')
        # plt.ylabel(data[0]["meta"]["EGU"])
        plt.title(data[0]["meta"]['name'])
        plt.ylabel(data[0]["meta"]['name'])
        plt.xlabel("Time Since Epics Epoch")
        plt.savefig(savepath + "\\" + savename + f"_pv_{pv_idx}.png")
        plt.close('all')
    except:
        print(f'Could not access {pv_name}')
        opaque_PVs_name.append(pv_name)
        opaque_PVs_index.append(pv_idx)

print('\nPVs unable to open:')
for i in range(len(opaque_PVs_name)):
    print(f'{opaque_PVs_index[i]}: {opaque_PVs_name[i]}')

# sub plots:

PV_idx_0 = 14
PV_idx_1 = 40

fig, axs = plt.subplots(2)
fig.suptitle(f'{all_mod_PVs[PV_idx_0]}\n{all_mod_PVs[PV_idx_1]}')
axs[0].plot(X_DATA[PV_idx_0], Y_DATA[PV_idx_0], ls='-', lw=1.0, color='b')
axs[0].scatter(X_DATA[PV_idx_0], Y_DATA[PV_idx_0], marker='o', s=3.0, c='r')
axs[1].plot(X_DATA[PV_idx_1], Y_DATA[PV_idx_1], ls='-', lw=1.0, color='b')
axs[1].scatter(X_DATA[PV_idx_1], Y_DATA[PV_idx_1], marker='o', s=3.0, c='r')
plt.savefig(savepath + f"\\_subplots_{PV_idx_0}_{PV_idx_1}.png")
plt.close('all')

# Multiple y-axes:

def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


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
make_patch_spines_invisible(par2)
# Second, show the right spine.
par2.spines["right"].set_visible(True)

PV_idx_1 = 1
PV_idx_2 = 37
PV_idx_3 = 8

#p1, = host.plot([0, 1, 2], [0, 1, 2], "b-", label="Density")
#p2, = par1.plot([0, 1, 2], [0, 3, 2], "r-", label="Temperature")
#p3, = par2.plot([0, 1, 2], [50, 30, 15], "g-", label="Velocity")

p1, = host.plot(X_DATA[PV_idx_1], Y_DATA[PV_idx_1], ls='-', lw=1.0, color='r')
#p1, = host.scatter(X_DATA[PV_idx_1], Y_DATA[PV_idx_1], marker='o', s=3.0, c='r')
p2, = par1.plot(X_DATA[PV_idx_2], Y_DATA[PV_idx_2], ls='-', lw=1.0, color='g')
#p2, = par1.scatter(X_DATA[PV_idx_2], Y_DATA[PV_idx_2], marker='o', s=3.0, c='r')
p3, = par2.plot(X_DATA[PV_idx_3], Y_DATA[PV_idx_3], ls='-', lw=1.0, color='b')
#p3, = par2.scatter(X_DATA[PV_idx_3], Y_DATA[PV_idx_3], marker='o', s=3.0, c='r')

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

#host.legend(lines, [l.get_label() for l in lines])

plt.savefig(savepath + f"\\_Multi_y_{PV_idx_1}_{PV_idx_2}_{PV_idx_3}.png")
plt.close('all')
