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
  const queryIndex: number = 11;
  const [gsData, setGSData] = useState(null);
  const [phData, setPHData] = useState(null);

  const toastMessage = (title: string, message: string, log: string) => {
    toast(title, {
      description: message,
      action: {
        label: "Dismiss",
        onClick: () => console.log(log),
      },
    });
  };

  const fetchData = async () => {
    try {
      const gsResponse = await fetch(
        process.env.NEXT_PUBLIC_GUN_STAT_AUDIT_URL! + `?index=${queryIndex}`
      );
      const gsResult = await gsResponse.json();

      toastMessage(
        "Successfully Fetched Data",
        "Fetched data from Gun Stat audit endpoint.",
        "Toast Dismissed"
      );

      const phResponse = await fetch(
        process.env.NEXT_PUBLIC_PURCHASE_HISTORY_AUDIT_URL! +
          `?index=${queryIndex}`
      );
      const phResult = await phResponse.json();

      toastMessage(
        "Successfully Fetched Data",
        "Fetched data from Purchase History audit endpoint.",
        "Toast Dismissed"
      );

      setGSData(gsResult);
      setPHData(phResult);
    } catch (error) {
      toastMessage(
        "Unable to Fetch Data",
        "There was an error fetching new data.",
        String(error)
      );
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      fetchData();
    }, +process.env.NEXT_PUBLIC_FREQUENCY!);

    return () => {
      clearInterval(interval);
    };
  }, []);

  return (
    <>
      <Card className="bg-neutral-900 p-10 text-white">
        <CardHeader className="text-center">
          <CardTitle className="text-4xl">Audit Endpoints Data</CardTitle>
        </CardHeader>

        <CardContent className="flex gap-10">
          <GunStatEventCard gsData={gsData} queryIndex={queryIndex} />
          <PurchaseEventCard phData={phData} queryIndex={queryIndex} />
        </CardContent>

        <CardFooter className="justify-center text-neutral-400">
          <p>Last Updated: "DATE TIME"</p>
        </CardFooter>
      </Card>
    </>
  );
};

export default AuditCard;
