\ Model GasLib-11
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  0 loadshed[N01] + 0 loadshed[N02] + 0 loadshed[N03] + 0 loadshed[N04]
   + 0 loadshed[N05] + 0 loadshed[entry03]
   + 21.80555555555556 loadshed[exit01]
   + 26.16666666666667 loadshed[exit02]
   + 17.44444444444444 loadshed[exit03]
Subject To
 PDAI_lower[entry01,entry03]: - 0.5660644491026487 flow[entry01,entry03]
   + pressure[entry01] - pressure[entry03]
   + 30 interdiction[entry01,entry03] >= 0
 PDAI_lower[N01,N02]: - 0.5660644491026487 flow[N01,N02] + pressure[N01]
   - pressure[N02] + 30 interdiction[N01,N02] >= 0
 PDAI_lower[entry02,N03]: - 0.5660644491026487 flow[entry02,N03]
   - pressure[N03] + pressure[entry02] + 30 interdiction[entry02,N03] >= 0
 PDAI_lower[N02,exit01]: - 0.5660644491026487 flow[N02,exit01]
   + pressure[N02] - pressure[exit01] + 30 interdiction[N02,exit01] >= 0
 PDAI_lower[N02,N04]: - 0.5660644491026487 flow[N02,N04] + pressure[N02]
   - pressure[N04] + 30 interdiction[N02,N04] >= 0
 PDAI_lower[N03,N04]: - 0.5660644491026487 flow[N03,N04] + pressure[N03]
   - pressure[N04] + 30 interdiction[N03,N04] >= 0
 PDAI_lower[N05,exit02]: - 0.5731961978256868 flow[N05,exit02]
   + pressure[N05] - pressure[exit02] + 20 interdiction[N05,exit02] >= 0
 PDAI_lower[N05,exit03]: - 0.5731961978256868 flow[N05,exit03]
   + pressure[N05] - pressure[exit03] + 20 interdiction[N05,exit03] >= 0
 PDAI_lower[entry03,N01]: - pressure[N01] + pressure[entry03]
   + 30 interdiction[entry03,N01] >= 0
 PDAI_lower[N04,N05]: pressure[N04] - pressure[N05]
   + 30 interdiction[N04,N05] >= 0
 PDAI_lower[N01,N03]: pressure[N01] - pressure[N03]
   + 30 interdiction[N01,N03] >= 0
 PDAI_upper[entry01,entry03]: - 0.5660644491026487 flow[entry01,entry03]
   + pressure[entry01] - pressure[entry03]
   - 30 interdiction[entry01,entry03] <= 0
 PDAI_upper[N01,N02]: - 0.5660644491026487 flow[N01,N02] + pressure[N01]
   - pressure[N02] - 30 interdiction[N01,N02] <= 0
 PDAI_upper[entry02,N03]: - 0.5660644491026487 flow[entry02,N03]
   - pressure[N03] + pressure[entry02] - 30 interdiction[entry02,N03] <= 0
 PDAI_upper[N02,exit01]: - 0.5660644491026487 flow[N02,exit01]
   + pressure[N02] - pressure[exit01] - 30 interdiction[N02,exit01] <= 0
 PDAI_upper[N02,N04]: - 0.5660644491026487 flow[N02,N04] + pressure[N02]
   - pressure[N04] - 30 interdiction[N02,N04] <= 0
 PDAI_upper[N03,N04]: - 0.5660644491026487 flow[N03,N04] + pressure[N03]
   - pressure[N04] - 30 interdiction[N03,N04] <= 0
 PDAI_upper[N05,exit02]: - 0.5731961978256868 flow[N05,exit02]
   + pressure[N05] - pressure[exit02] - 30 interdiction[N05,exit02] <= 0
 PDAI_upper[N05,exit03]: - 0.5731961978256868 flow[N05,exit03]
   + pressure[N05] - pressure[exit03] - 30 interdiction[N05,exit03] <= 0
 PDAI_upper[entry03,N01]: - pressure[N01] + pressure[entry03]
   - 30 interdiction[entry03,N01] <= 0
 PDAI_upper[N04,N05]: pressure[N04] - pressure[N05]
   - 30 interdiction[N04,N05] <= 0
 PDAI_upper[N01,N03]: pressure[N01] - pressure[N03]
   - 30 interdiction[N01,N03] <= 0
 flow_conservation[N01]: flow[N01,N02] - flow[entry03,N01] + flow[N01,N03]
   = 0
 flow_conservation[N02]: - flow[N01,N02] + flow[N02,exit01] + flow[N02,N04]
   = 0
 flow_conservation[N03]: - flow[entry02,N03] + flow[N03,N04]
   - flow[N01,N03] = 0
 flow_conservation[N04]: - flow[N02,N04] - flow[N03,N04] + flow[N04,N05]
   = 0
 flow_conservation[N05]: flow[N05,exit02] + flow[N05,exit03]
   - flow[N04,N05] = 0
 flow_conservation[entry01]: 34.88888888888889 loadshed[entry01]
   + flow[entry01,entry03] = 34.88888888888889
 flow_conservation[entry03]: - flow[entry01,entry03] + flow[entry03,N01]
   = 0
 flow_conservation[entry02]: 30.52777777777778 loadshed[entry02]
   + flow[entry02,N03] = 30.52777777777778
 flow_conservation[exit01]: - 21.80555555555556 loadshed[exit01]
   - flow[N02,exit01] = -21.80555555555556
 flow_conservation[exit02]: - 26.16666666666667 loadshed[exit02]
   - flow[N05,exit02] = -26.16666666666667
 flow_conservation[exit03]: - 17.44444444444444 loadshed[exit03]
   - flow[N05,exit03] = -17.44444444444444
 flow_lower[entry01,entry03]: - flow[entry01,entry03]
   + 65.41666666666666 interdiction[entry01,entry03] <= 65.41666666666666
 flow_lower[N01,N02]: - flow[N01,N02]
   + 65.41666666666666 interdiction[N01,N02] <= 65.41666666666666
 flow_lower[entry02,N03]: - flow[entry02,N03]
   + 65.41666666666666 interdiction[entry02,N03] <= 65.41666666666666
 flow_lower[N02,exit01]: - flow[N02,exit01]
   + 65.41666666666666 interdiction[N02,exit01] <= 65.41666666666666
 flow_lower[N02,N04]: - flow[N02,N04]
   + 65.41666666666666 interdiction[N02,N04] <= 65.41666666666666
 flow_lower[N03,N04]: - flow[N03,N04]
   + 65.41666666666666 interdiction[N03,N04] <= 65.41666666666666
 flow_lower[N05,exit02]: - flow[N05,exit02]
   + 65.41666666666666 interdiction[N05,exit02] <= 65.41666666666666
 flow_lower[N05,exit03]: - flow[N05,exit03]
   + 65.41666666666666 interdiction[N05,exit03] <= 65.41666666666666
 flow_lower[entry03,N01]: - flow[entry03,N01]
   + 65.41666666666666 interdiction[entry03,N01] <= 65.41666666666666
 flow_lower[N04,N05]: - flow[N04,N05]
   + 65.41666666666666 interdiction[N04,N05] <= 65.41666666666666
 flow_lower[N01,N03]: - flow[N01,N03]
   + 65.41666666666666 interdiction[N01,N03] <= 65.41666666666666
 flow_upper[entry01,entry03]: - flow[entry01,entry03]
   - 65.41666666666666 interdiction[entry01,entry03] >= -65.41666666666666
 flow_upper[N01,N02]: - flow[N01,N02]
   - 65.41666666666666 interdiction[N01,N02] >= -65.41666666666666
 flow_upper[entry02,N03]: - flow[entry02,N03]
   - 65.41666666666666 interdiction[entry02,N03] >= -65.41666666666666
 flow_upper[N02,exit01]: - flow[N02,exit01]
   - 65.41666666666666 interdiction[N02,exit01] >= -65.41666666666666
 flow_upper[N02,N04]: - flow[N02,N04]
   - 65.41666666666666 interdiction[N02,N04] >= -65.41666666666666
 flow_upper[N03,N04]: - flow[N03,N04]
   - 65.41666666666666 interdiction[N03,N04] >= -65.41666666666666
 flow_upper[N05,exit02]: - flow[N05,exit02]
   - 65.41666666666666 interdiction[N05,exit02] >= -65.41666666666666
 flow_upper[N05,exit03]: - flow[N05,exit03]
   - 65.41666666666666 interdiction[N05,exit03] >= -65.41666666666666
 flow_upper[entry03,N01]: - flow[entry03,N01]
   - 65.41666666666666 interdiction[entry03,N01] >= -65.41666666666666
 flow_upper[N04,N05]: - flow[N04,N05]
   - 65.41666666666666 interdiction[N04,N05] >= -65.41666666666666
 flow_upper[N01,N03]: - flow[N01,N03]
   - 65.41666666666666 interdiction[N01,N03] >= -65.41666666666666
 WCcheck_constraints[N01]: WCcheckFlow[N01,N02] - WCcheckFlow[entry03,N01]
   + WCcheckFlow[N01,N03] = -1
 WCcheck_constraints[N02]: - WCcheckFlow[N01,N02] + WCcheckFlow[N02,exit01]
   + WCcheckFlow[N02,N04] = -1
 WCcheck_constraints[N03]: - WCcheckFlow[entry02,N03]
   + WCcheckFlow[N03,N04] - WCcheckFlow[N01,N03] = -1
 WCcheck_constraints[N04]: - WCcheckFlow[N02,N04] - WCcheckFlow[N03,N04]
   + WCcheckFlow[N04,N05] = -1
 WCcheck_constraints[N05]: WCcheckFlow[N05,exit02]
   + WCcheckFlow[N05,exit03] - WCcheckFlow[N04,N05] = -1
 WCcheck_constraints[entry01]: WCcheckFlow[entry01,entry03] = 10
 WCcheck_constraints[entry03]: - WCcheckFlow[entry01,entry03]
   + WCcheckFlow[entry03,N01] = -1
 WCcheck_constraints[entry02]: WCcheckFlow[entry02,N03] = -1
 WCcheck_constraints[exit01]: - WCcheckFlow[N02,exit01] = -1
 WCcheck_constraints[exit02]: - WCcheckFlow[N05,exit02] = -1
 WCcheck_constraints[exit03]: - WCcheckFlow[N05,exit03] = -1
 R66: interdiction[entry01,entry03] + interdiction[N01,N02]
   + interdiction[entry02,N03] + interdiction[N02,exit01]
   + interdiction[N02,N04] + interdiction[N03,N04]
   + interdiction[N05,exit02] + interdiction[N05,exit03]
   + interdiction[entry03,N01] + interdiction[N04,N05]
   + interdiction[N01,N03] <= 3
 interdiction_fixation[entry01,entry03]: interdiction[entry01,entry03] = 1
 interdiction_fixation[N01,N02]: interdiction[N01,N02] = 1
 interdiction_fixation[entry02,N03]: interdiction[entry02,N03] = 0
 interdiction_fixation[N02,exit01]: interdiction[N02,exit01] = 1
 interdiction_fixation[N02,N04]: interdiction[N02,N04] = 0
 interdiction_fixation[N03,N04]: interdiction[N03,N04] = 0
 interdiction_fixation[N05,exit02]: interdiction[N05,exit02] = 0
 interdiction_fixation[N05,exit03]: interdiction[N05,exit03] = 0
 interdiction_fixation[entry03,N01]: interdiction[entry03,N01] = 0
 interdiction_fixation[N04,N05]: interdiction[N04,N05] = 0
 interdiction_fixation[N01,N03]: interdiction[N01,N03] = 0
 qc0: [ interdiction[entry01,entry03] * WCcheckFlow[entry01,entry03] ] = 0
 qc1: [ interdiction[N01,N02] * WCcheckFlow[N01,N02] ] = 0
 qc2: [ interdiction[entry02,N03] * WCcheckFlow[entry02,N03] ] = 0
 qc3: [ interdiction[N02,exit01] * WCcheckFlow[N02,exit01] ] = 0
 qc4: [ interdiction[N02,N04] * WCcheckFlow[N02,N04] ] = 0
 qc5: [ interdiction[N03,N04] * WCcheckFlow[N03,N04] ] = 0
 qc6: [ interdiction[N05,exit02] * WCcheckFlow[N05,exit02] ] = 0
 qc7: [ interdiction[N05,exit03] * WCcheckFlow[N05,exit03] ] = 0
 qc8: [ interdiction[entry03,N01] * WCcheckFlow[entry03,N01] ] = 0
 qc9: [ interdiction[N04,N05] * WCcheckFlow[N04,N05] ] = 0
 qc10: [ interdiction[N01,N03] * WCcheckFlow[N01,N03] ] = 0
