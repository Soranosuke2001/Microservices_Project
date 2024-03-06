import { FC } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Separator } from "./ui/separator";

interface PurchaseEventCardProps {
  phData: any
}

const PurchaseEventCard: FC<PurchaseEventCardProps> = ({ phData }) => {
  const index = 1
  const gunId = "sdfnsiufh-os8w9-skdjfh-9w83-asd"

  return (
    <>
      <Card className="h-fit bg-neutral-900 text-white p-7">
        <CardHeader>
          <CardTitle className="text-white">Purchase Transaction Event</CardTitle>
          <CardDescription className="text-neutral-600">Fetched index value: {index}</CardDescription>
        </CardHeader>

        <CardContent>
          <h3 className="text-lg font-semibold">Transaction ID</h3>
          <Separator className="mb-2" />
          <p className="text-neutral-300">{gunId}</p>
        </CardContent>

        <CardContent>
          <h3 className="text-lg font-semibold">Item ID</h3>
          <Separator className="mb-2" />
          <p className="text-neutral-300">{gunId}</p>
        </CardContent>

        <CardContent>
          <h3 className="text-lg font-semibold">User ID</h3>
          <Separator className="mb-2" />
          <p className="text-neutral-300">{gunId}</p>
        </CardContent>

        <CardContent>
          <h3 className="text-lg font-semibold">Transaction Date</h3>
          <Separator className="mb-2" />
          <p className="text-neutral-300">{gunId}</p>
        </CardContent>
        
        <CardContent>
          <h3 className="text-lg font-semibold">Item Price</h3>
          <Separator className="mb-2" />
          <p className="text-neutral-300">{gunId}</p>
        </CardContent>
      </Card>
    </>
  );
};

export default PurchaseEventCard;