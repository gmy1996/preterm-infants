# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 23:39:59 2021

@author: admin
"""

import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl


class FIS:
    def input(self, gest, bw, female, MAS, multip, lv3):
        self.gest = gest
        self.bw = bw
        self.female = female
        self.MAS = MAS
        self.multip = multip
        self.lv3 = lv3

        self.run()
        return self.op

    def run(self):

        x_gest_range = np.arange(22, 32.01, 0.01)
        x_birthweight_range = np.arange(400, 1200.01, 0.01)
        x_female_range = np.arange(0, 2, 1)
        x_MAS_range = np.arange(0, 2, 1)
        x_multip_range = np.arange(0, 2, 1)
        x_lv3_range = np.arange(0, 2, 1)

        y_survival_range = np.arange(0, 101, 1)

        # 创建模糊控制变量
        x_gest = ctrl.Antecedent(x_gest_range, 'gest')
        x_birthweight = ctrl.Antecedent(x_birthweight_range, 'birthweight')
        x_female = ctrl.Antecedent(x_female_range, 'female')
        x_MAS = ctrl.Antecedent(x_MAS_range, 'MAS')
        x_multip = ctrl.Antecedent(x_multip_range, 'multip')
        x_lv3 = ctrl.Antecedent(x_lv3_range, 'lv3')

        y_survival = ctrl.Consequent(y_survival_range, 'survival')

        # 定义模糊集和其隶属度函数
        x_gest['1_Early'] = fuzz.trimf(x_gest_range, [21.9, 21.9, 24.05])
        x_gest['2_Early'] = fuzz.trimf(x_gest_range, [21.9, 24.05, 26.12])
        x_gest['3_Early'] = fuzz.trimf(x_gest_range, [24.05, 26.12, 27.85])
        x_gest['4_Early'] = fuzz.trimf(x_gest_range, [26.12, 27.85, 32.1])
        x_gest['5_Early'] = fuzz.trimf(x_gest_range, [27.85, 32.1, 32.1])

        x_birthweight['1_Light_male'] = fuzz.trimf(
            x_birthweight_range, [399, 399, 653.7])
        x_birthweight['2_Light_male'] = fuzz.trimf(
            x_birthweight_range, [399, 653.7, 846.4])
        x_birthweight['3_Light_male'] = fuzz.trimf(
            x_birthweight_range, [653.7, 846.4, 986.3])
        x_birthweight['4_Light_male'] = fuzz.trimf(
            x_birthweight_range, [846.4, 986.3, 1201])
        x_birthweight['5_Light_male'] = fuzz.trimf(
            x_birthweight_range, [986.3, 1201, 1201])

        x_birthweight['1_Light_female'] = fuzz.trimf(
            x_birthweight_range, [399, 399, 570.7])
        x_birthweight['2_Light_female'] = fuzz.trimf(
            x_birthweight_range, [399, 570.7, 782])
        x_birthweight['3_Light_female'] = fuzz.trimf(
            x_birthweight_range, [570.7, 782, 961.1])
        x_birthweight['4_Light_female'] = fuzz.trimf(
            x_birthweight_range, [782, 961.1, 1201])
        x_birthweight['5_Light_female'] = fuzz.trimf(
            x_birthweight_range, [961.1, 1201, 1201])

        x_female['no'] = fuzz.trimf(x_female_range, [0, 0, 0])
        x_female['yes'] = fuzz.trimf(x_female_range, [1, 1, 1])

        x_MAS['incomplete treatment'] = fuzz.trimf(x_MAS_range, [0, 0, 0])
        x_MAS['complete treatment'] = fuzz.trimf(x_MAS_range, [1, 1, 1])

        x_multip['no'] = fuzz.trimf(x_multip_range, [0, 0, 0])
        x_multip['yes'] = fuzz.trimf(x_multip_range, [1, 1, 1])

        x_lv3['no'] = fuzz.trimf(x_lv3_range, [0, 0, 0])
        x_lv3['yes'] = fuzz.trimf(x_lv3_range, [1, 1, 1])

        y_survival['very low'] = fuzz.trimf(y_survival_range, [0, 0, 15])
        y_survival['low'] = fuzz.trimf(y_survival_range, [0, 16, 32])
        y_survival['median_incompleteMAS'] = fuzz.trimf(
            y_survival_range, [32, 45, 64])
        y_survival['median_completeMAS'] = fuzz.trimf(
            y_survival_range, [32, 62, 67])
        y_survival['high'] = fuzz.trimf(y_survival_range, [64, 95, 100])
        y_survival['very high'] = fuzz.trimf(y_survival_range, [96, 100, 100])

        # 设定输出powder的解模糊方法——质心解模糊方式
        y_survival.defuzzify_method = 'centroid'

        # 输出为very low的规则
        rule1 = ctrl.Rule(antecedent=((x_gest['1_Early'] & x_MAS['incomplete treatment']) |
                                      (x_gest['1_Early'] & x_MAS['complete treatment'] & x_lv3['no']) |
                                      # male
                                      (x_birthweight['1_Light_male'] & x_female['no'] & x_MAS['incomplete treatment']) |
                                      (x_birthweight['1_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_lv3['no']) |
                                      # female
                                      (x_birthweight['1_Light_female'] & x_female['yes'] & x_MAS['incomplete treatment']) |
                                      (x_birthweight['1_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_lv3['no'])),
                          consequent=y_survival['very low'], label='rule VeryLow')

        # 输出为low的规则
        rule2 = ctrl.Rule(antecedent=((x_gest['1_Early'] & x_MAS['complete treatment'] & x_lv3['yes']) |
                                      # male
                                      (x_birthweight['1_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_lv3['yes']) |
                                      (x_gest['2_Early'] & x_birthweight['2_Light_male'] & x_female['no'] & x_MAS['incomplete treatment']) |
                                      (x_gest['2_Early'] & x_birthweight['2_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_lv3['no']) |
                                      (x_gest['2_Early'] & x_birthweight['3_Light_male'] & x_female['no'] & x_MAS['incomplete treatment'] & x_multip['yes']) |
                                      (x_gest['2_Early'] & x_birthweight['3_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_multip['yes'] & x_lv3['no']) |
                                      (x_gest['2_Early'] & x_birthweight['4_Light_male'] & x_female['no'] & x_multip['yes'] & x_lv3['no']) |
                                      (x_gest['3_Early'] & x_birthweight['2_Light_male'] & x_female['no'] & x_multip['yes'] & x_lv3['no']) |
                                      # female
                                      (x_birthweight['1_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_lv3['yes']) |
                                      (x_gest['2_Early'] & x_birthweight['2_Light_female'] & x_female['yes'] & x_MAS['incomplete treatment']) |
                                      (x_gest['2_Early'] & x_birthweight['2_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_lv3['no']) |
                                      (x_gest['2_Early'] & x_birthweight['3_Light_female'] & x_female['yes'] & x_MAS['incomplete treatment'] & x_multip['yes']) |
                                      (x_gest['2_Early'] & x_birthweight['3_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_multip['yes'] & x_lv3['no']) |
                                      (x_gest['2_Early'] & x_birthweight['4_Light_female'] & x_female['yes'] & x_multip['yes'] & x_lv3['no']) |
                                      (x_gest['3_Early'] & x_birthweight['2_Light_female'] & x_female['yes'] & x_multip['yes'] & x_lv3['no'])),
                          consequent=y_survival['low'], label='rule Low')

        # 输出为median_incompleteMAS的规则
        rule3 = ctrl.Rule(antecedent=(  # male
            (x_gest['2_Early'] & x_birthweight['3_Light_male'] & x_female['no'] & x_MAS['incomplete treatment'] & x_multip['no']) |
            (x_gest['2_Early'] & x_birthweight['4_Light_male'] & x_female['no'] & x_MAS['incomplete treatment'] & x_multip['yes'] & x_lv3['yes']) |
            (x_gest['2_Early'] & x_birthweight['4_Light_male'] & x_female['no'] & x_MAS['incomplete treatment'] & x_multip['no']) |
            (x_gest['3_Early'] & x_birthweight['2_Light_male'] & x_female['no'] & x_MAS['incomplete treatment'] & x_multip['yes'] & x_lv3['yes']) |
            (x_gest['3_Early'] & x_birthweight['2_Light_male'] & x_female['no'] & x_MAS['incomplete treatment'] & x_multip['no']) |
            (x_gest['3_Early'] & x_birthweight['3_Light_male'] & x_female['no'] & x_MAS['incomplete treatment'] & x_multip['yes']) |
            (x_gest['3_Early'] & x_birthweight['3_Light_male'] & x_female['no'] & x_MAS['incomplete treatment'] & x_multip['no'] & x_lv3['no']) |
            (x_gest['3_Early'] & x_birthweight['4_Light_male'] & x_female['no'] & x_MAS['incomplete treatment'] & x_multip['yes']) |
            (x_gest['4_Early'] & x_birthweight['2_Light_male'] & x_female['no'] & x_MAS['incomplete treatment']) |
            (x_gest['4_Early'] & x_birthweight['3_Light_male'] & x_female['no'] & x_MAS['incomplete treatment'] & x_multip['yes']) |
            (x_gest['4_Early'] & x_birthweight['4_Light_male'] & x_female['no'] & x_MAS['incomplete treatment'] & x_multip['yes'] & x_lv3['no']) |
            # female
            (x_gest['2_Early'] & x_birthweight['3_Light_female'] & x_female['yes'] & x_MAS['incomplete treatment'] & x_multip['no']) |
            (x_gest['2_Early'] & x_birthweight['4_Light_female'] & x_female['yes'] & x_MAS['incomplete treatment'] & x_multip['yes'] & x_lv3['yes']) |
            (x_gest['2_Early'] & x_birthweight['4_Light_female'] & x_female['yes'] & x_MAS['incomplete treatment'] & x_multip['no']) |
            (x_gest['3_Early'] & x_birthweight['2_Light_female'] & x_female['yes'] & x_MAS['incomplete treatment'] & x_multip['yes'] & x_lv3['yes']) |
            (x_gest['3_Early'] & x_birthweight['2_Light_female'] & x_female['yes'] & x_MAS['incomplete treatment'] & x_multip['no']) |
            (x_gest['3_Early'] & x_birthweight['3_Light_female'] & x_female['yes'] & x_MAS['incomplete treatment'] & x_multip['yes']) |
            (x_gest['3_Early'] & x_birthweight['3_Light_female'] & x_female['yes'] & x_MAS['incomplete treatment'] & x_multip['no'] & x_lv3['no']) |
            (x_gest['3_Early'] & x_birthweight['4_Light_female'] & x_female['yes'] & x_MAS['incomplete treatment'] & x_multip['yes']) |
            (x_gest['4_Early'] & x_birthweight['2_Light_female'] & x_female['yes'] & x_MAS['incomplete treatment']) |
            (x_gest['4_Early'] & x_birthweight['3_Light_female'] & x_female['yes'] & x_MAS['incomplete treatment'] & x_multip['yes']) |
            (x_gest['4_Early'] & x_birthweight['4_Light_female'] & x_female['yes'] & x_MAS['incomplete treatment'] & x_multip['yes'] & x_lv3['no'])),
            consequent=y_survival['median_incompleteMAS'], label='rule Median_incompleteMAS')

        # 输出为median_completeMAS的规则
        rule4 = ctrl.Rule(antecedent=(  # male
            (x_gest['2_Early'] & x_birthweight['2_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_lv3['yes']) |
            (x_gest['2_Early'] & x_birthweight['3_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_multip['yes'] & x_lv3['yes']) |
            (x_gest['2_Early'] & x_birthweight['3_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_multip['no'] & x_lv3['no']) |
            (x_gest['2_Early'] & x_birthweight['4_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_multip['yes'] & x_lv3['yes']) |
            (x_gest['2_Early'] & x_birthweight['4_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_multip['no'] & x_lv3['no']) |
            (x_gest['3_Early'] & x_birthweight['2_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_multip['yes'] & x_lv3['yes']) |
            (x_gest['3_Early'] & x_birthweight['2_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_multip['no'] & x_lv3['no']) |
            (x_gest['3_Early'] & x_birthweight['3_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_multip['yes'] & x_lv3['no']) |
            (x_gest['3_Early'] & x_birthweight['4_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_multip['yes'] & x_lv3['no']) |
            (x_gest['4_Early'] & x_birthweight['2_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_multip['yes']) |
            (x_gest['4_Early'] & x_birthweight['3_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_multip['yes'] & x_lv3['no']) |
            # female
            (x_gest['2_Early'] & x_birthweight['2_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_lv3['yes']) |
            (x_gest['2_Early'] & x_birthweight['3_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_multip['yes'] & x_lv3['yes']) |
            (x_gest['2_Early'] & x_birthweight['3_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_multip['no'] & x_lv3['no']) |
            (x_gest['2_Early'] & x_birthweight['4_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_multip['yes'] & x_lv3['yes']) |
            (x_gest['2_Early'] & x_birthweight['4_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_multip['no'] & x_lv3['no']) |
            (x_gest['3_Early'] & x_birthweight['2_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_multip['yes'] & x_lv3['yes']) |
            (x_gest['3_Early'] & x_birthweight['2_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_multip['no'] & x_lv3['no']) |
            (x_gest['3_Early'] & x_birthweight['3_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_multip['yes'] & x_lv3['no']) |
            (x_gest['3_Early'] & x_birthweight['4_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_multip['yes'] & x_lv3['no']) |
            (x_gest['4_Early'] & x_birthweight['2_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_multip['yes']) |
            (x_gest['4_Early'] & x_birthweight['3_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_multip['yes'] & x_lv3['no'])),
            consequent=y_survival['median_completeMAS'], label='rule Median_completeMAS')

        # 输出为high的规则
        rule5 = ctrl.Rule(antecedent=(  # male
            (x_gest['2_Early'] & x_birthweight['3_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_multip['no'] & x_lv3['yes']) |
            (x_gest['2_Early'] & x_birthweight['4_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_multip['no'] & x_lv3['yes']) |
            (x_gest['3_Early'] & x_birthweight['2_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_multip['no'] & x_lv3['yes']) |
            (x_gest['3_Early'] & x_birthweight['3_Light_male'] & x_female['no'] & x_MAS['incomplete treatment'] & x_multip['no'] & x_lv3['yes']) |
            (x_gest['3_Early'] & x_birthweight['3_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_multip['yes'] & x_lv3['yes']) |
            (x_gest['3_Early'] & x_birthweight['3_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_multip['no']) |
            (x_gest['3_Early'] & x_birthweight['4_Light_male'] & x_female['no'] & x_MAS['incomplete treatment'] & x_multip['no']) |
            (x_gest['3_Early'] & x_birthweight['4_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_multip['yes'] & x_lv3['yes']) |
            (x_gest['3_Early'] & x_birthweight['4_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_multip['no']) |
            (x_gest['4_Early'] & x_birthweight['2_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_multip['no']) |
            (x_gest['4_Early'] & x_birthweight['3_Light_male'] & x_female['no'] & x_MAS['complete treatment'] & x_multip['yes'] & x_lv3['yes']) |
            (x_gest['4_Early'] & x_birthweight['3_Light_male'] & x_female['no'] & x_multip['no']) |
            (x_gest['4_Early'] & x_birthweight['4_Light_male'] & x_female['no'] & x_MAS['incomplete treatment'] & x_multip['yes'] & x_lv3['yes']) |
            (x_gest['4_Early'] & x_birthweight['4_Light_male'] & x_female['no'] & x_MAS['incomplete treatment'] & x_multip['no']) |
            (x_gest['4_Early'] & x_birthweight['4_Light_male'] & x_female['no'] & x_MAS['complete treatment']) |
            (x_birthweight['5_Light_male'] & x_female['no'] & x_MAS['incomplete treatment'] & x_lv3['no']) |
            # female
            (x_gest['2_Early'] & x_birthweight['3_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_multip['no'] & x_lv3['yes']) |
            (x_gest['2_Early'] & x_birthweight['4_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_multip['no'] & x_lv3['yes']) |
            (x_gest['3_Early'] & x_birthweight['2_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_multip['no'] & x_lv3['yes']) |
            (x_gest['3_Early'] & x_birthweight['3_Light_female'] & x_female['yes'] & x_MAS['incomplete treatment'] & x_multip['no'] & x_lv3['yes']) |
            (x_gest['3_Early'] & x_birthweight['3_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_multip['yes'] & x_lv3['yes']) |
            (x_gest['3_Early'] & x_birthweight['3_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_multip['no']) |
            (x_gest['3_Early'] & x_birthweight['4_Light_female'] & x_female['yes'] & x_MAS['incomplete treatment'] & x_multip['no']) |
            (x_gest['3_Early'] & x_birthweight['4_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_multip['yes'] & x_lv3['yes']) |
            (x_gest['3_Early'] & x_birthweight['4_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_multip['no']) |
            (x_gest['4_Early'] & x_birthweight['2_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_multip['no']) |
            (x_gest['4_Early'] & x_birthweight['3_Light_female'] & x_female['yes'] & x_MAS['complete treatment'] & x_multip['yes'] & x_lv3['yes']) |
            (x_gest['4_Early'] & x_birthweight['3_Light_female'] & x_female['yes'] & x_multip['no']) |
            (x_gest['4_Early'] & x_birthweight['4_Light_female'] & x_female['yes'] & x_MAS['incomplete treatment'] & x_multip['yes'] & x_lv3['yes']) |
            (x_gest['4_Early'] & x_birthweight['4_Light_female'] & x_female['yes'] & x_MAS['incomplete treatment'] & x_multip['no']) |
            (x_gest['4_Early'] & x_birthweight['4_Light_female'] & x_female['yes'] & x_MAS['complete treatment']) |
            (x_birthweight['5_Light_female'] & x_female['yes'] & x_MAS['incomplete treatment'] & x_lv3['no'])),
            consequent=y_survival['high'], label='rule High')

        # 输出为very high的规则
        rule6 = ctrl.Rule(antecedent=((x_gest['5_Early'] & x_MAS['incomplete treatment'] & x_lv3['yes']) |
                                      (x_gest['5_Early'] & x_MAS['complete treatment']) |
                                      # male
                                      (x_birthweight['5_Light_male'] & x_female['no'] & x_MAS['incomplete treatment'] & x_lv3['yes']) |
                                      (x_birthweight['5_Light_male'] & x_female['no'] & x_MAS['complete treatment']) |
                                      (x_birthweight['5_Light_male'] & x_female['no']) |
                                      # female
                                      (x_birthweight['5_Light_female'] & x_female['yes'] & x_MAS['incomplete treatment'] & x_lv3['yes']) |
                                      (x_birthweight['5_Light_female'] & x_female['yes'] & x_MAS['complete treatment'])),
                          consequent=y_survival['very high'], label='rule VeryHigh')

        # 系统和运行环境初始化
        system = ctrl.ControlSystem(
            rules=[rule1, rule2, rule3, rule4, rule5, rule6])
        sim = ctrl.ControlSystemSimulation(system)

        sim.input['gest'] = self.gest
        sim.input['birthweight'] = self.bw
        sim.input['female'] = self.female
        sim.input['MAS'] = self.MAS
        sim.input['multip'] = self.multip
        sim.input['lv3'] = self.lv3
        sim.compute()   # 运行系统
        self.op = round(sim.output['survival'], 2)

        self.output()

    def output(self):
        # 打印输出结果
        print(self.op)

