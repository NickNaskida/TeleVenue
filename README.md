# Venue Booking Mini Application

Bot link: [@TeleVenueBot](https://t.me/TeleVenueBot)

## Note
For a **detailed step-by-step guide** of the app development see [TUTORIAL.md](TUTORIAL.md)

## Description
This is a mini application that allows users to book venues.

## Video Demonstration
<img src="demo.gif" alt="demo video" width="50%">

## Tech Stack & Libraries

##### Client
  - React - [Documentation](https://react.dev)
  - Vite - [Documentation](https://vitejs.dev/guide/)
  - TailwindCSS - UI & CSS framework [Documentation](https://tailwindcss.com/docs)
  - React Hook Form - Form state [Documentation](https://react-hook-form.com/get-started)
  - React Router - Url navigation [Documentation](https://reactrouter.com/en/6.16.0/start/tutorial)  
  - Axios - Http requests [Documentation](https://axios-http.com/docs/intro)
  - NextUI - UI components [Documentation](https://nextui.org/docs/getting-started)
##### Server
  - Python 3.9 (3.8+ should work too)
  - FastAPI - Async web framework  [Documentation](https://fastapi.tiangolo.com/)
  - Aiogram - Async Telegram Bot API framework [Documentation](https://docs.aiogram.dev/en/latest/)
  - Pydantic - Validation Library [Documentation](https://docs.pydantic.dev/latest/)
  - SQLAlchemy - ORM [Documentation](https://docs.sqlalchemy.org/en/20/)
  - Alembic - Alembic [Documentation](https://alembic.sqlalchemy.org/en/latest/)
  - SQLite - Database  

## Project Structure
```
.
├── server/
│   ├── migrations         # alembic migrations
│   ├── scripts            # helper scripts
│   ├── src/
│   │   ├── api            # api stuff
│   │   ├── bot            # bot stuff
│   │   ├── models         # db models
│   │   ├── schemas        # data schemas
│   │   ├── utils          # other
│   │   ├── app.py         # main app file
│   │   └── config.py      # app config
│   ├── alembic.ini
│   ├── requirements.txt
│   ├── main.py
│   └── ...
└── frontend/
    ├── public
    ├── src
    │   ├── components     # reusable components
    │   ├── hooks          # custom hooks
    │   ├── pages          # pages
    │   ├── services       # api services
    │   ├── index.css
    │   └── index.jsx
    ├── example.env
    ├── index.html
    └── ...
```

## Setup

#### Cloning project

1. Clone project
    ```
    git clone https://github.com/NickNaskida/TeleVenue.git
    ```
2. Navigate to project directory
    ```
    cd TeleVenue
    ```
   
#### Telegram Bot Setup
1. Create a new bot using [BotFather](https://t.me/botfather)
2. Type `/newbot` and follow the instructions
3. Copy the bot token and save it somewhere. We will need it later
   ```
   ...
   
   Use this token to access the HTTP API:
    <your_bot_token>
   
   ...
   ```


#### Ngrok Setup
Telegram mini app requires a public url (https) to work. We will use `ngrok` to expose our local server to the internet.

1. Download & install ngrok from [here](https://ngrok.com/download)
2. Edit ngrok configuration file 
   ```
   sudo ngrok config edit      
   ```
3. Copy and paste this configuration. Remember to specify your `auth token`. You can get your auth token from dashboard [here](https://dashboard.ngrok.com/get-started/your-authtoken)
   ```
   version: "2"
   authtoken: <your_auth_token> # change this to your auth token
   tunnels:
     front:
       addr: 3000
       proto: http
     back:
       addr: 8000
       proto: http   
   ```
4. Save and exit the file: `Ctrl + X`, then `Y`, then `Enter`
5. Check configuration
   ```
   ngrok config check
   ```
6. Start ngrok
   ```
   ngrok start --all
   ```
7. Copy and save somewhere the forwarding url for `front` and `back`. We will need them later.

#### Configure application
1. Copy `example.env` file to `.env` in `frontend` directory
   ```
   cd frontend
   cp example.env .env
   ```
2. Edit `.env` file and paste the `back` url from ngrok in `VITE_BASE_API_URL` variable
   ```
   VITE_BASE_API_URL=<back_url>
   ```
4. Copy `example.env` file to `.env` in `server` directory
      ```
   cd ../server
   cp example.env .env
   ```
5. Edit `.env` file and paste the `front` and `back` url from ngrok in `FRONT_BASE_URL` and `BACK_BASE_URL` variables respectively. Also paste your bot token in `BOT_TOKEN` variable. Plus set `SECRET_KEY` to any random string
    ```
   SECRET_KEY=<secret_key>          # change this to random long string in production
   BOT_TOKEN=<your_bot_token>       # change this to your bot token that you obtained from botfather
   FRONT_BASE_URL=https://*********.ngrok-free.app   # change this to your front url from ngrok
   BACK_BASE_URL=https://*********.ngrok-free.app    # change this to your back url from ngrok
   ```

#### Run the application

###### frontend
1. Navigate to `frontend` directory
   ```
   cd frontend
   ```
2. Install dependencies
   ```
    npm install
    ```
3. Start the application
    ```
    npm run dev
    ```

###### server
1. Navigate to `server` directory in separate terminal
   ```
   cd server
   ```
2. Create virtual environment
   ```
   python3 -m venv venv
   ```
3. Activate virtual environment
   ```
   source venv/bin/activate
   ```
4. Install dependencies
    ```
    pip install -r requirements.txt
    ```
5. Run migrations
    ```
    alembic upgrade head
    ```
6. Start the application
   ```
   python main.py
   ```

#### Start bot with `/start` command and enjoy! 🎉🎉

## Common Errors and Troubleshooting

#### NPM package related errors

- if you get missing modules error when running the app, make sure you have installed all dependencies in `frontend` folder
   ```
   npm install
   ```

#### Python Related Errors

- Virtualenv issues
   - Make sure you activate virtual environment before installing dependencies and running the app
   - If you get `ModuleNotFoundError` when running the app, make sure you are in virtual environment and you have installed all dependencies
- Python Version issues
   - The project was developed with Python 3.10 but 3.8+ should work too
   - Make sure you have python 3.8+ installed

#### CORS Related Errors

Cross-Origin Resource Sharing (CORS) is a security feature implemented by web browsers to protect against unauthorized requests from different domains. When developing a web application, you might encounter CORS issues when your front-end code, hosted on one domain, tries to make requests to an API or server on a different domain. To enable these cross-domain requests safely, you need to configure CORS settings in your FastAPI app.

For instance, in this example app I already specified CORS settings in `server/src/app.py` file. CORS origins will auto include `FRONT_BASE_URL`.

```python
# backend/src/app.py

def create_app():
   # ...
   
   app.add_middleware(
     CORSMiddleware,
     allow_origins=[settings.FRONT_BASE_URL],  # Include your urls here to allow CORS issues
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"],
   )
   
   # ...

```

#### Telegram Bot Related Errors
- If you get `Unauthorized` error when trying to send messages to your bot, make sure you have specified the correct bot token in backend `.env` file

## Other Notes
- To enable inspect for web app, press settings icon 5 times and turn on `Debug Web App`

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details