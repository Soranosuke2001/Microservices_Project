"use client";

import { FC, useEffect, useState } from "react";
import { toast } from "sonner";
import GunStatEventCard from "./GunStatEventCard";
import PurchaseEventCard from "./PurchaseEventCard";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./ui/card";

interface AuditCardProps {}

const AuditCard: FC<AuditCardProps> = ({}) => {
  const [gsData, setGSData] = useState(null);
  const [phData, setPHData] = useState(null);

  useEffect(() => {
    const fetchAudit = async () => {
      try {
        const index = 1

        const gsResponse = await fetch(process.env.GUN_STAT_AUDIT_URL! + `?index=${index}`)
        const gsResult = await gsResponse.json()

        toast("Successfully Fetched Data", {
          description: "Fetched data from Gun Stat audit endpoint.",
          action: {
            label: "Dismiss",
            onClick: () => console.log("Toast Dismissed")
          }
        })
        
        const phResponse = await fetch(process.env.PURCHASE_HISTORY_AUDIT_URL! + `?index=${index}`)
        const phResult = await phResponse.json()

        toast("Successfully Fetched Data", {
          description: "Fetched data from Purchase History audit endpoint.",
          action: {
            label: "Dismiss",
            onClick: () => console.log("Toast Dismissed")
          }
        })
        
        setGSData(gsResult)
        setPHData(phResult)
        
      } catch (error) {
        toast("Unable to Fetch Data", {
          description: "There was an error fetching new data.",
          action: {
            label: "Dismiss",
            onClick: () => console.log(error)
          }
        })
      }
    };

    const interval = setInterval(fetchAudit, +process.env.FREQUENCY!)

    return () => clearInterval(interval)
  }, []);

  return (
    <>
      <Card className="bg-neutral-900 p-10 text-white">
        <CardHeader className="text-center">
          <CardTitle className="text-4xl">Audit Endpoints Data</CardTitle>
        </CardHeader>

        <CardContent className="flex gap-10">
          <GunStatEventCard gsData={gsData} />
          <PurchaseEventCard phData={phData} />
        </CardContent>

        <CardFooter className="justify-center text-neutral-400">
          <p>Last Updated: "DATE TIME"</p>
        </CardFooter>
      </Card>
    </>
  );
};

export default AuditCard;
