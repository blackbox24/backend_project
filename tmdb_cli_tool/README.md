### TMDB CLI TOOL
In this project, you will build a simple command line interface (CLI) to fetch data from The Movie Database (TMDB) and display it in the terminal. This project will help you practice your programming skills, including working with APIs, handling JSON data, and building a simple CLI application.

### Requirements
- The application should run from the command line, and be able to pull and show the popular, top-rated, upcoming and now playing movies from the TMDB API. The user should be able to specify the type of movies they want to see by passing a command line argument to the CLI tool.

- Here is how the CLI tool usage should look like:

```
tmdb-app --type "playing"
tmdb-app --type "popular"
tmdb-app --type "top"
tmdb-app --type "upcoming"
```

- You can look at the API documentation to understand how to fetch the data for each type of movie.

- [Now Playing Movies](https://developer.themoviedb.org/reference/movie-now-playing-list)
- [Popular](https://developer.themoviedb.org/reference/movie-popular-list)
- [Top Rated Movies](https://developer.themoviedb.org/reference/movie-top-rated-list)
- [Upcoming Movies](https://developer.themoviedb.org/reference/movie-upcoming-list)

- There are some considerations to keep in mind:
    - Handle errors gracefully, such as API failures or network issues.
    - Use a programming language of your choice to build this project.
    - Make sure to include a README file with instructions on how to run the application and any other relevant information.

```bash
python script.py --type playing
python script.py --type popular --language fr-FR --page 2
```

```
INFO 2025-08-04 15:41:23,123 Fetching playing movies...
INFO 2025-08-04 15:41:23,456 Status code: 200
INFO 2025-08-04 15:41:23,457 Date range: 2025-07-01 to 2025-08-15
INFO 2025-08-04 15:41:23,458 Page: 1
INFO 2025-08-04 15:41:23,459 Total results: 20

Playing Movies:
Title: Movie A, Release: 2025-07-10, Rating: 7.8
Title: Movie B, Release: 2025-07-15, Rating: 6.5
...
```