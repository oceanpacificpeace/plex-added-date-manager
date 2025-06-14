import streamlit as st
from plex_api import PlexAPI
import datetime

st.set_page_config(page_title="Plex Added Date Manager")

def main():
    # Initialize Plex API
    plex = PlexAPI()
    
    # Fetch all movies
    movies = plex.get_all_movies()

    # Sort movies by addedAt descending (most recent first)
    movies = sorted(movies, key=lambda m: int(m.get('addedAt', 0)), reverse=True)

    # Display movies
    if movies:
        section_id = "1"  # Movies section
        type_id = "1"     # 1 for movie, 4 for episode
        for movie in movies:
            cols = st.columns([1, 2])
            with cols[0]:
                thumb = movie.get('thumb')
                if thumb:
                    poster_url = f"{plex.base_url}{thumb}?X-Plex-Token={plex.token}"
                    st.image(poster_url, width=120)
            with cols[1]:
                st.subheader(movie.get('title', 'Unknown Title') + f" ({movie.get('year', 'Unknown Year')})")
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

if __name__ == "__main__":
    main()