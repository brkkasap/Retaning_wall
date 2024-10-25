# Importing Required Modules
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sb
import math
import plotly.graph_objects as go

# Page Layout Changes
st.set_page_config(layout="wide",page_icon=":magic_wand:")

# Sidebar Options
Title = st.sidebar.title("Classic Retaning Wall Design :magic_wand:")
Text_sidebar = st.sidebar.markdown("Easiest way to check your retaning wall")
st.sidebar.markdown("""
---
Created by [Burak](https://www.linkedin.com/in/burak-kasap/)
burakkasap98@hotmail.com

Feel free to reach me out 👋
""")

st.sidebar.markdown("---")  


tab1, tab2, tab3, tab4, tab5 = st.tabs(["Dimensions", "Soil Type" , "Sliding Check" , "Overturning Check" ,"Bearing Capacity Check"])

# Session State of Buttons
if 'button1' not in st.session_state:
    st.session_state.button1 = False
if 'button2' not in st.session_state:
    st.session_state.button2 = False
if 'button3' not in st.session_state:
    st.session_state.button3 = False
if 'button4' not in st.session_state:
    st.session_state.button4 = False
if 'button5' not in st.session_state:
    st.session_state.button5 = False


# TAB1 
with tab1:
    st.write ("Write your dimensions to create your retaning wall" )
    col1,col2 = st.columns(2)

    
    with col1:
        #Dimensions of Retaning Wall
        h1 = st.number_input("Stem height ",value=3.0)
        h2 = st.number_input("Base height ",value=0.5)
        t_f = st.number_input ("Foot width ",value=1.5)
        t_s = st.number_input("Stem width: ",value=0.75)
        t_t = st.number_input("Toe width: ",value=1.5)

        # Restart Anaysis Button Configration
        Restart = st.button("Reset Your Analysis")
        if Restart:
            st.session_state.button1 = True
        if st.session_state.button1:
            st.session_state.button3 = False
            st.session_state.button4 = False
            st.session_state.button5 = False
            st.session_state.button1 = False
    h_total = h1 + h2
    t_total = t_f + t_s + t_t

    
    # Coordinates of Points
    x_coor = [0, 0, t_f, t_f, t_f + t_s, t_f + t_s, t_total, t_total, 0] 
    y_coor = [0, h2, h2, h_total, h_total, h2, h2, 0, 0]  

    # Figure
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=x_coor, y=y_coor, mode='lines+markers', fill='toself', 
                         fillcolor='rgba(211, 211, 211, 0.5)', line=dict(color='black'), 
                         marker=dict(size=8), name='Retaining Wall'))
    
    # Earth Surface Line
    p5_x = x_coor[4]  
    p5_y = y_coor[4] 
    line_x = [p5_x, t_total+1.5]
    line_y = [p5_y, h_total]
    fig1.add_trace(go.Scatter(x=line_x, y=line_y, mode='lines', 
                         line=dict(color='blue', dash='dash', width=2), name='Earth Surface'))
    fig1.add_annotation(x=t_total+1.5, y=h_total, text="Upper Soil Start Point", showarrow=True, arrowhead=2, ax=-20, ay=+30, 
                   font=dict(color='blue', size=10))    
    
    # Lower Soil Line
    p8_x = x_coor[7]  
    p8_y = y_coor[7]  
    line_x1 = [p8_x, t_total+1.5]
    line_y1 = [p8_y, 0]
    fig1.add_trace(go.Scatter(x=line_x1, y=line_y1, mode='lines', 
                         line=dict(color='blue', dash='dash', width=2), name='Bottom of Retaning Wall'))

    fig1.add_annotation(x=t_total+1.5, y=0, text="Lower Soil Start Point", showarrow=True, arrowhead=2, ax=20, ay=-30, 
                   font=dict(color='blue', size=10))
    

    
    # Figure Optimization
    fig1.update_layout(title='Retaining Wall Shape',
                  xaxis_title='X Coordinate',
                  yaxis_title='Y Coordinate',
                  showlegend=True,
                  template='plotly_white',
                  width=800, height=800)
    


    with col2:   
        st.plotly_chart(fig1,key="1")

