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
    'mark.de.jong@ajax.nl': 'AFCA_1900!',
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

        @st.cache_data
        def load_data(file_path):
            return pd.read_excel(file_path)

        @st.cache_data
        def process_data(data):
            data = data.drop_duplicates(subset='Player', keep='first')
            data['Forward passes/ passes'] = data['Forward passes per 90'] / data['Passes per 90']
            data['Goals - xG'] = data['Goals per 90'] - data['xG per 90']
            return data


        @st.cache_data
        def bereken_percentiel_score(B):
            percentiel_scores_dict = {}
            for kolomnaam in B.columns:
                percentiel_scores_dict[kolomnaam] = B[kolomnaam].apply(lambda x: percentileofscore(B[kolomnaam], x))
            return pd.DataFrame(percentiel_scores_dict)

        @st.cache_data
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
        st.markdown("- The players are aged between 15 and 18, with both youth and professional leagues being considered.")
        st.markdown("- WyScout data is used, and only players who have played a minimum of 800 minutes are included to ensure the reliability of the data. All data is converted into averages per 90 minutes.")
        st.markdown("- A description of all the metrics used can be found at https://dataglossary.wyscout.com.")
        st.divider()
        st.write("")
        st.write("")

        options = st.sidebar.radio('Position', options=['Wingers', 'Strikers', 'Attacking Midfielders', 'Central Midfielders', 'Wingbacks', 'Central Defenders'])
        if options == 'Wingers':
            all_players = pd.concat([load_data(f'w{i}.xlsx') for i in range(1, 13)], ignore_index=True)
        elif options == 'Strikers':
            all_players = pd.concat([load_data(f'spitsU18_{i}.xlsx') for i in range(1, 5)], ignore_index=True)

        A = process_data(all_players)
        Profiles = A
        A_per = A

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

        parameters = ['Passes per 90', 'Accurate passes, %', 'Forward passes per 90',
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
            'Direct free kicks on target, %', 'Corners per 90']
        with col5:
            metrics = st.multiselect('show parameters', parameters)
            general = st.multiselect('show info', ['Team', 'Position', 'Age', 'Matches played', 'Minutes played'])
            if not general:
                general = ['Team', 'Position', 'Age', 'Matches played', 'Minutes played']
            if not metrics:
                metrics =  parameters

            A_per = A_per[['Player', 'Team', 'Position', 'Age'] + metrics]
        with col7:
            filter = st.multiselect('filter parameters', parameters)
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

        Percentiles = bereken_percentiel_score(B)
        Percentiles = Percentiles.reset_index()
        if player_search:
            Percentiles = Percentiles[(Percentiles['Player'].isin(player_search))]
        if team_search:
            Percentiles = Percentiles[(Percentiles['Team'].isin(team_search))]
        Percentiles = Percentiles.set_index(['Player', 'Team', 'Position', 'Age'])


        Percentiles.rename(columns={'Average pass length, m': 'Average pass length'}, inplace=True)
        

        Percentiles = Percentiles.reset_index()
        Percentiles = Percentiles.set_index(['Player', 'Team', 'Position', 'Age'])

        st.subheader("Percentile Scores of the Subset")
        if metrics == parameters:
            metrics[metrics.index('Passes per 90')] = 'passes per 90'

        filter2 = st.multiselect('filter parameters', metrics)
        if filter2:
            for filter in filter2:
                if filter == 'passes per 90':
                    filter = 'Passes per 90'
                slider = st.slider(filter, min_value=0, max_value=100, value=(0, 100))
                Percentiles = Percentiles[(Percentiles[filter] >= slider[0]) & (Percentiles[filter] <= slider[1])]

        

        st.dataframe(Percentiles.round(1), height = 700)
        Profiles = Profiles.reset_index()
        Profiles = Profiles.set_index(['Player', 'Team', 'Age'])
        Profiles = bereken_percentiel_score(Profiles)

        if options == 'Wingers':
            winger_types = ['Inside forward', 'Technical winger', 'Dynamical winger']
            col1, col2 = st.columns([2, 2])
            with col1:
                st.subheader('Overview player profiles')
                st.markdown("Combined parameters:")
                st.markdown("- **Build up:** Gives an insight on the contribution to the build up play a player has. Considering the amount of passes, the accuracy of passes, the forward to backward passes, Long passes and so on..")
                st.markdown("- **Creating Chances:** Gives an insight in the contribution of the player on creating chances. Takes into account Amount of dribbles, succesfull dribbles, Key passes and crosses aswell as the provided assists. ")
                st.markdown("- **Finishing:** Gives an insight in the finishing ability of the player. Goals are considered, but also the goals compared to the expected goeals and the goal conversion rates are considered. ")
                st.markdown("- **Defending:** Gives an insight in the defensive contribution of the player. Defending duels won and balls recovered are considered")
                st.markdown("- **Role score:** Based on the selected role and the combined parameters the role score is calculated for each player, reflecting how good he is in a specifik role.")
            col1, col2 = st.columns([2, 2.9])   
            with col1:
                wingertype = st.selectbox('type of winger', winger_types)
            Profiles = Profiles.reset_index()
            if player_search:
                Profiles = Profiles[(Profiles['Player'].isin(player_search))]
            if team_search:
                Profiles = Profiles[(Profiles['Team'].isin(team_search))]
            Profiles = Profiles.set_index(['Player', 'Team', 'Age'])
            rolescore = bereken_rolscore(Profiles, wingertype)
            rolscoreInside = bereken_rolscore(Profiles, 'Inside forward')
            rolscoreTechnical = bereken_rolscore(Profiles, 'Technical winger')
            rolscoreDynamical = bereken_rolscore(Profiles, 'Dynamical winger')

            summary = pd.DataFrame(index=Profiles.index)
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
        else:
            st.subheader('Overview player profiles')
            st.write("")

            st.write("")
            st.write("To be continued..")
            st.write("")
            st.write("")