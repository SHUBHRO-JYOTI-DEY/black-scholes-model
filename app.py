import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm


def app1():
    
    st.title('Black Scholes Calculator')

    with st.expander('About this App'):
        st.write('This app calculates the Option Prices and Option Greeks based on 5 inputs - Spot Price, Strike Price, Daily Volatility, Risk Free Rate of Return and Time to expiry of Contract.')
        st.write('The Black Scholes formula and calculations are based on the work of economists Fischer Black and Myron Scholes.')

    col1, col2 = st.columns(2)

    with col1:
        spot = st.number_input('Spot Price', step=100)
    with col2: 
        strike = st.number_input('Strike Price', min_value=1, step=100)

    col3, col4, col5 = st.columns(3)

    with col3:
        risk = st.number_input('Risk Free Rate', step=0.5)
    with col4:
        dailyvol = st.number_input('Daily Volatility', step=0.5)
    with col5:
        t = st.number_input("Time to Expiry (in months)", step=1)

    if st.button('Calculate Prices and Greeks'):
        annual_vol = (dailyvol*(252**(1/2)))/100
        rf = risk/100
        time = t/12

        kenegrt = strike*(2.718281828459045**(-rf*time))
        lnsk = np.log(spot/strike)
        v22 = (annual_vol**2)/2
        vt12 = annual_vol*(time**(1/2))

        d1 = (lnsk + (rf + v22)*time)/vt12
        d2 = d1 - vt12

        nd1 = norm.cdf(d1)
        nd2 = norm.cdf(d2)

        ndneg1 = 1 - nd1
        ndneg2 = 1 - nd2

        ndashd1 = (2.718281828459045**(-(d1**2)/2))/(2*3.14159265359)**(1/2)

        callprice = spot*nd1 - kenegrt*nd2
        putprice = kenegrt*ndneg2 - spot*ndneg1

        call_delta = nd1
        put_delta = ndneg1

        call_gamma = ndashd1/(spot*vt12)
        put_gamma = call_gamma

        call_theta = -((spot*annual_vol*ndashd1)/(2*(time**(1/2)))) - rf*kenegrt*nd2
        put_theta = -((spot*annual_vol*ndashd1)/(2*(time**(1/2)))) + rf*kenegrt*ndneg2

        call_vega = spot*ndashd1*(time**(1/2))
        put_vega = call_vega

        call_rho = kenegrt*time*nd2
        put_rho = -kenegrt*time*ndneg2

        data = {
            "Parameter": ["Annual Volatility", "Call Price", "Put Price"],
            "Value": [annual_vol, callprice, putprice]
        }

        data_delta = {
            "Call Delta": [call_delta],
            "Put Delta": [put_delta]
        }

        data_rho = {
            "Call Rho": [call_rho],
            "Put Rho": [put_rho]
        }

        data_theta = {
            "Call Theta": [call_theta],
            "Put Theta": [put_theta]
        }

        data_gamma = {
            "Call Gamma": [call_gamma],
            "Put Gamma": [put_gamma]
        }

        data_vega = {
            "Call Vega": [call_vega],
            "Put Vega": [put_vega]
        }

        headers = ["Parameter", "Value"]
        delta_headers = ["Call Delta", "Put Delta"]
        rho_headers = ["Call Rho", "Put Rho"]
        theta_headers = ["Call Theta", "Put Theta"]
        gamma_headers = ["Call Gamma", "Put Gamma"]
        vega_headers = ["Call Vega", "Put Vega"]

        df = pd.DataFrame(data, columns=headers)
        df_delta = pd.DataFrame(data_delta, columns=delta_headers)
        df_delta.reset_index(drop=True, inplace=True)

        df_rho = pd.DataFrame(data_rho, columns=rho_headers)
        df_rho.reset_index(drop=True, inplace=True)

        df_theta = pd.DataFrame(data_theta, columns=theta_headers)
        df_theta.reset_index(drop=True, inplace=True)

        df_gamma = pd.DataFrame(data_gamma, columns=gamma_headers)
        df_gamma.reset_index(drop=True, inplace=True)

        df_vega = pd.DataFrame(data_vega, columns=vega_headers)
        df_vega.reset_index(drop=True, inplace=True)

        st.table(df)
        st.table(df_delta)
        st.table(df_rho)
        st.table(df_theta)
        st.table(df_gamma)
        st.table(df_vega)

