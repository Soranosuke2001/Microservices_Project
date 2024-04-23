"use client";

import { FC, useEffect, useState } from "react";
import { toast } from "sonner";
import { getCurrentDateTime } from "@/lib/currentDate";
import AnomaliesDataCard from "./AnomaliesStatsCard";

interface AnomaliesCardProps {}

const AnomaliesCard: FC<AnomaliesCardProps> = ({}) => {
  const [anomaliesStats, setAnomaliesStats] = useState<any>(null);
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
        const gun_stats_response = await fetch(process.env.NEXT_PUBLIC_ANOMALY_URL! + `?anomaly_type=gun_stats`, { cache: 'no-store' });
        const purchase_history_response = await fetch(process.env.NEXT_PUBLIC_ANOMALY_URL! + `?anomaly_type=purchase_history`, { cache: 'no-store' });

        if (!gun_stats_response.ok) {
          throw new Error("No new data found");
        }

        if (!purchase_history_response.ok) {
          throw new Error("No new data found");
        }

        const gun_stats_anomalies = await gun_stats_response.json();
        const purchase_history_anomalies = await purchase_history_response.json();

        const data = {
          "gun_stat": gun_stats_anomalies.message[0],
          "purchase_history": purchase_history_anomalies.message[0]
        }

        toastMessage(
          "Successfully Fetched Data",
          "Fetched data from Anomalies Detector endpoint.",
          "Toast Dismissed"
        );

        setAnomaliesStats(data);
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
    }, +process.env.NEXT_PUBLIC_FREQUENCY!);

    return () => {
      clearInterval(interval);
    };
  }, []);
  return (
    <AnomaliesDataCard data={anomaliesStats} last_updated={currentDate}/>
  );
};

export default AnomaliesCard;
