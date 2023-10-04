# Venue Booking Mini Application

### Description
This is a mini application that allows users to book venues.

Video Demonstration - [demo]()

### Note
This file contains only the setup of this application. For a detailed explanation of my code see [TUTORIAL.md](TUTORIAL.md)

### Tech Stack & Libraries

##### Client
  - React - [Documentation](https://react.dev)
  - Vite - [Documentation](https://vitejs.dev/guide/)
  - TailwindCSS - UI & CSS framework [Documentation](https://tailwindcss.com/docs)
  - React Hook Form - Form state [Documentation](https://react-hook-form.com/get-started)
  - React Router - Url navigation [Documentation](https://reactrouter.com/en/6.16.0/start/tutorial)  
  - Axios - Http requests [Documentation](https://axios-http.com/docs/intro)
  - NextUI - UI components [Documentation](https://nextui.org/docs/getting-started)
##### Server
  - Python
  - FastAPI - Async web framework  [Documentation](https://fastapi.tiangolo.com/)
  - Aiogram - Async Telegram Bot API framework [Documentation](https://docs.aiogram.dev/en/latest/)
  - Pydantic - Validation Library [Documentation](https://docs.pydantic.dev/latest/)
  - SQLAlchemy - ORM [Documentation](https://docs.sqlalchemy.org/en/20/)
  - SQLite - Database  

### Project Structure
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

### Setup

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

#### Ngrok Setup
Telegram mini app requires a public url (https) to work. We will use `ngrok` to expose our local server to the internet.

1. Download ngrok from [here](https://ngrok.com/download)
2. Edit ngrok configuration file 
```
sudo ngrok config edit      
```
3. Copy and paste this configuration. Remember to specify your `auth token`
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
4. Save and exit the file: `Ctrl + X, Y, Enter`
5. Check configuration
```
ngrok config check
```
6. Start ngrok
```
ngrok start --all
```
7. Copy the `forwarding` url for `front` and `back` 

### Common Errors and Troubleshooting

### Other notes
- To enable inspect for web app, press settings icon 5 times and turn on `Debug Web App`

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details