#TAB2   
with tab2:
    col1,col2 = st.columns(2)


    with col1:
        # Soil Parameters' Inputs
        st.write("Write your soil parameters to complete your retaning wall pre-design ")
        st.subheader("Upper Soil Parameters")
        soil_name_1 = st.selectbox("Upper Soil Name",("Sand","Clay","Other"))
        soil_gamma_1 = st.number_input ("Write your γ value of upper soil (kN/m3)")
        soil_friction_1 = st.number_input("Write your friction angle of upper soil  (°)")
        soil_mu_value = st.number_input("Write your μ value of upper soil ", value=0.5)

        st.subheader("Lower Soil Parameters")
        soil_name_2 = st.selectbox("Lower Soil Name",("Clay","Other"))
        soil_C_2 = st.number_input ("Write your cohesion force value of lower soil (kN/m2)")
        soil_friction_2 = st.number_input("Write your friction angle of lower soil  (°)")
        soil_q_allowable_2 = st.number_input("Write your allowable stress of your lower soil (kN/m2)")

        # Restart Analysis Button Configration
        Restart = st.button("Reset Your Analysis",key="Restart")
        if Restart:
            st.session_state.button2 = True
        if st.session_state.button2:
            st.session_state.button3 = False
            st.session_state.button4 = False
            st.session_state.button5 = False
            st.session_state.button2 = False
    with col2:
        st.plotly_chart(fig1,key="2")

