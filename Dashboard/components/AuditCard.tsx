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
import Loading from "./Loading";
import { getCurrentDateTime } from "@/lib/currentDate";

interface AuditCardProps {}

const AuditCard: FC<AuditCardProps> = ({}) => {
  const [gsData, setGSData] = useState(null);
  const [phData, setPHData] = useState(null);
  const [queryIndex, setQueryIndex] = useState<number>(0);
  const [currentDate, setCurrentDate] = useState<string | null>(null);

  const toastMessage = (title: string, message: string, log: string) => {
    toast(title, {
      description: message,
      action: {
        label: "Dismiss",
        onClick: () => console.log(log),
      },
    });
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const gsResponse = await fetch(
          process.env.NEXT_PUBLIC_GUN_STAT_AUDIT_URL! + `?index=${queryIndex}`
        );

        if (!gsResponse.ok) {
          throw new Error("No new data found");
        }

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

        if (!phResponse.ok) {
          throw new Error("No new data found");
        }

        const phResult = await phResponse.json();

        toastMessage(
          "Successfully Fetched Data",
          "Fetched data from Purchase History audit endpoint.",
          "Toast Dismissed"
        );

        setGSData(gsResult);
        setPHData(phResult);
        setCurrentDate(getCurrentDateTime());
      } catch (error) {
        toastMessage(
          "Unable to Fetch Data",
          "There was an error fetching new data.",
          String(error)
        );
      }
    };

    const interval = setInterval(() => {
      fetchData();
      setQueryIndex((prev) => prev + 1);
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

        {gsData === null || phData === null ? (
          <Loading />
        ) : (
          <>
            <CardContent className="flex gap-10">
              <GunStatEventCard gsData={gsData} queryIndex={queryIndex} />
              <PurchaseEventCard phData={phData} queryIndex={queryIndex} />
            </CardContent>
            <CardFooter className="justify-center text-neutral-400">
              <p>Last Updated: {currentDate}</p>
            </CardFooter>
          </>
        )}
      </Card>
    </>
  );
};

export default AuditCard;
