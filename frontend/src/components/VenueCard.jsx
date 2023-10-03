import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import { Card, CardHeader, CardFooter, Image, Button } from "@nextui-org/react";

import Image1 from "@/assets/images/1.jpg";
import Image2 from "@/assets/images/2.jpg";
import Image3 from "@/assets/images/3.jpg";
import Image4 from "@/assets/images/4.jpg";
import Image5 from "@/assets/images/5.jpg";
import Image6 from "@/assets/images/6.jpg";
import Image7 from "@/assets/images/7.jpg";
import Image8 from "@/assets/images/8.jpg";
import Image9 from "@/assets/images/9.jpg";
import Image10 from "@/assets/images/10.jpg";

const VenueCard = ({ venue }) => {
  const navigate = useNavigate();

  const [selectedImageUrl, setSelectedImageUrl] = useState(null);
  const imageUrls = [
    Image1,
    Image2,
    Image3,
    Image4,
    Image5,
    Image6,
    Image7,
    Image8,
    Image9,
    Image10,
  ];

  useEffect(() => {
    const randomIndex = Math.floor(Math.random() * imageUrls.length);
    setSelectedImageUrl(imageUrls[randomIndex]);
  }, []);

  return (
    <Card radius="lg" className="border-none max-w-xl h-full">
      <CardHeader className="absolute z-10 top-0 flex-col !items-start">
        <span className="font-bold text-lg drop-shadow-2xl">{venue.name}</span>
      </CardHeader>
      <Image
        src={selectedImageUrl}
        removeWrapper
        className="z-0 object-cover"
      />
      <CardFooter className="flex flex-col items-start overflow-hidden pb-1 absolute bottom-0 shadow-small z-10">
        <Button
          className="text-xs font-bold tg-button w-full"
          variant="flat"
          color="default"
          radius="md"
          size="sm"
          onClick={() => {navigate(`/book/${venue.id}`, { state: { imageUrl : selectedImageUrl }})}}
        >
          Book Now
        </Button>
      </CardFooter>
    </Card>
  );
};

export default VenueCard;
