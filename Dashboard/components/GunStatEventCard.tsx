import { FC } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Separator } from "./ui/separator";

interface GunStatEventCardProps {
  gsData: any
}

const GunStatEventCard: FC<GunStatEventCardProps> = ({ gsData }) => {
  const index = 1
  const gunId = "sdfnsiufh-os8w9-skdjfh-9w83-asd"

  return (
    <>
      <Card className="bg-neutral-900 text-white p-7">
        <CardHeader>
          <CardTitle>Gun Stat Event</CardTitle>
          <CardDescription className="text-neutral-600">Fetched index value: {index}</CardDescription>
        </CardHeader>

        <CardContent>
          <h3 className="text-lg font-semibold">Gun ID</h3>
          <Separator className="mb-2" />
          <p className="text-neutral-300">{gunId}</p>
        </CardContent>

        <CardContent>
          <h3 className="text-lg font-semibold">Game ID</h3>
          <Separator className="mb-2" />
          <p className="text-neutral-300">{gunId}</p>
        </CardContent>

        <CardContent>
          <h3 className="text-lg font-semibold">User ID</h3>
          <Separator className="mb-2" />
          <p className="text-neutral-300">{gunId}</p>
        </CardContent>

        <CardContent>
          <h3 className="text-lg font-semibold">Number Bullets Shot</h3>
          <Separator className="mb-2" />
          <p className="text-neutral-300">{gunId}</p>
        </CardContent>
        
        <CardContent>
          <h3 className="text-lg font-semibold">Number Bullets Missed</h3>
          <Separator className="mb-2" />
          <p className="text-neutral-300">{gunId}</p>
        </CardContent>

        <CardContent>
          <h3 className="text-lg font-semibold">Number Head Shots</h3>
          <Separator className="mb-2" />
          <p className="text-neutral-300">{gunId}</p>
        </CardContent>

        <CardContent>
          <h3 className="text-lg font-semibold">Number Body Shots</h3>
          <Separator className="mb-2" />
          <p className="text-neutral-300">{gunId}</p>
        </CardContent>
      </Card>
    </>
  );
};

export default GunStatEventCard;
