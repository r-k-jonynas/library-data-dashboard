# A web app for visualization of occupancy trends of a building with multiple spaces

This is a Dash dashboard-style web app which displays interactive visualizations of occupancy data for a building in a browser window. The app reacts to user's selections and renders appropriate graphs.

This project is based upon my previous space occupancy data analysis projects for a university library.

## Libraries used:
- Dash & Plotly (for interactive visualizations);
- Pandas (for data cleaning and selection)

## Improvements to be implemented
- [ ] a production version of a fake data generator
 - [ ] a customizable data generator (a user can enter the name / type of a building, a number of spaces within the building, names of the spaces, their maximum capacities)
 - [ ] a randomized data corruption mechanism (to generate more realistic datasets)
- [ ] a fully-functioning pipeline: data generator (in development) -> data cleaning app (in development)-> a Dash app
- [ ] 'Update data' button generating a new dataset
- [ ] dataset preview functionality (Dash Table)
- [ ] Insights about Missing data (dynamically rendered depending upon user's selections)
- [ ] Flask app wrapping the dash app (login window, contact form)
