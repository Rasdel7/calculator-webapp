import streamlit as st
import math
import json
import os
from datetime import datetime
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Scientific Calculator",
    page_icon="🔢",
    layout="wide"
)

st.title("🔢 Scientific Calculator")
st.markdown("Calculate, convert units and "
            "reference formulas — all in one place.")
st.markdown("---")

# Session state
if 'history'    not in st.session_state:
    st.session_state.history    = []
if 'expression' not in st.session_state:
    st.session_state.expression = ""
if 'result'     not in st.session_state:
    st.session_state.result     = ""

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🔢 Calculator",
    "📐 Unit Converter",
    "📚 Formula Reference",
    "📋 History"
])

# Tab 1 — Calculator
with tab1:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Standard Calculator")

        # Display
        st.markdown(
            f"<div style='"
            f"background:#1e1e2e; "
            f"padding:15px; "
            f"border-radius:8px; "
            f"font-family:monospace; "
            f"font-size:14px; "
            f"color:gray; "
            f"min-height:30px'>"
            f"{st.session_state.expression or ' '}"
            f"</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div style='"
            f"background:#1e1e2e; "
            f"padding:15px; "
            f"border-radius:8px; "
            f"font-family:monospace; "
            f"font-size:28px; "
            f"color:white; "
            f"text-align:right; "
            f"min-height:50px; "
            f"margin-top:5px'>"
            f"{st.session_state.result or '0'}"
            f"</div>",
            unsafe_allow_html=True
        )
        st.markdown("")

        # Button layout
        buttons = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '−'],
            ['1', '2', '3', '+'],
            ['0', '.', '⌫', '=']
        ]

        for row in buttons:
            cols = st.columns(4)
            for j, btn in enumerate(row):
                with cols[j]:
                    if btn in ['÷', '×',
                               '−', '+', '=']:
                        btn_type = "primary"
                    elif btn in ['C', '±',
                                 '%', '⌫']:
                        btn_type = "secondary"
                    else:
                        btn_type = "secondary"

                    if st.button(
                        btn,
                        key=f"btn_{btn}_{j}",
                        use_container_width=True,
                        type=btn_type
                    ):
                        expr = st.session_state\
                            .expression
                        res  = st.session_state\
                            .result

                        if btn == 'C':
                            st.session_state\
                                .expression = ""
                            st.session_state\
                                .result = ""

                        elif btn == '⌫':
                            st.session_state\
                                .expression = \
                                expr[:-1]

                        elif btn == '±':
                            if expr:
                                if expr[0] == '-':
                                    st.session_state\
                                        .expression \
                                        = expr[1:]
                                else:
                                    st.session_state\
                                        .expression \
                                        = '-' + expr

                        elif btn == '%':
                            if expr:
                                try:
                                    val = eval(expr)
                                    st.session_state\
                                        .expression \
                                        = str(
                                        val / 100)
                                    st.session_state\
                                        .result = str(
                                        val / 100)
                                except:
                                    st.session_state\
                                        .result = \
                                        "Error"

                        elif btn == '=':
                            try:
                                clean = expr\
                                    .replace('×', '*')\
                                    .replace('÷', '/')\
                                    .replace('−', '-')
                                result = eval(clean)
                                if isinstance(
                                    result, float
                                ):
                                    result = round(
                                        result, 10)
                                    if result == \
                                            int(result):
                                        result = int(
                                            result)
                                st.session_state\
                                    .result = str(
                                    result)
                                st.session_state\
                                    .history.insert(
                                    0, {
                                        'expression':
                                            expr,
                                        'result':
                                            str(result),
                                        'time':
                                            datetime
                                            .now()
                                            .strftime(
                                            '%H:%M:%S')
                                    })
                            except:
                                st.session_state\
                                    .result = "Error"

                        elif btn in ['÷', '×',
                                     '−', '+']:
                            st.session_state\
                                .expression += btn

                        else:
                            st.session_state\
                                .expression += btn

                        st.rerun()

    with col2:
        st.markdown("### Scientific Functions")

        expr_input = st.text_input(
            "Enter expression:",
            placeholder="e.g. sin(45), log(100), sqrt(16)"
        )

        sci_functions = {
            "sin(x)":   "Sine (degrees)",
            "cos(x)":   "Cosine (degrees)",
            "tan(x)":   "Tangent (degrees)",
            "sqrt(x)":  "Square root",
            "log(x)":   "Log base 10",
            "ln(x)":    "Natural log",
            "x²":       "Square",
            "x³":       "Cube",
            "1/x":      "Reciprocal",
            "x!":       "Factorial",
            "abs(x)":   "Absolute value",
            "ceil(x)":  "Ceiling",
            "floor(x)": "Floor"
        }

        col_a, col_b = st.columns(2)
        funcs = list(sci_functions.items())
        for i, (func, desc) in enumerate(funcs):
            with (col_a if i % 2 == 0 else col_b):
                if st.button(
                    f"{func}",
                    key=f"sci_{func}",
                    use_container_width=True
                ):
                    if expr_input:
                        try:
                            x = float(expr_input)
                            if func == "sin(x)":
                                r = math.sin(
                                    math.radians(x))
                            elif func == "cos(x)":
                                r = math.cos(
                                    math.radians(x))
                            elif func == "tan(x)":
                                r = math.tan(
                                    math.radians(x))
                            elif func == "sqrt(x)":
                                r = math.sqrt(x)
                            elif func == "log(x)":
                                r = math.log10(x)
                            elif func == "ln(x)":
                                r = math.log(x)
                            elif func == "x²":
                                r = x ** 2
                            elif func == "x³":
                                r = x ** 3
                            elif func == "1/x":
                                r = 1 / x
                            elif func == "x!":
                                r = math.factorial(
                                    int(x))
                            elif func == "abs(x)":
                                r = abs(x)
                            elif func == "ceil(x)":
                                r = math.ceil(x)
                            elif func == "floor(x)":
                                r = math.floor(x)
                            else:
                                r = 0

                            result_str = str(
                                round(r, 8))
                            st.success(
                                f"{func.replace('x', str(int(x) if x == int(x) else x))} "
                                f"= **{result_str}**"
                            )
                            st.session_state\
                                .history.insert(0, {
                                'expression':
                                    f"{func}({x})",
                                'result':
                                    result_str,
                                'time':
                                    datetime.now()
                                    .strftime(
                                    '%H:%M:%S')
                            })
                        except Exception as e:
                            st.error(
                                f"Error: {str(e)}")
                    else:
                        st.warning(
                            "Enter a number first!")

        # Constants
        st.markdown("### 🔵 Constants")
        constants = {
            'π (Pi)':      3.14159265358979,
            'e (Euler)':   2.71828182845905,
            '√2':          1.41421356237310,
            'φ (Golden)':  1.61803398874989,
            'c (light)':   299792458,
            'g (gravity)': 9.80665
        }
        const_cols = st.columns(3)
        for i, (name, val) in enumerate(
            constants.items()
        ):
            with const_cols[i % 3]:
                st.metric(name, val)

