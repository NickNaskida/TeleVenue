import { useEffect } from "react";

import { Outlet } from "react-router-dom"

import { useTelegram } from "@/hooks/useTelegram";

const BaseLayout = () => {
  const { tg } = useTelegram();

  // Call the ready method as soon as the interface is loaded
  useEffect(() => {
    tg.ready();
  });

  return (
    <div
      className="w-full min-h-screen p-4"
    >
      <Outlet />
    </div>
  );
}

export default BaseLayout