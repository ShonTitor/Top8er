# Top 8 Graphic Generator

Top8er is a Django app that generates top 8 result graphics for many different fighting games tournaments using Pillow. These graphics include a picture of the player's main character as well as their nicknames and tournament placing. The graphic template parts used were made by [EDM](https://twitter.com/Elenriqu3). Character portraits are not included in this repository. You can see the app working [here](https://www.top8er.com/).

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/E1E4K0N2)  
[support the designer on paypal](https://www.paypal.com/paypalme/Elenriqu3)

![Top 8 Graphic Generator](https://i.imgur.com/iXjo0pU.png)

## Table of Contents

- [Features](#features)
- [Usage](#usage)
  - [Previous Requirements](#previous-requirements)
  - [Installation Instructions](#installation-instructions)
- [Contributing](#contributing)

## Features

- Boxes under each player's name for their twitter handle.
- Bottom Left, Top Left and Top Right texts to insert details regarding tournaments or other related information.
- Custom layout and font colors, custom backgrounds.
- Custom Palettes (only Eternal Fighter Zero)
- Support for Japanese and European characters (by changing the font).
- Option to import data from a [start.gg](https://start.gg/), [challonge](https://challonge.com/), or [tonamel](https://tonamel.com/) link.

## Usage

### Previous Requirements

- Python 3.12
- Node.js (any version)

### Installation Instructions

1. Clone the repository:
    ```sh
    git clone -b new-project-structure git@github.com:ShonTitor/Top8er.git
    cd Top8er
    ```

2. Copy the contents of the `starter_files` directory to the project root:
    ```sh
    cp -r starter_files/* .
    ```

3. Set up a virtual environment and install the required Python packages:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

4. Run the tests to ensure everything is set up correctly:
    ```sh
    python manage.py test
    ```

5. Apply the database migrations:
    ```sh
    python manage.py migrate
    ```

6. Start the Django development server:
    ```sh
    python manage.py runserver
    ```

7. Navigate to the `frontend` directory and install the required Node packages:
    ```sh
    cd frontend
    npm install
    ```

8. Build the frontend assets:
    ```sh
    npm run build
    ```

9. Open your browser and navigate to `http://127.0.0.1:8000` to see the app in action.

## Contributing

If you would like to contribute to this project, please follow the guidelines in the [HowToHelp.md](HowToHelp.md) file.