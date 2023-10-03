import { useState, useEffect, useCallback } from "react";
import { useParams, useLocation, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";

import { Image, Input } from "@nextui-org/react";

import axiosInstance from "@/services/api";
import { useTelegram } from "@/hooks/useTelegram";

const BookingConfirm = () => {
  const { tg } = useTelegram();
  const navigate = useNavigate();
  const location = useLocation();

  const { venueId } = useParams();
  const venueAddress = location.state.venueAddress;
  const venueName = location.state.venueName;

  const { register, handleSubmit } = useForm();
  const onSubmit = useCallback((data) => {
    console.log(data);

    //   axiosInstance.post(`/bookings/${venueId}`, {
    //     signal: abortController.signal,
    //     _auth: tg.initData,
    //     queryId: queryId,
    //   });
  }, []);

  // handle back button click
  tg.onEvent("backButtonClicked", () => {
    navigate(`/book/${venueId}`);
  });

  useEffect(() => {
    tg.MainButton.text = "Confirm Booking";
  }, [tg]);



  return (
    <section className="w-full">
      
      
    </section>
  );
};

export default BookingConfirm;
