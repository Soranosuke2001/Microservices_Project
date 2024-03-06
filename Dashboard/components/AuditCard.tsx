import { FC } from "react";
import GunStatEventCard from "./GunStatEventCard";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "./ui/card";
import PurchaseEventCard from "./PurchaseEventCard";

interface AuditCardProps {}

const AuditCard: FC<AuditCardProps> = ({}) => {
  return (
    <>
      <Card className="bg-neutral-900 p-10 text-white">
        <CardHeader className="text-center">
          <CardTitle className="text-4xl">Audit Endpoints Data</CardTitle>
        </CardHeader>

        <CardContent className="flex gap-10">
          <GunStatEventCard />
          <PurchaseEventCard />
        </CardContent>

        <CardFooter className="justify-center text-neutral-400">
          <p>Last Updated: "DATE TIME"</p>
        </CardFooter>
      </Card>
    </>
  );
};

export default AuditCard;