#TAB3
with tab3:
    concrete = 25 #kN/m3
    col1,col2 = st.columns(2)

    # Stress Calculation
    radian1 = math.radians( 45 - (soil_friction_1)/2)
    stress_a = (soil_gamma_1) * (h_total) * (math.tan(radian1)) * (math.tan(radian1))
    P_a = (stress_a * h_total ) / 2

    # Weight Vertical Loads
    w_stem = t_s * h1 * concrete * 1
    w_base = h2 * t_total * concrete * 1
    w_soil = t_t * h1 * soil_gamma_1 * 1
    total_W = w_stem+w_base+w_soil
    FR = ((total_W) * soil_mu_value) + (0.6 * soil_C_2 * t_total)

    try:
        G_Sliding = FR / P_a
    except:
        pass
    Location_Resultant = (h_total/3)
    

    with col1:
        # Anaysis Button
        Start = st.button("Start Sliding Analysis")
        if Start:
            st.session_state.button3 = True
        if st.session_state.button3:
            if 1.5 < G_Sliding <2 :
                st.success("Sliding check is good")
            else:
                st.warning("Dimensions are not enough ")

            # New figure optimization
            fig2 = go.Figure(fig1)

            tri_x_coor = [t_total+3, t_total+3, t_total+7, t_total+3] 
            tri_y_coor = [0, h_total, 0, 0] 

            fig2.add_trace(go.Scatter(x=tri_x_coor, y=tri_y_coor, mode='lines+markers', fill='toself', 
                         fillcolor='rgba(173, 216, 230, 0.5)', line=dict(color='red',dash = "dash"), 
                         marker=dict(size=8), name='Upper Soil Force'))
            

            # Arrow
            fig2.add_shape(
                type="line",
                x0=t_total+5, y0=h_total/3,  
                x1=t_total+3, y1=h_total/3,    #
                line=dict(color="red", width=4),
            )
            fig2.add_shape(
                type="line",
                x0=t_total+3, y0=h_total/3,  
                x1=t_total+3.5, y1=(h_total/3)+0.25,    
                line=dict(color="red", width=4),)
            
            fig2.add_shape(
                type="line",
                x0=t_total+3, y0=h_total/3,  
                x1=t_total+3.5, y1=(h_total/3)-0.25,  
                line=dict(color="red", width=4),)

            st.plotly_chart(fig2,key="3") 
            





    with col2:
        #Anaysis Button
        if Start:
            st.session_state.button3 = True
        if st.session_state.button3:
            with st.expander("Hand Calculations"):
                st.subheader("1. Calculation of forces")

                # Formulation
                st.latex(r'''
                    σ= Ɣ \cdot z \cdot Ka
                ''')
                st.markdown(
                    "<p style='text-align: center; font-size: 14px; color: #555;'>"
                    "σ: Stress, Ɣ: Gamma, z: Height, Ka: Active Earth Pressure"
                    "</p>",
                    unsafe_allow_html=True)
                
                # Force Calculation
                st.write("At z = 0 m earth force")
                st.latex(r'''
                    σ  = 18 \cdot 0 \cdot tan(45-({}/2)\quad  = 0  \quad kN/m^2
                    '''.format(int(soil_friction_1)))

                st.write("At z = {} m earth force".format(h_total))
                st.latex(r'''
                    σ  = 18 \cdot {} \cdot tan(45-({}/2))\quad  = {}  \quad kN/m^2
                    '''.format(int(h_total),int(soil_friction_1),round(stress_a,1)))
            
                #Resultant Force And It's Location
                st.subheader("2. Resultant Force and It's Location")
                st.latex(r"""
                    Pa= (σa \cdot z) / 2 
                
                """)
                st.latex(r'''
                    Pa  = ({} \cdot {}) / 2\quad = {}  \quad kN/m
                    '''.format(int(stress_a),int(h_total),round(P_a,1)))
                
                st.latex(r'''
                    Location  = {} m \quad (From\, base\, of\, retainig\, wall)
                    '''.format(round((h_total/3),2)))
                
                # Weight Vertical Loads

                st.subheader("3. Naturel Loads")
                st.latex(r"""
                W_(stem) = Stem\, width \cdot Stem\, height \cdot Concrete\,Ɣ \cdot 1(m)
                """)
                st.latex(r"""
                W_(stem) = ({}) \cdot ({}) \cdot ({}) \cdot (1)\quad = {}  \quad kN/m
                """.format(t_s,h1,concrete,w_stem))

                st.latex(r"""              
                W_(base) = Base\, width \cdot Base\, height \cdot Concrete\,Ɣ \cdot 1(m)
                """)
                st.latex(r"""
                W_(base) = ({}) \cdot ({}) \cdot ({}) \cdot (1)\quad = {}  \quad kN/m
                """.format(t_total,h2,concrete,w_base))

                st.latex(r"""
                W_(soil) = Toe\, width \cdot Total\, height \cdot Soil\,Ɣ \cdot 1(m)
                """)
                st.latex(r"""
                W_(soil) = ({}) \cdot ({}) \cdot ({}) \cdot (1)\quad = {}  \quad kN/m
                """.format(t_t,h_total,soil_gamma_1,w_soil))

                # Friction Force

                st.subheader("4. Friction Force")
                st.latex(r"""
                F_(r) = (ƩW)  \cdot μ)\,  + \,((Ca)  \cdot (B))
                """)
                st.latex(r"""
                Friction\,Force = (total\, W \cdot μ\, value)\,  + \, (((0.5)\cdot Cohesion\,Force) \cdot (Base\,Width))
                """)

                st.latex(r"""
                F_(r) = ({}) \cdot ({}) \,  + \, ({}) \cdot {}\quad = {}  \quad kN/m
                """.format(total_W ,soil_mu_value, (0.6*soil_C_2),t_total, FR ))
                
                # Sliding Safety Factor
                st.subheader("5. Sliding Safety Factor Check")
                st.latex(r"""
                G_(sliding) = F_(r)\,   /  \,P_a
                """)
                st.latex(r'''
                G_(Sliding)  = {}\, / \,  {} \quad = {}  \quad 
                '''.format(FR,round(P_a,2),round((FR/P_a),2)))
                st.warning("G_(Sliding) value should be between 1.5 and 2.0")