Bounds
 loadshed[N01] = 0
 loadshed[N02] = 0
 loadshed[N03] = 0
 loadshed[N04] = 0
 loadshed[N05] = 0
 -3.6875 <= loadshed[entry01] <= 1
 loadshed[entry03] <= 1
 -2.571428571428571 <= loadshed[entry02] <= 1
 loadshed[exit01] <= 1
 loadshed[exit02] <= 1
 loadshed[exit03] <= 1
 flow[entry01,entry03] free
 flow[N01,N02] free
 flow[entry02,N03] free
 flow[N02,exit01] free
 flow[N02,N04] free
 flow[N03,N04] free
 flow[N05,exit02] free
 flow[N05,exit03] free
 flow[entry03,N01] free
 flow[N04,N05] free
 flow[N01,N03] free
 40 <= pressure[N01] <= 70
 40 <= pressure[N02] <= 70
 40 <= pressure[N03] <= 70
 40 <= pressure[N04] <= 70
 40 <= pressure[N05] <= 70
 40 <= pressure[entry01] <= 70
 40 <= pressure[entry03] <= 70
 40 <= pressure[entry02] <= 70
 40 <= pressure[exit01] <= 70
 40 <= pressure[exit02] <= 60
 40 <= pressure[exit03] <= 60
 WCcheckFlow[entry01,entry03] free
 WCcheckFlow[N01,N02] free
 WCcheckFlow[entry02,N03] free
 WCcheckFlow[N02,exit01] free
 WCcheckFlow[N02,N04] free
 WCcheckFlow[N03,N04] free
 WCcheckFlow[N05,exit02] free
 WCcheckFlow[N05,exit03] free
 WCcheckFlow[entry03,N01] free
 WCcheckFlow[N04,N05] free
 WCcheckFlow[N01,N03] free
Binaries
 interdiction[entry01,entry03] interdiction[N01,N02]
 interdiction[entry02,N03] interdiction[N02,exit01] interdiction[N02,N04]
 interdiction[N03,N04] interdiction[N05,exit02] interdiction[N05,exit03]
 interdiction[entry03,N01] interdiction[N04,N05] interdiction[N01,N03]
End
