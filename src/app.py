import streamlit as st
import requests
from plex_api import PlexAPI
import datetime

st.set_page_config(page_title="Plex Added Date Manager")


def select_library(sections, label, key):
    """Let the user pick one library from a list of Plex sections. Returns its key, or None."""
    if not sections:
        return None
    if len(sections) == 1:
        return str(sections[0].get('key'))
    titles = {str(s.get('key')): s.get('title', f"Library {s.get('key')}") for s in sections}
    return st.selectbox(label, options=list(titles), format_func=titles.get, key=key)


def main():
    st.markdown("<h2 style='text-align: center;'>Plex Added Date Manager</h2>", unsafe_allow_html=True)
    # Initialize Plex API
    plex = PlexAPI()

    if not plex.base_url or not plex.token:
        st.error("PLEX_BASE_URL and PLEX_TOKEN must be set (see README).")
        st.stop()

    try:
        sections = plex.fetch_sections()
    except requests.exceptions.RequestException as e:
        st.error(f"Could not load libraries from {plex.base_url}: {e}")
        st.stop()
    movie_sections = [s for s in sections if s.get('type') == 'movie']
    show_sections = [s for s in sections if s.get('type') == 'show']

    tab1, tab2 = st.tabs(["Movies", "TV Series"])

    # --- Movies Tab ---
    with tab1:
        section_id = select_library(movie_sections, "Movie library", "movie_library")
        if section_id is None:
            st.write("No movie libraries found.")
            movies = []
        else:
            movies = plex.get_all_movies(section_id) or []

        # Sort movies by addedAt descending (most recent first)
        movies = sorted(movies, key=lambda m: int(m.get('addedAt', 0)), reverse=True)

        # Display movies
        if movies:
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
        elif section_id is not None:
            st.write("No movies found.")

    # --- TV Series Tab ---
    with tab2:
        type_id = "2"
        section_id = select_library(show_sections, "TV library", "tv_library")
        if section_id is None:
            st.write("No TV libraries found.")
            seasons = []
        else:
            seasons = plex.fetch_seasons(section_id) or []
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
                    
                    if st.button("Update Date", key=f"update_all_{season.get('ratingKey')}"):
                        with st.spinner("Updating season and all episodes..."):
                            # Method 1: Update the season/series itself
                            try:
                                plex.update_added_date(section_id, season.get('ratingKey'), type_id, new_date_unix)
                                st.info("✓ Updated season metadata")
                            except Exception as e:
                                st.warning(f"⚠ Season update failed: {str(e)}")
                            
                            # Method 2: Update all episodes in the series
                            try:
                                season_rating_key = season.get('ratingKey')
                                parent_rating_key = season.get('parentRatingKey')
                                if not parent_rating_key:
                                    parent_rating_key = season_rating_key
                                
                                updated, failed = plex.update_all_episodes_date(section_id, parent_rating_key, new_date_unix)
                                if failed == 0:
                                    st.success(f"✅ Updated {updated} episodes to {new_date}")
                                else:
                                    st.success(f"✅ Updated {updated} episodes, {failed} failed")
                            except Exception as e:
                                st.error(f"❌ Episode update failed: {str(e)}")
        elif section_id is not None:
            st.write("No TV seasons found.")

if __name__ == "__main__":
    main()