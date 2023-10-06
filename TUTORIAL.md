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


### Backend side

### Common Errors and Troubleshooting

### Other notes
- To enable inspect for web app, press settings icon 5 times and turn on `Debug Web App`
