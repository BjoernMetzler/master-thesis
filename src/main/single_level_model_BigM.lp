\ Model GasLib-11
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  0 lambda[N01] + 0 lambda[N02] + 0 lambda[N03] + 0 lambda[N04]
   + 0 lambda[N05] + 21.80555555555556 lambda[exit01]
   + 26.16666666666667 lambda[exit02] + 17.44444444444444 lambda[exit03]
Subject To
 PDAI_lower[entry01,entry03]: - 0.5660644491026487 q[entry01,entry03]
   + pi[entry01] - pi[entry03] + 30 x[entry01,entry03] >= 0
 PDAI_lower[N01,N02]: - 0.5660644491026487 q[N01,N02] + pi[N01] - pi[N02]
   + 30 x[N01,N02] >= 0
 PDAI_lower[entry02,N03]: - 0.5660644491026487 q[entry02,N03] - pi[N03]
   + pi[entry02] + 30 x[entry02,N03] >= 0
 PDAI_lower[N02,exit01]: - 0.5660644491026487 q[N02,exit01] + pi[N02]
   - pi[exit01] + 30 x[N02,exit01] >= 0
 PDAI_lower[N02,N04]: - 0.5660644491026487 q[N02,N04] + pi[N02] - pi[N04]
   + 30 x[N02,N04] >= 0
 PDAI_lower[N03,N04]: - 0.5660644491026487 q[N03,N04] + pi[N03] - pi[N04]
   + 30 x[N03,N04] >= 0
 PDAI_lower[N05,exit02]: - 0.5731961978256868 q[N05,exit02] + pi[N05]
   - pi[exit02] + 20 x[N05,exit02] >= 0
 PDAI_lower[N05,exit03]: - 0.5731961978256868 q[N05,exit03] + pi[N05]
   - pi[exit03] + 20 x[N05,exit03] >= 0
 PDAI_lower[entry03,N01]: - 1e-05 q[entry03,N01] - pi[N01] + pi[entry03]
   + 30 x[entry03,N01] >= 0
 PDAI_lower[N04,N05]: - 1e-05 q[N04,N05] + pi[N04] - pi[N05]
   + 30 x[N04,N05] >= 0
 PDAI_lower[N01,N03]: - 1e-05 q[N01,N03] + pi[N01] - pi[N03]
   + 30 x[N01,N03] >= 0
 PDAI_upper[entry01,entry03]: - 0.5660644491026487 q[entry01,entry03]
   + pi[entry01] - pi[entry03] - 30 x[entry01,entry03] <= 0
 PDAI_upper[N01,N02]: - 0.5660644491026487 q[N01,N02] + pi[N01] - pi[N02]
   - 30 x[N01,N02] <= 0
 PDAI_upper[entry02,N03]: - 0.5660644491026487 q[entry02,N03] - pi[N03]
   + pi[entry02] - 30 x[entry02,N03] <= 0
 PDAI_upper[N02,exit01]: - 0.5660644491026487 q[N02,exit01] + pi[N02]
   - pi[exit01] - 30 x[N02,exit01] <= 0
 PDAI_upper[N02,N04]: - 0.5660644491026487 q[N02,N04] + pi[N02] - pi[N04]
   - 30 x[N02,N04] <= 0
 PDAI_upper[N03,N04]: - 0.5660644491026487 q[N03,N04] + pi[N03] - pi[N04]
   - 30 x[N03,N04] <= 0
 PDAI_upper[N05,exit02]: - 0.5731961978256868 q[N05,exit02] + pi[N05]
   - pi[exit02] - 30 x[N05,exit02] <= 0
 PDAI_upper[N05,exit03]: - 0.5731961978256868 q[N05,exit03] + pi[N05]
   - pi[exit03] - 30 x[N05,exit03] <= 0
 PDAI_upper[entry03,N01]: - 1e-05 q[entry03,N01] - pi[N01] + pi[entry03]
   - 30 x[entry03,N01] <= 0
 PDAI_upper[N04,N05]: - 1e-05 q[N04,N05] + pi[N04] - pi[N05]
   - 30 x[N04,N05] <= 0
 PDAI_upper[N01,N03]: - 1e-05 q[N01,N03] + pi[N01] - pi[N03]
   - 30 x[N01,N03] <= 0
 flow_conservation[N01]: q[N01,N02] - q[entry03,N01] + q[N01,N03] = 0
 flow_conservation[N02]: - q[N01,N02] + q[N02,exit01] + q[N02,N04] = 0
 flow_conservation[N03]: - q[entry02,N03] + q[N03,N04] - q[N01,N03] = 0
 flow_conservation[N04]: - q[N02,N04] - q[N03,N04] + q[N04,N05] = 0
 flow_conservation[N05]: q[N05,exit02] + q[N05,exit03] - q[N04,N05] = 0
 flow_conservation[entry01]: 34.88888888888889 lambda[entry01]
   + q[entry01,entry03] = 34.88888888888889
 flow_conservation[entry03]: 1e-05 lambda[entry03] - q[entry01,entry03]
   + q[entry03,N01] = 1e-05
 flow_conservation[entry02]: 30.52777777777778 lambda[entry02]
   + q[entry02,N03] = 30.52777777777778
 flow_conservation[exit01]: - 21.80555555555556 lambda[exit01]
   - q[N02,exit01] = -21.80555555555556
 flow_conservation[exit02]: - 26.16666666666667 lambda[exit02]
   - q[N05,exit02] = -26.16666666666667
 flow_conservation[exit03]: - 17.44444444444444 lambda[exit03]
   - q[N05,exit03] = -17.44444444444444
 flow_lower[entry01,entry03]: - q[entry01,entry03]
   + 65.41666666666666 x[entry01,entry03] <= 65.41666666666666
 flow_lower[N01,N02]: - q[N01,N02] + 65.41666666666666 x[N01,N02]
   <= 65.41666666666666
 flow_lower[entry02,N03]: - q[entry02,N03]
   + 65.41666666666666 x[entry02,N03] <= 65.41666666666666
 flow_lower[N02,exit01]: - q[N02,exit01] + 65.41666666666666 x[N02,exit01]
   <= 65.41666666666666
 flow_lower[N02,N04]: - q[N02,N04] + 65.41666666666666 x[N02,N04]
   <= 65.41666666666666
 flow_lower[N03,N04]: - q[N03,N04] + 65.41666666666666 x[N03,N04]
   <= 65.41666666666666
 flow_lower[N05,exit02]: - q[N05,exit02] + 65.41666666666666 x[N05,exit02]
   <= 65.41666666666666
 flow_lower[N05,exit03]: - q[N05,exit03] + 65.41666666666666 x[N05,exit03]
   <= 65.41666666666666
 flow_lower[entry03,N01]: - q[entry03,N01]
   + 65.41666666666666 x[entry03,N01] <= 65.41666666666666
 flow_lower[N04,N05]: - q[N04,N05] + 65.41666666666666 x[N04,N05]
   <= 65.41666666666666
 flow_lower[N01,N03]: - q[N01,N03] + 65.41666666666666 x[N01,N03]
   <= 65.41666666666666
 flow_upper[entry01,entry03]: - q[entry01,entry03]
   - 65.41666666666666 x[entry01,entry03] >= -65.41666666666666
 flow_upper[N01,N02]: - q[N01,N02] - 65.41666666666666 x[N01,N02]
   >= -65.41666666666666
 flow_upper[entry02,N03]: - q[entry02,N03]
   - 65.41666666666666 x[entry02,N03] >= -65.41666666666666
 flow_upper[N02,exit01]: - q[N02,exit01] - 65.41666666666666 x[N02,exit01]
   >= -65.41666666666666
 flow_upper[N02,N04]: - q[N02,N04] - 65.41666666666666 x[N02,N04]
   >= -65.41666666666666
 flow_upper[N03,N04]: - q[N03,N04] - 65.41666666666666 x[N03,N04]
   >= -65.41666666666666
 flow_upper[N05,exit02]: - q[N05,exit02] - 65.41666666666666 x[N05,exit02]
   >= -65.41666666666666
 flow_upper[N05,exit03]: - q[N05,exit03] - 65.41666666666666 x[N05,exit03]
   >= -65.41666666666666
 flow_upper[entry03,N01]: - q[entry03,N01]
   - 65.41666666666666 x[entry03,N01] >= -65.41666666666666
 flow_upper[N04,N05]: - q[N04,N05] - 65.41666666666666 x[N04,N05]
   >= -65.41666666666666
 flow_upper[N01,N03]: - q[N01,N03] - 65.41666666666666 x[N01,N03]
   >= -65.41666666666666
 EnNdfC[entry01]: - eta_minus[entry01] + eta_plus[entry01]
   - 34.88888888888889 alpha[entry01] = 0
 EnNdfC[entry03]: - eta_minus[entry03] + eta_plus[entry03]
   - 1e-05 alpha[entry03] = 0
 EnNdfC[entry02]: - eta_minus[entry02] + eta_plus[entry02]
   - 30.52777777777778 alpha[entry02] = 0
 ExNdfC[exit01]: - mu_minus[exit01] + minus_plus[exit01]
   + 21.80555555555556 alpha[exit01] = -21.80555555555556
 ExNdfC[exit02]: - mu_minus[exit02] + minus_plus[exit02]
   + 26.16666666666667 alpha[exit02] = -26.16666666666667
 ExNdfC[exit03]: - mu_minus[exit03] + minus_plus[exit03]
   + 17.44444444444444 alpha[exit03] = -17.44444444444444
 ArcdfC[entry01,entry03]: - delta_minus[entry01,entry03]
   + delta_plus[entry01,entry03]
   + 0.5660644491026487 epsilon_minus[entry01,entry03]
   - 0.5660644491026487 epsilon_plus[entry01,entry03] - alpha[entry01]
   + alpha[entry03] = 0
 ArcdfC[N01,N02]: - delta_minus[N01,N02] + delta_plus[N01,N02]
   + 0.5660644491026487 epsilon_minus[N01,N02]
   - 0.5660644491026487 epsilon_plus[N01,N02] - alpha[N01] + alpha[N02]
   = 0
 ArcdfC[entry02,N03]: - delta_minus[entry02,N03] + delta_plus[entry02,N03]
   + 0.5660644491026487 epsilon_minus[entry02,N03]
   - 0.5660644491026487 epsilon_plus[entry02,N03] + alpha[N03]
   - alpha[entry02] = 0
 ArcdfC[N02,exit01]: - delta_minus[N02,exit01] + delta_plus[N02,exit01]
   + 0.5660644491026487 epsilon_minus[N02,exit01]
   - 0.5660644491026487 epsilon_plus[N02,exit01] - alpha[N02]
   + alpha[exit01] = 0
 ArcdfC[N02,N04]: - delta_minus[N02,N04] + delta_plus[N02,N04]
   + 0.5660644491026487 epsilon_minus[N02,N04]
   - 0.5660644491026487 epsilon_plus[N02,N04] - alpha[N02] + alpha[N04]
   = 0
 ArcdfC[N03,N04]: - delta_minus[N03,N04] + delta_plus[N03,N04]
   + 0.5660644491026487 epsilon_minus[N03,N04]
   - 0.5660644491026487 epsilon_plus[N03,N04] - alpha[N03] + alpha[N04]
   = 0
 ArcdfC[N05,exit02]: - delta_minus[N05,exit02] + delta_plus[N05,exit02]
   + 0.5731961978256868 epsilon_minus[N05,exit02]
   - 0.5731961978256868 epsilon_plus[N05,exit02] - alpha[N05]
   + alpha[exit02] = 0
 ArcdfC[N05,exit03]: - delta_minus[N05,exit03] + delta_plus[N05,exit03]
   + 0.5731961978256868 epsilon_minus[N05,exit03]
   - 0.5731961978256868 epsilon_plus[N05,exit03] - alpha[N05]
   + alpha[exit03] = 0
 ArcdfC[entry03,N01]: - delta_minus[entry03,N01] + delta_plus[entry03,N01]
   + 1e-05 epsilon_minus[entry03,N01] - 1e-05 epsilon_plus[entry03,N01]
   + alpha[N01] - alpha[entry03] = 0
 ArcdfC[N04,N05]: - delta_minus[N04,N05] + delta_plus[N04,N05]
   + 1e-05 epsilon_minus[N04,N05] - 1e-05 epsilon_plus[N04,N05]
   - alpha[N04] + alpha[N05] = 0
 ArcdfC[N01,N03]: - delta_minus[N01,N03] + delta_plus[N01,N03]
   + 1e-05 epsilon_minus[N01,N03] - 1e-05 epsilon_plus[N01,N03]
   - alpha[N01] + alpha[N03] = 0
 NodedfC[N01]: - epsilon_minus[N01,N02] + epsilon_minus[entry03,N01]
   - epsilon_minus[N01,N03] + epsilon_plus[N01,N02]
   - epsilon_plus[entry03,N01] + epsilon_plus[N01,N03] - zeta_minus[N01]
   + zeta_plus[N01] = 0
 NodedfC[N02]: epsilon_minus[N01,N02] - epsilon_minus[N02,exit01]
   - epsilon_minus[N02,N04] - epsilon_plus[N01,N02]
   + epsilon_plus[N02,exit01] + epsilon_plus[N02,N04] - zeta_minus[N02]
   + zeta_plus[N02] = 0
 NodedfC[N03]: epsilon_minus[entry02,N03] - epsilon_minus[N03,N04]
   + epsilon_minus[N01,N03] - epsilon_plus[entry02,N03]
   + epsilon_plus[N03,N04] - epsilon_plus[N01,N03] - zeta_minus[N03]
   + zeta_plus[N03] = 0
 NodedfC[N04]: epsilon_minus[N02,N04] + epsilon_minus[N03,N04]
   - epsilon_minus[N04,N05] - epsilon_plus[N02,N04] - epsilon_plus[N03,N04]
   + epsilon_plus[N04,N05] - zeta_minus[N04] + zeta_plus[N04] = 0
 NodedfC[N05]: - epsilon_minus[N05,exit02] - epsilon_minus[N05,exit03]
   + epsilon_minus[N04,N05] + epsilon_plus[N05,exit02]
   + epsilon_plus[N05,exit03] - epsilon_plus[N04,N05] - zeta_minus[N05]
   + zeta_plus[N05] = 0
 NodedfC[entry01]: - epsilon_minus[entry01,entry03]
   + epsilon_plus[entry01,entry03] - zeta_minus[entry01]
   + zeta_plus[entry01] = 0
 NodedfC[entry03]: epsilon_minus[entry01,entry03]
   - epsilon_minus[entry03,N01] - epsilon_plus[entry01,entry03]
   + epsilon_plus[entry03,N01] - zeta_minus[entry03] + zeta_plus[entry03]
   = 0
 NodedfC[entry02]: - epsilon_minus[entry02,N03] + epsilon_plus[entry02,N03]
   - zeta_minus[entry02] + zeta_plus[entry02] = 0
 NodedfC[exit01]: epsilon_minus[N02,exit01] - epsilon_plus[N02,exit01]
   - zeta_minus[exit01] + zeta_plus[exit01] = 0
 NodedfC[exit02]: epsilon_minus[N05,exit02] - epsilon_plus[N05,exit02]
   - zeta_minus[exit02] + zeta_plus[exit02] = 0
 NodedfC[exit03]: epsilon_minus[N05,exit03] - epsilon_plus[N05,exit03]
   - zeta_minus[exit03] + zeta_plus[exit03] = 0
 R83: alpha[N01] <= 1
 R84: alpha[N02] <= 1
 R85: alpha[N03] <= 1
 R86: alpha[N04] <= 1
 R87: alpha[N05] <= 1
 R88: alpha[entry01] <= 1
 R89: alpha[entry03] <= 1
 R90: alpha[entry02] <= 1
 R91: alpha[exit01] <= 1
 R92: alpha[exit02] <= 1
 R93: alpha[exit03] <= 1
 R94: alpha[N01] >= -1
 R95: alpha[N02] >= -1
 R96: alpha[N03] >= -1
 R97: alpha[N04] >= -1
 R98: alpha[N05] >= -1
 R99: alpha[entry01] >= -1
 R100: alpha[entry03] >= -1
 R101: alpha[entry02] >= -1
 R102: alpha[exit01] >= -1
 R103: alpha[exit02] >= -1
 R104: alpha[exit03] >= -1
 UB_bigM_for__dual_flow_var_at_arcs_lower[entry01,entry03]:
   delta_minus[entry01,entry03]
   - binary_var_for__dual_flow_var_at_arcs_lower[entry01,entry03] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_lower[N01,N02]: delta_minus[N01,N02]
   - binary_var_for__dual_flow_var_at_arcs_lower[N01,N02] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_lower[entry02,N03]:
   delta_minus[entry02,N03]
   - binary_var_for__dual_flow_var_at_arcs_lower[entry02,N03] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_lower[N02,exit01]:
   delta_minus[N02,exit01]
   - binary_var_for__dual_flow_var_at_arcs_lower[N02,exit01] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_lower[N02,N04]: delta_minus[N02,N04]
   - binary_var_for__dual_flow_var_at_arcs_lower[N02,N04] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_lower[N03,N04]: delta_minus[N03,N04]
   - binary_var_for__dual_flow_var_at_arcs_lower[N03,N04] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_lower[N05,exit02]:
   delta_minus[N05,exit02]
   - binary_var_for__dual_flow_var_at_arcs_lower[N05,exit02] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_lower[N05,exit03]:
   delta_minus[N05,exit03]
   - binary_var_for__dual_flow_var_at_arcs_lower[N05,exit03] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_lower[entry03,N01]:
   delta_minus[entry03,N01]
   - binary_var_for__dual_flow_var_at_arcs_lower[entry03,N01] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_lower[N04,N05]: delta_minus[N04,N05]
   - binary_var_for__dual_flow_var_at_arcs_lower[N04,N05] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_lower[N01,N03]: delta_minus[N01,N03]
   - binary_var_for__dual_flow_var_at_arcs_lower[N01,N03] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_upper[entry01,entry03]:
   delta_plus[entry01,entry03]
   - binary_var_for__dual_flow_var_at_arcs_upper[entry01,entry03] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_upper[N01,N02]: delta_plus[N01,N02]
   - binary_var_for__dual_flow_var_at_arcs_upper[N01,N02] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_upper[entry02,N03]:
   delta_plus[entry02,N03]
   - binary_var_for__dual_flow_var_at_arcs_upper[entry02,N03] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_upper[N02,exit01]:
   delta_plus[N02,exit01]
   - binary_var_for__dual_flow_var_at_arcs_upper[N02,exit01] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_upper[N02,N04]: delta_plus[N02,N04]
   - binary_var_for__dual_flow_var_at_arcs_upper[N02,N04] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_upper[N03,N04]: delta_plus[N03,N04]
   - binary_var_for__dual_flow_var_at_arcs_upper[N03,N04] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_upper[N05,exit02]:
   delta_plus[N05,exit02]
   - binary_var_for__dual_flow_var_at_arcs_upper[N05,exit02] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_upper[N05,exit03]:
   delta_plus[N05,exit03]
   - binary_var_for__dual_flow_var_at_arcs_upper[N05,exit03] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_upper[entry03,N01]:
   delta_plus[entry03,N01]
   - binary_var_for__dual_flow_var_at_arcs_upper[entry03,N01] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_upper[N04,N05]: delta_plus[N04,N05]
   - binary_var_for__dual_flow_var_at_arcs_upper[N04,N05] <= 0
 UB_bigM_for__dual_flow_var_at_arcs_upper[N01,N03]: delta_plus[N01,N03]
   - binary_var_for__dual_flow_var_at_arcs_upper[N01,N03] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_lower[entry01,entry03]:
   epsilon_minus[entry01,entry03]
   - 100000 binary_var_for__dual_PDAI_var_at_arcs_lower[entry01,entry03]
   <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_lower[N01,N02]: epsilon_minus[N01,N02]
   - 100000 binary_var_for__dual_PDAI_var_at_arcs_lower[N01,N02] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_lower[entry02,N03]:
   epsilon_minus[entry02,N03]
   - 100000 binary_var_for__dual_PDAI_var_at_arcs_lower[entry02,N03] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_lower[N02,exit01]:
   epsilon_minus[N02,exit01]
   - 100000 binary_var_for__dual_PDAI_var_at_arcs_lower[N02,exit01] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_lower[N02,N04]: epsilon_minus[N02,N04]
   - 100000 binary_var_for__dual_PDAI_var_at_arcs_lower[N02,N04] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_lower[N03,N04]: epsilon_minus[N03,N04]
   - 100000 binary_var_for__dual_PDAI_var_at_arcs_lower[N03,N04] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_lower[N05,exit02]:
   epsilon_minus[N05,exit02]
   - 100000 binary_var_for__dual_PDAI_var_at_arcs_lower[N05,exit02] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_lower[N05,exit03]:
   epsilon_minus[N05,exit03]
   - 100000 binary_var_for__dual_PDAI_var_at_arcs_lower[N05,exit03] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_lower[entry03,N01]:
   epsilon_minus[entry03,N01]
   - 100000 binary_var_for__dual_PDAI_var_at_arcs_lower[entry03,N01] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_lower[N04,N05]: epsilon_minus[N04,N05]
   - 100000 binary_var_for__dual_PDAI_var_at_arcs_lower[N04,N05] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_lower[N01,N03]: epsilon_minus[N01,N03]
   - 100000 binary_var_for__dual_PDAI_var_at_arcs_lower[N01,N03] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_upper[entry01,entry03]:
   epsilon_plus[entry01,entry03]
   - 100000 binary_var_for__dual_PDAI_var_at_arcs_upper[entry01,entry03]
   <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_upper[N01,N02]: epsilon_plus[N01,N02]
   - 100000 binary_var_for__dual_PDAI_var_at_arcs_upper[N01,N02] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_upper[entry02,N03]:
   epsilon_plus[entry02,N03]
   - 100000 binary_var_for__dual_PDAI_var_at_arcs_upper[entry02,N03] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_upper[N02,exit01]:
   epsilon_plus[N02,exit01]
   - 100000 binary_var_for__dual_PDAI_var_at_arcs_upper[N02,exit01] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_upper[N02,N04]: epsilon_plus[N02,N04]
   - 100000 binary_var_for__dual_PDAI_var_at_arcs_upper[N02,N04] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_upper[N03,N04]: epsilon_plus[N03,N04]
   - 100000 binary_var_for__dual_PDAI_var_at_arcs_upper[N03,N04] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_upper[N05,exit02]:
   epsilon_plus[N05,exit02]
   - 100000 binary_var_for__dual_PDAI_var_at_arcs_upper[N05,exit02] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_upper[N05,exit03]:
   epsilon_plus[N05,exit03]
   - 100000 binary_var_for__dual_PDAI_var_at_arcs_upper[N05,exit03] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_upper[entry03,N01]:
   epsilon_plus[entry03,N01]
   - 100000 binary_var_for__dual_PDAI_var_at_arcs_upper[entry03,N01] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_upper[N04,N05]: epsilon_plus[N04,N05]
   - 100000 binary_var_for__dual_PDAI_var_at_arcs_upper[N04,N05] <= 0
 UB_bigM_for__dual_PDAI_var_at_arcs_upper[N01,N03]: epsilon_plus[N01,N03]
   - 100000 binary_var_for__dual_PDAI_var_at_arcs_upper[N01,N03] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_lower[N01]: zeta_minus[N01]
   - 300000 binary_var_for__dual_pressure_var_at_nodes_lower[N01] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_lower[N02]: zeta_minus[N02]
   - 300000 binary_var_for__dual_pressure_var_at_nodes_lower[N02] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_lower[N03]: zeta_minus[N03]
   - 300000 binary_var_for__dual_pressure_var_at_nodes_lower[N03] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_lower[N04]: zeta_minus[N04]
   - 300000 binary_var_for__dual_pressure_var_at_nodes_lower[N04] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_lower[N05]: zeta_minus[N05]
   - 300000 binary_var_for__dual_pressure_var_at_nodes_lower[N05] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_lower[entry01]:
   zeta_minus[entry01]
   - 300000 binary_var_for__dual_pressure_var_at_nodes_lower[entry01] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_lower[entry03]:
   zeta_minus[entry03]
   - 300000 binary_var_for__dual_pressure_var_at_nodes_lower[entry03] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_lower[entry02]:
   zeta_minus[entry02]
   - 300000 binary_var_for__dual_pressure_var_at_nodes_lower[entry02] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_lower[exit01]: zeta_minus[exit01]
   - 300000 binary_var_for__dual_pressure_var_at_nodes_lower[exit01] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_lower[exit02]: zeta_minus[exit02]
   - 300000 binary_var_for__dual_pressure_var_at_nodes_lower[exit02] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_lower[exit03]: zeta_minus[exit03]
   - 300000 binary_var_for__dual_pressure_var_at_nodes_lower[exit03] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_upper[N01]: zeta_plus[N01]
   - 300000 binary_var_for__dual_pressure_var_at_nodes_upper[N01] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_upper[N02]: zeta_plus[N02]
   - 300000 binary_var_for__dual_pressure_var_at_nodes_upper[N02] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_upper[N03]: zeta_plus[N03]
   - 300000 binary_var_for__dual_pressure_var_at_nodes_upper[N03] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_upper[N04]: zeta_plus[N04]
   - 300000 binary_var_for__dual_pressure_var_at_nodes_upper[N04] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_upper[N05]: zeta_plus[N05]
   - 300000 binary_var_for__dual_pressure_var_at_nodes_upper[N05] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_upper[entry01]: zeta_plus[entry01]
   - 300000 binary_var_for__dual_pressure_var_at_nodes_upper[entry01] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_upper[entry03]: zeta_plus[entry03]
   - 300000 binary_var_for__dual_pressure_var_at_nodes_upper[entry03] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_upper[entry02]: zeta_plus[entry02]
   - 300000 binary_var_for__dual_pressure_var_at_nodes_upper[entry02] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_upper[exit01]: zeta_plus[exit01]
   - 300000 binary_var_for__dual_pressure_var_at_nodes_upper[exit01] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_upper[exit02]: zeta_plus[exit02]
   - 300000 binary_var_for__dual_pressure_var_at_nodes_upper[exit02] <= 0
 UB_bigM_for__dual_pressure_var_at_nodes_upper[exit03]: zeta_plus[exit03]
   - 300000 binary_var_for__dual_pressure_var_at_nodes_upper[exit03] <= 0
 UB_bigM_for__dual_loadshed_var_at_exit_nodes_lower[exit01]:
   mu_minus[exit01]
   - 69.77777777777777 binary_var_for__dual_loadshed_var_at_exit_nodes_lower[exit01]
   <= 0
 UB_bigM_for__dual_loadshed_var_at_exit_nodes_lower[exit02]:
   mu_minus[exit02]
   - 69.77777777777777 binary_var_for__dual_loadshed_var_at_exit_nodes_lower[exit02]
   <= 0
 UB_bigM_for__dual_loadshed_var_at_exit_nodes_lower[exit03]:
   mu_minus[exit03]
   - 69.77777777777777 binary_var_for__dual_loadshed_var_at_exit_nodes_lower[exit03]
   <= 0
 UB_bigM_for__dual_loadshed_var_at_exit_nodes_upper[exit01]:
   minus_plus[exit01]
   - 69.77777777777777 binary_var_for__dual_loadshed_var_at_exit_nodes_upper[exit01]
   <= 0
 UB_bigM_for__dual_loadshed_var_at_exit_nodes_upper[exit02]:
   minus_plus[exit02]
   - 69.77777777777777 binary_var_for__dual_loadshed_var_at_exit_nodes_upper[exit02]
   <= 0
 UB_bigM_for__dual_loadshed_var_at_exit_nodes_upper[exit03]:
   minus_plus[exit03]
   - 69.77777777777777 binary_var_for__dual_loadshed_var_at_exit_nodes_upper[exit03]
   <= 0
 UB_bigM_for__dual_loadshed_var_at_entry_nodes_lower[entry01]:
   eta_minus[entry01]
   - 34.88888888888889 binary_var_for__dual_loadshed_var_at_entry_nodes_lower[entry01]
   <= 0
 UB_bigM_for__dual_loadshed_var_at_entry_nodes_lower[entry03]:
   eta_minus[entry03]
   - 34.88888888888889 binary_var_for__dual_loadshed_var_at_entry_nodes_lower[entry03]
   <= 0
 UB_bigM_for__dual_loadshed_var_at_entry_nodes_lower[entry02]:
   eta_minus[entry02]
   - 34.88888888888889 binary_var_for__dual_loadshed_var_at_entry_nodes_lower[entry02]
   <= 0
 UB_bigM_for__dual_loadshed_var_at_entry_nodes_upper[entry01]:
   eta_plus[entry01]
   - 34.88888888888889 binary_var_for__dual_loadshed_var_at_entry_nodes_upper[entry01]
   <= 0
 UB_bigM_for__dual_loadshed_var_at_entry_nodes_upper[entry03]:
   eta_plus[entry03]
   - 34.88888888888889 binary_var_for__dual_loadshed_var_at_entry_nodes_upper[entry03]
   <= 0
 UB_bigM_for__dual_loadshed_var_at_entry_nodes_upper[entry02]:
   eta_plus[entry02]
   - 34.88888888888889 binary_var_for__dual_loadshed_var_at_entry_nodes_upper[entry02]
   <= 0
 UB_for__flow_var_at_arcs_lower[entry01,entry03]: q[entry01,entry03]
   - 65.41666666666666 x[entry01,entry03]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_lower[entry01,entry03]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_lower[N01,N02]: q[N01,N02]
   - 65.41666666666666 x[N01,N02]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_lower[N01,N02]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_lower[entry02,N03]: q[entry02,N03]
   - 65.41666666666666 x[entry02,N03]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_lower[entry02,N03]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_lower[N02,exit01]: q[N02,exit01]
   - 65.41666666666666 x[N02,exit01]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_lower[N02,exit01]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_lower[N02,N04]: q[N02,N04]
   - 65.41666666666666 x[N02,N04]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_lower[N02,N04]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_lower[N03,N04]: q[N03,N04]
   - 65.41666666666666 x[N03,N04]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_lower[N03,N04]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_lower[N05,exit02]: q[N05,exit02]
   - 65.41666666666666 x[N05,exit02]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_lower[N05,exit02]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_lower[N05,exit03]: q[N05,exit03]
   - 65.41666666666666 x[N05,exit03]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_lower[N05,exit03]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_lower[entry03,N01]: q[entry03,N01]
   - 65.41666666666666 x[entry03,N01]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_lower[entry03,N01]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_lower[N04,N05]: q[N04,N05]
   - 65.41666666666666 x[N04,N05]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_lower[N04,N05]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_lower[N01,N03]: q[N01,N03]
   - 65.41666666666666 x[N01,N03]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_lower[N01,N03]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_upper[entry01,entry03]: - q[entry01,entry03]
   - 65.41666666666666 x[entry01,entry03]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_upper[entry01,entry03]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_upper[N01,N02]: - q[N01,N02]
   - 65.41666666666666 x[N01,N02]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_upper[N01,N02]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_upper[entry02,N03]: - q[entry02,N03]
   - 65.41666666666666 x[entry02,N03]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_upper[entry02,N03]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_upper[N02,exit01]: - q[N02,exit01]
   - 65.41666666666666 x[N02,exit01]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_upper[N02,exit01]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_upper[N02,N04]: - q[N02,N04]
   - 65.41666666666666 x[N02,N04]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_upper[N02,N04]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_upper[N03,N04]: - q[N03,N04]
   - 65.41666666666666 x[N03,N04]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_upper[N03,N04]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_upper[N05,exit02]: - q[N05,exit02]
   - 65.41666666666666 x[N05,exit02]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_upper[N05,exit02]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_upper[N05,exit03]: - q[N05,exit03]
   - 65.41666666666666 x[N05,exit03]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_upper[N05,exit03]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_upper[entry03,N01]: - q[entry03,N01]
   - 65.41666666666666 x[entry03,N01]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_upper[entry03,N01]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_upper[N04,N05]: - q[N04,N05]
   - 65.41666666666666 x[N04,N05]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_upper[N04,N05]
   <= 65.41666666666666
 UB_for__flow_var_at_arcs_upper[N01,N03]: - q[N01,N03]
   - 65.41666666666666 x[N01,N03]
   + 130.8333333333333 binary_var_for__dual_flow_var_at_arcs_upper[N01,N03]
   <= 65.41666666666666
 UB_for__PDAI_var_at_arcs_lower[entry01,entry03]:
   - 0.5660644491026487 q[entry01,entry03] + pi[entry01] - pi[entry03]
   + 30 x[entry01,entry03]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_lower[entry01,entry03] <= 60
 UB_for__PDAI_var_at_arcs_lower[N01,N02]: - 0.5660644491026487 q[N01,N02]
   + pi[N01] - pi[N02] + 30 x[N01,N02]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_lower[N01,N02] <= 60
 UB_for__PDAI_var_at_arcs_lower[entry02,N03]:
   - 0.5660644491026487 q[entry02,N03] - pi[N03] + pi[entry02]
   + 30 x[entry02,N03]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_lower[entry02,N03] <= 60
 UB_for__PDAI_var_at_arcs_lower[N02,exit01]:
   - 0.5660644491026487 q[N02,exit01] + pi[N02] - pi[exit01]
   + 30 x[N02,exit01]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_lower[N02,exit01] <= 60
 UB_for__PDAI_var_at_arcs_lower[N02,N04]: - 0.5660644491026487 q[N02,N04]
   + pi[N02] - pi[N04] + 30 x[N02,N04]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_lower[N02,N04] <= 60
 UB_for__PDAI_var_at_arcs_lower[N03,N04]: - 0.5660644491026487 q[N03,N04]
   + pi[N03] - pi[N04] + 30 x[N03,N04]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_lower[N03,N04] <= 60
 UB_for__PDAI_var_at_arcs_lower[N05,exit02]:
   - 0.5731961978256868 q[N05,exit02] + pi[N05] - pi[exit02]
   + 20 x[N05,exit02]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_lower[N05,exit02] <= 60
 UB_for__PDAI_var_at_arcs_lower[N05,exit03]:
   - 0.5731961978256868 q[N05,exit03] + pi[N05] - pi[exit03]
   + 20 x[N05,exit03]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_lower[N05,exit03] <= 60
 UB_for__PDAI_var_at_arcs_lower[entry03,N01]: - 1e-05 q[entry03,N01]
   - pi[N01] + pi[entry03] + 30 x[entry03,N01]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_lower[entry03,N01] <= 60
 UB_for__PDAI_var_at_arcs_lower[N04,N05]: - 1e-05 q[N04,N05] + pi[N04]
   - pi[N05] + 30 x[N04,N05]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_lower[N04,N05] <= 60
 UB_for__PDAI_var_at_arcs_lower[N01,N03]: - 1e-05 q[N01,N03] + pi[N01]
   - pi[N03] + 30 x[N01,N03]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_lower[N01,N03] <= 60
 UB_for__PDAI_var_at_arcs_upper[entry01,entry03]:
   0.5660644491026487 q[entry01,entry03] - pi[entry01] + pi[entry03]
   + 30 x[entry01,entry03]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_upper[entry01,entry03] <= 60
 UB_for__PDAI_var_at_arcs_upper[N01,N02]: 0.5660644491026487 q[N01,N02]
   - pi[N01] + pi[N02] + 30 x[N01,N02]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_upper[N01,N02] <= 60
 UB_for__PDAI_var_at_arcs_upper[entry02,N03]:
   0.5660644491026487 q[entry02,N03] + pi[N03] - pi[entry02]
   + 30 x[entry02,N03]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_upper[entry02,N03] <= 60
 UB_for__PDAI_var_at_arcs_upper[N02,exit01]:
   0.5660644491026487 q[N02,exit01] - pi[N02] + pi[exit01]
   + 30 x[N02,exit01]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_upper[N02,exit01] <= 60
 UB_for__PDAI_var_at_arcs_upper[N02,N04]: 0.5660644491026487 q[N02,N04]
   - pi[N02] + pi[N04] + 30 x[N02,N04]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_upper[N02,N04] <= 60
 UB_for__PDAI_var_at_arcs_upper[N03,N04]: 0.5660644491026487 q[N03,N04]
   - pi[N03] + pi[N04] + 30 x[N03,N04]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_upper[N03,N04] <= 60
 UB_for__PDAI_var_at_arcs_upper[N05,exit02]:
   0.5731961978256868 q[N05,exit02] - pi[N05] + pi[exit02]
   + 30 x[N05,exit02]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_upper[N05,exit02] <= 60
 UB_for__PDAI_var_at_arcs_upper[N05,exit03]:
   0.5731961978256868 q[N05,exit03] - pi[N05] + pi[exit03]
   + 30 x[N05,exit03]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_upper[N05,exit03] <= 60
 UB_for__PDAI_var_at_arcs_upper[entry03,N01]: 1e-05 q[entry03,N01]
   + pi[N01] - pi[entry03] + 30 x[entry03,N01]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_upper[entry03,N01] <= 60
 UB_for__PDAI_var_at_arcs_upper[N04,N05]: 1e-05 q[N04,N05] - pi[N04]
   + pi[N05] + 30 x[N04,N05]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_upper[N04,N05] <= 60
 UB_for__PDAI_var_at_arcs_upper[N01,N03]: 1e-05 q[N01,N03] - pi[N01]
   + pi[N03] + 30 x[N01,N03]
   + 60 binary_var_for__dual_PDAI_var_at_arcs_upper[N01,N03] <= 60
 UB_for__pressure_var_at_nodes_lower[N01]: pi[N01]
   + 30 binary_var_for__dual_pressure_var_at_nodes_lower[N01] <= 70
 UB_for__pressure_var_at_nodes_lower[N02]: pi[N02]
   + 30 binary_var_for__dual_pressure_var_at_nodes_lower[N02] <= 70
 UB_for__pressure_var_at_nodes_lower[N03]: pi[N03]
   + 30 binary_var_for__dual_pressure_var_at_nodes_lower[N03] <= 70
 UB_for__pressure_var_at_nodes_lower[N04]: pi[N04]
   + 30 binary_var_for__dual_pressure_var_at_nodes_lower[N04] <= 70
 UB_for__pressure_var_at_nodes_lower[N05]: pi[N05]
   + 30 binary_var_for__dual_pressure_var_at_nodes_lower[N05] <= 70
 UB_for__pressure_var_at_nodes_lower[entry01]: pi[entry01]
   + 30 binary_var_for__dual_pressure_var_at_nodes_lower[entry01] <= 70
 UB_for__pressure_var_at_nodes_lower[entry03]: pi[entry03]
   + 30 binary_var_for__dual_pressure_var_at_nodes_lower[entry03] <= 70
 UB_for__pressure_var_at_nodes_lower[entry02]: pi[entry02]
   + 30 binary_var_for__dual_pressure_var_at_nodes_lower[entry02] <= 70
 UB_for__pressure_var_at_nodes_lower[exit01]: pi[exit01]
   + 30 binary_var_for__dual_pressure_var_at_nodes_lower[exit01] <= 70
 UB_for__pressure_var_at_nodes_lower[exit02]: pi[exit02]
   + 30 binary_var_for__dual_pressure_var_at_nodes_lower[exit02] <= 70
 UB_for__pressure_var_at_nodes_lower[exit03]: pi[exit03]
   + 30 binary_var_for__dual_pressure_var_at_nodes_lower[exit03] <= 70
 UB_for__pressure_var_at_nodes_upper[N01]: - pi[N01]
   + 30 binary_var_for__dual_pressure_var_at_nodes_upper[N01] <= -40
 UB_for__pressure_var_at_nodes_upper[N02]: - pi[N02]
   + 30 binary_var_for__dual_pressure_var_at_nodes_upper[N02] <= -40
 UB_for__pressure_var_at_nodes_upper[N03]: - pi[N03]
   + 30 binary_var_for__dual_pressure_var_at_nodes_upper[N03] <= -40
 UB_for__pressure_var_at_nodes_upper[N04]: - pi[N04]
   + 30 binary_var_for__dual_pressure_var_at_nodes_upper[N04] <= -40
 UB_for__pressure_var_at_nodes_upper[N05]: - pi[N05]
   + 30 binary_var_for__dual_pressure_var_at_nodes_upper[N05] <= -40
 UB_for__pressure_var_at_nodes_upper[entry01]: - pi[entry01]
   + 30 binary_var_for__dual_pressure_var_at_nodes_upper[entry01] <= -40
 UB_for__pressure_var_at_nodes_upper[entry03]: - pi[entry03]
   + 30 binary_var_for__dual_pressure_var_at_nodes_upper[entry03] <= -40
 UB_for__pressure_var_at_nodes_upper[entry02]: - pi[entry02]
   + 30 binary_var_for__dual_pressure_var_at_nodes_upper[entry02] <= -40
 UB_for__pressure_var_at_nodes_upper[exit01]: - pi[exit01]
   + 30 binary_var_for__dual_pressure_var_at_nodes_upper[exit01] <= -40
 UB_for__pressure_var_at_nodes_upper[exit02]: - pi[exit02]
   + 30 binary_var_for__dual_pressure_var_at_nodes_upper[exit02] <= -30
 UB_for__pressure_var_at_nodes_upper[exit03]: - pi[exit03]
   + 30 binary_var_for__dual_pressure_var_at_nodes_upper[exit03] <= -30
 UB_for__loadshed_var_at_exit_nodes_lower[exit01]: lambda[exit01]
   + binary_var_for__dual_loadshed_var_at_exit_nodes_lower[exit01] <= 1
 UB_for__loadshed_var_at_exit_nodes_lower[exit02]: lambda[exit02]
   + binary_var_for__dual_loadshed_var_at_exit_nodes_lower[exit02] <= 1
 UB_for__loadshed_var_at_exit_nodes_lower[exit03]: lambda[exit03]
   + binary_var_for__dual_loadshed_var_at_exit_nodes_lower[exit03] <= 1
 UB_for__loadshed_var_at_exit_nodes_upper[exit01]: - lambda[exit01]
   + binary_var_for__dual_loadshed_var_at_exit_nodes_upper[exit01] <= 0
 UB_for__loadshed_var_at_exit_nodes_upper[exit02]: - lambda[exit02]
   + binary_var_for__dual_loadshed_var_at_exit_nodes_upper[exit02] <= 0
 UB_for__loadshed_var_at_exit_nodes_upper[exit03]: - lambda[exit03]
   + binary_var_for__dual_loadshed_var_at_exit_nodes_upper[exit03] <= 0
 UB_for__loadshed_var_at_entry_nodes_lower[entry01]: lambda[entry01]
   + 4.6875 binary_var_for__dual_loadshed_var_at_entry_nodes_lower[entry01]
   <= 1
 UB_for__loadshed_var_at_entry_nodes_lower[entry03]: lambda[entry03]
   + 4.6875 binary_var_for__dual_loadshed_var_at_entry_nodes_lower[entry03]
   <= 4.6875
 UB_for__loadshed_var_at_entry_nodes_lower[entry02]: lambda[entry02]
   + 4.6875 binary_var_for__dual_loadshed_var_at_entry_nodes_lower[entry02]
   <= 2.116071428571429
 UB_for__loadshed_var_at_entry_nodes_upper[entry01]: - lambda[entry01]
   + 4.6875 binary_var_for__dual_loadshed_var_at_entry_nodes_upper[entry01]
   <= 3.6875
 UB_for__loadshed_var_at_entry_nodes_upper[entry03]: - lambda[entry03]
   + 4.6875 binary_var_for__dual_loadshed_var_at_entry_nodes_upper[entry03]
   <= 3.6875
 UB_for__loadshed_var_at_entry_nodes_upper[entry02]: - lambda[entry02]
   + 4.6875 binary_var_for__dual_loadshed_var_at_entry_nodes_upper[entry02]
   <= 3.6875
 WCcheck_constraints[N01]: f[N01,N02] - f[entry03,N01] + f[N01,N03] = -1
 WCcheck_constraints[N02]: - f[N01,N02] + f[N02,exit01] + f[N02,N04] = -1
 WCcheck_constraints[N03]: - f[entry02,N03] + f[N03,N04] - f[N01,N03] = -1
 WCcheck_constraints[N04]: - f[N02,N04] - f[N03,N04] + f[N04,N05] = -1
 WCcheck_constraints[N05]: f[N05,exit02] + f[N05,exit03] - f[N04,N05] = -1
 WCcheck_constraints[entry01]: f[entry01,entry03] = 10
 WCcheck_constraints[entry03]: - f[entry01,entry03] + f[entry03,N01] = -1
 WCcheck_constraints[entry02]: f[entry02,N03] = -1
 WCcheck_constraints[exit01]: - f[N02,exit01] = -1
 WCcheck_constraints[exit02]: - f[N05,exit02] = -1
 WCcheck_constraints[exit03]: - f[N05,exit03] = -1
 R272: x[entry01,entry03] + x[N01,N02] + x[entry02,N03] + x[N02,exit01]
   + x[N02,N04] + x[N03,N04] + x[N05,exit02] + x[N05,exit03]
   + x[entry03,N01] + x[N04,N05] + x[N01,N03] <= 0
 qc0: [ x[entry01,entry03] * f[entry01,entry03] ] = 0
 qc1: [ x[N01,N02] * f[N01,N02] ] = 0
 qc2: [ x[entry02,N03] * f[entry02,N03] ] = 0
 qc3: [ x[N02,exit01] * f[N02,exit01] ] = 0
 qc4: [ x[N02,N04] * f[N02,N04] ] = 0
 qc5: [ x[N03,N04] * f[N03,N04] ] = 0
 qc6: [ x[N05,exit02] * f[N05,exit02] ] = 0
 qc7: [ x[N05,exit03] * f[N05,exit03] ] = 0
 qc8: [ x[entry03,N01] * f[entry03,N01] ] = 0
 qc9: [ x[N04,N05] * f[N04,N05] ] = 0
 qc10: [ x[N01,N03] * f[N01,N03] ] = 0