def app2():

    st.title('Options Strategy Builder')

    with st.expander('About this App'):
        st.write('This App shows the Payoff of a single or a combination of Options Positions, based on the inputs - Strike Price, Option Type, Buy/Sell and Lot Size.')
        st.write('Pre-built Options Strategies will be available in the future iterations of the App.')

    class OptionPosition:
        def __init__(self, strike_price, option_type, lots, buy_or_sell):
            self.strike_price = strike_price
            self.option_type = option_type
            self.lots = lots
            self.buy_or_sell = buy_or_sell

        def __hash__(self):
            return hash((self.strike_price, self.option_type, self.lots, self.buy_or_sell))

    def calculate_payoff(option_positions, underlying_price):
        total_payoff = 0
        for position in option_positions:
            if position.option_type == 'Call':
                if position.buy_or_sell == 'Buy':
                    payoff = np.maximum(underlying_price - position.strike_price, 0) * position.lots
                else:
                    payoff = np.maximum(position.strike_price - underlying_price, 0) * position.lots
            else:
                if position.buy_or_sell == 'Buy':
                    payoff = np.maximum(position.strike_price - underlying_price, 0) * position.lots
                else:
                    payoff = np.maximum(underlying_price - position.strike_price, 0) * position.lots
            total_payoff += payoff
        return total_payoff

    @st.cache_resource(hash_funcs={OptionPosition: lambda x: hash((x.strike_price, x.option_type, x.lots, x.buy_or_sell))})
    def generate_payoff_chart(option_positions, start_price, end_price, num_points):
        underlying_prices = np.linspace(start_price, end_price, num_points)
        payoffs = []
        for price in underlying_prices:
            payoff = calculate_payoff(option_positions, price)
            payoffs.append(payoff)
        return underlying_prices, payoffs

    def main():
        st.title("Options Payoff Chart")

        # Input components
        num_positions = st.number_input("Number of Positions", value=1, step=1)
        option_positions = []
        for i in range(num_positions):
            st.subheader(f"Position {i+1}")
            strike_price = st.number_input(f"Strike Price {i+1}", value=100.0, key=f"strike_price_{i}")
            option_type = st.selectbox(f"Option Type {i+1}", ['Call', 'Put'], key=f"option_type_{i}")
            lots = st.number_input(f"Lots {i+1}", value=1, step=1, key=f"lots_{i}")
            buy_or_sell = st.selectbox(f"Buy or Sell {i+1}", ['Buy', 'Sell'], key=f"buy_or_sell_{i}")
            position = OptionPosition(strike_price, option_type, lots, buy_or_sell)
            option_positions.append(position)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("Chart Axes Configuration")
        start_price = st.number_input("Start Price", value=0.0)
        end_price = st.number_input("End Price", value=200.0)
        num_points = st.number_input("Number of Points", value=100, step=10)

        # Generate payoff chart
        underlying_prices, payoffs = generate_payoff_chart(option_positions, start_price, end_price, num_points)

        st.subheader("Payoff Chart")
        # Plot payoff chart
        plt.plot(underlying_prices, payoffs)
        plt.xlabel("Underlying Price")
        plt.ylabel("Payoff")
        st.pyplot()

    st.set_option('deprecation.showPyplotGlobalUse', False)

    if __name__ == "__main__":
        main()


def main():

    # Create tabs
    tabs = ["Black Scholes Calculator", "Options Strategy Builder"]
    selected_tab = st.sidebar.selectbox("Select a tab", tabs)

    # Footer text on the sidebar using HTML tags
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    st.sidebar.markdown("Developed by [Shubhro Jyoti Dey](https://linkedin.com/in/shubhrojyotidey)", unsafe_allow_html=True)

    st.set_option('deprecation.showPyplotGlobalUse', False)

    # Display the selected app based on the tab
    if selected_tab == "Black Scholes Calculator":
        app1()
    elif selected_tab == "Options Strategy Builder":
        app2()

if __name__ == "__main__":
    main()
