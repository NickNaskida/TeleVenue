import { useState, useEffect } from "react";
import { useParams, useLocation, useNavigate } from "react-router-dom";

import { Image, Spinner } from "@nextui-org/react";

import axiosInstance from "@/services/api";
import { useTelegram } from "@/hooks/useTelegram";

const STATUS = {
  IDLE: "IDLE",
  LOADING: "LOADING",
  ERROR: "ERROR",
  SUCCESS: "SUCCESS",
};

const BookingIndex = () => {
  const { tg, queryId } = useTelegram();
  const navigate = useNavigate();
  const location = useLocation();

  const { venueId } = useParams();
  const [venue, setVenue] = useState(null);
  const [status, setStatus] = useState(STATUS.IDLE);

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

  // handle main button click
  useEffect(() => {
    const abortController = new AbortController();

    tg.onEvent("mainButtonClicked", () => {
      axiosInstance.post(`/bookings/${venueId}`, {
        signal: abortController.signal,
        _auth: tg.initData,
        queryId: queryId,
      });
    });

    return () => {
      abortController.abort();
    };
  }, [tg, venueId]);

  // handle back button click
  tg.onEvent("backButtonClicked", () => {
    navigate("/");
  });

  return (
    <section>
      {status === STATUS.SUCCESS ? (
        <>
          {location.state && (
            <Image src={location.state.imageUrl} className="w-full h-full" />
          )}
          <h1 className="text-2xl pt-2 font-black">{venue.name}</h1>
          <h2 className="text-sm font-medium hint pb-2">
            {venue.address}, {venue.city}
          </h2>
          <span className="text-sm">{venue.description}</span>
        </>
      ) : status === STATUS.LOADING ? (
        <div className="flex justify-center items-center h-48">
          <Spinner color="primary" size="lg" />
        </div>
      ) : (
        <div className="flex justify-center items-center h-48">
          <span className="text-2xl font-bold">Error.</span>
        </div>
      )}
    </section>
  );
};

export default BookingIndex;
