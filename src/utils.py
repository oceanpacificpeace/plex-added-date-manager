def format_date(date_string):
    from datetime import datetime

    try:
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        return None

def validate_date(date):
    from datetime import datetime

    if isinstance(date, datetime):
        return True
    return False

def format_movie_data(movie):
    return {
        "title": movie.title,
        "added_date": movie.addedAt.strftime("%Y-%m-%d"),
        "rating": movie.rating,
        "summary": movie.summary,
    }