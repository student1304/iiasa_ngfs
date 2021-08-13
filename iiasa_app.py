import streamlit as st
import pandas as pd
import os
path = os.getcwd()
datapath = os.path.join(path, 'data')
print('###### PATH:\t', path) # '/home/bjoern/Desktop/data/ngfs-iiasa/Phase2Files'
print('###### DATAPATH:\t', datapath)

encodings = {
    'NIGEM_V2.0.csv': 'UTF-8',
    'Climate_Damages_V2.0.csv': 'UTF-8',
    'IAM_outputs_V2.2.csv': 'ISO-8859-1',
    'Downscaled_National_Data_V2.0.csv': 'UTF-8'
}
      
@st.cache
def load_file(file, path=datapath, encodings=encodings):
    df = pd.read_csv(os.path.join(path, file), encoding=encodings[file])
    return df

st.title('NGFS Explorer')
st.write("<br><hr>", unsafe_allow_html=True)

st.write(f"*[Download](https://github.com/student1304/pyam_ngfs/raw/main/scenarios_overview.pdf)  .pdf with scenario overview*", unsafe_allow_html=True)


files = [f for f in os.listdir(datapath) if f.endswith('.csv')]

file = st.sidebar.selectbox(label='Select DB File', index=0, options = files)
st.sidebar.info(f'Loading {file}')
st.sidebar.info(f'Size {round(os.path.getsize(os.path.join(datapath, file))/1000000, 2)} MB')
#  df = pd.read_csv('Phase2Files/NGFS_Scenario_Data_NIGEM_V2.0.csv')
df = load_file(file=file)

model = st.sidebar.selectbox(label='Model', options = df.Model.unique())
df2 = df[df.Model == model]

region = st.sidebar.selectbox(label='Region', options = df2.Region.unique())
df3 = df2[df2.Region==region]

scenario = st.sidebar.selectbox(label='Scenario', options = df3.Scenario.unique())
df4 = df3[df3.Scenario==scenario]

variable = st.sidebar.selectbox(label='Variable', options = df4.Variable.unique())
df5 = df4[df4.Variable==variable]

yrs = df[df.columns[df.columns.str.startswith('2')]].columns
#years = st.slider(label='Timeframe', value=(yrs[0], yrs[-1]))
#yr_cols = yrs #[str(i) for i in range(years[0], years[1])]

#my_cols = ['Model', 'Variable'] + yr_cols

#data = df[(df.Region==region) & (df.Model==model) & (df.Scenario==scenario) & (df.Variable==variable)].drop(columns=['Model', 'Scenario', 'Region', 'Variable', ])
st.write(f'<h5>Data for:</h5><br>Model: {model} <br>Region: {region}<br>Scenario: {scenario}<br>Variable: {variable}<hr>', unsafe_allow_html=True)

#data = df5[my_cols]
data = df5[yrs].dropna(axis=1)
st.dataframe(data)
st.line_chart(data.astype('float').T)
   