# Tab 2 — Unit Converter
with tab2:
    st.markdown("### 📐 Unit Converter")

    unit_category = st.selectbox(
        "Category:",
        ["Length", "Weight", "Temperature",
         "Speed", "Area", "Volume", "Time"]
    )

    CONVERSIONS = {
        "Length": {
            "units": ["Meter", "Kilometer",
                      "Mile", "Foot", "Inch",
                      "Centimeter", "Millimeter"],
            "to_base": {
                "Meter": 1,
                "Kilometer": 1000,
                "Mile": 1609.344,
                "Foot": 0.3048,
                "Inch": 0.0254,
                "Centimeter": 0.01,
                "Millimeter": 0.001
            }
        },
        "Weight": {
            "units": ["Kilogram", "Gram",
                      "Pound", "Ounce",
                      "Ton", "Milligram"],
            "to_base": {
                "Kilogram": 1,
                "Gram": 0.001,
                "Pound": 0.453592,
                "Ounce": 0.0283495,
                "Ton": 1000,
                "Milligram": 0.000001
            }
        },
        "Speed": {
            "units": ["m/s", "km/h",
                      "mph", "knot"],
            "to_base": {
                "m/s": 1,
                "km/h": 0.277778,
                "mph": 0.44704,
                "knot": 0.514444
            }
        },
        "Area": {
            "units": ["m²", "km²", "acre",
                      "hectare", "ft²"],
            "to_base": {
                "m²": 1,
                "km²": 1e6,
                "acre": 4046.86,
                "hectare": 10000,
                "ft²": 0.092903
            }
        },
        "Volume": {
            "units": ["Liter", "Milliliter",
                      "Gallon", "Cup",
                      "Fluid oz"],
            "to_base": {
                "Liter": 1,
                "Milliliter": 0.001,
                "Gallon": 3.78541,
                "Cup": 0.236588,
                "Fluid oz": 0.0295735
            }
        },
        "Time": {
            "units": ["Second", "Minute",
                      "Hour", "Day",
                      "Week", "Month", "Year"],
            "to_base": {
                "Second": 1,
                "Minute": 60,
                "Hour": 3600,
                "Day": 86400,
                "Week": 604800,
                "Month": 2592000,
                "Year": 31536000
            }
        }
    }

    col1, col2, col3 = st.columns([2, 1, 2])

    if unit_category == "Temperature":
        with col1:
            temp_val = st.number_input(
                "Value:", value=0.0)
            from_unit = st.selectbox(
                "From:",
                ["Celsius", "Fahrenheit",
                 "Kelvin"],
                key="temp_from"
            )
        with col2:
            st.markdown("###")
            st.markdown("###")
            st.markdown(
                "<h2 style='text-align:center'>"
                "→</h2>",
                unsafe_allow_html=True
            )
        with col3:
            to_unit = st.selectbox(
                "To:",
                ["Celsius", "Fahrenheit",
                 "Kelvin"],
                key="temp_to"
            )
            if st.button("Convert",
                         type="primary"):
                if from_unit == to_unit:
                    result = temp_val
                elif from_unit == "Celsius":
                    if to_unit == "Fahrenheit":
                        result = (temp_val
                                  * 9/5) + 32
                    else:
                        result = temp_val + 273.15
                elif from_unit == "Fahrenheit":
                    if to_unit == "Celsius":
                        result = (temp_val
                                  - 32) * 5/9
                    else:
                        result = (temp_val - 32
                                  ) * 5/9 + 273.15
                else:
                    if to_unit == "Celsius":
                        result = temp_val - 273.15
                    else:
                        result = (temp_val - 273.15
                                  ) * 9/5 + 32

                st.success(
                    f"**{temp_val} {from_unit}"
                    f" = {result:.4f} {to_unit}**"
                )
    else:
        conv_data = CONVERSIONS[unit_category]
        units     = conv_data['units']
        to_base   = conv_data['to_base']

        with col1:
            value     = st.number_input(
                "Value:", value=1.0)
            from_unit = st.selectbox(
                "From:", units, key="from_unit")
        with col2:
            st.markdown("###")
            st.markdown("###")
            st.markdown(
                "<h2 style='text-align:center'>"
                "→</h2>",
                unsafe_allow_html=True
            )
        with col3:
            to_unit = st.selectbox(
                "To:", units, key="to_unit")
            if st.button("Convert",
                         type="primary"):
                base_val = value * \
                           to_base[from_unit]
                result   = base_val / \
                           to_base[to_unit]
                st.success(
                    f"**{value} {from_unit} "
                    f"= {result:.6f} {to_unit}**"
                )

        # Quick reference table
        st.markdown("### 📊 Quick Reference")
        base_amounts = [1, 5, 10, 50, 100]
        ref_data     = {}
        for u in units[:5]:
            ref_data[u] = [
                round(a * to_base[units[0]] /
                      to_base[u], 4)
                for a in base_amounts
            ]
        ref_df = pd.DataFrame(
            ref_data,
            index=[f"{a} {units[0]}"
                   for a in base_amounts]
        )
        st.dataframe(ref_df,
                     use_container_width=True)

