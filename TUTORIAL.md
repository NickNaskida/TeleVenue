# Mini App Development Step-by-Step Guide With React (Vite) & Python (Aiogram + FastAPI)

### Telegram Bot Setup
First before we start creating an application, we need to setup a Telegram bot. This bot will be used to communicate with our application.

1. Create a new bot using [BotFather](https://t.me/botfather)
2. Type `/newbot` and follow the instructions
3. Copy the bot token and save it somewhere. We will need it later
    ```
    ...
    
    Use this token to access the HTTP API:
    <your_bot_token>
    
    ...
    ```

### Ngrok Setup
Telegram mini app requires a public url (https) to work. We will use `ngrok` to expose our local server to the internet and obtain `https` temporary urls.

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


### Client side

Explanation & tutorial for client side. All of this happens inside `frontend` folder. 

#### React Setup with Vite
This project utilizes React & Vite as the frontend framework. To start developing, follow these steps:

1. Make sure you have Node.js installed. You can download it from [here](https://nodejs.org/en/download/)
2. Create react app with vite - [Vite Setup Guide](https://vitejs.dev/guide/#scaffolding-your-first-vite-project)
   ```
   npm create vite@latest
   ```
   Then follow the prompts. (Make sure you choose `react` as the framework and `javascript` as the language) I didn't use Typescript because it's a bit more complicated to setup.
3. Navigate to project and install dependencies
   ```
   cd <project_name>
   npm install
   ```
4. Run the project to test if it works
   ```
   npm run dev
   ```
   
#### Tailwind & NextUI Setup

In my project, I also use tailwind and NextUI as the UI framework. You can setup them by following these steps:

1. Install tailwindcss. Follow this straightforward tutorial to setup tailwindcss - [Tailwind Setup Guide](https://tailwindcss.com/docs/installation)

2. Then, install NextUI. Follow this straightforward tutorial to setup NextUI - [NextUI Setup Guide](https://nextui.org/docs/guide/installation) (By the way, you already completed step 1 which is installing tailwindcss)

#### Telegram Mini App Integration

Now lets initialize telegram mini app in our project, setup styling & create custom hook to work with `window.Telegram.WebApp` object.

##### Adding Telegram Script

Initialize Telegram mini app [Documentation here](https://core.telegram.org/widgets/login#initialization)

To connect your Mini App to the Telegram client, place the script telegram-web-app.js in the `<head>` tag before any other scripts in `frontend/index.html`, using this code:
   ```html
   <script src="https://telegram.org/js/telegram-web-app.js"></script>
   ```

##### Configuring App Styles according to telegram theme

Mini Apps can adjust the appearance of the interface to match the Telegram user's app in real time. 

Telegram provides a great API to access theme params. [Documentation here](https://core.telegram.org/bots/webapps#themeparams)

Let's set global html document theme so NextUI and Tailwind can adjust automatically according to the theme. Navigate to `frontend/index.html` and add following script in `<head>` tag

```html
<script>
     function setThemeClass() {
         document.documentElement.className = Telegram.WebApp.colorScheme;
     }
     Telegram.WebApp.onEvent('themeChanged', setThemeClass);
     setThemeClass();
</script>
```

This script ensures that if Telegram theme changes, our app will adjust accordingly. Moreover, NextUi and TailwindCSS will also adjust accordingly.

Lets also set styles with help of [css variables](https://core.telegram.org/bots/webapps#themeparams) that Telegram provides to us.

Navigate to `src/index.css` and add following styles

```css
body {
   color: var(--tg-theme-text-color);
   background: var(--tg-theme-bg-color);
}

.hint { 
   color: var(--tg-theme-hint-color);
}

.link {
   color: var(--tg-theme-link-color);
}

.tg-button {
   background: var(--tg-theme-button-color);
   color: var(--tg-theme-button-text-color);
}

.card {
  background: var(--tg-theme-bg-color);
}
```

You can change class names according to your needs. I used these classes in my project.

##### Creating custom React hook to work with Telegram object.

Now lets create a custom hook to work with `window.Telegram.WebApp` object.

Create a new file  in `src/hooks/` with name `useTelegram.js` and add following code

```javascript
const tg = window.Telegram.WebApp;  // access telegram object

export function useTelegram() {
  // Telegram docs for main button methods - https://core.telegram.org/bots/webapps#mainbutton 
  const onToggleButton = () => {   // toggle telegram main button.
    if (tg.MainButton.isVisible) {
      tg.MainButton.hide();
    } else {
      tg.MainButton.show();
    }
  }

  return {
    onToggleButton,  // return toggle button function
    tg, // return telegram window object
    user: tg.initDataUnsafe?.user,  // return user data
    queryId: tg.initDataUnsafe?.queryId,  // return query id
  }
}
```

Note:
   - tg is a telegram window object. [Documentation here](https://core.telegram.org/bots/webapps#initializing-mini-apps)
   - user is a user data object obtained from `WebAppInitData`. [Documentation here](https://core.telegram.org/bots/webapps#webappinitdata)
   - queryId is a unique identifier for the Mini App session, required for sending messages via the `answerWebAppQuery` method [Documentation here](https://core.telegram.org/bots/webapps#webappinitdata)

I provide minimal functionality in this hook. You can add more functionality according to your needs.

#### React Router V6 Setup

Next lets setup routing. We will use `react-router-dom` version 6 for this.

Here is a detailed tutorial of how to use react-router-dom v6 - [React Router v6 Tutorial](https://reactrouter.com/en/6.16.0/start/tutorial). I will focus on the specific parts only that I used in my project.

1. Navigate to `src/main.jsx` and configure the router
```javascript
import React from "react";
import ReactDOM from "react-dom/client";

// Import react router
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { NextUIProvider } from "@nextui-org/react";

import "./index.css";

// Route components
import BaseLayout from "@/pages/BaseLayout.jsx";
import Index from "@/pages/Index.jsx";
import BookingIndex from "@/pages/BookingIndex.jsx";

// Initialize react router
const router = createBrowserRouter([
 {
   path: "/",  // base route path
   element: <BaseLayout />,   // Define main layout component. All child routes will be rendered inside this component
   children: [
     { path: "/", element: <Index /> },  // Define index component
     { path: "/book/:venueId", element: <BookingIndex /> },  // Define booking index component. Notice that it has venueId parameter in the url
   ],
 },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
 <React.StrictMode>
   <NextUIProvider>
      // add router provider
     <RouterProvider router={router} />
   </NextUIProvider>
 </React.StrictMode>
);

```

Then lets create the layout component. This component will be used as the main layout for all pages.

2. Navigate to `/src/pages/BaseLayout.jsx` and create the layout component
```javascript
import { useEffect } from "react";

import { Outlet } from "react-router-dom"

import { useTelegram } from "@/hooks/useTelegram";

const BaseLayout = () => {
 const { tg } = useTelegram();  // obtain telegram object from custom hook that we created earlier

 // Call the ready method as soon as the interface is loaded
 useEffect(() => {
   tg.ready();
 });

 return (
   <div
     className="w-full min-h-screen p-4"
   >
     <Outlet />  // Place where child route components will be rendered
   </div>
 );
}

export default BaseLayout;
```
- `<Outlet>` is a specific layout component from react-router-dom v6. It will render all child routes inside this component.
- Notice that I also added the `tg.ready()` (method that informs the Telegram app that the Mini App is ready to be displayed). By wrapping it inside `useEffect` hook, we ensure that this method will be called as soon as the interface is loaded.

Now, lets create the index page component. This component will be rendered when user opens the mini app.

3. Navigate to `/src/pages/Index.jsx` and create the index page component
```javascript
import { useState, useEffect } from 'react'

import axiosInstance from '@/services/api'

import VenueCard from "@/components/VenueCard";
import { useTelegram } from '@/hooks/useTelegram';


const Index = () => {
  const { tg } = useTelegram();
  const [venueData, setVenueData] = useState([])

  useEffect(() => {
    const getVenueData = async () => {
      await axiosInstance.get(
        "/venues/"
      ).then((res) => {
        setVenueData(res.data)
      })
    }
    getVenueData();

    // Hide buttons so they are not visible when we navigate from page that had them visible
    // Hide back button
    tg.BackButton.hide();
    // Hide main button
    tg.MainButton.hide();
  }, [])

  return (
    <>
      <header className="flex justify-center items-center pb-2 font-bold">
        Venue Listing
      </header>
      <section className="grid grid-cols-2 grid-rows-2 gap-5">
        {venueData.map((venue) => (
          <VenueCard key={venue.id} venue={venue} />
        ))}
      </section>
    </>
  );
}

export default Index;
```
- Here `useEffect` hook is used to fetch venue data from backend. It runs on page load and fetches data from `/venues/` endpoint. (more about this endpoint later when we will implement backend side)
- Fetched data is stored in `venueData` state variable. We use this variable to render venue cards via cycling through it with `map` function.
- I also added `tg.BackButton.hide()` and `tg.MainButton.hide()` to hide back and main buttons. This is done so that these buttons are not visible when we navigate from page that had them visible.


You should also create a separate axios Instance `src/services/api.js` that automatically sets base url for all requests.
- I assume is axios installed at this point. If not, install it with `npm install axios`
    
```javascript
import axios from "axios";


const axiosInstance = axios.create({
  baseURL: `${import.meta.env.VITE_BASE_API_URL}`
});

export default axiosInstance;
```

Since, we use environment variable to store base url, we need to create `.env` file in `frontend` directory and add following line to it
```
VITE_BASE_API_URL=<back_url>
```

Replace `<back_url>` with the url that you obtained from ngrok earlier.

        
Next, create a venue card component to display venue data. You can create your own component or use mine. Here is the code for venue card component:

```javascript
import { useNavigate } from "react-router-dom";

import { Card, CardHeader, CardFooter, Image, Button } from "@nextui-org/react";

const VenueCard = ({ venue }) => {
  const navigate = useNavigate();

  return (
    <Card radius="lg" className="border-none max-w-xl h-full">
      <CardHeader className="absolute z-10 top-0 flex-col !items-start">
        <span className="font-bold text-lg drop-shadow-2xl">{venue.name}</span>
      </CardHeader>
      <Image
        src={`/images/${venue.id}.jpg`}
        removeWrapper
        className="z-0 object-cover"
        loading="lazy"
      />
      <CardFooter className="flex flex-col items-start overflow-hidden pb-1 absolute bottom-0 shadow-small z-10">
        <Button
          className="text-xs font-bold tg-button w-full"
          variant="flat"
          color="default"
          radius="md"
          size="sm"
          onClick={() => {navigate(`/book/${venue.id}`)}}
        >
          Book Now
        </Button>
      </CardFooter>
    </Card>
  );
};

export default VenueCard;
```
- For demonstration purposes I assign image url to `/images/${venue.id}.jpg`. Ideally image links should be provided by backend.
- Also, I use `useNavigate` hook from react-router-dom v6 to navigate to booking page. I also passed `venueId` parameter in the url. We get this parameter to from backend.

At this point, we have successfully setup index page. Now lets setup booking page.

4. Navigate to `/src/pages/BookingIndex.jsx` and create the booking page component
```javascript
import { useState, useEffect, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";

import { Image, Spinner, Input } from "@nextui-org/react";

import axiosInstance from "@/services/api";
import { useTelegram } from "@/hooks/useTelegram";

const STATUS = {
  IDLE: "IDLE",
  LOADING: "LOADING",
  ERROR: "ERROR",
  SUCCESS: "SUCCESS",
};

const BookingIndex = () => {
  const { tg } = useTelegram();
  const navigate = useNavigate();

  const { venueId } = useParams();
  const [venue, setVenue] = useState(null);
  const [status, setStatus] = useState(STATUS.IDLE);

  const {
    register,
    formState: { errors },
    handleSubmit,
  } = useForm();
  const onSubmit = useCallback(
    (data) => {
      const abortController = new AbortController();

      // Send required fields
      axiosInstance.post(`/bookings/${venueId}`, {
        signal: abortController.signal,
        _auth: tg.initData,
        queryId: tg.initData.queryId,
        under_name: data.under_name,
        date: data.date,
        comment: data.comment,
      });
    },
    [venueId, tg]
  );

  useEffect(() => {
    const abortController = new AbortController();
    tg.onEvent("mainButtonClicked", () => {
      handleSubmit(onSubmit)();
    });

    return () => {
      abortController.abort();
    };
  }, [tg, handleSubmit, onSubmit]);

  useEffect(() => {
    setStatus(STATUS.LOADING);

    const getVenueData = async () => {
      try {
        const response = await axiosInstance.get(`/venues/${venueId}`);
        setVenue(response.data);
        setStatus(STATUS.SUCCESS);
      } catch (error) {
        setStatus(STATUS.ERROR);
      }
    };

    getVenueData();

    // set telegram button
    tg.MainButton.text = "Book Now";
    tg.MainButton.show();
    // show back button
    tg.BackButton.show();
  }, [venueId]);

  // handle back button click
  tg.onEvent("backButtonClicked", () => {
    navigate("/");
  });

  return (
    <section>
      {status === STATUS.SUCCESS ? (
        <>
          <div className="flex flex-row gap-3 mb-4">
            <Image
              src={`/images/${venueId}.jpg`}
              className="w-20 h-20"
              loading="lazy"
            />
            <div className="flex flex-col justify-center">
              <span className="text-xl font-bold">{venue.name}</span>
              <span className="text-xs hint mb-1">
                {venue.address}, {venue.city}
              </span>
              <span className="text-xs">{venue.description}</span>
            </div>
          </div>
          <form className="flex flex-col gap-2">
            <Input
              variant="bordered"
              label="Under Name"
              labelPlacement="outside"
              placeholder="your name"
              validationState={errors.under_name ? "invalid" : "valid"}
              errorMessage={errors.under_name && errors.under_name.message}
              {...register("under_name", {
                required: "under name is required",
              })}
            />
            <p className="text-small">Date</p>
            <Input
              type="date"
              variant="bordered"
              validationState={errors.date ? "invalid" : "valid"}
              errorMessage={errors.date && errors.date.message}
              {...register("date", { required: "date is required" })}
            />
            <Input
              variant="bordered"
              label="Comment (optional)"
              labelPlacement="outside"
              placeholder="any comments?"
              {...register("comment")}
            />
          </form>
        </>
      ) : status === STATUS.LOADING ? (
        <div className="flex justify-center items-center h-48">
          <Spinner color="primary" size="lg" />
        </div>
      ) : (
        <div className="flex justify-center items-center h-48">
          <span className="text-2xl font-bold">Error</span>
        </div>
      )}
    </section>
  );
};

export default BookingIndex;
```

Wow! That's a lot of code. Let's break it down.

1. First, we define `STATUS` object. This object will be used to display different components depending on the status of the request. We will use this object later in the code.
2. Then, we define `useForm` hook from `react-hook-form` library. This hook will be used to handle form data. [Documentation here](https://react-hook-form.com/get-started)
3. Next, we define `onSubmit` function. This function will be used to send form data to backend. We use `axiosInstance` to send data. We created this instance earlier.
    - Here you can see that we send a lot of stuff to backend. Lets look at it in more detail:
      - signal: abortController.signal
      -  _auth: tg.initData - this is auth data that we obtained from `WebAppInitData` object. It is essential to check the data validity in our backend. [Validating data received via the Mini App](https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app)
      -  queryId: tg.initData.queryId - this is query id that we obtained from `WebAppInitData` object. It is a unique identifier for the Mini App session, required for sending messages via the answerWebAppQuery method.
      -  under_name: data.under_name - this is name from our form input
      -  date: data.date - this is date from our form input
      -  comment: data.comment - this is optional field from our form input
4. Then, we define `useEffect` hook. This hook will be used to handle `mainButtonClicked` event. This event is triggered when user clicks on the main button. We use `handleSubmit` function from `react-hook-form` to handle form submission. We also pass `onSubmit` function to `handleSubmit` function. This is done so that `onSubmit` function is called when user clicks on the main button.
    - we also define abort controller to cancel the request if user navigates away from the page. [Abort Controller Explanation](https://medium.com/@icjoseph/using-react-to-understand-abort-controllers-eb10654485df)
5. Next, we define another `useEffect` hook. This hook will be used to fetch venue data from backend. We use `axiosInstance` to fetch data. We also set `tg.MainButton.text` to `Book Now` and show the main & back buttons. [Telegram Main Button Docs](https://core.telegram.org/bots/webapps#mainbutton), [Telegram Back Button Docs](https://core.telegram.org/bots/webapps#backbutton)
6. Then, we define `tg.onEvent("backButtonClicked")` event. This event is triggered when user clicks on the back button. We use `useNavigate` hook from `react-router-dom` to navigate to index page.
7. Finally, we render different components depending on the status of the request. If status is `SUCCESS`, we render the form. If status is `LOADING`, we render the spinner. If status is `ERROR`, we render the error message.

### Backend side

Explanation & tutorial for backend side. All of this happens inside `server` folder.

#### Base Setup

Okay, now lets setup backend side. We will use `FastAPI` as the core backend framework. To start developing, follow these steps:

1. Make sure you have Python 3.8+ installed. You can download it from [here](https://www.python.org/downloads/)
2. Create a new virtual environment
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

For this project I use `aiogram` library to work with telegram bot. [Documentation here](https://docs.aiogram.dev/en/latest/)

To combine `FastAPI` and `aiogram` I use [aiogram-fastapi-server](https://github.com/4u-org/aiogram_fastapi_server) library. Also this library has its own [bot template](https://github.com/4u-org/bot-template) that shows how to use the library.

I will not discuss project structure here. You can read about it in [README.md](README.md#tech-stack--libraries)

#### Base FastAPI and Aiogram app Setup

First lets create app factory function. This function will be used to create FastAPI app.

1. Navigate to `server/src/app.py` and create app factory function
```python
import sys
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware

from src.config import settings


def create_app():
    """Application factory."""
    # logging configuration
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    # configure application
    app = FastAPI(
        title="Venue Booking API",
        docs_url="/",
    )

    # Register application routers
    register_app_routers(app)

    # Add app middleware
    app.add_middleware(
        SQLAlchemyMiddleware,
        db_url=settings.SQLALCHEMY_DATABASE_URI,
        engine_args={  # SQLAlchemy engine example setup
            "echo": True,
            "pool_pre_ping": True
        },
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONT_BASE_URL],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


def register_app_routers(app: FastAPI):
    pass
```
- Here we do several things
    - configure basic python logging `logging.basicConfig(level=logging.INFO, stream=sys.stdout)`
    - configure FastAPI app `app = FastAPI(...)`
    - register application routers `register_app_routers(app)`. We will add routers later
    - add SQLAlchemy middleware `app.add_middleware(SQLAlchemyMiddleware, ...)`. This middleware will be used to work with database. [Documentation here](https://pypi.org/project/fastapi-async-sqlalchemy/)
    - add CORS middleware `app.add_middleware(CORSMiddleware, ...)`. Note that we specify our frontend url from ngrok in allow_origins `allow_origins=[settings.FRONT_BASE_URL]`. [Documentation here](https://fastapi.tiangolo.com/tutorial/cors/)

As you can see we import settings from `src.config` module. Lets create this module.

2. Navigate to `server/src/config.py` and create settings module
```python
import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class DevSettings(BaseSettings):
    DEBUG: bool = True
    SECRET_KEY: str = "NOT_A_SECRET"

    BOT_TOKEN: str
    FRONT_BASE_URL: str
    BACK_BASE_URL: str

    SQLALCHEMY_DATABASE_URI: str = 'sqlite+aiosqlite:///' + os.path.join(BASE_DIR, 'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    # Environment
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding='utf-8'
    )


settings = DevSettings()
```
- Here we use `pydantic_settings` library to load settings from `.env` file. [Documentation here](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- Lets break down some things that we define here:
    - `BOT_TOKEN` - this is the token that we obtained from BotFather earlier
    - `FRONT_BASE_URL` - this is the url that we obtained from ngrok earlier. It is used to handle CORS issues
    - `BACK_BASE_URL` - this is the url that we obtained from ngrok earlier. It is used to handle CORS issues
    - `SQLALCHEMY_DATABASE_URI` - this is the database url. We use `aiosqlite` library to work with database.
    - All of this variables are loaded from `.env` file. You can read more about `.env` file [here](https://pypi.org/project/python-dotenv/)
      - `model_config` - this is the configuration for `pydantic_settings` library. We specify `.env` file path and encoding here.

Lets also create `.env` file in `src/` folder to store environment variables that we defined above. Add the following lines to `.env` file
```
SECRET_KEY=<secret_key>          # change this to random long string in production
BOT_TOKEN=<your_bot_token>       # change this to your bot token that you obtained from botfather
FRONT_BASE_URL=https://*********.ngrok-free.app   # change this to your front url from ngrok
BACK_BASE_URL=https://*********.ngrok-free.app    # change this to your back url from ngrok
```



3. Now lets integrate bot with FastAPI app. Navigate to `server/src/bot/__init__.py` and add following code
```python
from aiogram import Bot

from src.bot import start
from src.config import settings


# Bot initialization
bot = Bot(token=settings.BOT_TOKEN, parse_mode="HTML")

bot_routers = [start.router]
```
- Here we initialize bot with `Bot` class from `aiogram` library. [Documentation here](https://docs.aiogram.dev/en/latest/api/bot.html)
- We also add bot routers that will handle bot commands.

4. Now lets create bot routers. Navigate to `server/src/bot/start.py` and add following code
```python
from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    Message,
    WebAppInfo,
)

router = Router()


welcome_message = """
Hey! What's up?\n
Looking where to hang out?\n
I got you covered! Press the button below to find the best places.
"""


@router.message(Command("start"))
async def command_start(message: Message, bot: Bot, base_url: str):
    await bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=MenuButtonWebApp(text="See Venues", web_app=WebAppInfo(url=f"{base_url}")),
    )
    await message.answer(
        welcome_message,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="See Venue Listing", web_app=WebAppInfo(url=f"{base_url}")
                    )
                ]
            ]
        ),
    )
```
- Here we first define bot router from aiogram library `router = Router()`
- Then we add a handler for `/start` command `@router.message(Command("start"))`. This will listen to every message and execute the function if the message is `/start` command.
    - Inside the handler we do two things:
      - We add a button to the chat menu `await bot.set_chat_menu_button(...)`. This button will be visible in the chat menu. [Documentation here](https://docs.aiogram.dev/en/latest/api/methods/set_chat_menu_button.html)
      - We send a welcome message with an inline button `await message.answer(...)`. This inline button will be visible under the reply message. [Documentation here](https://docs.aiogram.dev/en/latest/api/methods/send_message.html)

Note that both `MenuButtonWebApp` and `InlineKeyboardButton` have `web_app` parameter. [web_app param | aiogram](https://docs.aiogram.dev/uk_UA/latest/api/types/inline_keyboard_button.html#aiogram.types.inline_keyboard_button.InlineKeyboardButton.web_app)

5. Now lets add bot to FastAPI app factory. Navigate to `server/src/app.py` and add following code
```python
import sys
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# add these 3 lines of imports
from aiogram_fastapi_server import SimpleRequestHandler, setup_application  # NEW
from aiogram import Bot, Dispatcher   # NEW
from aiogram.types import MenuButtonWebApp, WebAppInfo  # NEW

from fastapi_async_sqlalchemy import SQLAlchemyMiddleware

from src.config import settings

# import our bot and bot routers
from src.bot import bot, bot_routers # NEW


# Create a startup event handler
# NEW
async def on_startup(bot: Bot, base_url: str):   
    await bot.set_webhook(f"{settings.BACK_BASE_URL}/webhook")
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="Book Venue", web_app=WebAppInfo(url=base_url))
    )


def create_app():
    """Application factory."""
    # logging configuration
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    # Configure dispatcher
    dispatcher = Dispatcher()    # NEW
    dispatcher["base_url"] = settings.FRONT_BASE_URL  # NEW
    dispatcher.startup.register(on_startup)   # NEW

    # Register bot routers
    register_bot_router(dispatcher)  # NEW

    # configure application
    app = FastAPI(
        title="Venue Booking API",
        docs_url="/",
    )

    # Register application routers
    register_app_routers(app)

    # Add app middleware
    app.add_middleware(
        SQLAlchemyMiddleware,
        db_url=settings.SQLALCHEMY_DATABASE_URI,
        engine_args={  # SQLAlchemy engine example setup
            "echo": True,
            "pool_pre_ping": True
        },
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONT_BASE_URL],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add bot and dispatcher to application
    # NEW
    SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot
    ).register(app, path="/webhook")
    setup_application(app, dispatcher, bot=bot)

    return app


# add this lines where we loop through bot routers and register them.
# NEW
def register_bot_router(dispatcher: Dispatcher):
    for router in bot_routers:
        dispatcher.include_router(router)


def register_app_routers(app: FastAPI):
    pass
```
- Here we do several things:
    - First, we configure a bot startup event that sets menu button and webhook.
    - Then, we configure dispatcher `dispatcher = Dispatcher()`. [Documentation here](https://docs.aiogram.dev/en/latest/dispatcher/dispatcher.html)
        - We also add `base_url` variable to dispatcher. This variable will be used to pass base url to bot routers.
        - We also register `on_startup` event that we created earlier to dispatcher.
    - Then, we register bot routers `register_bot_router(dispatcher)`. We loop through all bot routers and register them.


Okay, now we have a base setup that allows us to handle bot events and API calls. Let's move on to building the actual app.

First, lets create all necessary models and setup database migrations with [alembic](https://alembic.sqlalchemy.org/en/latest/)

#### Creating DB Models
1. install sqlalchemy if you haven't already
    ```
    pip install sqlalchemy
    ```
2. Create a base model file `server/src/models/base.py` and add following code:
```python
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class PkBase:
    """Base model with default columns."""
    id = Column(Integer, primary_key=True, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
```
- This is a standard sqlalchemy model. `@as_declarative` decorator is used to create a base class for all models. [Documentation here](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.as_declarative)
- PkBase is the base model that others inherit from. it has 3 properties. `id` is the primary key. `updated_at` and `created_at` are timestamps that are automatically updated when the model is updated or created.

3. Create a venue model file `server/src/models/venue.py` and add following code:
```python
from sqlalchemy import Column, String

from src.models.base import PkBase


class Venue(PkBase):
    """Venues model."""
    __tablename__ = 'venues'

    name = Column(String(255), nullable=False)
    description = Column(String(600), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
```
- Here we create a `Venue` model that inherits from `PkBase` model.
- We also define `__tablename__` property. This property is used to specify the table name in the database.

4. Finally, create a booking model file `server/src/models/booking.py` and add following code:
```python
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from src.models.base import PkBase


class Booking(PkBase):
    """Booking model."""
    __tablename__ = 'bookings'

    venue_id = Column(String, ForeignKey('venues.id'))
    venue = relationship('Venue', lazy="selectin")
    user_id = Column(String)
    under_name = Column(String)
    date = Column(Date)
    comment = Column(String, nullable=True)
```
- Here we create a `Booking` model that again inherits from `PkBase` model.
- We also specify `venue_id` as a foreign key and `venue` as a relationship. [More about SQLAlchemy relationships](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#relationship-patterns)

5. Also remember to add these models to `server/src/models/__init__.py` file. We need this to ensure that migrations will work properly and see our models.
```python
from src.models.venue import Venue
from src.models.booking import Booking
```

#### Alembic Setup
1. Install alembic if you haven't already
    ```
    pip install alembic
    ```
2. Initialize async alembic migrations in `server` folder
    ```
    alembic init -t async migrations
    ```
3. The folder named `migrations` will be created. Navigate to `server/migrations/env.py` and add modify the file as follows:
```python
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool, engine_from_config  # UPDATED
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine  # NEW

from alembic import context

from src.config import settings  # NEW
from src.models.base import PkBase  # NEW

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set metadata
target_metadata = PkBase.metadata   # UPDATED

target_metadata.naming_convention = {  # NEW
   "ix": "ix_%(column_0_label)s",
   "uq": "uq_%(table_name)s_%(column_0_name)s",
   "ck": "ck_%(table_name)s_%(constraint_name)s",
   "fk": "fk_%(table_name)s_%(column_0_name)"
         "s_%(referred_table_name)s",
   "pk": "pk_%(table_name)s"
}


def run_migrations_offline() -> None:
    url = settings.SQLALCHEMY_DATABASE_URI  # UPDATED
    context.configure(
        url=url,  # UPDATED
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# Other code ...


async def run_async_migrations() -> None:
    configuration = config.get_section(config.config_ini_section)  # UPDATED
    configuration["sqlalchemy.url"] = settings.SQLALCHEMY_DATABASE_URI  # UPDATED

    connectable = AsyncEngine(  # NEW
        engine_from_config(  # UPDATED
            configuration,  # UPDATED
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

# Other code ...
```
- Here we imported necessary libraries and functions. 
- Imported `settings` and `PkBase` from `src.config` and `src.models.base` respectively
- Changed `target_metadata` to `PkBase.metadata`
- Added naming convention to `target_metadata.naming_convention`. [More about naming convention](https://docs.sqlalchemy.org/en/20/core/constraints.html#constraint-naming-conventions)
- Also Edited database url in `run_migrations_offline` function
- Finally, Edited database configuration in `run_async_migrations` function. We provided `AsyncEngine` with custom url in configuration.

4. Running migrations
- You can run them manually with commands:
```
alembic revision --autogenerate -m "init"
alembic upgrade head
```
- Or you can use one of my bash scripts to run them automatically
```
sudo bash scripts/linux/migrate.sh
```

5. Now check your database with visual tool like [DB Browser for SQLite](https://sqlitebrowser.org/). You should see tables created.



### Common Errors and Troubleshooting

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

#### Alembic migrations related errors
- Migration conflicts and errors
  - Sometimes your migrations may conflict with each other. To fix this, you can delete sqlite database file and versions folder. After that just run migrations again.
    ```
    alembic revision --autogenerate -m "init"
    alembic upgrade head
    ```
- Models aren't seen by alembic. No tables get created.
  - In this case make sure you inherit from `PkBase` model in your models.
  - Also if you define another base model, you should import it and any other model(s) in `migrations/env.py` file


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


### Other notes
- To enable inspect for web app, press settings icon 5 times and turn on `Debug Web App`
