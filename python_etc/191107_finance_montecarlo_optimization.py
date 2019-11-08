# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 12:50:35 2019



@author: Donggeun Kwon (donggeun.kwon@gmail.com)

Cryptographic Algorithm Lab.
Graduate School of Information Security, Korea University

"""
import numpy as np
from datetime import date
import time

def original(n = 100):
    # n : 시뮬레이션 횟수, r : 이자율
    r = 0.0165;
    #아마존 변동성 : 29.78% , 엔비디아 변동성 : 48.44%
    x_vol = 0.2978; y_vol = 0.4844;
    #최초기준가격평가일 : 2019.10.11.
    #만기일 : 2020.4.2
    n0 = date.toordinal(date(2019, 10, 11));
    n1 = date.toordinal(date(2019, 11, 6));
    n2 = date.toordinal(date(2019, 12, 6));
    n3 = date.toordinal(date(2020, 1, 7));
    n4 = date.toordinal(date(2020, 2, 6));
    n5 = date.toordinal(date(2020, 3, 6));
    n6 = date.toordinal(date(2020, 4, 2));
    #월수익지급평가일 벡터
    check_day = np.array([n1-n0, n2-n0, n3-n0,\
                          n4-n0, n5-n0, n6-n0]);
    #아마존, 엔비디아 일별수익률 간의 상관계수 : 0.5678
    rho = 0.5678;
    #촐레스키 분해를 사용하기 위한 상관계수 행렬
    corr = np.array([[1, rho], [rho, 1]]);
    #chol 함수를 이용하여 촐레스키 분해
    k = np.linalg.cholesky(corr);
    #쿠폰투자수익률 : 0.8425%
    coupon_rate = 0.008425;
    #1년의 일수
    oneyear = 365;
    #만기
    tot_date = n6-n0;
    #시간 격차 간격
    dt = 1/oneyear;
    #두 자산 벡터
    S1 = np.zeros((tot_date+1, 1));
    S2 = np.zeros((tot_date+1, 1));
    #기초 자산의 초깃값
    S1[0] = 100; S2[0] = 100;
    #초깃값 저장
    ratio_S1 = S1[0]; ratio_S2 = S2[0];
    #월수익지급평가일 횟수
    repay_n = len(check_day);
    #액면금액
    face_value = 10**4;
    #낙인 배리어
    kib = 0.70;
    #전체 페이오프 가치
    tot_payoff = 0;
    #만기 시 총 쿠폰 가치
    sumpayment = 0;
    for i in range(repay_n):
        sumpayment = sumpayment + face_value*coupon_rate\
        *np.exp(r*(tot_date-check_day[i])/oneyear);
    #몬테카를로 시뮬레이션을 이용한 ELS 가격 결정
    for i in range(n):
        w0 = np.random.normal(0, 1,size = [2 , tot_date])
        w = np.matmul(k,w0);
        for j in range(tot_date):
            S1[j + 1] = S1[j] * np.exp((r - 0.5*x_vol**2)\
              *dt + x_vol*np.sqrt(dt)*w[0,j]);
            S2[j + 1] = S2[j] * np.exp((r - 0.5*y_vol**2)\
              *dt + y_vol*np.sqrt(dt)*w[1,j]);
        R1 = S1/ratio_S1; R2 = S2/ratio_S2;
        WP = np.minimum(R1,R2);
        payoff = 0;
    #만약 두 기초자산의 만기가격이 최초가격의 100%이상인 경우
    #[70%]미만으로 하락한 적이 없는 경우
    #만기때 원금지급
    #두 경우에 포함되지 않을 시 실물인도(1주 미만 현금지급)
        if min(S1[tot_date],S2[tot_date]) >= 100:
            payoff = sumpayment + face_value
        else:
            if min(WP) >= kib:
                payoff = sumpayment + face_value;
            else:
                payoff = sumpayment + min(S1[tot_date]/ratio_S1,S2[tot_date]/ratio_S2)*face_value;
    #시뮬레이션마다 페이오프를 더함
        tot_payoff = tot_payoff + payoff;
    #모든 시뮬레이션의 페이오프의 평균을 구함
    mean_payoff = tot_payoff/n;
    #ELS 현재 가격을 구함
    price = mean_payoff * np.exp(-r * tot_date/oneyear);
    
    return price

def optimal(n = 100):
    # n : 시뮬레이션 횟수, r : 이자율
    r = 0.0165;
    #아마존 변동성 : 29.78% , 엔비디아 변동성 : 48.44%
    x_vol = 0.2978; y_vol = 0.4844;
    #최초기준가격평가일 : 2019.10.11.
    #만기일 : 2020.4.2
    n0 = date.toordinal(date(2019, 10, 11));
    n1 = date.toordinal(date(2019, 11, 6));
    n2 = date.toordinal(date(2019, 12, 6));
    n3 = date.toordinal(date(2020, 1, 7));
    n4 = date.toordinal(date(2020, 2, 6));
    n5 = date.toordinal(date(2020, 3, 6));
    n6 = date.toordinal(date(2020, 4, 2));
    #월수익지급평가일 벡터
    check_day = np.array([n1-n0, n2-n0, n3-n0,\
                          n4-n0, n5-n0, n6-n0]);
    #아마존, 엔비디아 일별수익률 간의 상관계수 : 0.5678
    rho = 0.5678;
    #촐레스키 분해를 사용하기 위한 상관계수 행렬
    corr = np.array([[1, rho], [rho, 1]]);
    #chol 함수를 이용하여 촐레스키 분해
    k = np.linalg.cholesky(corr);
    #쿠폰투자수익률 : 0.8425%
    coupon_rate = 0.008425;
    #1년의 일수
    oneyear = 365;
    #만기
    tot_date = n6-n0;
    #시간 격차 간격
    dt = 1/oneyear;
    #두 자산 벡터
    S1 = np.zeros((tot_date+1, 1));
    S2 = np.zeros((tot_date+1, 1));
    #기초 자산의 초깃값
    S1[0] = 100; S2[0] = 100;
    #초깃값 저장
    ratio_S1 = S1[0]; ratio_S2 = S2[0];
    #월수익지급평가일 횟수
    # repay_n = len(check_day);
    #액면금액
    face_value = 10**4;
    #낙인 배리어
    kib = 0.70;
    #전체 페이오프 가치
    tot_payoff = 0;
    #만기 시 총 쿠폰 가치
    sumpayment = np.sum(face_value * coupon_rate * np.exp(r*(tot_date-check_day) / oneyear));
        
    #case 2
    #몬테카를로 시뮬레이션을 이용한 ELS 가격 결정
    w0 = np.random.normal(0, 1, size = [n, 2 , tot_date])    
    w = np.matmul(k, w0);
    
    S1 = np.zeros((n, tot_date+1)); S1[:, 0] = 100;
    S2 = np.zeros((n, tot_date+1)); S2[:, 0] = 100;
    
    for j in range(tot_date):
        S1[:, j + 1] = S1[:, j] * np.exp((r - 0.5*x_vol**2) * dt + x_vol * np.sqrt(dt) * w[:, 0, j]);
        S2[:, j + 1] = S2[:, j] * np.exp((r - 0.5*y_vol**2) * dt + y_vol * np.sqrt(dt) * w[:, 1, j]);
        
    WP = np.minimum(S1/ratio_S1, S2/ratio_S2);
    
    #만약 두 기초자산의 만기가격이 최초가격의 100%이상인 경우
    #[70%]미만으로 하락한 적이 없는 경우
    #만기때 원금지급
    #두 경우에 포함되지 않을 시 실물인도(1주 미만 현금지급)
    payoff = np.zeros((n,))
    
    condition_1 = (np.minimum(S1[:, tot_date], S2[:, tot_date]) >= 100)
    # True
    payoff += (sumpayment + face_value) * condition_1
    # False
    condition_2 = (np.min(WP, -1) >= kib)
    # False True
    payoff += (sumpayment + face_value) * (1 - condition_1) * condition_2
    # False False
    payoff += (sumpayment + np.minimum(S1[:, tot_date]/ratio_S1, S2[:, tot_date]/ratio_S2) * face_value) * (1 - condition_1) * (1 - condition_2)
    
    tot_payoff = np.sum(payoff)
    
    #모든 시뮬레이션의 페이오프의 평균을 구함
    mean_payoff = tot_payoff/n;
    #ELS 현재 가격을 구함
    price = mean_payoff * np.exp(-r * tot_date/oneyear);
    
    return price

def main():
    start_time = time.time()
    price = original(100000)
    end_time = time.time()
    print(end_time - start_time, price)

    start_time = time.time()
    price = optimal(100000)
    end_time = time.time()
    print(end_time - start_time, price)

if __name__ == '__main__':
    main()