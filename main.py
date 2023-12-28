import streamlit as st
import pandas as pd
import openai
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

#authenticate widjet
if authentication_status:
    authenticator.logout('Logout', 'main', key='unique_key')
    if username in ['jsmith','cedrics']:
        st.write(f'Bonjour *{name}*')
        openai.api_key = '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'
        df = st.file_uploader('Deposit file and the type is csv', type=["csv","xls","xlsx"], label_visibility = 'hidden')
        if df is not None:
            try:
                #read the drag and drop file
                data = pd.read_csv(df,low_memory=False, sep=',',index_col = False, encoding='utf-8',decimal=".")

                st.dataframe(data)
                nbr_col = 0
                # Liste des noms de colonnes à vérifier
                colonnes_a_verifier = ['sepal_length', 'sepal_width', 'petal_length','petal_width','species']

                # Vérifier l'existence de chaque colonne
                for colonne in colonnes_a_verifier:
                    if colonne in data.columns:
                        nbr_col +=1
                if nbr_col == len(data.columns):
                    st.markdown("C'est bon")
                    prompt = f"Ecris moi une conclusion d'un article qui parle de l'utilisation de google"
                    completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", 
                    messages=[{"role": "user", "content": prompt}])
                    st.markdown(prompt)
                    st.markdown(completion['choices'][0]['message']['content'])
                else:
                    st.markdown(f'Il manque des colonnes, le bon format est {data.columns}')
            except Exception as e:
                if e =="":
                    st.error('you cant do that')
    else:
        st.write(f'Bonjour *{name}*')
        st.title("Attente d'un administrateur")
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')


#Update the file configuration
with open('config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)


