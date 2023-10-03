import { useState, useEffect } from 'react'

import apiInstance from '@/services/api'

import VenueCard from "@/components/VenueCard";
import { useTelegram } from '@/hooks/useTelegram';


const Index = () => {
  const { tg, user } = useTelegram();
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

export default Index