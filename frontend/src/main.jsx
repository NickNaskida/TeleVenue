import React from "react";
import ReactDOM from "react-dom/client";

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
    path: "/",
    element: <BaseLayout />,
    children: [
      { path: "/", element: <Index /> },
      { path: "/book/:venueId", element: <BookingIndex /> },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <NextUIProvider>
      <RouterProvider router={router} />
    </NextUIProvider>
  </React.StrictMode>
);
