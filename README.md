# Venue Booking Mini Application

### Description

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

#### Ngrok
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
7. Copy the `forwarding` url for `front` and `back` and ...

### Common Errors and Troubleshooting

### Other notes
- To enable inspect for web app, press settings icon 5 times and turn on `Debug Web App`