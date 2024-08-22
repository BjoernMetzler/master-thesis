\ Model GasLib-11
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  0 loadshed[N01] + 0 loadshed[N02] + 0 loadshed[N03] + 0 loadshed[N04]
   + 0 loadshed[N05] + 21.80555555555556 loadshed[exit01]
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
 EnNdfC[entry01]: - dual_loadshed_entry_lower[entry01]
   + dual_loadshed_entry_upper[entry01]
   - 34.88888888888889 dual_flowConservation[entry01] = 0
 EnNdfC[entry03]: - dual_loadshed_entry_lower[entry03]
   + dual_loadshed_entry_upper[entry03] = 0
 EnNdfC[entry02]: - dual_loadshed_entry_lower[entry02]
   + dual_loadshed_entry_upper[entry02]
   - 30.52777777777778 dual_flowConservation[entry02] = 0
 ExNdfC[exit01]: - dual_loadshed_exit_lower[exit01]
   + dual_loadshed_exit_upper[exit01]
   + 21.80555555555556 dual_flowConservation[exit01] = -21.80555555555556
 ExNdfC[exit02]: - dual_loadshed_exit_lower[exit02]
   + dual_loadshed_exit_upper[exit02]
   + 26.16666666666667 dual_flowConservation[exit02] = -26.16666666666667
 ExNdfC[exit03]: - dual_loadshed_exit_lower[exit03]
   + dual_loadshed_exit_upper[exit03]
   + 17.44444444444444 dual_flowConservation[exit03] = -17.44444444444444
 ArcdfC[entry01,entry03]: - dual_flow_lower[entry01,entry03]
   + dual_flow_upper[entry01,entry03]
   + 0.5660644491026487 dual_PDAI_lower[entry01,entry03]
   - 0.5660644491026487 dual_PDAI_upper[entry01,entry03]
   - dual_flowConservation[entry01] + dual_flowConservation[entry03] = 0
 ArcdfC[N01,N02]: - dual_flow_lower[N01,N02] + dual_flow_upper[N01,N02]
   + 0.5660644491026487 dual_PDAI_lower[N01,N02]
   - 0.5660644491026487 dual_PDAI_upper[N01,N02]
   - dual_flowConservation[N01] + dual_flowConservation[N02] = 0
 ArcdfC[entry02,N03]: - dual_flow_lower[entry02,N03]
   + dual_flow_upper[entry02,N03]
   + 0.5660644491026487 dual_PDAI_lower[entry02,N03]
   - 0.5660644491026487 dual_PDAI_upper[entry02,N03]
   + dual_flowConservation[N03] - dual_flowConservation[entry02] = 0
 ArcdfC[N02,exit01]: - dual_flow_lower[N02,exit01]
   + dual_flow_upper[N02,exit01]
   + 0.5660644491026487 dual_PDAI_lower[N02,exit01]
   - 0.5660644491026487 dual_PDAI_upper[N02,exit01]
   - dual_flowConservation[N02] + dual_flowConservation[exit01] = 0
 ArcdfC[N02,N04]: - dual_flow_lower[N02,N04] + dual_flow_upper[N02,N04]
   + 0.5660644491026487 dual_PDAI_lower[N02,N04]
   - 0.5660644491026487 dual_PDAI_upper[N02,N04]
   - dual_flowConservation[N02] + dual_flowConservation[N04] = 0
 ArcdfC[N03,N04]: - dual_flow_lower[N03,N04] + dual_flow_upper[N03,N04]
   + 0.5660644491026487 dual_PDAI_lower[N03,N04]
   - 0.5660644491026487 dual_PDAI_upper[N03,N04]
   - dual_flowConservation[N03] + dual_flowConservation[N04] = 0
 ArcdfC[N05,exit02]: - dual_flow_lower[N05,exit02]
   + dual_flow_upper[N05,exit02]
   + 0.5731961978256868 dual_PDAI_lower[N05,exit02]
   - 0.5731961978256868 dual_PDAI_upper[N05,exit02]
   - dual_flowConservation[N05] + dual_flowConservation[exit02] = 0
 ArcdfC[N05,exit03]: - dual_flow_lower[N05,exit03]
   + dual_flow_upper[N05,exit03]
   + 0.5731961978256868 dual_PDAI_lower[N05,exit03]
   - 0.5731961978256868 dual_PDAI_upper[N05,exit03]
   - dual_flowConservation[N05] + dual_flowConservation[exit03] = 0
 ArcdfC[entry03,N01]: - dual_flow_lower[entry03,N01]
   + dual_flow_upper[entry03,N01] + dual_flowConservation[N01]
   - dual_flowConservation[entry03] = 0
 ArcdfC[N04,N05]: - dual_flow_lower[N04,N05] + dual_flow_upper[N04,N05]
   - dual_flowConservation[N04] + dual_flowConservation[N05] = 0
 ArcdfC[N01,N03]: - dual_flow_lower[N01,N03] + dual_flow_upper[N01,N03]
   - dual_flowConservation[N01] + dual_flowConservation[N03] = 0
 NodedfC[N01]: - dual_PDAI_lower[N01,N02] + dual_PDAI_lower[entry03,N01]
   - dual_PDAI_lower[N01,N03] + dual_PDAI_upper[N01,N02]
   - dual_PDAI_upper[entry03,N01] + dual_PDAI_upper[N01,N03]
   - dual_pressure_lower[N01] + dual_pressure_upper[N01] = 0
 NodedfC[N02]: dual_PDAI_lower[N01,N02] - dual_PDAI_lower[N02,exit01]
   - dual_PDAI_lower[N02,N04] - dual_PDAI_upper[N01,N02]
   + dual_PDAI_upper[N02,exit01] + dual_PDAI_upper[N02,N04]
   - dual_pressure_lower[N02] + dual_pressure_upper[N02] = 0
 NodedfC[N03]: dual_PDAI_lower[entry02,N03] - dual_PDAI_lower[N03,N04]
   + dual_PDAI_lower[N01,N03] - dual_PDAI_upper[entry02,N03]
   + dual_PDAI_upper[N03,N04] - dual_PDAI_upper[N01,N03]
   - dual_pressure_lower[N03] + dual_pressure_upper[N03] = 0
 NodedfC[N04]: dual_PDAI_lower[N02,N04] + dual_PDAI_lower[N03,N04]
   - dual_PDAI_lower[N04,N05] - dual_PDAI_upper[N02,N04]
   - dual_PDAI_upper[N03,N04] + dual_PDAI_upper[N04,N05]
   - dual_pressure_lower[N04] + dual_pressure_upper[N04] = 0
 NodedfC[N05]: - dual_PDAI_lower[N05,exit02] - dual_PDAI_lower[N05,exit03]
   + dual_PDAI_lower[N04,N05] + dual_PDAI_upper[N05,exit02]
   + dual_PDAI_upper[N05,exit03] - dual_PDAI_upper[N04,N05]
   - dual_pressure_lower[N05] + dual_pressure_upper[N05] = 0
 NodedfC[entry01]: - dual_PDAI_lower[entry01,entry03]
   + dual_PDAI_upper[entry01,entry03] - dual_pressure_lower[entry01]
   + dual_pressure_upper[entry01] = 0
 NodedfC[entry03]: dual_PDAI_lower[entry01,entry03]
   - dual_PDAI_lower[entry03,N01] - dual_PDAI_upper[entry01,entry03]
   + dual_PDAI_upper[entry03,N01] - dual_pressure_lower[entry03]
   + dual_pressure_upper[entry03] = 0
 NodedfC[entry02]: - dual_PDAI_lower[entry02,N03]
   + dual_PDAI_upper[entry02,N03] - dual_pressure_lower[entry02]
   + dual_pressure_upper[entry02] = 0
 NodedfC[exit01]: dual_PDAI_lower[N02,exit01] - dual_PDAI_upper[N02,exit01]
   - dual_pressure_lower[exit01] + dual_pressure_upper[exit01] = 0
 NodedfC[exit02]: dual_PDAI_lower[N05,exit02] - dual_PDAI_upper[N05,exit02]
   - dual_pressure_lower[exit02] + dual_pressure_upper[exit02] = 0
 NodedfC[exit03]: dual_PDAI_lower[N05,exit03] - dual_PDAI_upper[N05,exit03]
   - dual_pressure_lower[exit03] + dual_pressure_upper[exit03] = 0
 R83: dual_flowConservation[N01] <= 1
 R84: dual_flowConservation[N02] <= 1
 R85: dual_flowConservation[N03] <= 1
 R86: dual_flowConservation[N04] <= 1
 R87: dual_flowConservation[N05] <= 1
 R88: dual_flowConservation[entry01] <= 1
 R89: dual_flowConservation[entry03] <= 1
 R90: dual_flowConservation[entry02] <= 1
 R91: dual_flowConservation[exit01] <= 1
 R92: dual_flowConservation[exit02] <= 1
 R93: dual_flowConservation[exit03] <= 1
 R94: dual_flowConservation[N01] >= -1
 R95: dual_flowConservation[N02] >= -1
 R96: dual_flowConservation[N03] >= -1
 R97: dual_flowConservation[N04] >= -1
 R98: dual_flowConservation[N05] >= -1
 R99: dual_flowConservation[entry01] >= -1
 R100: dual_flowConservation[entry03] >= -1
 R101: dual_flowConservation[entry02] >= -1
 R102: dual_flowConservation[exit01] >= -1
 R103: dual_flowConservation[exit02] >= -1
 R104: dual_flowConservation[exit03] >= -1
 UB_bigM_for__dual_flow_var_at_arcs_lower[entry01,entry03]:
   dual_flow_lower[entry01,entry03]
   - binary_var_for__dual_flow_var_at_arcs_lower[entry01,entry03] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_lower[N01,N02]:
   dual_flow_lower[N01,N02]
   - binary_var_for__dual_flow_var_at_arcs_lower[N01,N02] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_lower[entry02,N03]:
   dual_flow_lower[entry02,N03]
   - binary_var_for__dual_flow_var_at_arcs_lower[entry02,N03] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_lower[N02,exit01]:
   dual_flow_lower[N02,exit01]
   - binary_var_for__dual_flow_var_at_arcs_lower[N02,exit01] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_lower[N02,N04]:
   dual_flow_lower[N02,N04]
   - binary_var_for__dual_flow_var_at_arcs_lower[N02,N04] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_lower[N03,N04]:
   dual_flow_lower[N03,N04]
   - binary_var_for__dual_flow_var_at_arcs_lower[N03,N04] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_lower[N05,exit02]:
   dual_flow_lower[N05,exit02]
   - binary_var_for__dual_flow_var_at_arcs_lower[N05,exit02] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_lower[N05,exit03]:
   dual_flow_lower[N05,exit03]
   - binary_var_for__dual_flow_var_at_arcs_lower[N05,exit03] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_lower[entry03,N01]:
   dual_flow_lower[entry03,N01]
   - binary_var_for__dual_flow_var_at_arcs_lower[entry03,N01] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_lower[N04,N05]:
   dual_flow_lower[N04,N05]
   - binary_var_for__dual_flow_var_at_arcs_lower[N04,N05] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_lower[N01,N03]:
   dual_flow_lower[N01,N03]
   - binary_var_for__dual_flow_var_at_arcs_lower[N01,N03] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_upper[entry01,entry03]:
   dual_flow_upper[entry01,entry03]
   - binary_var_for__dual_flow_var_at_arcs_upper[entry01,entry03] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_upper[N01,N02]:
   dual_flow_upper[N01,N02]
   - binary_var_for__dual_flow_var_at_arcs_upper[N01,N02] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_upper[entry02,N03]:
   dual_flow_upper[entry02,N03]
   - binary_var_for__dual_flow_var_at_arcs_upper[entry02,N03] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_upper[N02,exit01]:
   dual_flow_upper[N02,exit01]
   - binary_var_for__dual_flow_var_at_arcs_upper[N02,exit01] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_upper[N02,N04]:
   dual_flow_upper[N02,N04]
   - binary_var_for__dual_flow_var_at_arcs_upper[N02,N04] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_upper[N03,N04]:
   dual_flow_upper[N03,N04]
   - binary_var_for__dual_flow_var_at_arcs_upper[N03,N04] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_upper[N05,exit02]:
   dual_flow_upper[N05,exit02]
   - binary_var_for__dual_flow_var_at_arcs_upper[N05,exit02] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_upper[N05,exit03]:
   dual_flow_upper[N05,exit03]
   - binary_var_for__dual_flow_var_at_arcs_upper[N05,exit03] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_upper[entry03,N01]:
   dual_flow_upper[entry03,N01]
   - binary_var_for__dual_flow_var_at_arcs_upper[entry03,N01] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_upper[N04,N05]:
   dual_flow_upper[N04,N05]
   - binary_var_for__dual_flow_var_at_arcs_upper[N04,N05] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_upper[N01,N03]:
   dual_flow_upper[N01,N03]
   - binary_var_for__dual_flow_var_at_arcs_upper[N01,N03] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_lower[entry01,entry03]:
   dual_PDAI_lower[entry01,entry03]
   - 1e+100 binary_var_for__dual_PDAI_var_at_arcs_lower[entry01,entry03]
   <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_lower[N01,N02]:
   dual_PDAI_lower[N01,N02]
   - 1e+100 binary_var_for__dual_PDAI_var_at_arcs_lower[N01,N02] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_lower[entry02,N03]:
   dual_PDAI_lower[entry02,N03]
   - 1e+100 binary_var_for__dual_PDAI_var_at_arcs_lower[entry02,N03] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_lower[N02,exit01]:
   dual_PDAI_lower[N02,exit01]
   - 1e+100 binary_var_for__dual_PDAI_var_at_arcs_lower[N02,exit01] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_lower[N02,N04]:
   dual_PDAI_lower[N02,N04]
   - 1e+100 binary_var_for__dual_PDAI_var_at_arcs_lower[N02,N04] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_lower[N03,N04]:
   dual_PDAI_lower[N03,N04]
   - 1e+100 binary_var_for__dual_PDAI_var_at_arcs_lower[N03,N04] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_lower[N05,exit02]:
   dual_PDAI_lower[N05,exit02]
   - 1e+100 binary_var_for__dual_PDAI_var_at_arcs_lower[N05,exit02] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_lower[N05,exit03]:
   dual_PDAI_lower[N05,exit03]
   - 1e+100 binary_var_for__dual_PDAI_var_at_arcs_lower[N05,exit03] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_lower[entry03,N01]:
   dual_PDAI_lower[entry03,N01]
   - 1e+100 binary_var_for__dual_PDAI_var_at_arcs_lower[entry03,N01] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_lower[N04,N05]:
   dual_PDAI_lower[N04,N05]
   - 1e+100 binary_var_for__dual_PDAI_var_at_arcs_lower[N04,N05] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_lower[N01,N03]:
   dual_PDAI_lower[N01,N03]
   - 1e+100 binary_var_for__dual_PDAI_var_at_arcs_lower[N01,N03] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_upper[entry01,entry03]:
   dual_PDAI_upper[entry01,entry03]
   - 1e+100 binary_var_for__dual_PDAI_var_at_arcs_upper[entry01,entry03]
   <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_upper[N01,N02]:
   dual_PDAI_upper[N01,N02]
   - 1e+100 binary_var_for__dual_PDAI_var_at_arcs_upper[N01,N02] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_upper[entry02,N03]:
   dual_PDAI_upper[entry02,N03]
   - 1e+100 binary_var_for__dual_PDAI_var_at_arcs_upper[entry02,N03] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_upper[N02,exit01]:
   dual_PDAI_upper[N02,exit01]
   - 1e+100 binary_var_for__dual_PDAI_var_at_arcs_upper[N02,exit01] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_upper[N02,N04]:
   dual_PDAI_upper[N02,N04]
   - 1e+100 binary_var_for__dual_PDAI_var_at_arcs_upper[N02,N04] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_upper[N03,N04]:
   dual_PDAI_upper[N03,N04]
   - 1e+100 binary_var_for__dual_PDAI_var_at_arcs_upper[N03,N04] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_upper[N05,exit02]:
   dual_PDAI_upper[N05,exit02]
   - 1e+100 binary_var_for__dual_PDAI_var_at_arcs_upper[N05,exit02] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_upper[N05,exit03]:
   dual_PDAI_upper[N05,exit03]
   - 1e+100 binary_var_for__dual_PDAI_var_at_arcs_upper[N05,exit03] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_upper[entry03,N01]:
   dual_PDAI_upper[entry03,N01]
   - 1e+100 binary_var_for__dual_PDAI_var_at_arcs_upper[entry03,N01] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_upper[N04,N05]:
   dual_PDAI_upper[N04,N05]
   - 1e+100 binary_var_for__dual_PDAI_var_at_arcs_upper[N04,N05] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_upper[N01,N03]:
   dual_PDAI_upper[N01,N03]
   - 1e+100 binary_var_for__dual_PDAI_var_at_arcs_upper[N01,N03] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_lower[N01]:
   dual_pressure_lower[N01]
   - 3e+100 binary_var_for__dual_pressure_var_at_nodes_lower[N01] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_lower[N02]:
   dual_pressure_lower[N02]
   - 3e+100 binary_var_for__dual_pressure_var_at_nodes_lower[N02] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_lower[N03]:
   dual_pressure_lower[N03]
   - 3e+100 binary_var_for__dual_pressure_var_at_nodes_lower[N03] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_lower[N04]:
   dual_pressure_lower[N04]
   - 3e+100 binary_var_for__dual_pressure_var_at_nodes_lower[N04] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_lower[N05]:
   dual_pressure_lower[N05]
   - 3e+100 binary_var_for__dual_pressure_var_at_nodes_lower[N05] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_lower[entry01]:
   dual_pressure_lower[entry01]
   - 3e+100 binary_var_for__dual_pressure_var_at_nodes_lower[entry01] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_lower[entry03]:
   dual_pressure_lower[entry03]
   - 3e+100 binary_var_for__dual_pressure_var_at_nodes_lower[entry03] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_lower[entry02]:
   dual_pressure_lower[entry02]
   - 3e+100 binary_var_for__dual_pressure_var_at_nodes_lower[entry02] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_lower[exit01]:
   dual_pressure_lower[exit01]
   - 3e+100 binary_var_for__dual_pressure_var_at_nodes_lower[exit01] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_lower[exit02]:
   dual_pressure_lower[exit02]
   - 3e+100 binary_var_for__dual_pressure_var_at_nodes_lower[exit02] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_lower[exit03]:
   dual_pressure_lower[exit03]
   - 3e+100 binary_var_for__dual_pressure_var_at_nodes_lower[exit03] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_upper[N01]:
   dual_pressure_upper[N01]
   - 3e+100 binary_var_for__dual_pressure_var_at_nodes_upper[N01] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_upper[N02]:
   dual_pressure_upper[N02]
   - 3e+100 binary_var_for__dual_pressure_var_at_nodes_upper[N02] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_upper[N03]:
   dual_pressure_upper[N03]
   - 3e+100 binary_var_for__dual_pressure_var_at_nodes_upper[N03] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_upper[N04]:
   dual_pressure_upper[N04]
   - 3e+100 binary_var_for__dual_pressure_var_at_nodes_upper[N04] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_upper[N05]:
   dual_pressure_upper[N05]
   - 3e+100 binary_var_for__dual_pressure_var_at_nodes_upper[N05] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_upper[entry01]:
   dual_pressure_upper[entry01]
   - 3e+100 binary_var_for__dual_pressure_var_at_nodes_upper[entry01] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_upper[entry03]:
   dual_pressure_upper[entry03]
   - 3e+100 binary_var_for__dual_pressure_var_at_nodes_upper[entry03] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_upper[entry02]:
   dual_pressure_upper[entry02]
   - 3e+100 binary_var_for__dual_pressure_var_at_nodes_upper[entry02] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_upper[exit01]:
   dual_pressure_upper[exit01]
   - 3e+100 binary_var_for__dual_pressure_var_at_nodes_upper[exit01] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_upper[exit02]:
   dual_pressure_upper[exit02]
   - 3e+100 binary_var_for__dual_pressure_var_at_nodes_upper[exit02] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_upper[exit03]:
   dual_pressure_upper[exit03]
   - 3e+100 binary_var_for__dual_pressure_var_at_nodes_upper[exit03] <= 0
 UB_bigM_for__dual_loadshed_var_at_exit_nodes_lower[exit01]:
   dual_loadshed_exit_lower[exit01]
   - 69.77777777777777 binary_var_for__dual_loadshed_var_at_exit_nodes_lower[exit01]
   <= 0
 UB_bigM_for__dual_loadshed_var_at_exit_nodes_lower[exit02]:
   dual_loadshed_exit_lower[exit02]
   - 69.77777777777777 binary_var_for__dual_loadshed_var_at_exit_nodes_lower[exit02]
   <= 0
 UB_bigM_for__dual_loadshed_var_at_exit_nodes_lower[exit03]:
   dual_loadshed_exit_lower[exit03]
   - 69.77777777777777 binary_var_for__dual_loadshed_var_at_exit_nodes_lower[exit03]
   <= 0
 UB_bigM_for__dual_loadshed_var_at_exit_nodes_upper[exit01]:
   dual_loadshed_exit_upper[exit01]
   - 69.77777777777777 binary_var_for__dual_loadshed_var_at_exit_nodes_upper[exit01]
   <= 0
 UB_bigM_for__dual_loadshed_var_at_exit_nodes_upper[exit02]:
   dual_loadshed_exit_upper[exit02]
   - 69.77777777777777 binary_var_for__dual_loadshed_var_at_exit_nodes_upper[exit02]
   <= 0
 UB_bigM_for__dual_loadshed_var_at_exit_nodes_upper[exit03]:
   dual_loadshed_exit_upper[exit03]
   - 69.77777777777777 binary_var_for__dual_loadshed_var_at_exit_nodes_upper[exit03]
   <= 0
 UB_bigM_for__dual_loadshed_var_at_entry_nodes_lower[entry01]:
   dual_loadshed_entry_lower[entry01]
   - 34.88888888888889 binary_var_for__dual_loadshed_var_at_entry_nodes_lower[entry01]
   <= 0
 UB_bigM_for__dual_loadshed_var_at_entry_nodes_lower[entry03]:
   dual_loadshed_entry_lower[entry03]
   - 34.88888888888889 binary_var_for__dual_loadshed_var_at_entry_nodes_lower[entry03]
   <= 0
 UB_bigM_for__dual_loadshed_var_at_entry_nodes_lower[entry02]:
   dual_loadshed_entry_lower[entry02]
   - 34.88888888888889 binary_var_for__dual_loadshed_var_at_entry_nodes_lower[entry02]
   <= 0
 UB_bigM_for__dual_loadshed_var_at_entry_nodes_upper[entry01]:
   dual_loadshed_entry_upper[entry01]
   - 34.88888888888889 binary_var_for__dual_loadshed_var_at_entry_nodes_upper[entry01]
   <= 0
 UB_bigM_for__dual_loadshed_var_at_entry_nodes_upper[entry03]:
   dual_loadshed_entry_upper[entry03]
   - 34.88888888888889 binary_var_for__dual_loadshed_var_at_entry_nodes_upper[entry03]
   <= 0
 UB_bigM_for__dual_loadshed_var_at_entry_nodes_upper[entry02]:
   dual_loadshed_entry_upper[entry02]
   - 34.88888888888889 binary_var_for__dual_loadshed_var_at_entry_nodes_upper[entry02]
   <= 0
 UB_for__flow_var_at_arcs_lower[entry01,entry03]: flow[entry01,entry03]
   - 65.41666666666666 interdiction[entry01,entry03]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_lower[entry01,entry03]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_lower[N01,N02]: flow[N01,N02]
   - 65.41666666666666 interdiction[N01,N02]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_lower[N01,N02]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_lower[entry02,N03]: flow[entry02,N03]
   - 65.41666666666666 interdiction[entry02,N03]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_lower[entry02,N03]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_lower[N02,exit01]: flow[N02,exit01]
   - 65.41666666666666 interdiction[N02,exit01]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_lower[N02,exit01]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_lower[N02,N04]: flow[N02,N04]
   - 65.41666666666666 interdiction[N02,N04]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_lower[N02,N04]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_lower[N03,N04]: flow[N03,N04]
   - 65.41666666666666 interdiction[N03,N04]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_lower[N03,N04]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_lower[N05,exit02]: flow[N05,exit02]
   - 65.41666666666666 interdiction[N05,exit02]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_lower[N05,exit02]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_lower[N05,exit03]: flow[N05,exit03]
   - 65.41666666666666 interdiction[N05,exit03]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_lower[N05,exit03]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_lower[entry03,N01]: flow[entry03,N01]
   - 65.41666666666666 interdiction[entry03,N01]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_lower[entry03,N01]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_lower[N04,N05]: flow[N04,N05]
   - 65.41666666666666 interdiction[N04,N05]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_lower[N04,N05]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_lower[N01,N03]: flow[N01,N03]
   - 65.41666666666666 interdiction[N01,N03]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_lower[N01,N03]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_upper[entry01,entry03]: - flow[entry01,entry03]
   - 65.41666666666666 interdiction[entry01,entry03]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_upper[entry01,entry03]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_upper[N01,N02]: - flow[N01,N02]
   - 65.41666666666666 interdiction[N01,N02]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_upper[N01,N02]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_upper[entry02,N03]: - flow[entry02,N03]
   - 65.41666666666666 interdiction[entry02,N03]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_upper[entry02,N03]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_upper[N02,exit01]: - flow[N02,exit01]
   - 65.41666666666666 interdiction[N02,exit01]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_upper[N02,exit01]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_upper[N02,N04]: - flow[N02,N04]
   - 65.41666666666666 interdiction[N02,N04]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_upper[N02,N04]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_upper[N03,N04]: - flow[N03,N04]
   - 65.41666666666666 interdiction[N03,N04]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_upper[N03,N04]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_upper[N05,exit02]: - flow[N05,exit02]
   - 65.41666666666666 interdiction[N05,exit02]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_upper[N05,exit02]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_upper[N05,exit03]: - flow[N05,exit03]
   - 65.41666666666666 interdiction[N05,exit03]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_upper[N05,exit03]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_upper[entry03,N01]: - flow[entry03,N01]
   - 65.41666666666666 interdiction[entry03,N01]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_upper[entry03,N01]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_upper[N04,N05]: - flow[N04,N05]
   - 65.41666666666666 interdiction[N04,N05]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_upper[N04,N05]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_upper[N01,N03]: - flow[N01,N03]
   - 65.41666666666666 interdiction[N01,N03]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_upper[N01,N03]
   <= 65.41666666666666
 UB_for__PDAI_var_at_arcs_lower[entry01,entry03]:
   - 0.5660644491026487 flow[entry01,entry03] + pressure[entry01]
   - pressure[entry03] + 30 interdiction[entry01,entry03]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_lower[entry01,entry03] <= 60
 UB_for__PDAI_var_at_arcs_lower[N01,N02]:
   - 0.5660644491026487 flow[N01,N02] + pressure[N01] - pressure[N02]
   + 30 interdiction[N01,N02]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_lower[N01,N02] <= 60
 UB_for__PDAI_var_at_arcs_lower[entry02,N03]:
   - 0.5660644491026487 flow[entry02,N03] - pressure[N03]
   + pressure[entry02] + 30 interdiction[entry02,N03]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_lower[entry02,N03] <= 60
 UB_for__PDAI_var_at_arcs_lower[N02,exit01]:
   - 0.5660644491026487 flow[N02,exit01] + pressure[N02] - pressure[exit01]
   + 30 interdiction[N02,exit01]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_lower[N02,exit01] <= 60
 UB_for__PDAI_var_at_arcs_lower[N02,N04]:
   - 0.5660644491026487 flow[N02,N04] + pressure[N02] - pressure[N04]
   + 30 interdiction[N02,N04]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_lower[N02,N04] <= 60
 UB_for__PDAI_var_at_arcs_lower[N03,N04]:
   - 0.5660644491026487 flow[N03,N04] + pressure[N03] - pressure[N04]
   + 30 interdiction[N03,N04]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_lower[N03,N04] <= 60
 UB_for__PDAI_var_at_arcs_lower[N05,exit02]:
   - 0.5731961978256868 flow[N05,exit02] + pressure[N05] - pressure[exit02]
   + 20 interdiction[N05,exit02]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_lower[N05,exit02] <= 60
 UB_for__PDAI_var_at_arcs_lower[N05,exit03]:
   - 0.5731961978256868 flow[N05,exit03] + pressure[N05] - pressure[exit03]
   + 20 interdiction[N05,exit03]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_lower[N05,exit03] <= 60
 UB_for__PDAI_var_at_arcs_lower[entry03,N01]: - pressure[N01]
   + pressure[entry03] + 30 interdiction[entry03,N01]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_lower[entry03,N01] <= 60
 UB_for__PDAI_var_at_arcs_lower[N04,N05]: pressure[N04] - pressure[N05]
   + 30 interdiction[N04,N05]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_lower[N04,N05] <= 60
 UB_for__PDAI_var_at_arcs_lower[N01,N03]: pressure[N01] - pressure[N03]
   + 30 interdiction[N01,N03]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_lower[N01,N03] <= 60
 UB_for__PDAI_var_at_arcs_upper[entry01,entry03]:
   0.5660644491026487 flow[entry01,entry03] - pressure[entry01]
   + pressure[entry03] + 30 interdiction[entry01,entry03]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_upper[entry01,entry03] <= 60
 UB_for__PDAI_var_at_arcs_upper[N01,N02]: 0.5660644491026487 flow[N01,N02]
   - pressure[N01] + pressure[N02] + 30 interdiction[N01,N02]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_upper[N01,N02] <= 60
 UB_for__PDAI_var_at_arcs_upper[entry02,N03]:
   0.5660644491026487 flow[entry02,N03] + pressure[N03] - pressure[entry02]
   + 30 interdiction[entry02,N03]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_upper[entry02,N03] <= 60
 UB_for__PDAI_var_at_arcs_upper[N02,exit01]:
   0.5660644491026487 flow[N02,exit01] - pressure[N02] + pressure[exit01]
   + 30 interdiction[N02,exit01]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_upper[N02,exit01] <= 60
 UB_for__PDAI_var_at_arcs_upper[N02,N04]: 0.5660644491026487 flow[N02,N04]
   - pressure[N02] + pressure[N04] + 30 interdiction[N02,N04]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_upper[N02,N04] <= 60
 UB_for__PDAI_var_at_arcs_upper[N03,N04]: 0.5660644491026487 flow[N03,N04]
   - pressure[N03] + pressure[N04] + 30 interdiction[N03,N04]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_upper[N03,N04] <= 60
 UB_for__PDAI_var_at_arcs_upper[N05,exit02]:
   0.5731961978256868 flow[N05,exit02] - pressure[N05] + pressure[exit02]
   + 30 interdiction[N05,exit02]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_upper[N05,exit02] <= 60
 UB_for__PDAI_var_at_arcs_upper[N05,exit03]:
   0.5731961978256868 flow[N05,exit03] - pressure[N05] + pressure[exit03]
   + 30 interdiction[N05,exit03]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_upper[N05,exit03] <= 60
 UB_for__PDAI_var_at_arcs_upper[entry03,N01]: pressure[N01]
   - pressure[entry03] + 30 interdiction[entry03,N01]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_upper[entry03,N01] <= 60
 UB_for__PDAI_var_at_arcs_upper[N04,N05]: - pressure[N04] + pressure[N05]
   + 30 interdiction[N04,N05]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_upper[N04,N05] <= 60
 UB_for__PDAI_var_at_arcs_upper[N01,N03]: - pressure[N01] + pressure[N03]
   + 30 interdiction[N01,N03]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_upper[N01,N03] <= 60
 UB_for__pressure_var_at_nodes_lower[N01]: pressure[N01]
   + 30 binary_var_for__dual_pressure_var_at_nodes_lower[N01] <= 70
 UB_for__pressure_var_at_nodes_lower[N02]: pressure[N02]
   + 30 binary_var_for__dual_pressure_var_at_nodes_lower[N02] <= 70
 UB_for__pressure_var_at_nodes_lower[N03]: pressure[N03]
   + 30 binary_var_for__dual_pressure_var_at_nodes_lower[N03] <= 70
 UB_for__pressure_var_at_nodes_lower[N04]: pressure[N04]
   + 30 binary_var_for__dual_pressure_var_at_nodes_lower[N04] <= 70
 UB_for__pressure_var_at_nodes_lower[N05]: pressure[N05]
   + 30 binary_var_for__dual_pressure_var_at_nodes_lower[N05] <= 70
 UB_for__pressure_var_at_nodes_lower[entry01]: pressure[entry01]
   + 30 binary_var_for__dual_pressure_var_at_nodes_lower[entry01] <= 70
 UB_for__pressure_var_at_nodes_lower[entry03]: pressure[entry03]
   + 30 binary_var_for__dual_pressure_var_at_nodes_lower[entry03] <= 70
 UB_for__pressure_var_at_nodes_lower[entry02]: pressure[entry02]
   + 30 binary_var_for__dual_pressure_var_at_nodes_lower[entry02] <= 70
 UB_for__pressure_var_at_nodes_lower[exit01]: pressure[exit01]
   + 30 binary_var_for__dual_pressure_var_at_nodes_lower[exit01] <= 70
 UB_for__pressure_var_at_nodes_lower[exit02]: pressure[exit02]
   + 30 binary_var_for__dual_pressure_var_at_nodes_lower[exit02] <= 70
 UB_for__pressure_var_at_nodes_lower[exit03]: pressure[exit03]
   + 30 binary_var_for__dual_pressure_var_at_nodes_lower[exit03] <= 70
 UB_for__pressure_var_at_nodes_upper[N01]: - pressure[N01]
   + 30 binary_var_for__dual_pressure_var_at_nodes_upper[N01] <= -40
 UB_for__pressure_var_at_nodes_upper[N02]: - pressure[N02]
   + 30 binary_var_for__dual_pressure_var_at_nodes_upper[N02] <= -40
 UB_for__pressure_var_at_nodes_upper[N03]: - pressure[N03]
   + 30 binary_var_for__dual_pressure_var_at_nodes_upper[N03] <= -40
 UB_for__pressure_var_at_nodes_upper[N04]: - pressure[N04]
   + 30 binary_var_for__dual_pressure_var_at_nodes_upper[N04] <= -40
 UB_for__pressure_var_at_nodes_upper[N05]: - pressure[N05]
   + 30 binary_var_for__dual_pressure_var_at_nodes_upper[N05] <= -40
 UB_for__pressure_var_at_nodes_upper[entry01]: - pressure[entry01]
   + 30 binary_var_for__dual_pressure_var_at_nodes_upper[entry01] <= -40
 UB_for__pressure_var_at_nodes_upper[entry03]: - pressure[entry03]
   + 30 binary_var_for__dual_pressure_var_at_nodes_upper[entry03] <= -40
 UB_for__pressure_var_at_nodes_upper[entry02]: - pressure[entry02]
   + 30 binary_var_for__dual_pressure_var_at_nodes_upper[entry02] <= -40
 UB_for__pressure_var_at_nodes_upper[exit01]: - pressure[exit01]
   + 30 binary_var_for__dual_pressure_var_at_nodes_upper[exit01] <= -40
 UB_for__pressure_var_at_nodes_upper[exit02]: - pressure[exit02]
   + 30 binary_var_for__dual_pressure_var_at_nodes_upper[exit02] <= -30
 UB_for__pressure_var_at_nodes_upper[exit03]: - pressure[exit03]
   + 30 binary_var_for__dual_pressure_var_at_nodes_upper[exit03] <= -30
 UB_for__loadshed_var_at_exit_nodes_lower[exit01]: loadshed[exit01]
   + binary_var_for__dual_loadshed_var_at_exit_nodes_lower[exit01] <= 1
 UB_for__loadshed_var_at_exit_nodes_lower[exit02]: loadshed[exit02]
   + binary_var_for__dual_loadshed_var_at_exit_nodes_lower[exit02] <= 1
 UB_for__loadshed_var_at_exit_nodes_lower[exit03]: loadshed[exit03]
   + binary_var_for__dual_loadshed_var_at_exit_nodes_lower[exit03] <= 1
 UB_for__loadshed_var_at_exit_nodes_upper[exit01]: - loadshed[exit01]
   + binary_var_for__dual_loadshed_var_at_exit_nodes_upper[exit01] <= 0
 UB_for__loadshed_var_at_exit_nodes_upper[exit02]: - loadshed[exit02]
   + binary_var_for__dual_loadshed_var_at_exit_nodes_upper[exit02] <= 0
 UB_for__loadshed_var_at_exit_nodes_upper[exit03]: - loadshed[exit03]
   + binary_var_for__dual_loadshed_var_at_exit_nodes_upper[exit03] <= 0
 UB_for__loadshed_var_at_entry_nodes_lower[entry01]: loadshed[entry01]
   + 4.6875 binary_var_for__dual_loadshed_var_at_entry_nodes_lower[entry01]
   <= 1
 UB_for__loadshed_var_at_entry_nodes_lower[entry03]: loadshed[entry03]
   + 4.6875 binary_var_for__dual_loadshed_var_at_entry_nodes_lower[entry03]
   <= 4.6875
 UB_for__loadshed_var_at_entry_nodes_lower[entry02]: loadshed[entry02]
   + 4.6875 binary_var_for__dual_loadshed_var_at_entry_nodes_lower[entry02]
   <= 2.116071428571429
 UB_for__loadshed_var_at_entry_nodes_upper[entry01]: - loadshed[entry01]
   + 4.6875 binary_var_for__dual_loadshed_var_at_entry_nodes_upper[entry01]
   <= 3.6875
 UB_for__loadshed_var_at_entry_nodes_upper[entry03]: - loadshed[entry03]
   + 4.6875 binary_var_for__dual_loadshed_var_at_entry_nodes_upper[entry03]
   <= 3.6875
 UB_for__loadshed_var_at_entry_nodes_upper[entry02]: - loadshed[entry02]
   + 4.6875 binary_var_for__dual_loadshed_var_at_entry_nodes_upper[entry02]
   <= 3.6875
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
 R272: interdiction[entry01,entry03] + interdiction[N01,N02]
   + interdiction[entry02,N03] + interdiction[N02,exit01]
   + interdiction[N02,N04] + interdiction[N03,N04]
   + interdiction[N05,exit02] + interdiction[N05,exit03]
   + interdiction[entry03,N01] + interdiction[N04,N05]
   + interdiction[N01,N03] <= 1
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
 dual_flowConservation[N01] free
 dual_flowConservation[N02] free
 dual_flowConservation[N03] free
 dual_flowConservation[N04] free
 dual_flowConservation[N05] free
 dual_flowConservation[entry01] free
 dual_flowConservation[entry03] free
 dual_flowConservation[entry02] free
 dual_flowConservation[exit01] free
 dual_flowConservation[exit02] free
 dual_flowConservation[exit03] free
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
 binary_var_for__dual_flow_var_at_arcs_lower[entry01,entry03]
 binary_var_for__dual_flow_var_at_arcs_lower[N01,N02]
 binary_var_for__dual_flow_var_at_arcs_lower[entry02,N03]
 binary_var_for__dual_flow_var_at_arcs_lower[N02,exit01]
 binary_var_for__dual_flow_var_at_arcs_lower[N02,N04]
 binary_var_for__dual_flow_var_at_arcs_lower[N03,N04]
 binary_var_for__dual_flow_var_at_arcs_lower[N05,exit02]
 binary_var_for__dual_flow_var_at_arcs_lower[N05,exit03]
 binary_var_for__dual_flow_var_at_arcs_lower[entry03,N01]
 binary_var_for__dual_flow_var_at_arcs_lower[N04,N05]
 binary_var_for__dual_flow_var_at_arcs_lower[N01,N03]
 binary_var_for__dual_flow_var_at_arcs_upper[entry01,entry03]
 binary_var_for__dual_flow_var_at_arcs_upper[N01,N02]
 binary_var_for__dual_flow_var_at_arcs_upper[entry02,N03]
 binary_var_for__dual_flow_var_at_arcs_upper[N02,exit01]
 binary_var_for__dual_flow_var_at_arcs_upper[N02,N04]
 binary_var_for__dual_flow_var_at_arcs_upper[N03,N04]
 binary_var_for__dual_flow_var_at_arcs_upper[N05,exit02]
 binary_var_for__dual_flow_var_at_arcs_upper[N05,exit03]
 binary_var_for__dual_flow_var_at_arcs_upper[entry03,N01]
 binary_var_for__dual_flow_var_at_arcs_upper[N04,N05]
 binary_var_for__dual_flow_var_at_arcs_upper[N01,N03]
 binary_var_for__dual_PDAI_var_at_arcs_lower[entry01,entry03]
 binary_var_for__dual_PDAI_var_at_arcs_lower[N01,N02]
 binary_var_for__dual_PDAI_var_at_arcs_lower[entry02,N03]
 binary_var_for__dual_PDAI_var_at_arcs_lower[N02,exit01]
 binary_var_for__dual_PDAI_var_at_arcs_lower[N02,N04]
 binary_var_for__dual_PDAI_var_at_arcs_lower[N03,N04]
 binary_var_for__dual_PDAI_var_at_arcs_lower[N05,exit02]
 binary_var_for__dual_PDAI_var_at_arcs_lower[N05,exit03]
 binary_var_for__dual_PDAI_var_at_arcs_lower[entry03,N01]
 binary_var_for__dual_PDAI_var_at_arcs_lower[N04,N05]
 binary_var_for__dual_PDAI_var_at_arcs_lower[N01,N03]
 binary_var_for__dual_PDAI_var_at_arcs_upper[entry01,entry03]
 binary_var_for__dual_PDAI_var_at_arcs_upper[N01,N02]
 binary_var_for__dual_PDAI_var_at_arcs_upper[entry02,N03]
 binary_var_for__dual_PDAI_var_at_arcs_upper[N02,exit01]
 binary_var_for__dual_PDAI_var_at_arcs_upper[N02,N04]
 binary_var_for__dual_PDAI_var_at_arcs_upper[N03,N04]
 binary_var_for__dual_PDAI_var_at_arcs_upper[N05,exit02]
 binary_var_for__dual_PDAI_var_at_arcs_upper[N05,exit03]
 binary_var_for__dual_PDAI_var_at_arcs_upper[entry03,N01]
 binary_var_for__dual_PDAI_var_at_arcs_upper[N04,N05]
 binary_var_for__dual_PDAI_var_at_arcs_upper[N01,N03]
 binary_var_for__dual_pressure_var_at_nodes_lower[N01]
 binary_var_for__dual_pressure_var_at_nodes_lower[N02]
 binary_var_for__dual_pressure_var_at_nodes_lower[N03]
 binary_var_for__dual_pressure_var_at_nodes_lower[N04]
 binary_var_for__dual_pressure_var_at_nodes_lower[N05]
 binary_var_for__dual_pressure_var_at_nodes_lower[entry01]
 binary_var_for__dual_pressure_var_at_nodes_lower[entry03]
 binary_var_for__dual_pressure_var_at_nodes_lower[entry02]
 binary_var_for__dual_pressure_var_at_nodes_lower[exit01]
 binary_var_for__dual_pressure_var_at_nodes_lower[exit02]
 binary_var_for__dual_pressure_var_at_nodes_lower[exit03]
 binary_var_for__dual_pressure_var_at_nodes_upper[N01]
 binary_var_for__dual_pressure_var_at_nodes_upper[N02]
 binary_var_for__dual_pressure_var_at_nodes_upper[N03]
 binary_var_for__dual_pressure_var_at_nodes_upper[N04]
 binary_var_for__dual_pressure_var_at_nodes_upper[N05]
 binary_var_for__dual_pressure_var_at_nodes_upper[entry01]
 binary_var_for__dual_pressure_var_at_nodes_upper[entry03]
 binary_var_for__dual_pressure_var_at_nodes_upper[entry02]
 binary_var_for__dual_pressure_var_at_nodes_upper[exit01]
 binary_var_for__dual_pressure_var_at_nodes_upper[exit02]
 binary_var_for__dual_pressure_var_at_nodes_upper[exit03]
 binary_var_for__dual_loadshed_var_at_exit_nodes_lower[exit01]
 binary_var_for__dual_loadshed_var_at_exit_nodes_lower[exit02]
 binary_var_for__dual_loadshed_var_at_exit_nodes_lower[exit03]
 binary_var_for__dual_loadshed_var_at_exit_nodes_upper[exit01]
 binary_var_for__dual_loadshed_var_at_exit_nodes_upper[exit02]
 binary_var_for__dual_loadshed_var_at_exit_nodes_upper[exit03]
 binary_var_for__dual_loadshed_var_at_entry_nodes_lower[entry01]
 binary_var_for__dual_loadshed_var_at_entry_nodes_lower[entry03]
 binary_var_for__dual_loadshed_var_at_entry_nodes_lower[entry02]
 binary_var_for__dual_loadshed_var_at_entry_nodes_upper[entry01]
 binary_var_for__dual_loadshed_var_at_entry_nodes_upper[entry03]
 binary_var_for__dual_loadshed_var_at_entry_nodes_upper[entry02]
End
