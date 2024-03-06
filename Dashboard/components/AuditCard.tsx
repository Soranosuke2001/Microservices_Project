import { FC } from "react";
import GunStatEventCard from "./GunStatEventCard";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import PurchaseEventCard from "./PurchaseEventCard";

interface AuditCardProps {}

const AuditCard: FC<AuditCardProps> = ({}) => {
  return (
    <>
      <Card className="bg-neutral-900 p-10">
        <CardHeader className="text-center">
          <CardTitle className="text-white text-4xl">Audit Endpoints Data</CardTitle>
        </CardHeader>
        <CardContent className="flex gap-10">
          <GunStatEventCard />
          <PurchaseEventCard />
        </CardContent>
      </Card>
    </>
  );
};

export default AuditCard;
