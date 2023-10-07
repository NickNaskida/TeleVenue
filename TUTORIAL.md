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
   - queryId is A unique identifier for the Mini App session, required for sending messages via the `answerWebAppQuery` method [Documentation here](https://core.telegram.org/bots/webapps#webappinitdata)

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

import apiInstance from '@/services/api'

import VenueCard from "@/components/VenueCard";
import { useTelegram } from '@/hooks/useTelegram';


const Index = () => {
  const { tg } = useTelegram();
  const [venueData, setVenueData] = useState([])

  useEffect(() => {
    const getVenueData = async () => {
      await apiInstance.get(
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


const apiInstance = axios.create({
  baseURL: `${import.meta.env.VITE_BASE_API_URL}`
});

export default apiInstance;
```
    
        
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

...
...
...

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
