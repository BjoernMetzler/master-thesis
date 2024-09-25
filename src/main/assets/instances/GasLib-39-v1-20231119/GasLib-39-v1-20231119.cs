<?xml version="1.0" encoding="UTF-8"?>

<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -->
<!--                                                                                   -->
<!--   This file is part of the project MODAL-EnergyLab in the Research Campus MODAL   -->
<!--                      funded by the BMBF (05M14ZAM, 05M20ZBM)                      -->
<!--                                                                                   -->
<!-- Copyright (C) 2023                                                                -->
<!-- Zuse Institute Berlin                                                             -->
<!-- Contact: Thorsten Koch (koch@zib.de)                                              -->
<!-- All rights reserved.                                                              -->
<!--                                                                                   -->
<!-- This work is licensed under the Creative Commons Attribution 3.0 Unported License.-->
<!-- To view a copy of this license, visit http://creativecommons.org/licenses/by/3.0/ -->
<!-- or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View,-->
<!-- California, 94041, USA.                                                           -->
<!--                                                                                   -->
<!--                         Please note that you have to cite                         -->
<!-- F. Hennings, "Modeling and solving real-world transient gas network transport     -->
<!-- problems using mathematical programming",                                         -->
<!-- Doctoral Thesis, Technische Universität Berlin, 2023                              -->
<!--                               if you use this data                                -->
<!--                                                                                   -->
<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -->

