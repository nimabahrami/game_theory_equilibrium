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

This is a Flask application (Python backend). To deploy it online, you will need a hosting provider that supports Python, such as:

*   **Render**
*   **Railway**
*   **PythonAnywhere**
*   **Heroku**

**Note:** This application cannot be hosted on GitHub Pages, as GitHub Pages only supports static websites (HTML/CSS/JS).