#TAB4
with tab4:
    
    # Force Arms
    r_Pa = Location_Resultant
    r_w_stem = t_f + (t_s/2)
    r_w_base = t_total / 2
    r_w_soil = t_f + t_s + (t_t/2)

    # Turning Moment
    M_turning = P_a * r_Pa

    # Resisting Moment
    M_Resisting = (w_stem*r_w_stem) + (w_base*r_w_base) + (w_soil * r_w_soil)

    # Overturning Safety Factor Check
    try:
        G_overturning_check = M_Resisting / M_turning
    except:
        pass
    
    col1,col2 = st.columns(2)

    with col1:
        # Analysis Button 
        Start_overturning = st.button("Start Overturning Analysis")

        if Start_overturning:
            st.session_state.button4 = True
        if st.session_state.button4:
            if G_overturning_check >= 2.0:
                st.success("Overturning check is good")
            else:
                st.warning("Dimensions are not enough")
            
            fig3 = go.Figure(fig2)
            st.plotly_chart(fig3,key="4")
        

    with col2:
        if Start_overturning:
            st.session_state.button4 = True
        if st.session_state.button4:
            with st.expander("Hand Calculation"):
                st.warning("All moments have been calculated with respect to the reference point origin (0,0)")
                st.subheader("1. Turning Moment Calculation")
                
                st.latex(r"""
                M_{o} = P_{a} \cdot r_{(Pa)}             
                """)

                st.markdown(
                    "<p style='text-align: center; font-size: 14px; color: #555;'>"
                    "<strong>M_o:</strong> Overturning Moment, <strong>P_a:</strong> Resultant Force, <strong>r_Pa:</strong> Resultant Force Arm Length"
                    "</p>",
                    unsafe_allow_html=True)
                
                st.latex(r"""
                M_o = ({}) \cdot ({}) \quad = {} \quad kNm/m             
                """.format(round(P_a,2),round(r_Pa,2),round(M_turning,2)))

                st.subheader("2. Resisting Moment Calculation")
                st.latex(r"""
                M_{r} = ( W_{stem} \cdot r_{stem} )  \,  + \, ( W_{base} \cdot r_{base} )  \,  + \,  ( W_{soil} \cdot r_{soil} )  
                """)

                st.markdown(
                    "<p style='text-align: center; font-size: 14px; color: #555;'>"
                    "<strong>M_r</strong>: Resisting Moment<br>, <strong>W_s:</strong> Stem Vertical Load,<strong> r_stem:</strong> Stem Vertical Load Arm Length<br> "
                    "<strong> W_b</strong>: Base Vertical Load, <strong>r_base:</strong> Base Vertical Load  Arm Length <br>"
                    "<strong> W_soil</strong>: Soil Vertical Load, <strong>r_soil:</strong> Soil Vertical Load Arm Length<br> "
                    "</p>",
                    unsafe_allow_html=True)
                
                st.latex(r"""
                M_r =  ({}) \cdot ({}) )  \,  + \, ( ({}) \cdot ({}) )  \,  + \,  ( ({}) \cdot ({})  \quad = {} \quad kNm/m 
                """.format(round(w_stem,2),round(r_w_stem,2),round(w_base,2),round(r_w_base,2),round(w_soil),round(r_w_soil),round(M_Resisting,2)))

                st.subheader("3. Overturning Safety Factor Check")
                st.latex(r"""
                Overturning \,Check = ( M_{r} )  \,  /  \, ( M_{o} ) 
                """)

                st.latex(r"""
                Overturning\,Check = ({}) \,  /  \, ({}) \quad = {} \quad kNm/m             
                """.format(round(M_Resisting,2),round(M_turning,2),round(G_overturning_check,2)))

                st.warning(" Overturning check value should be greater than 2.0 ")

