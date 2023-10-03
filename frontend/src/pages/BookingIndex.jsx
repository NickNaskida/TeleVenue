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

  const { register, handleSubmit } = useForm();
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
              placeholder="Under name"
              {...register("under_name")}
            />
            <Input type="date" variant="bordered" {...register("date")} />
            <Input
              variant="bordered"
              placeholder="comment"
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
