import { FC } from "react";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "./ui/card";
import Image from "next/image";

interface TitleCardProps {}

const TitleCard: FC<TitleCardProps> = ({}) => {
  return (
    <>
      <Card className="bg-neutral-900">
        <CardHeader>
          <Image src="/logo.png" alt="Video Game Logo" width={100} height={100}/>
          <CardTitle className="text-white">Apex Gunners Statistics</CardTitle>
          <CardDescription>Learn all sorts of statistics based on the game Apex Gunners!</CardDescription>
        </CardHeader>
      </Card>
    </>
  );
};

export default TitleCard;
