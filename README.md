# A web app for visualization of occupancy trends of a building with multiple spaces

[![Build Status](https://travis-ci.com/r-k-jonynas/rest-api-adventures.svg?branch=master)](https://travis-ci.com/r-k-jonynas/rest-api-adventures) [![codecov](https://codecov.io/gh/r-k-jonynas/library-spc-study-reports/branch/master/graph/badge.svg?token=Yp0SAC5MJa)](https://codecov.io/gh/r-k-jonynas/library-spc-study-reports)


This is a Dash dashboard-style web app which displays interactive visualizations of occupancy data for a building in a browser window. The app reacts to user's selections and renders appropriate graphs.

This project is based upon my previous space occupancy data analysis projects for a university library.

**NOTE:** This is an almost complete mirror of a private Github repo from which Heroku app is hosted. This repo contains all the code which could be displayed without compromising security or revealing private data of my registered users. In this repo, I omitted the user database and layout & callbacks files for one Dash app. I also omitted some code in the `__init__.py`file.

If you'd like to see all the production code or have any questions, send me an email at [rytis.kazimieras@gmail.com] and we will work something out.

## Libraries used:
- Dash & Plotly (for interactive visualizations);
- Pandas (for data cleaning and selection)
- Flask (for the main app);
- Flask-Login (for authentication, authorization, user management).
- SQLAlchemy (ORM for SQLite user database.)

## History of the project:

<table>
<thead>
<tr>
<th>Version</th>
<th>Libraries added / taken down</th>
<th>Project state</th>
</tr>
</thead>
<tbody>
<tr>
<td> v1.0 </td>
<td> + Dash & Pandas</td>
<td> Standalone Dash App</td>
</tr>
<tr>
<td> prototyping stage </td>
<td> experiments with Werkzeug(server) & Flask (homepage)</td>
<td> Flask app for homepage, Dash Apps at their endpoints; all tied together by Werkzeug's `DispatcherMiddleware`</td>
</tr>
<tr>
<td> v2.0 </td>
<td> + Flask, Flask-Login</td>
<td> Multi-page Flask app with embeded Dash Apps and added authentication system </td>
</tr>
<tr>
<td> v2.1 </td>
<td> -</td>
<td> v2.0 with added roled-based authentication </td>
</tr>
</tbody></table>

## Improvements to be implemented
- [ ] a fully-functioning pipeline: data generator (in development) -> data cleaning app (in development)-> a Dash app.
  - [X] a production version of a fake data generator.
    - [ ] a customizable data generator (a user can enter the name / type of a building, a number of spaces within the building, names of the spaces, their maximum capacities).
    - [X] a randomized data corruption mechanism (to generate more realistic datasets).

- [ ] 'Update data' button generating a new fake dataset.

- [ ] dataset preview functionality (Dash Table displaying the head of a dataset) (in the Dash App).
- [ ] Insights about the dataset, ie. metadata (displayed as a Dash Table).
- [ ] Insights about Missing data (dynamically rendered depending upon user's selections in the Dash App).

- [X] Flask app wrapping the dash app (home page, login & logout views)
  - [ ] a Contact form, which automatically sends an email to the page owner.

  - [ ] Tests
  - [X] CI/CD

- [ ] Better UI.
- [ ] Registration form and a third type of Dash Viz - customizable one
