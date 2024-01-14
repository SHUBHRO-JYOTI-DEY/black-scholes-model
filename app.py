import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm

#inputs
# spot, strike, risk free rate, volatility, time to expiry

st.title('Black Scholes Calculator')

col1, col2 = st.columns(2)

with col1:
    spot = st.number_input('Spot Price')
with col2: 
    strike = st.number_input('Strike Price')

col3, col4, col5 = st.columns(3)

with col3:
    risk = st.number_input('Risk Free Rate')
with col4:
    dailyvol = st.number_input('Daily Volatility')
with col5:
    t = st.number_input("Time to Expiry (in months)")

if st.button('Calculate Prices and Greeks'):
    annual_vol = (dailyvol*(252**(1/2)))/100
    rf = risk/100
    time = t/12

    kenegrt = strike*(2.718281**(-rf*time))
    lnsk = np.log(spot/strike)
    v22 = (annual_vol**2)/2
    vt12 = annual_vol*(time**(1/2))

    d1 = (lnsk + (rf + v22)*time)/vt12
    d2 = d1 - vt12

    nd1 = norm.cdf(d1)
    nd2 = norm.cdf(d2)

    callprice = spot*norm.cdf(d1) - kenegrt*norm.cdf(d2)
    putprice = kenegrt*norm.cdf(-d2) - spot*norm.cdf(-d1)

    call_delta = norm.cdf(d1)
    put_delta = norm.cdf(-d1)

    call_gamma = norm.cdf(d1)/(spot*vt12)
    put_gamma = call_gamma

    call_theta = -((spot*annual_vol*norm.cdf(d1))/(2*(time**(1/2)))) - rf*kenegrt*norm.cdf(d2)
    put_theta = -((spot*annual_vol*norm.cdf(d1))/(2*(time**(1/2)))) + rf*kenegrt*norm.cdf(-d2)

    call_vega = spot*norm.cdf(d1)*(time**(1/2))
    put_vega = call_vega

    call_rho = kenegrt*time*norm.cdf(d2)
    put_rho = -kenegrt*time*norm.cdf(-d2)

    st.subheader("Annual Volatility: " + str(annual_vol))
    st.subheader("kenegrt: " + str(kenegrt))
    st.subheader("lnsk: " + str(lnsk))
    st.subheader("v22: " + str(v22))
    st.subheader("vt12: " + str(vt12))
    st.subheader("d1: " + str(d1))
    st.subheader("d2: " + str(d2))
    st.subheader("nd1: " + str(nd1))
    st.subheader("nd2: " + str(nd2))


    st.subheader("Call Price: " + str(callprice))
    st.subheader("Put Price: " + str(putprice))
    st.subheader("Call Delta: " + str(call_delta))
    st.subheader("Put Delta: " + str(put_delta))
    st.subheader("Call Gamma: " + str(call_gamma))
    st.subheader("Put Gamma: " + str(put_gamma))
    st.subheader("Call Theta: " + str(call_theta))
    st.subheader("Put Theta: " + str(put_theta))
    st.subheader("Call Vega: " + str(call_vega))
    st.subheader("Put Vega: " + str(put_vega))
    st.subheader("Call Rho: " + str(call_rho))
    st.subheader("Put Rho: " + str(put_rho))

