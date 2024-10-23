import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the dataset
df = pd.read_csv('data/final_data.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Create a layout for the app
app.layout = html.Div([
    html.H1("Tech Job Trends Dashboard"),
    
    # Dropdown for selecting job title
    dcc.Dropdown(
        id='job-title-dropdown',
        options=[{'label': title, 'value': title} for title in df['Designation'].unique()],
        value=df['Designation'].unique()[0],  # Default value
        className='dropdown mb-3'
    ),
    
    # Dropdown for selecting experience level
    dcc.Dropdown(
        id='experience-dropdown',
        options=[
            {'label': 'All Experience Levels', 'value': 'All'},
            {'label': 'Entry Level', 'value': 'Entry'},
            {'label': 'Mid Level', 'value': 'Mid'},
            {'label': 'Senior Level', 'value': 'Senior'},
        ],
        value='All',  # Default value
        className='dropdown mb-3'
    ),
    
    # Graph for job titles
    dcc.Graph(id='job-title-graph', className='graph mb-3'),

    # Graph for locations
    dcc.Graph(id='location-graph', className='graph mb-3'),

    # Graph for skills
    dcc.Graph(id='skills-graph', className='graph mb-3'),
])

# Callback to update job title graph
@app.callback(
    Output('job-title-graph', 'figure'),
    [Input('job-title-dropdown', 'value'),
     Input('experience-dropdown', 'value')]
)
def update_job_title_graph(selected_title, experience_level):
    filtered_df = df[df['Designation'] == selected_title]
    
    if experience_level != 'All':
        filtered_df = filtered_df[filtered_df['ExperienceLevel'] == experience_level]
    
    fig = px.bar(filtered_df, x='Location', title=f'Job Postings for {selected_title}')
    return fig

# Callback to update location graph
@app.callback(
    Output('location-graph', 'figure'),
    [Input('job-title-dropdown', 'value'),
     Input('experience-dropdown', 'value')]
)
def update_location_graph(selected_title, experience_level):
    filtered_df = df[df['Designation'] == selected_title]
    
    if experience_level != 'All':
        filtered_df = filtered_df[filtered_df['ExperienceLevel'] == experience_level]
        
    location_counts = filtered_df['Location'].value_counts()
    fig = px.bar(x=location_counts.index, y=location_counts.values, title='Job Postings by Location')
    return fig

# Callback to update skills graph
@app.callback(
    Output('skills-graph', 'figure'),
    Input('job-title-dropdown', 'value')
)
def update_skills_graph(selected_title):
    filtered_df = df[df['Designation'] == selected_title]
    
    # Get skill columns (assume skill columns start at index 10)
    skills_columns = df.columns[10:]  # Adjust according to your data structure
    skill_data = filtered_df[skills_columns].sum().reset_index()
    skill_data.columns = ['Skill', 'Count']
    
    fig = px.bar(skill_data, x='Skill', y='Count', title=f'Skills Required for {selected_title}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
