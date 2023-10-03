import { useState, useEffect } from "react";
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
