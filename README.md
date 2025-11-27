# TrippleB - Game Theory Analysis Platform

A modern, AI-driven web application for analyzing strategic form games and calculating Nash Equilibria.

## Features

*   **Strategic Form Analysis**: Define players, strategies, and payoff variables.
*   **Dynamic Payoffs**: Add unlimited payoff variables for complex game modeling.
*   **Nash Equilibrium Calculation**: Automatically finds equilibria and valid ranges for parameters.
*   **Modern Dashboard UI**: A professional, dark-themed financial dashboard interface.
*   **Interactive**: Inline editing and dynamic table management.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/nimabahrami/game_theory_equilibrium.git
    cd trippleB
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the application:**
    ```bash
    python3 app.py
    ```

2.  **Open your browser:**
    Navigate to `http://127.0.0.1:5000`.

3.  **Analyze a Game:**
    *   Define Nature's states (if applicable).
    *   Configure Player 1 and Player 2 names and strategies.
    *   Add payoff variables (e.g., Revenue, Cost) and enter values for each case.
    *   Click "Run Simulation" to see the results.

## Deployment

### Deploying to PythonAnywhere

1.  **Create an Account:** Sign up at [www.pythonanywhere.com](https://www.pythonanywhere.com/).

2.  **Open a Bash Console:**
    *   Go to the **Consoles** tab and start a new **Bash** console.

3.  **Clone the Repository:**
    ```bash
    git clone https://github.com/nimabahrami/game_theory_equilibrium.git
    cd game_theory_equilibrium
    ```

4.  **Create a Virtual Environment & Install Dependencies:**
    ```bash
    mkvirtualenv --python=/usr/bin/python3.9 myenv
    pip install -r requirements.txt
    ```
    *(Note: `mkvirtualenv` is a helper tool on PythonAnywhere. You can name your environment whatever you like, e.g., `myenv` or `venv`)*

5.  **Configure the Web App:**
    *   Go to the **Web** tab.
    *   Click **Add a new web app**.
    *   Click **Next**, then select **Flask**.
    *   Select **Python 3.9** (or whichever version you used for the virtualenv).
    *   Enter the path to your app file (e.g., `/home/yourusername/game_theory_equilibrium/app.py`) or just accept the default for now (we will edit the WSGI file next).

6.  **Configure WSGI File:**
    *   On the **Web** tab, look for the **WSGI configuration file** link (e.g., `/var/www/yourusername_pythonanywhere_com_wsgi.py`) and click it.
    *   Delete the default content and replace it with:
        ```python
        import sys
        import os

        # Add your project directory to the sys.path
        project_home = '/home/yourusername/game_theory_equilibrium'
        if project_home not in sys.path:
            sys.path = [project_home] + sys.path

        # Import flask app but need to call it "application" for WSGI to work
        from app import app as application
        ```
    *   **Important:** Replace `yourusername` with your actual PythonAnywhere username.

7.  **Set Virtual Environment:**
    *   Back on the **Web** tab, under the **Virtualenv** section, enter the path to your virtual environment:
        `/home/yourusername/.virtualenvs/myenv`

8.  **Reload:**
    *   Click the big green **Reload** button at the top of the Web tab.
    *   Visit your site at `https://yourusername.pythonanywhere.com`.
