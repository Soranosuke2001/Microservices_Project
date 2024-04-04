"use client";

import { FC, useEffect, useState } from "react";
import { toast } from "sonner";
import { getCurrentDateTime } from "@/lib/currentDate";
import EventStatsCard from "./EventStatsCard";

interface EventLoggerCardProps {}

const EventLoggerCard: FC<EventLoggerCardProps> = ({}) => {
  const [eventStats, setEventStats] = useState(null);
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
        const response = await fetch(process.env.NEXT_PUBLIC_EVENT_STATS_URL!, { cache: 'no-store' });

        if (!response.ok) {
          throw new Error("No new data found");
        }

        const data = await response.json();

        toastMessage(
          "Successfully Fetched Data",
          "Fetched data from Event Stats endpoint.",
          "Toast Dismissed"
        );

        setEventStats(data);
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
    <EventStatsCard data={eventStats} last_updated={currentDate}/>
  );
};

export default EventLoggerCard;
