"use client";

import { FC } from "react";
import { Card, CardContent, CardFooter } from "../ui/card";
import { Separator } from "../ui/separator";
import Loading from "../Loading";

interface AnomaliesStatsCardProps {
  data: any;
  last_updated: string | null;
}

const AnomaliesDataCard: FC<AnomaliesStatsCardProps> = ({
  data,
  last_updated,
}) => {
  if (!data) {
    return <Loading />;
  }

  const { gun_stat, purchase_history } = data;

  return (
    <>
      <div className="flex gap-10">
        <CardContent className="flex flex-col gap-5">
          <div>
            <h3 className="text-lg font-semibold">Gun Stat Anomaly</h3>
            <Separator className="mb-2" />
            <p className="text-neutral-300">Event ID: {gun_stat["event_id"]}</p>
          </div>
          <div>
            <Separator className="mb-2" />
            <p className="text-neutral-300">
              Description: {gun_stat["description"]}
            </p>
          </div>
          <div>
            <Separator className="mb-2" />
            <p className="text-neutral-300">
              Date Detected: {gun_stat["date_created"]}
            </p>
          </div>
        </CardContent>

        <CardContent className="flex flex-col gap-5">
          <div>
            <h3 className="text-lg font-semibold">
              Purchase History Anomalies
            </h3>
            <Separator className="mb-2" />
            <p className="text-neutral-300">
              Event ID: {purchase_history["event_id"]}
            </p>
          </div>
          <div>
            <Separator className="mb-2" />
            <p className="text-neutral-300">
              Description: {purchase_history["description"]}
            </p>
          </div>
          <div>
            <Separator className="mb-2" />
            <p className="text-neutral-300">
              Date Detected: {purchase_history["date_created"]}
            </p>
          </div>
        </CardContent>
      </div>

      <CardFooter className="justify-center text-neutral-400">
        <p>Last Updated: {last_updated}</p>
      </CardFooter>
    </>
  );
};

export default AnomaliesDataCard;