with tab5:  
    # Check 1 (Eccentiricity check)                     e < B/6
 
    x = (M_Resisting - M_turning) / total_W #m
    e = (t_total/2) - x #m

    # Check 2 (q max check)                            qmax < qa
    q_max = (total_W/t_total) * (1+(6*e/t_total)) #kN/m2

    # Check 3 (qmin check)                              qmin< qa
    q_min = (total_W/t_total) * (1-(6*e/t_total)) #kN/m2

    # Check 4 (qmin check)                             qmin> 0 
    
    col1,col2 = st.columns(2)

    with col1:
        Start_checks = st.button("Start Checks")
        if Start_checks:
            st.session_state.button5 = True

        if st.session_state.button5:
            if e < t_total/6:
                st.success("Eccentiricity check good")
            else:
                st.warning("Eccentiricity check fail")
            
            if q_max < soil_q_allowable_2:
                st.success("Q max check good")
            else:
                st.warning("Q max check fail")
            
            if q_min < soil_q_allowable_2:
                st.success("Q min check good")
            else:
                st.warning("Q min check fail")
            if q_min > 0:
                st.success("Q min check good")
            else:
                st.warning("Q min check fail")
    
    with col2: 
        if Start_checks:
            st.session_state.button5 = True
        if st.session_state.button5:
            with st.expander("Hand Calculation Of Checks"):
                st.subheader("1. Eccentiricity Check")
                st.latex(r"""
                e < B \,  /  \, 6            
                """)
                st.markdown(
                    "<p style='text-align: center; font-size: 14px; color: #555;'>"
                    "<strong>e:</strong> Eccentiricity, <strong>B:</strong> Base width"
                    "</p>",
                    unsafe_allow_html=True)
                st.write("Calculation of 'e' value")
                st.latex(r"""
                e = (B/2) \,  -  \, x          
                """)
                st.latex(r"""
                x = (M{r}-M{o}) \,  /  \, ƩW         
                """)
                st.latex(r"""
                x = (({}) \,  -  \, ({})) \,  /  \, {} \quad = {} \quad m             
                """.format(round(M_Resisting,2),round(M_turning,2),round(total_W,2),round(x,2)))
                st.latex(r"""
                e = (({}) \,  /  \, (2)) \,  -  \, {} \quad = {} \quad m             
                """.format(round(t_total,2),round(x,2),round(e,3)))
                st.latex(r"""
                B/6 = {} \,  /  \, 6    \quad = {} \quad m        
                """.format(round(t_total,2),round((t_total/6),2)))

                if e < t_total/6:
                    st.success("e < {}".format(round((t_total/6),2)))
                else:
                    st.warning("e > {}".format(round((t_total/6),2)))

                st.subheader("2. Q max Check")
                st.latex(r"""
                Q{max} <  Q{a}      
                """)

                st.latex(r"""
                Q{max} =  ((ƩW)\,  /  \, (B))    \cdot (1+(6e/B))
                """)
                st.markdown(
                    "<p style='text-align: center; font-size: 14px; color: #555;'>"
                    "<strong>Qmax:</strong> Maximum stress, <strong>ƩW:</strong> Total vertical load,<strong>B:</strong> Base width, <strong>e</strong> Eccentiricity"
                    "</p>",
                    unsafe_allow_html=True)
                st.latex(r"""
                Qmax =  (({})\,  /  \, ({}))    \cdot (1+(6\cdot({})/{})) \quad = {} \quad kN/m^2  
                
                """.format(round(total_W,2),round(t_total,2),round(e,2),round(t_total),round(q_max,2))
                )

                if q_max < soil_q_allowable_2:
                    st.success("{} < {}".format(round(q_max,2),round(soil_q_allowable_2)))
                else:
                    st.warning("{} > {}".format(round(q_max,2),round(soil_q_allowable_2)))

                st.subheader("3. Q min Check")
                st.latex(r"""
                Q{min} <  Q{a}    
                """)

                st.latex(r"""
                Q{min} =  ((ƩW)\,  /  \, (B))    \cdot (1-(6e/B))
                """)
                st.markdown(
                    "<p style='text-align: center; font-size: 14px; color: #555;'>"
                    "<strong>Qmax:</strong> Maximum stress, <strong>ƩW:</strong> Total vertical load,<strong>B:</strong> Base width, <strong>e</strong> Eccentiricity"
                    "</p>",
                    unsafe_allow_html=True)
                st.latex(r"""
                Qmax =  (({})\,  /  \, ({}))    \cdot (1-(6\cdot({})/{})) \quad = {} \quad kN/m^2  
                
                """.format(round(total_W,2),round(t_total,2),round(e,2),round(t_total),round(q_min,2))
                )

                if q_min < soil_q_allowable_2:
                    st.success("{} < {}".format(round(q_min,2),round(soil_q_allowable_2)))
                    
                else:
                    st.warning("{} > {}".format(round(q_min,2),round(soil_q_allowable_2)))

                st.subheader("4. Q min Check")
                st.latex(r"""
                Q{min} >  0   
                """)
                st.latex(r"""
                Qmin = \quad {}\quad kN/m^2
                """.format(round(q_min,2)))

                if q_min > 0:
                    st.success("{} > {}".format(round(q_min,2),round(0)))
                else:
                    st.warning("{} < {}".format(round(q_min,2),round(0)))




    
