# Venue Booking Mini Application

### Description

### Tech Stack & Libraries

##### Client
  - React - [Documentation](https://react.dev)
  - Vite - [Documentation](https://vitejs.dev/guide/)
  - TailwindCSS - [Documentation](https://tailwindcss.com/docs)

##### Server
  - Python
  - FastAPI - Async web framework  [Documentation](https://fastapi.tiangolo.com/)
  - Aiogram - Async Telegram Bot API framework [Documentation](https://docs.aiogram.dev/en/latest/)
  - Pydantic - Validation Library [Documentation](https://docs.pydantic.dev/latest/)
  - SQLAlchemy - ORM [Documentation](https://docs.sqlalchemy.org/en/20/)
  - SQLite - Database  

### Project Structure
```
...
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