Bounds
 lambda[N01] = 0
 lambda[N02] = 0
 lambda[N03] = 0
 lambda[N04] = 0
 lambda[N05] = 0
 -3.6875 <= lambda[entry01] <= 1
 lambda[entry03] <= 1
 -2.571428571428571 <= lambda[entry02] <= 1
 lambda[exit01] <= 1
 lambda[exit02] <= 1
 lambda[exit03] <= 1
 q[entry01,entry03] free
 q[N01,N02] free
 q[entry02,N03] free
 q[N02,exit01] free
 q[N02,N04] free
 q[N03,N04] free
 q[N05,exit02] free
 q[N05,exit03] free
 q[entry03,N01] free
 q[N04,N05] free
 q[N01,N03] free
 40 <= pi[N01] <= 70
 40 <= pi[N02] <= 70
 40 <= pi[N03] <= 70
 40 <= pi[N04] <= 70
 40 <= pi[N05] <= 70
 40 <= pi[entry01] <= 70
 40 <= pi[entry03] <= 70
 40 <= pi[entry02] <= 70
 40 <= pi[exit01] <= 70
 40 <= pi[exit02] <= 60
 40 <= pi[exit03] <= 60
 alpha[N01] free
 alpha[N02] free
 alpha[N03] free
 alpha[N04] free
 alpha[N05] free
 alpha[entry01] free
 alpha[entry03] free
 alpha[entry02] free
 alpha[exit01] free
 alpha[exit02] free
 alpha[exit03] free
 f[entry01,entry03] free
 f[N01,N02] free
 f[entry02,N03] free
 f[N02,exit01] free
 f[N02,N04] free
 f[N03,N04] free
 f[N05,exit02] free
 f[N05,exit03] free
 f[entry03,N01] free
 f[N04,N05] free
 f[N01,N03] free
Binaries
 x[entry01,entry03] x[N01,N02] x[entry02,N03] x[N02,exit01] x[N02,N04]
 x[N03,N04] x[N05,exit02] x[N05,exit03] x[entry03,N01] x[N04,N05]
 x[N01,N03] binary_var_for__dual_flow_var_at_arcs_lower[entry01,entry03]
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
