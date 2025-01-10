import pandas as pd
import numpy as np
import streamlit as st
from scipy.stats import percentileofscore

st.set_page_config(page_title = 'Data-screening tool AFC Ajax',
                   page_icon = ':bar_chart:',
                   layout="wide")

st.markdown("""
    <style>
        .title-wrapper {
            display: flex;
            align-items: center;
        }
        .icon {
            margin-right: 10px;
        }
    </style>
""", unsafe_allow_html=True)


#Haal de whitelist van e-mailadressen en wachtwoorden op uit de secret
whitelist_credentials = {
    'niels.nederlof@ajax.nl': 'AFCA_1900!',
    'r.demesel@ajax.nl': 'AFCA_1900!',
}

#secrets = st.secrets["whitelist_credentials"]

# Vraag de gebruiker om in te loggen
user_email = st.text_input("Email adress:")
user_password = st.text_input("Password:", type="password")

# Controleer of de verstrekte inloggegevens overeenkomen met de whitelist
if user_email in whitelist_credentials:
    if user_password == whitelist_credentials[user_email]:
        st.success('Welcome')

        def title_with_icon(icon, title):
            st.markdown(f"<div class='title-wrapper'><div class='icon'>{icon}</div><h4>{title}</h4></div>", unsafe_allow_html=True)

        def bereken_percentiel_score(B):
            percentiel_scores_dict = {}
            for kolomnaam in B.columns:
                percentiel_scores_dict[kolomnaam] = B[kolomnaam].apply(lambda x: percentileofscore(B[kolomnaam], x))
            return pd.DataFrame(percentiel_scores_dict)

        def bereken_rolscore(C, wingertype):

            C['Build up'] = (C['Accurate passes, %']*0.15 + 
                                        C['Forward passes/ passes']*0.2 + 
                                        C['Accurate forward passes, %']*0.15 + 
                                        C['Accurate long passes, %']*0.1 + 
                                        C['Progressive passes per 90']*0.25 + 
                                        C['Accurate progressive passes, %']*0.15)
                                        

            C['Defending'] = (C['Interceptions per 90']*1.5 + 
                                            C['Defensive duels per 90']*1 + 
                                            C['Defensive duels won, %']*2.5) / 5

            # Inside forward berekeningen
            if wingertype == 'Inside forward':
                
                C['Creating chances'] = (C['Through passes per 90']*2 + C['Accurate through passes, %']*1.5 + 
                                                    C['Passes to final third per 90']*4 + 
                                                    C['Accurate passes to final third, %']*3 + 
                                                    C['Crosses per 90']*1 +
                                                    C['Accurate crosses, %']*1 + 
                                                    C['Touches in box per 90']*1 +
                                                    C['Offensive duels won, %']*2 + 
                                                    C['Successful dribbles, %']*3 +
                                                    C['Dribbles per 90']*2 + 
                                                    C['xA per 90']*5 + 
                                                    #C['Progressive runs per 90']*1 + 
                                                    C['Smart passes per 90']*2 +
                                                    C['Accurate smart passes, %']*1.5) / 29
                                                    
                C['Finishing'] = (C['Non-penalty goals per 90']*5 + 
                                                C['Goals - xG']*3 + 
                                                C['Goal conversion, %']*2 + 
                                                C['Shots on target, %']*1.5 + 
                                                C['Shots per 90']*2) / 13.5
                C['Rol Score'] = (C['Build up']*5 + 
                                                C['Creating chances']*10 + 
                                                C['Finishing']*7 + 
                                                C['Defending']*2) / 24
                rolescore = C[['Build up','Creating chances','Finishing','Defending', 'Rol Score']]                               
            # Technical winger berekeningen
            if wingertype == 'Technical winger':
                C['Creating chances'] = (C['Through passes per 90']*1.25 + 
                                                    C['Accurate through passes, %']*0.75 + 
                                                    C['Passes to final third per 90']*2.5 + 
                                                    C['Accurate passes to final third, %']*1.5 + 
                                                    C['Crosses per 90']*3 +
                                                    C['Accurate crosses, %']*2 + 
                                                    C['Touches in box per 90']*1 +
                                                    C['Offensive duels won, %']*2 + 
                                                    C['Successful dribbles, %']*5 +
                                                    C['Dribbles per 90']*5 + 
                                                    C['xA per 90']*5 + 
                                                    #C['Progressive runs per 90']*2,5 + 
                                                    C['Smart passes per 90']*1.25 +
                                                    C['Accurate smart passes, %']*0.75) / 31
                                                    
                C['Finishing'] = (C['Non-penalty goals per 90']*5 + 
                                                C['Goals - xG']*3 + 
                                                C['Goal conversion, %']*2 + 
                                                C['Shots on target, %']*1.5 + 
                                                C['Shots per 90']*2) / 13.5

                C['Rol Score'] = (C['Build up']*4 + 
                                                C['Creating chances']*10 + 
                                                C['Finishing']*8 + 
                                                C['Defending']*2) / 24
                rolescore = C[['Build up','Creating chances','Finishing','Defending', 'Rol Score']]                                 
            # Dynamical winger berekeningen
            if wingertype == 'Dynamical winger':
                C['Creating chances'] = (C['Through passes per 90']*0.5 + 
                                                    C['Accurate through passes, %']*0.5 + 
                                                    C['Passes to final third per 90']*2.5 + 
                                                    C['Accurate passes to final third, %']*1.5 + 
                                                    C['Crosses per 90']*3 +
                                                    C['Accurate crosses, %']*2 + 
                                                    C['Touches in box per 90']*2 +
                                                    C['Offensive duels won, %']*2 + 
                                                    C['Successful dribbles, %']*3 +
                                                    C['Dribbles per 90']*4 + 
                                                    C['xA per 90']*5 + 
                                                    #C['Progressive runs per 90']*2 + 
                                                    C['Smart passes per 90']*0.5 +
                                                    C['Accurate smart passes, %']*0.5) / 27
                                                    
                C['Finishing'] = (C['Non-penalty goals per 90']*5 + 
                                                C['Goals - xG']*2 + 
                                                C['Goal conversion, %']*1 + 
                                                C['Shots on target, %']*1.5 + 
                                                C['Shots per 90']*2 +
                                                C['xG per 90']*2) / 13.5
                C['Rol Score'] = (C['Build up']*3 + 
                                                C['Creating chances']*10 + 
                                                C['Finishing']*9 + 
                                                C['Defending']*2) / 24
                rolescore = C[['Build up','Creating chances','Finishing','Defending', 'Rol Score']]
            return rolescore
        st.subheader('Datascreening-tool AFC Ajax')
        #st.divider()
        st.write("")
        st.markdown('Description of the app:')      
        st.markdown("- This tool allows for comparing data of different players across various positions throughout the 2024 calendar year. It can be used to screen players based on their data output.")
        st.markdown("- The players included are aged between 15 and 18, with both youth and professional leagues being considered.")
        st.markdown("- WyScout data is used, and only players who have played a minimum of 800 minutes are included to ensure the reliability of the data. All data is converted into averages per 90 minutes.")
        st.markdown("- A description of all the metrics used can be found at https://dataglossary.wyscout.com.")


        st.divider()
        st.write("")
        st.write("")

        options = st.sidebar.radio('Position', options=['Wingers', 'Strikers', 'Attacking Midfielders', 'Central Midfielders', 'Wingbacks', 'Central Defenders'])
        if options == 'Wingers':
            df = pd.read_excel('w1.xlsx')
            df1 = pd.read_excel('w2.xlsx')
            df2 = pd.read_excel('w3.xlsx')
            df3 = pd.read_excel('w4.xlsx')
            df4 = pd.read_excel('w5.xlsx')
            df5 = pd.read_excel('w10.xlsx')
            df6 = pd.read_excel('w11.xlsx')
            df7 = pd.read_excel('w12.xlsx')
            df8 = pd.read_excel('w13.xlsx')
            df9 = pd.read_excel('w14.xlsx')
            df10 = pd.read_excel('w15.xlsx')
            df11 = pd.read_excel('w16.xlsx')
            #winger = pd.concat([ df5, df6, df7, df8, df9, df10, df11], ignore_index=True)
            winger = pd.concat([df,df1,df2,df3, df4, df5, df6, df7, df8, df9, df10, df11], ignore_index=True)
            #winger = pd.read_excel('top.xlsx')

        A = winger.drop_duplicates(subset='Player', keep='first')
        A_per = A
        A_winger = A
        A['Forward passes/ passes'] = A['Forward passes per 90'] / A['Passes per 90']
        A['Goals - xG'] = A['Goals per 90'] - A['xG per 90']
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 0.25, 0.75, 0.25, 1.5, 0.25, 1.5])

        with col3:
            min_age = int(A['Age'].min())
            max_age = int(A['Age'].max())
            leeftijd = st.slider('Age', min_value=min_age, max_value=max_age, value=(min_age, max_age))
            A = A[(A['Age'] >= leeftijd[0]) & (A['Age'] <= leeftijd[1])]
            min_matches = int(A['Matches played'].min())
            max_matches = int(A['Matches played'].max())
            matchen = st.slider('Games played', min_value=3, max_value=max_matches, value=(3, max_matches))
            A = A[(A['Matches played'] >= matchen[0]) & (A['Matches played'] <= matchen[1])]

        with col1:
            player_search = st.multiselect('search player(s)', A['Player'].unique())
            if player_search:
                A = A[(A['Player'].isin(player_search))]
                
            team_search = st.multiselect('search team(s)', A['Team'].unique())
            if team_search:
                A = A[(A['Team'].isin(team_search))]
                A_per = A_per[(A_per['Team'].isin(team_search))]

        with col5:
            metrics = st.multiselect('show parameters', ['Passes per 90', 'Accurate passes, %', 'Forward passes per 90',
            'Accurate forward passes, %', 'Forward passes/ passes', 'Back passes per 90',
            'Accurate back passes, %', 'Lateral passes per 90',
            'Accurate lateral passes, %', 'Average pass length, m',
            'Smart passes per 90', 'Accurate smart passes, %',
            'Passes to final third per 90', 'Accurate passes to final third, %',
            'Long passes per 90', 'Accurate long passes, %',
            'Through passes per 90', 'Accurate through passes, %', 'Assists',
            'Assists per 90', 'Progressive passes per 90',
            'Accurate progressive passes, %', 'Defensive duels per 90',
            'Defensive duels won, %', 'Interceptions per 90', 'Fouls per 90',
            'Yellow cards per 90', 'Red cards per 90', 'Offensive duels per 90',
            'Offensive duels won, %', 'Goals per 90', 'Goals - xG', 'Non-penalty goals per 90',
            'xG per 90', 'Head goals per 90', 'Shots per 90', 'Shots on target, %',
            'Goal conversion, %', 'xA', 'xA per 90', 'Crosses per 90',
            'Accurate crosses, %', 'Dribbles per 90', 'Successful dribbles, %',
            'Touches in box per 90', 'Direct free kicks per 90',
            'Direct free kicks on target, %', 'Corners per 90', 'Penalties per 90',
            'Penalty conversion, %'])
            general = st.multiselect('show info', ['Team', 'Position', 'Age', 'Matches played', 'Minutes played'])
            if not general:
                general = ['Team', 'Position', 'Age', 'Matches played', 'Minutes played']
            if not metrics:
                metrics =  ['Passes per 90', 'Accurate passes, %', 'Forward passes per 90',
            'Accurate forward passes, %', 'Forward passes/ passes', 'Back passes per 90',
            'Accurate back passes, %', 'Lateral passes per 90',
            'Accurate lateral passes, %', 'Average pass length, m',
            'Smart passes per 90', 'Accurate smart passes, %',
            'Passes to final third per 90', 'Accurate passes to final third, %',
            'Long passes per 90', 'Accurate long passes, %',
            'Through passes per 90', 'Accurate through passes, %', 'Assists',
            'Assists per 90', 'Progressive passes per 90',
            'Accurate progressive passes, %', 'Defensive duels per 90',
            'Defensive duels won, %', 'Interceptions per 90', 'Fouls per 90',
            'Yellow cards per 90', 'Red cards per 90', 'Offensive duels per 90',
            'Offensive duels won, %', 'Goals per 90', 'Goals - xG', 'Non-penalty goals per 90',
            'xG per 90', 'Head goals per 90', 'Shots per 90', 'Shots on target, %',
            'Goal conversion, %', 'xA', 'xA per 90', 'Crosses per 90',
            'Accurate crosses, %', 'Dribbles per 90', 'Successful dribbles, %',
            'Touches in box per 90', 'Direct free kicks per 90',
            'Direct free kicks on target, %', 'Corners per 90', 'Penalties per 90',
            'Penalty conversion, %']

            A_per = A_per[['Player', 'Team', 'Position', 'Age'] + metrics]
        with col7:
            filter = st.multiselect('filter parameters', ['Passes per 90', 'Accurate passes, %', 'Forward passes per 90',
            'Accurate forward passes, %', 'Forward passes/ passes', 'Back passes per 90',
            'Accurate back passes, %', 'Lateral passes per 90',
            'Accurate lateral passes, %', 'Average pass length, m',
            'Smart passes per 90', 'Accurate smart passes, %',
            'Passes to final third per 90', 'Accurate passes to final third, %',
            'Long passes per 90', 'Accurate long passes, %',
            'Through passes per 90', 'Accurate through passes, %', 'Assists',
            'Assists per 90', 'Progressive passes per 90',
            'Accurate progressive passes, %', 'Defensive duels per 90',
            'Defensive duels won, %', 'Interceptions per 90', 'Fouls per 90',
            'Yellow cards per 90', 'Red cards per 90', 'Offensive duels per 90',
            'Offensive duels won, %', 'Goals per 90', 'Goals - xG', 'Non-penalty goals per 90',
            'xG per 90', 'Head goals per 90', 'Shots per 90', 'Shots on target, %',
            'Goal conversion, %', 'xA', 'xA per 90', 'Crosses per 90',
            'Accurate crosses, %', 'Dribbles per 90', 'Successful dribbles, %',
            'Touches in box per 90', 'Direct free kicks per 90',
            'Direct free kicks on target, %', 'Corners per 90', 'Penalties per 90',
            'Penalty conversion, %'])
            if filter:
                for parameter in filter:
                    min_val = int(A[parameter].min())
                    max_val = int(A[parameter].max())
                    parafilter = st.slider(parameter, min_value=min_val, max_value=max_val, value=(min_val, max_val))
                    A = A[(A[parameter] >= parafilter[0]) & (A[parameter] <= parafilter[1])]

        weergave = ['Player'] + general + metrics 
        index = ['Player'] + general
        A2 = A[weergave]
        A2 = A2.set_index(index)
        st.markdown(f'There are  {A2.shape[0]} {options} in the table')
        st.dataframe(A2, height = 700)

        B = A_per
        B = B.set_index(['Player', 'Team', 'Position', 'Age'])
        if player_search:
            A_winger = A_winger[(A_winger['Player'].isin(player_search))]
        A_winger = A_winger.set_index(['Player', 'Team'])
        A_winger.drop(columns=['Position', 'Age'], inplace=True)
        C = bereken_percentiel_score(B)
        C = C.reset_index()
        if player_search:
            C = C[(C['Player'].isin(player_search))]
        C = C.set_index(['Player', 'Team', 'Position', 'Age'])
        C_winger = bereken_percentiel_score(A_winger)

        C.rename(columns={'Average pass length, m': 'Average pass length'}, inplace=True)
        C2 = C
        #C2 = C2.set_index('Player')
        st.subheader("Percentile Scores of the Subset")




        if metrics == ['Passes per 90', 'Accurate passes, %', 'Forward passes per 90',
            'Accurate forward passes, %', 'Forward passes/ passes', 'Back passes per 90',
            'Accurate back passes, %', 'Lateral passes per 90',
            'Accurate lateral passes, %', 'Average pass length, m',
            'Smart passes per 90', 'Accurate smart passes, %',
            'Passes to final third per 90', 'Accurate passes to final third, %',
            'Long passes per 90', 'Accurate long passes, %',
            'Through passes per 90', 'Accurate through passes, %', 'Assists',
            'Assists per 90', 'Progressive passes per 90',
            'Accurate progressive passes, %', 'Defensive duels per 90',
            'Defensive duels won, %', 'Interceptions per 90', 'Fouls per 90',
            'Yellow cards per 90', 'Red cards per 90', 'Offensive duels per 90',
            'Offensive duels won, %', 'Goals per 90', 'Goals - xG', 'Non-penalty goals per 90',
            'xG per 90', 'Head goals per 90', 'Shots per 90', 'Shots on target, %',
            'Goal conversion, %', 'xA', 'xA per 90', 'Crosses per 90',
            'Accurate crosses, %', 'Dribbles per 90', 'Successful dribbles, %',
            'Touches in box per 90', 'Direct free kicks per 90',
            'Direct free kicks on target, %', 'Corners per 90', 'Penalties per 90',
            'Penalty conversion, %']:
            metrics[metrics.index('Passes per 90')] = 'passes per 90'

        filter2 = st.multiselect('filter parameters', metrics)
        if filter2:
            for filter in filter2:
                if filter == 'passes per 90':
                    filter = 'Passes per 90'
                slider = st.slider(filter, min_value=0, max_value=100, value=(0, 100))
                C = C[(C[filter] >= slider[0]) & (C[filter] <= slider[1])]

        C = C.reset_index()
        C = C.set_index(['Player', 'Team', 'Position', 'Age'])

        st.dataframe(C.round(1), height = 700)

        winger_types = ['Inside forward', 'Technical winger', 'Dynamical winger']
        col1, col2 = st.columns([2, 2])
        with col1:
            st.subheader('Overview player profiles')
            st.markdown("Combined parameters:")
            st.markdown("- **Build up:** Gives an insight on the contribution to the build up play a player has. Considering the amount of passes, the accuracy of passes, the forward to backward passes, Long passes and so on..")
            st.markdown("- **Creating Chances:** Gives an insight in the contribution of the player on creating chances. Takes into account Amount of dribbles, succesfull dribbles, Key passes and crosses aswell as the provided assists. ")
            st.markdown("- **Finishing:** Gives an insight in the finishing ability of the player. Goals are considered, but also the goals compared to the expected goeals and the goal conversion rates are considered. ")
            st.markdown("- **Defending:** Gives an insight in the defensive contribution of the player. Defending duels won and balls recovered are considered**")
            st.markdown("- **Role score:** Based on the selected role and the combined parameters role score is calculated for each player, reflecting how good he is in a specifik role.")
        col1, col2 = st.columns([2, 2.9])   
        with col1:
            wingertype = st.selectbox('type of winger', winger_types)

        rolescore = bereken_rolscore(C_winger, wingertype)
        rolscoreInside = bereken_rolscore(C_winger, 'Inside forward')
        rolscoreTechnical = bereken_rolscore(C_winger, 'Technical winger')
        rolscoreDynamical = bereken_rolscore(C_winger, 'Dynamical winger')

        summary = pd.DataFrame(index=C_winger.index)
        summary['Inside forward'] = rolscoreInside['Rol Score']
        summary['Technical winger'] = rolscoreTechnical['Rol Score']
        summary['Dynamical winger'] = rolscoreDynamical['Rol Score']
        summary['Best Role'] = summary[['Inside forward', 'Technical winger', 'Dynamical winger']].idxmax(axis=1)
        summary['Average score'] = summary[['Inside forward', 'Technical winger', 'Dynamical winger']].mean(axis=1)


        col1, col2 = st.columns([2, 2.9])   
        with col1:
            st.dataframe(rolescore.round(1), height = 700)
        with col2:
            st.dataframe(summary.round(1), height=700)