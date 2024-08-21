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
 PDAI_lower[entry03,N01]: - 1e-05 flow[entry03,N01] - pressure[N01]
   + pressure[entry03] + 30 interdiction[entry03,N01] >= 0
 PDAI_lower[N04,N05]: - 1e-05 flow[N04,N05] + pressure[N04] - pressure[N05]
   + 30 interdiction[N04,N05] >= 0
 PDAI_lower[N01,N03]: - 1e-05 flow[N01,N03] + pressure[N01] - pressure[N03]
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
 PDAI_upper[entry03,N01]: - 1e-05 flow[entry03,N01] - pressure[N01]
   + pressure[entry03] - 30 interdiction[entry03,N01] <= 0
 PDAI_upper[N04,N05]: - 1e-05 flow[N04,N05] + pressure[N04] - pressure[N05]
   - 30 interdiction[N04,N05] <= 0
 PDAI_upper[N01,N03]: - 1e-05 flow[N01,N03] + pressure[N01] - pressure[N03]
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
 flow_conservation[entry03]: 1e-05 loadshed[entry03]
   - flow[entry01,entry03] + flow[entry03,N01] = 1e-05
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
   + dual_loadshed_entry_upper[entry03]
   - 1e-05 dual_flowConservation[entry03] = 0
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
   + dual_flow_upper[entry03,N01] + 1e-05 dual_PDAI_lower[entry03,N01]
   - 1e-05 dual_PDAI_upper[entry03,N01] + dual_flowConservation[N01]
   - dual_flowConservation[entry03] = 0
 ArcdfC[N04,N05]: - dual_flow_lower[N04,N05] + dual_flow_upper[N04,N05]
   + 1e-05 dual_PDAI_lower[N04,N05] - 1e-05 dual_PDAI_upper[N04,N05]
   - dual_flowConservation[N04] + dual_flowConservation[N05] = 0
 ArcdfC[N01,N03]: - dual_flow_lower[N01,N03] + dual_flow_upper[N01,N03]
   + 1e-05 dual_PDAI_lower[N01,N03] - 1e-05 dual_PDAI_upper[N01,N03]
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
 aux_constr_lower_('entry01',_'entry03'): - flow[entry01,entry03]
   + 65.41666666666666 interdiction[entry01,entry03]
   + aux_var_lower[entry01,entry03] = 65.41666666666666
 aux_constr_upper_('entry01',_'entry03'): flow[entry01,entry03]
   + 65.41666666666666 interdiction[entry01,entry03]
   + aux_var_upper[entry01,entry03] = 65.41666666666666
 aux_constr_pdai_lower_('entry01',_'entry03'):
   0.5660644491026487 flow[entry01,entry03] - pressure[entry01]
   + pressure[entry03] - 30 interdiction[entry01,entry03]
   + aux_var_pdai_lower[entry01,entry03] = 0
 aux_constr_pdai_upper_('entry01',_'entry03'):
   - 0.5660644491026487 flow[entry01,entry03] + pressure[entry01]
   - pressure[entry03] - 30 interdiction[entry01,entry03]
   + aux_var_pdai_upper[entry01,entry03] = 0
 aux_constr_lower_('N01',_'N02'): - flow[N01,N02]
   + 65.41666666666666 interdiction[N01,N02] + aux_var_lower[N01,N02]
   = 65.41666666666666
 aux_constr_upper_('N01',_'N02'): flow[N01,N02]
   + 65.41666666666666 interdiction[N01,N02] + aux_var_upper[N01,N02]
   = 65.41666666666666
 aux_constr_pdai_lower_('N01',_'N02'): 0.5660644491026487 flow[N01,N02]
   - pressure[N01] + pressure[N02] - 30 interdiction[N01,N02]
   + aux_var_pdai_lower[N01,N02] = 0
 aux_constr_pdai_upper_('N01',_'N02'): - 0.5660644491026487 flow[N01,N02]
   + pressure[N01] - pressure[N02] - 30 interdiction[N01,N02]
   + aux_var_pdai_upper[N01,N02] = 0
 aux_constr_lower_('entry02',_'N03'): - flow[entry02,N03]
   + 65.41666666666666 interdiction[entry02,N03]
   + aux_var_lower[entry02,N03] = 65.41666666666666
 aux_constr_upper_('entry02',_'N03'): flow[entry02,N03]
   + 65.41666666666666 interdiction[entry02,N03]
   + aux_var_upper[entry02,N03] = 65.41666666666666
 aux_constr_pdai_lower_('entry02',_'N03'):
   0.5660644491026487 flow[entry02,N03] + pressure[N03] - pressure[entry02]
   - 30 interdiction[entry02,N03] + aux_var_pdai_lower[entry02,N03] = 0
 aux_constr_pdai_upper_('entry02',_'N03'):
   - 0.5660644491026487 flow[entry02,N03] - pressure[N03]
   + pressure[entry02] - 30 interdiction[entry02,N03]
   + aux_var_pdai_upper[entry02,N03] = 0
 aux_constr_lower_('N02',_'exit01'): - flow[N02,exit01]
   + 65.41666666666666 interdiction[N02,exit01] + aux_var_lower[N02,exit01]
   = 65.41666666666666
 aux_constr_upper_('N02',_'exit01'): flow[N02,exit01]
   + 65.41666666666666 interdiction[N02,exit01] + aux_var_upper[N02,exit01]
   = 65.41666666666666
 aux_constr_pdai_lower_('N02',_'exit01'):
   0.5660644491026487 flow[N02,exit01] - pressure[N02] + pressure[exit01]
   - 30 interdiction[N02,exit01] + aux_var_pdai_lower[N02,exit01] = 0
 aux_constr_pdai_upper_('N02',_'exit01'):
   - 0.5660644491026487 flow[N02,exit01] + pressure[N02] - pressure[exit01]
   - 30 interdiction[N02,exit01] + aux_var_pdai_upper[N02,exit01] = 0
 aux_constr_lower_('N02',_'N04'): - flow[N02,N04]
   + 65.41666666666666 interdiction[N02,N04] + aux_var_lower[N02,N04]
   = 65.41666666666666
 aux_constr_upper_('N02',_'N04'): flow[N02,N04]
   + 65.41666666666666 interdiction[N02,N04] + aux_var_upper[N02,N04]
   = 65.41666666666666
 aux_constr_pdai_lower_('N02',_'N04'): 0.5660644491026487 flow[N02,N04]
   - pressure[N02] + pressure[N04] - 30 interdiction[N02,N04]
   + aux_var_pdai_lower[N02,N04] = 0
 aux_constr_pdai_upper_('N02',_'N04'): - 0.5660644491026487 flow[N02,N04]
   + pressure[N02] - pressure[N04] - 30 interdiction[N02,N04]
   + aux_var_pdai_upper[N02,N04] = 0
 aux_constr_lower_('N03',_'N04'): - flow[N03,N04]
   + 65.41666666666666 interdiction[N03,N04] + aux_var_lower[N03,N04]
   = 65.41666666666666
 aux_constr_upper_('N03',_'N04'): flow[N03,N04]
   + 65.41666666666666 interdiction[N03,N04] + aux_var_upper[N03,N04]
   = 65.41666666666666
 aux_constr_pdai_lower_('N03',_'N04'): 0.5660644491026487 flow[N03,N04]
   - pressure[N03] + pressure[N04] - 30 interdiction[N03,N04]
   + aux_var_pdai_lower[N03,N04] = 0
 aux_constr_pdai_upper_('N03',_'N04'): - 0.5660644491026487 flow[N03,N04]
   + pressure[N03] - pressure[N04] - 30 interdiction[N03,N04]
   + aux_var_pdai_upper[N03,N04] = 0
 aux_constr_lower_('N05',_'exit02'): - flow[N05,exit02]
   + 65.41666666666666 interdiction[N05,exit02] + aux_var_lower[N05,exit02]
   = 65.41666666666666
 aux_constr_upper_('N05',_'exit02'): flow[N05,exit02]
   + 65.41666666666666 interdiction[N05,exit02] + aux_var_upper[N05,exit02]
   = 65.41666666666666
 aux_constr_pdai_lower_('N05',_'exit02'):
   0.5731961978256868 flow[N05,exit02] - pressure[N05] + pressure[exit02]
   - 20 interdiction[N05,exit02] + aux_var_pdai_lower[N05,exit02] = 0
 aux_constr_pdai_upper_('N05',_'exit02'):
   - 0.5731961978256868 flow[N05,exit02] + pressure[N05] - pressure[exit02]
   - 30 interdiction[N05,exit02] + aux_var_pdai_upper[N05,exit02] = 0
 aux_constr_lower_('N05',_'exit03'): - flow[N05,exit03]
   + 65.41666666666666 interdiction[N05,exit03] + aux_var_lower[N05,exit03]
   = 65.41666666666666
 aux_constr_upper_('N05',_'exit03'): flow[N05,exit03]
   + 65.41666666666666 interdiction[N05,exit03] + aux_var_upper[N05,exit03]
   = 65.41666666666666
 aux_constr_pdai_lower_('N05',_'exit03'):
   0.5731961978256868 flow[N05,exit03] - pressure[N05] + pressure[exit03]
   - 20 interdiction[N05,exit03] + aux_var_pdai_lower[N05,exit03] = 0
 aux_constr_pdai_upper_('N05',_'exit03'):
   - 0.5731961978256868 flow[N05,exit03] + pressure[N05] - pressure[exit03]
   - 30 interdiction[N05,exit03] + aux_var_pdai_upper[N05,exit03] = 0
 aux_constr_lower_('entry03',_'N01'): - flow[entry03,N01]
   + 65.41666666666666 interdiction[entry03,N01]
   + aux_var_lower[entry03,N01] = 65.41666666666666
 aux_constr_upper_('entry03',_'N01'): flow[entry03,N01]
   + 65.41666666666666 interdiction[entry03,N01]
   + aux_var_upper[entry03,N01] = 65.41666666666666
 aux_constr_pdai_lower_('entry03',_'N01'): 1e-05 flow[entry03,N01]
   + pressure[N01] - pressure[entry03] - 30 interdiction[entry03,N01]
   + aux_var_pdai_lower[entry03,N01] = 0
 aux_constr_pdai_upper_('entry03',_'N01'): - 1e-05 flow[entry03,N01]
   - pressure[N01] + pressure[entry03] - 30 interdiction[entry03,N01]
   + aux_var_pdai_upper[entry03,N01] = 0
 aux_constr_lower_('N04',_'N05'): - flow[N04,N05]
   + 65.41666666666666 interdiction[N04,N05] + aux_var_lower[N04,N05]
   = 65.41666666666666
 aux_constr_upper_('N04',_'N05'): flow[N04,N05]
   + 65.41666666666666 interdiction[N04,N05] + aux_var_upper[N04,N05]
   = 65.41666666666666
 aux_constr_pdai_lower_('N04',_'N05'): 1e-05 flow[N04,N05] - pressure[N04]
   + pressure[N05] - 30 interdiction[N04,N05] + aux_var_pdai_lower[N04,N05]
   = 0
 aux_constr_pdai_upper_('N04',_'N05'): - 1e-05 flow[N04,N05]
   + pressure[N04] - pressure[N05] - 30 interdiction[N04,N05]
   + aux_var_pdai_upper[N04,N05] = 0
 aux_constr_lower_('N01',_'N03'): - flow[N01,N03]
   + 65.41666666666666 interdiction[N01,N03] + aux_var_lower[N01,N03]
   = 65.41666666666666
 aux_constr_upper_('N01',_'N03'): flow[N01,N03]
   + 65.41666666666666 interdiction[N01,N03] + aux_var_upper[N01,N03]
   = 65.41666666666666
 aux_constr_pdai_lower_('N01',_'N03'): 1e-05 flow[N01,N03] - pressure[N01]
   + pressure[N03] - 30 interdiction[N01,N03] + aux_var_pdai_lower[N01,N03]
   = 0
 aux_constr_pdai_upper_('N01',_'N03'): - 1e-05 flow[N01,N03]
   + pressure[N01] - pressure[N03] - 30 interdiction[N01,N03]
   + aux_var_pdai_upper[N01,N03] = 0
 aux_constr_pressure_lower_N01: - pressure[N01]
   + aux_var_pressure_lower[N01] = -40
 aux_constr_pressure_upper_N01: pressure[N01] + aux_var_pressure_upper[N01]
   = 70
 aux_constr_pressure_lower_N02: - pressure[N02]
   + aux_var_pressure_lower[N02] = -40
 aux_constr_pressure_upper_N02: pressure[N02] + aux_var_pressure_upper[N02]
   = 70
 aux_constr_pressure_lower_N03: - pressure[N03]
   + aux_var_pressure_lower[N03] = -40
 aux_constr_pressure_upper_N03: pressure[N03] + aux_var_pressure_upper[N03]
   = 70
 aux_constr_pressure_lower_N04: - pressure[N04]
   + aux_var_pressure_lower[N04] = -40
 aux_constr_pressure_upper_N04: pressure[N04] + aux_var_pressure_upper[N04]
   = 70
 aux_constr_pressure_lower_N05: - pressure[N05]
   + aux_var_pressure_lower[N05] = -40
 aux_constr_pressure_upper_N05: pressure[N05] + aux_var_pressure_upper[N05]
   = 70
 aux_constr_pressure_lower_entry01: - pressure[entry01]
   + aux_var_pressure_lower[entry01] = -40
 aux_constr_pressure_upper_entry01: pressure[entry01]
   + aux_var_pressure_upper[entry01] = 70
 aux_constr_pressure_lower_entry03: - pressure[entry03]
   + aux_var_pressure_lower[entry03] = -40
 aux_constr_pressure_upper_entry03: pressure[entry03]
   + aux_var_pressure_upper[entry03] = 70
 aux_constr_pressure_lower_entry02: - pressure[entry02]
   + aux_var_pressure_lower[entry02] = -40
 aux_constr_pressure_upper_entry02: pressure[entry02]
   + aux_var_pressure_upper[entry02] = 70
 aux_constr_pressure_lower_exit01: - pressure[exit01]
   + aux_var_pressure_lower[exit01] = -40
 aux_constr_pressure_upper_exit01: pressure[exit01]
   + aux_var_pressure_upper[exit01] = 70
 aux_constr_pressure_lower_exit02: - pressure[exit02]
   + aux_var_pressure_lower[exit02] = -40
 aux_constr_pressure_upper_exit02: pressure[exit02]
   + aux_var_pressure_upper[exit02] = 60
 aux_constr_pressure_lower_exit03: - pressure[exit03]
   + aux_var_pressure_lower[exit03] = -40
 aux_constr_pressure_upper_exit03: pressure[exit03]
   + aux_var_pressure_upper[exit03] = 60
 aux_constr_loadshed_exit_lower_exit01: - loadshed[exit01]
   + aux_var_loadshed_exit_lower[exit01] = 0
 aux_constr_loadshed_exit_upper_exit01: loadshed[exit01]
   + aux_var_loadshed_exit_upper[exit01] = 1
 aux_constr_loadshed_exit_lower_exit02: - loadshed[exit02]
   + aux_var_loadshed_exit_lower[exit02] = 0
 aux_constr_loadshed_exit_upper_exit02: loadshed[exit02]
   + aux_var_loadshed_exit_upper[exit02] = 1
 aux_constr_loadshed_exit_lower_exit03: - loadshed[exit03]
   + aux_var_loadshed_exit_lower[exit03] = 0
 aux_constr_loadshed_exit_upper_exit03: loadshed[exit03]
   + aux_var_loadshed_exit_upper[exit03] = 1
 aux_constr_loadshed_entry_lower_entry01: - loadshed[entry01]
   + aux_var_loadshed_entry_lower[entry01] = 3.6875
 aux_constr_loadshed_entry_upper_entry01: loadshed[entry01]
   + aux_var_loadshed_entry_upper[entry01] = 1
 aux_constr_loadshed_entry_lower_entry03: - loadshed[entry03]
   + aux_var_loadshed_entry_lower[entry03] = 0
 aux_constr_loadshed_entry_upper_entry03: loadshed[entry03]
   + aux_var_loadshed_entry_upper[entry03] = 1
 aux_constr_loadshed_entry_lower_entry02: - loadshed[entry02]
   + aux_var_loadshed_entry_lower[entry02] = 2.571428571428571
 aux_constr_loadshed_entry_upper_entry02: loadshed[entry02]
   + aux_var_loadshed_entry_upper[entry02] = 1
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
 R172: interdiction[entry01,entry03] + interdiction[N01,N02]
   + interdiction[entry02,N03] + interdiction[N02,exit01]
   + interdiction[N02,N04] + interdiction[N03,N04]
   + interdiction[N05,exit02] + interdiction[N05,exit03]
   + interdiction[entry03,N01] + interdiction[N04,N05]
   + interdiction[N01,N03] <= 0
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
SOS
 s0:  S1 :: dual_flow_lower[entry01,entry03]:1
     aux_var_lower[entry01,entry03]:2
 s1:  S1 :: dual_flow_upper[entry01,entry03]:1
     aux_var_upper[entry01,entry03]:2
 s2:  S1 :: dual_PDAI_lower[entry01,entry03]:1
     aux_var_pdai_lower[entry01,entry03]:2
 s3:  S1 :: dual_PDAI_upper[entry01,entry03]:1
     aux_var_pdai_upper[entry01,entry03]:2
 s4:  S1 :: dual_flow_lower[N01,N02]:1 aux_var_lower[N01,N02]:2
 s5:  S1 :: dual_flow_upper[N01,N02]:1 aux_var_upper[N01,N02]:2
 s6:  S1 :: dual_PDAI_lower[N01,N02]:1 aux_var_pdai_lower[N01,N02]:2
 s7:  S1 :: dual_PDAI_upper[N01,N02]:1 aux_var_pdai_upper[N01,N02]:2
 s8:  S1 :: dual_flow_lower[entry02,N03]:1 aux_var_lower[entry02,N03]:2
 s9:  S1 :: dual_flow_upper[entry02,N03]:1 aux_var_upper[entry02,N03]:2
 s10:  S1 :: dual_PDAI_lower[entry02,N03]:1
     aux_var_pdai_lower[entry02,N03]:2
 s11:  S1 :: dual_PDAI_upper[entry02,N03]:1
     aux_var_pdai_upper[entry02,N03]:2
 s12:  S1 :: dual_flow_lower[N02,exit01]:1 aux_var_lower[N02,exit01]:2
 s13:  S1 :: dual_flow_upper[N02,exit01]:1 aux_var_upper[N02,exit01]:2
 s14:  S1 :: dual_PDAI_lower[N02,exit01]:1 aux_var_pdai_lower[N02,exit01]:2
 s15:  S1 :: dual_PDAI_upper[N02,exit01]:1 aux_var_pdai_upper[N02,exit01]:2
 s16:  S1 :: dual_flow_lower[N02,N04]:1 aux_var_lower[N02,N04]:2
 s17:  S1 :: dual_flow_upper[N02,N04]:1 aux_var_upper[N02,N04]:2
 s18:  S1 :: dual_PDAI_lower[N02,N04]:1 aux_var_pdai_lower[N02,N04]:2
 s19:  S1 :: dual_PDAI_upper[N02,N04]:1 aux_var_pdai_upper[N02,N04]:2
 s20:  S1 :: dual_flow_lower[N03,N04]:1 aux_var_lower[N03,N04]:2
 s21:  S1 :: dual_flow_upper[N03,N04]:1 aux_var_upper[N03,N04]:2
 s22:  S1 :: dual_PDAI_lower[N03,N04]:1 aux_var_pdai_lower[N03,N04]:2
 s23:  S1 :: dual_PDAI_upper[N03,N04]:1 aux_var_pdai_upper[N03,N04]:2
 s24:  S1 :: dual_flow_lower[N05,exit02]:1 aux_var_lower[N05,exit02]:2
 s25:  S1 :: dual_flow_upper[N05,exit02]:1 aux_var_upper[N05,exit02]:2
 s26:  S1 :: dual_PDAI_lower[N05,exit02]:1 aux_var_pdai_lower[N05,exit02]:2
 s27:  S1 :: dual_PDAI_upper[N05,exit02]:1 aux_var_pdai_upper[N05,exit02]:2
 s28:  S1 :: dual_flow_lower[N05,exit03]:1 aux_var_lower[N05,exit03]:2
 s29:  S1 :: dual_flow_upper[N05,exit03]:1 aux_var_upper[N05,exit03]:2
 s30:  S1 :: dual_PDAI_lower[N05,exit03]:1 aux_var_pdai_lower[N05,exit03]:2
 s31:  S1 :: dual_PDAI_upper[N05,exit03]:1 aux_var_pdai_upper[N05,exit03]:2
 s32:  S1 :: dual_flow_lower[entry03,N01]:1 aux_var_lower[entry03,N01]:2
 s33:  S1 :: dual_flow_upper[entry03,N01]:1 aux_var_upper[entry03,N01]:2
 s34:  S1 :: dual_PDAI_lower[entry03,N01]:1
     aux_var_pdai_lower[entry03,N01]:2
 s35:  S1 :: dual_PDAI_upper[entry03,N01]:1
     aux_var_pdai_upper[entry03,N01]:2
 s36:  S1 :: dual_flow_lower[N04,N05]:1 aux_var_lower[N04,N05]:2
 s37:  S1 :: dual_flow_upper[N04,N05]:1 aux_var_upper[N04,N05]:2
 s38:  S1 :: dual_PDAI_lower[N04,N05]:1 aux_var_pdai_lower[N04,N05]:2
 s39:  S1 :: dual_PDAI_upper[N04,N05]:1 aux_var_pdai_upper[N04,N05]:2
 s40:  S1 :: dual_flow_lower[N01,N03]:1 aux_var_lower[N01,N03]:2
 s41:  S1 :: dual_flow_upper[N01,N03]:1 aux_var_upper[N01,N03]:2
 s42:  S1 :: dual_PDAI_lower[N01,N03]:1 aux_var_pdai_lower[N01,N03]:2
 s43:  S1 :: dual_PDAI_upper[N01,N03]:1 aux_var_pdai_upper[N01,N03]:2
 s44:  S1 :: dual_pressure_lower[N01]:1 aux_var_pressure_lower[N01]:2
 s45:  S1 :: dual_pressure_upper[N01]:1 aux_var_pressure_upper[N01]:2
 s46:  S1 :: dual_pressure_lower[N02]:1 aux_var_pressure_lower[N02]:2
 s47:  S1 :: dual_pressure_upper[N02]:1 aux_var_pressure_upper[N02]:2
 s48:  S1 :: dual_pressure_lower[N03]:1 aux_var_pressure_lower[N03]:2
 s49:  S1 :: dual_pressure_upper[N03]:1 aux_var_pressure_upper[N03]:2
 s50:  S1 :: dual_pressure_lower[N04]:1 aux_var_pressure_lower[N04]:2
 s51:  S1 :: dual_pressure_upper[N04]:1 aux_var_pressure_upper[N04]:2
 s52:  S1 :: dual_pressure_lower[N05]:1 aux_var_pressure_lower[N05]:2
 s53:  S1 :: dual_pressure_upper[N05]:1 aux_var_pressure_upper[N05]:2
 s54:  S1 :: dual_pressure_lower[entry01]:1
     aux_var_pressure_lower[entry01]:2
 s55:  S1 :: dual_pressure_upper[entry01]:1
     aux_var_pressure_upper[entry01]:2
 s56:  S1 :: dual_pressure_lower[entry03]:1
     aux_var_pressure_lower[entry03]:2
 s57:  S1 :: dual_pressure_upper[entry03]:1
     aux_var_pressure_upper[entry03]:2
 s58:  S1 :: dual_pressure_lower[entry02]:1
     aux_var_pressure_lower[entry02]:2
 s59:  S1 :: dual_pressure_upper[entry02]:1
     aux_var_pressure_upper[entry02]:2
 s60:  S1 :: dual_pressure_lower[exit01]:1 aux_var_pressure_lower[exit01]:2
 s61:  S1 :: dual_pressure_upper[exit01]:1 aux_var_pressure_upper[exit01]:2
 s62:  S1 :: dual_pressure_lower[exit02]:1 aux_var_pressure_lower[exit02]:2
 s63:  S1 :: dual_pressure_upper[exit02]:1 aux_var_pressure_upper[exit02]:2
 s64:  S1 :: dual_pressure_lower[exit03]:1 aux_var_pressure_lower[exit03]:2
 s65:  S1 :: dual_pressure_upper[exit03]:1 aux_var_pressure_upper[exit03]:2
 s66:  S1 :: dual_loadshed_exit_lower[exit01]:1
     aux_var_loadshed_exit_lower[exit01]:2
 s67:  S1 :: dual_loadshed_exit_upper[exit01]:1
     aux_var_loadshed_exit_upper[exit01]:2
 s68:  S1 :: dual_loadshed_exit_lower[exit02]:1
     aux_var_loadshed_exit_lower[exit02]:2
 s69:  S1 :: dual_loadshed_exit_upper[exit02]:1
     aux_var_loadshed_exit_upper[exit02]:2
 s70:  S1 :: dual_loadshed_exit_lower[exit03]:1
     aux_var_loadshed_exit_lower[exit03]:2
 s71:  S1 :: dual_loadshed_exit_upper[exit03]:1
     aux_var_loadshed_exit_upper[exit03]:2
 s72:  S1 :: dual_loadshed_entry_lower[entry01]:1
     aux_var_loadshed_entry_lower[entry01]:2
 s73:  S1 :: dual_loadshed_entry_upper[entry01]:1
     aux_var_loadshed_entry_upper[entry01]:2
 s74:  S1 :: dual_loadshed_entry_lower[entry03]:1
     aux_var_loadshed_entry_lower[entry03]:2
 s75:  S1 :: dual_loadshed_entry_upper[entry03]:1
     aux_var_loadshed_entry_upper[entry03]:2
 s76:  S1 :: dual_loadshed_entry_lower[entry02]:1
     aux_var_loadshed_entry_lower[entry02]:2
 s77:  S1 :: dual_loadshed_entry_upper[entry02]:1
     aux_var_loadshed_entry_upper[entry02]:2
End