<compressorStations xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xmlns="http://gaslib.zib.de/CompressorStations"
                    xsi:schemaLocation="http://gaslib.zib.de/CompressorStations
                                        http://gaslib.zib.de/schema/CompressorStations.xsd"
                    xmlns:gas="http://gaslib.zib.de/Gas"
                    xmlns:framework="http://gaslib.zib.de/CompressorStations">

  <compressorStation id="CS_NW">
    <compressors>
      <turboCompressor drive="P_T1001" id="T1001">
        <speedMin value="6000" unit="per_min"/>
        <speedMax value="12000" unit="per_min"/>
        <n_isoline_coeff_1 value="-43.93290049751657"/>
        <n_isoline_coeff_2 value="0.006760822313789693"/>
        <n_isoline_coeff_3 value="7.141677558127747e-08"/>
        <n_isoline_coeff_4 value="3.195761588245756"/>
        <n_isoline_coeff_5 value="-0.00025241047865835444"/>
        <n_isoline_coeff_6 value="1.77417023251214e-08"/>
        <n_isoline_coeff_7 value="1.1102230246251565e-16"/>
        <n_isoline_coeff_8 value="-3.333333333333336e-05"/>
        <n_isoline_coeff_9 value="1.5419764230904952e-24"/>
        <eta_ad_isoline_coeff_1 value="0.5093999999999994"/>
        <eta_ad_isoline_coeff_2 value="6.32666666666668e-05"/>
        <eta_ad_isoline_coeff_3 value="-4.97222222222223e-09"/>
        <eta_ad_isoline_coeff_4 value="0.00975000000000008"/>
        <eta_ad_isoline_coeff_5 value="2.358333333333315e-06"/>
        <eta_ad_isoline_coeff_6 value="1.4166666666666765e-10"/>
        <eta_ad_isoline_coeff_7 value="-0.0015"/>
        <eta_ad_isoline_coeff_8 value="-1.6666666666666668e-07"/>
        <eta_ad_isoline_coeff_9 value="0.0"/>
        <surgeline_coeff_1 value="-23.65665727324966"/>
        <surgeline_coeff_2 value="16.44730911212327"/>
        <surgeline_coeff_3 value="-0.1"/>
        <chokeline_coeff_1 value="-86.28514967121204"/>
        <chokeline_coeff_2 value="7.868818697735961"/>
        <chokeline_coeff_3 value="0.1"/>
      </turboCompressor>
      <turboCompressor drive="P_T1002" id="T1002">
        <speedMin value="6000" unit="per_min"/>
        <speedMax value="12000" unit="per_min"/>
        <n_isoline_coeff_1 value="-43.93290049751657"/>
        <n_isoline_coeff_2 value="0.006760822313789693"/>
        <n_isoline_coeff_3 value="7.141677558127747e-08"/>
        <n_isoline_coeff_4 value="3.195761588245756"/>
        <n_isoline_coeff_5 value="-0.00025241047865835444"/>
        <n_isoline_coeff_6 value="1.77417023251214e-08"/>
        <n_isoline_coeff_7 value="1.1102230246251565e-16"/>
        <n_isoline_coeff_8 value="-3.333333333333336e-05"/>
        <n_isoline_coeff_9 value="1.5419764230904952e-24"/>
        <eta_ad_isoline_coeff_1 value="0.5093999999999994"/>
        <eta_ad_isoline_coeff_2 value="6.32666666666668e-05"/>
        <eta_ad_isoline_coeff_3 value="-4.97222222222223e-09"/>
        <eta_ad_isoline_coeff_4 value="0.00975000000000008"/>
        <eta_ad_isoline_coeff_5 value="2.358333333333315e-06"/>
        <eta_ad_isoline_coeff_6 value="1.4166666666666765e-10"/>
        <eta_ad_isoline_coeff_7 value="-0.0015"/>
        <eta_ad_isoline_coeff_8 value="-1.6666666666666668e-07"/>
        <eta_ad_isoline_coeff_9 value="0.0"/>
        <surgeline_coeff_1 value="-23.65665727324966"/>
        <surgeline_coeff_2 value="16.44730911212327"/>
        <surgeline_coeff_3 value="-0.1"/>
        <chokeline_coeff_1 value="-86.28514967121204"/>
        <chokeline_coeff_2 value="7.868818697735961"/>
        <chokeline_coeff_3 value="0.1"/>
      </turboCompressor>
    </compressors>
    <drives>
      <gasDrivenMotor id="P_T1001">
        <energy_rate_fun_coeff_1 value="10399.3304223"/>
        <energy_rate_fun_coeff_2 value="2.83969382239"/>
        <energy_rate_fun_coeff_3 value="3.60541969571e-08"/>
        <power_fun_coeff_1 value="-2960.0"/>
        <power_fun_coeff_2 value="1.758"/>
        <power_fun_coeff_3 value="-5.65e-05"/>
      </gasDrivenMotor>
      <gasDrivenMotor id="P_T1002">
        <energy_rate_fun_coeff_1 value="10399.3304223"/>
        <energy_rate_fun_coeff_2 value="2.83969382239"/>
        <energy_rate_fun_coeff_3 value="3.60541969571e-08"/>
        <power_fun_coeff_1 value="-2960.0"/>
        <power_fun_coeff_2 value="1.758"/>
        <power_fun_coeff_3 value="-5.65e-05"/>
      </gasDrivenMotor>
    </drives>
    <configurations>
      <configuration confId="1" nrOfSerialStages="1">
        <stage stageNr="1" nrOfParallelUnits="1">
          <compressor id="T1001" nominalSpeed="8000"/>
        </stage>
      </configuration>
      <configuration confId="2" nrOfSerialStages="2">
        <stage stageNr="1" nrOfParallelUnits="1">
          <compressor id="T1001" nominalSpeed="8000"/>
        </stage>
        <stage stageNr="2" nrOfParallelUnits="1">
          <compressor id="T1002" nominalSpeed="8000"/>
        </stage>
      </configuration>
    </configurations>
  </compressorStation>

  <compressorStation id="CS_SE">
    <compressors>
      <turboCompressor drive="P_T2001" id="T2001">
        <speedMin value="6000" unit="per_min"/>
        <speedMax value="12000" unit="per_min"/>
        <n_isoline_coeff_1 value="-43.93290049751657"/>
        <n_isoline_coeff_2 value="0.006760822313789693"/>
        <n_isoline_coeff_3 value="7.141677558127747e-08"/>
        <n_isoline_coeff_4 value="3.195761588245756"/>
        <n_isoline_coeff_5 value="-0.00025241047865835444"/>
        <n_isoline_coeff_6 value="1.77417023251214e-08"/>
        <n_isoline_coeff_7 value="1.1102230246251565e-16"/>
        <n_isoline_coeff_8 value="-3.333333333333336e-05"/>
        <n_isoline_coeff_9 value="1.5419764230904952e-24"/>
        <eta_ad_isoline_coeff_1 value="0.5093999999999994"/>
        <eta_ad_isoline_coeff_2 value="6.32666666666668e-05"/>
        <eta_ad_isoline_coeff_3 value="-4.97222222222223e-09"/>
        <eta_ad_isoline_coeff_4 value="0.00975000000000008"/>
        <eta_ad_isoline_coeff_5 value="2.358333333333315e-06"/>
        <eta_ad_isoline_coeff_6 value="1.4166666666666765e-10"/>
        <eta_ad_isoline_coeff_7 value="-0.0015"/>
        <eta_ad_isoline_coeff_8 value="-1.6666666666666668e-07"/>
        <eta_ad_isoline_coeff_9 value="0.0"/>
        <surgeline_coeff_1 value="-23.65665727324966"/>
        <surgeline_coeff_2 value="16.44730911212327"/>
        <surgeline_coeff_3 value="-0.1"/>
        <chokeline_coeff_1 value="-86.28514967121204"/>
        <chokeline_coeff_2 value="7.868818697735961"/>
        <chokeline_coeff_3 value="0.1"/>
      </turboCompressor>
      <turboCompressor drive="P_T2002" id="T2002">
        <speedMin value="6000" unit="per_min"/>
        <speedMax value="12000" unit="per_min"/>
        <n_isoline_coeff_1 value="-43.93290049751657"/>
        <n_isoline_coeff_2 value="0.006760822313789693"/>
        <n_isoline_coeff_3 value="7.141677558127747e-08"/>
        <n_isoline_coeff_4 value="3.195761588245756"/>
        <n_isoline_coeff_5 value="-0.00025241047865835444"/>
        <n_isoline_coeff_6 value="1.77417023251214e-08"/>
        <n_isoline_coeff_7 value="1.1102230246251565e-16"/>
        <n_isoline_coeff_8 value="-3.333333333333336e-05"/>
        <n_isoline_coeff_9 value="1.5419764230904952e-24"/>
        <eta_ad_isoline_coeff_1 value="0.5093999999999994"/>
        <eta_ad_isoline_coeff_2 value="6.32666666666668e-05"/>
        <eta_ad_isoline_coeff_3 value="-4.97222222222223e-09"/>
        <eta_ad_isoline_coeff_4 value="0.00975000000000008"/>
        <eta_ad_isoline_coeff_5 value="2.358333333333315e-06"/>
        <eta_ad_isoline_coeff_6 value="1.4166666666666765e-10"/>
        <eta_ad_isoline_coeff_7 value="-0.0015"/>
        <eta_ad_isoline_coeff_8 value="-1.6666666666666668e-07"/>
        <eta_ad_isoline_coeff_9 value="0.0"/>
        <surgeline_coeff_1 value="-23.65665727324966"/>
        <surgeline_coeff_2 value="16.44730911212327"/>
        <surgeline_coeff_3 value="-0.1"/>
        <chokeline_coeff_1 value="-86.28514967121204"/>
        <chokeline_coeff_2 value="7.868818697735961"/>
        <chokeline_coeff_3 value="0.1"/>
      </turboCompressor>
    </compressors>
    <drives>
      <gasDrivenMotor id="P_T2001">
        <energy_rate_fun_coeff_1 value="10399.3304223"/>
        <energy_rate_fun_coeff_2 value="2.83969382239"/>
        <energy_rate_fun_coeff_3 value="3.60541969571e-08"/>
        <power_fun_coeff_1 value="-2960.0"/>
        <power_fun_coeff_2 value="1.758"/>
        <power_fun_coeff_3 value="-5.65e-05"/>
      </gasDrivenMotor>
      <gasDrivenMotor id="P_T2002">
        <energy_rate_fun_coeff_1 value="10399.3304223"/>
        <energy_rate_fun_coeff_2 value="2.83969382239"/>
        <energy_rate_fun_coeff_3 value="3.60541969571e-08"/>
        <power_fun_coeff_1 value="-2960.0"/>
        <power_fun_coeff_2 value="1.758"/>
        <power_fun_coeff_3 value="-5.65e-05"/>
      </gasDrivenMotor>
    </drives>
    <configurations>
      <configuration confId="1" nrOfSerialStages="1">
        <stage stageNr="1" nrOfParallelUnits="1">
          <compressor id="T2001" nominalSpeed="8000"/>
        </stage>
      </configuration>
      <configuration confId="2" nrOfSerialStages="2">
        <stage stageNr="1" nrOfParallelUnits="1">
          <compressor id="T2001" nominalSpeed="8000"/>
        </stage>
        <stage stageNr="2" nrOfParallelUnits="1">
          <compressor id="T2002" nominalSpeed="8000"/>
        </stage>
      </configuration>
    </configurations>
  </compressorStation>

</compressorStations>
