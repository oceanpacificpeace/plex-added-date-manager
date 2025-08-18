import streamlit as st
from plex_api import PlexAPI
import datetime

st.set_page_config(page_title="Plex Added Date Manager")

def main():
    st.markdown("<h2 style='text-align: center;'>Plex Added Date Manager</h2>", unsafe_allow_html=True)
    # Initialize Plex API
    plex = PlexAPI()
    
    tab1, tab2 = st.tabs(["Movies", "TV Series"])

    # --- Movies Tab ---
    with tab1:
        # Fetch all movies
        movies = plex.get_all_movies()

        # Sort movies by addedAt descending (most recent first)
        movies = sorted(movies, key=lambda m: int(m.get('addedAt', 0)), reverse=True)

        # Display movies
        if movies:
            section_id = "1"
            type_id = "1" 
            for movie in movies:
                cols = st.columns([1, 2])
                with cols[0]:
                    thumb = movie.get('thumb')
                    if thumb:
                        poster_url = f"{plex.base_url}{thumb}?X-Plex-Token={plex.token}"
                        st.image(poster_url, width=120)
                with cols[1]:
                    movie_title = movie.get('title', 'Unknown Title')
                    year = movie.get('year', 'Unknown Year')
                    release_date = movie.get('originallyAvailableAt')
                    display_title = f"{movie_title} ({year})" if year else movie_title
                    if release_date:
                        st.markdown(f"<h3 title='Release Date: {release_date}' style='margin-bottom:0'>{display_title}</h3>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<h3 style='margin-bottom:0'>{display_title}</h3>", unsafe_allow_html=True)
                    added_at = movie.get('addedAt')
                    # Convert Unix timestamp to date
                    if added_at:
                        added_at_date = datetime.datetime.fromtimestamp(int(added_at))
                    else:
                        added_at_date = datetime.datetime.now()

                    new_date = st.date_input(
                        "Edit Added Date",
                        value=added_at_date.date(),
                        key=f"date_{movie.get('ratingKey')}"
                    )
                    # Convert date back to Unix timestamp for update
                    new_date_unix = int(datetime.datetime.combine(new_date, datetime.datetime.min.time()).timestamp())
                    if st.button("Update Date", key=f"update_{movie.get('ratingKey')}"):
                        plex.update_added_date(section_id, movie.get('ratingKey'), type_id, new_date_unix)
                        st.success(f"Updated added date for {movie.get('title', 'Unknown Title')} to {new_date}")
        else:
            st.write("No movies found.")

    # --- TV Series Tab ---
    with tab2:
        section_id = "2" 
        type_id = "2"
        # Fetch TV Series
        seasons = plex.fetch_seasons(section_id)
        seasons = sorted(seasons, key=lambda s: int(s.get('addedAt', 0)), reverse=True)
        if seasons:
            for season in seasons:
                cols = st.columns([1, 2])
                with cols[0]:
                    thumb = season.get('thumb')
                    if thumb:
                        poster_url = f"{plex.base_url}{thumb}?X-Plex-Token={plex.token}"
                        st.image(poster_url, width=120)
                with cols[1]:
                    season_title = season.get('title', 'Unknown Season')
                    year = season.get('year')
                    release_date = season.get('originallyAvailableAt')
                    if year:
                        display_title = f"{season_title} ({year})"
                    else:
                        display_title = season_title
                    if release_date:
                        st.markdown(f"<h3 title='Release Date: {release_date}' style='margin-bottom:0'>{display_title}</h3>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<h3 style='margin-bottom:0'>{display_title}</h3>", unsafe_allow_html=True)
                    added_at = season.get('addedAt')
                    if added_at:
                        added_at_date = datetime.datetime.fromtimestamp(int(added_at))
                    else:
                        added_at_date = datetime.datetime.now()
                    new_date = st.date_input(
                        "Edit Added Date",
                        value=added_at_date.date(),
                        key=f"season_date_{season.get('ratingKey')}"
                    )
                    new_date_unix = int(datetime.datetime.combine(new_date, datetime.datetime.min.time()).timestamp())
                    if st.button("Update Date", key=f"update_season_{season.get('ratingKey')}"):
                        plex.update_added_date(section_id, season.get('ratingKey'), type_id, new_date_unix)
                        st.success(f"Updated added date for {season.get('title', 'Unknown Season')} to {new_date}")
        else:
            st.write("No TV seasons found.")

if __name__ == "__main__":
    main()