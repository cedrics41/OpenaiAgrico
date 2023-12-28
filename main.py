import streamlit as st
import pandas as pd
import openai

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