# Tab 3 — Formula Reference
with tab3:
    st.markdown("### 📚 Formula Reference")

    subject = st.selectbox(
        "Subject:",
        ["Mathematics", "Physics",
         "Statistics", "Finance"]
    )

    formulas = {
        "Mathematics": [
            ("Quadratic Formula",
             "x = (-b ± √(b²-4ac)) / 2a",
             "Solving ax² + bx + c = 0"),
            ("Pythagorean Theorem",
             "a² + b² = c²",
             "Right triangle sides"),
            ("Circle Area",
             "A = πr²",
             "Area of a circle"),
            ("Sphere Volume",
             "V = (4/3)πr³",
             "Volume of a sphere"),
            ("Compound Interest",
             "A = P(1 + r/n)^(nt)",
             "P=principal, r=rate, n=compounds, t=time"),
            ("Distance Formula",
             "d = √((x₂-x₁)² + (y₂-y₁)²)",
             "Distance between two points"),
            ("Slope Formula",
             "m = (y₂-y₁) / (x₂-x₁)",
             "Slope between two points"),
            ("Log Rules",
             "log(ab) = log(a) + log(b)",
             "Product rule of logarithms")
        ],
        "Physics": [
            ("Newton's 2nd Law",
             "F = ma",
             "Force = mass × acceleration"),
            ("Kinetic Energy",
             "KE = ½mv²",
             "m=mass, v=velocity"),
            ("Potential Energy",
             "PE = mgh",
             "m=mass, g=gravity, h=height"),
            ("Ohm's Law",
             "V = IR",
             "Voltage = Current × Resistance"),
            ("Wave Speed",
             "v = fλ",
             "Speed = frequency × wavelength"),
            ("Einstein's E=mc²",
             "E = mc²",
             "Energy = mass × speed of light²"),
            ("Pressure",
             "P = F/A",
             "Pressure = Force / Area"),
            ("Gravitational Force",
             "F = Gm₁m₂/r²",
             "Newton's law of gravitation")
        ],
        "Statistics": [
            ("Mean",
             "x̄ = Σx / n",
             "Sum of values divided by count"),
            ("Variance",
             "σ² = Σ(x-x̄)² / n",
             "Average squared deviation"),
            ("Standard Deviation",
             "σ = √(Σ(x-x̄)² / n)",
             "Square root of variance"),
            ("Correlation",
             "r = Σ(x-x̄)(y-ȳ) / (nσxσy)",
             "Pearson correlation coefficient"),
            ("Z-Score",
             "z = (x - μ) / σ",
             "Standard deviations from mean"),
            ("Bayes Theorem",
             "P(A|B) = P(B|A)P(A) / P(B)",
             "Conditional probability"),
            ("Normal Distribution",
             "f(x) = e^(-(x-μ)²/2σ²) / σ√(2π)",
             "Probability density function"),
            ("Regression Line",
             "y = mx + b",
             "Linear regression equation")
        ],
        "Finance": [
            ("Simple Interest",
             "I = PRT",
             "P=principal, R=rate, T=time"),
            ("Compound Interest",
             "A = P(1+r/n)^(nt)",
             "A=amount, n=compounds per year"),
            ("Present Value",
             "PV = FV / (1+r)^n",
             "Current worth of future money"),
            ("Future Value",
             "FV = PV(1+r)^n",
             "Future worth of current money"),
            ("SIP Returns",
             "M = P×((1+i)^n-1)/i×(1+i)",
             "Systematic Investment Plan"),
            ("EMI Formula",
             "EMI = P×r×(1+r)^n/((1+r)^n-1)",
             "Equated Monthly Installment"),
            ("ROI",
             "ROI = (Gain-Cost)/Cost × 100",
             "Return on investment"),
            ("CAGR",
             "CAGR = (End/Start)^(1/n) - 1",
             "Compound annual growth rate")
        ]
    }

    for name, formula, desc in \
            formulas[subject]:
        with st.expander(f"📐 {name}"):
            st.markdown(
                f"<div style='"
                f"background:#1e1e2e; "
                f"padding:15px; "
                f"border-radius:8px; "
                f"font-family:monospace; "
                f"font-size:18px; "
                f"color:#f39c12; "
                f"text-align:center'>"
                f"{formula}"
                f"</div>",
                unsafe_allow_html=True
            )
            st.caption(desc)

# Tab 4 — History
with tab4:
    st.markdown("### 📋 Calculation History")

    if not st.session_state.history:
        st.info("No calculations yet. "
                "Use the calculator to see history!")
    else:
        st.markdown(
            f"**{len(st.session_state.history)}"
            f" calculations**"
        )

        for calc in st.session_state.history[:20]:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(
                    f"`{calc['expression']}` "
                    f"= **{calc['result']}**"
                )
            with col2:
                st.caption(calc['time'])

        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()

        # Download history
        if st.session_state.history:
            hist_df = pd.DataFrame(
                st.session_state.history)
            st.download_button(
                "⬇️ Download History",
                hist_df.to_csv(index=False),
                "calc_history.csv",
                "text/csv"
            )

st.markdown("---")
st.markdown(
    "Built by **Jyotiraditya** | "
    "Scientific Calculator | "
    "Math made simple 🔢"
)