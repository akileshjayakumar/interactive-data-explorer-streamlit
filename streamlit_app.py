import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

# Page title and icon
st.set_page_config(page_title='Movie Genre Insights', page_icon='🍿')
st.title('🍿 Movie Genre Insights')

# Introduction section
st.subheader('Discover which Movie Genre performs best at the box office')

# Load data
df = pd.read_csv('data/movies_genres_summary.csv')
df.year = df.year.astype('int')

# Input widgets
# Genres selection
genres_list = df.genre.unique()
genres_selection = st.multiselect('Select genres', genres_list,
                                  ['Action', 'Adventure', 'Biography', 'Comedy', 'Drama', 'Horror'])

# Year selection
year_selection = st.slider(
    'Select year duration', 1986, 2006, (2000, 2016))
year_selection_list = list(
    np.arange(year_selection[0], year_selection[1]+1))

# Filter data based on user selection
df_selection = df[df.genre.isin(
    genres_selection) & df['year'].isin(year_selection_list)]
reshaped_df = df_selection.pivot_table(
    index='year', columns='genre', values='gross', aggfunc='sum', fill_value=0)
reshaped_df = reshaped_df.sort_values(by='year', ascending=False)

# Display DataFrame
st.write('## Data Summary')
st.dataframe(reshaped_df)

# Display chart
st.write('## Visualize Data')
chart = alt.Chart(df_selection).mark_bar().encode(
    x=alt.X('year:O', title='Year'),
    y=alt.Y('gross:Q', title='Gross Earnings ($)'),
    color='genre:N',
    tooltip=['genre', 'gross']
).properties(width=700, height=400)

st.altair_chart(chart, use_container_width=True)

# Footer
st.markdown(
    """
    <footer class="footer">
        <small class="footer">
            © Akilesh Jayakumar | Created with Python and Streamlit
        </small>
    </footer>
    """,
    unsafe_allow_html=True
)
