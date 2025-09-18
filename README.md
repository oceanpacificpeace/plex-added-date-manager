# Plex Added Date Manager

Streamlit (Python) app that interacts with the Plex API to fetch and manage Added Date values.

<img width="1672" height="1217" alt="screen" src="https://github.com/user-attachments/assets/4d897988-9c44-4737-b4cf-eb4a53379d92" />


## Setup Instructions

1. **Clone the repository**
2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure your Plex credentials:** Create a `.env` file at project root
   ```ini
     PLEX_TOKEN=your_plex_token_here
     PLEX_BASE_URL=http://your-plex-ip:32400
   ```

## Usage

1. **Run the Streamlit application:**
   ```bash
   streamlit run src/app.py
   ```

2. **Access the application:**
   Open your web browser and go to `http://localhost:8501`.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
