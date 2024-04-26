"use client";

import { FC } from "react";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "../ui/card";
import { Separator } from "../ui/separator";
import Loading from "../Loading";

interface EventStatsCardProps {
  data: any;
  last_updated: string | null;
}

const EventStatsCard: FC<EventStatsCardProps> = ({ data, last_updated }) => {
  return (
    <>
      <Card className="bg-neutral-900 text-white mb-4 p-6">
        {data === null ? (
          <Loading />
        ) : (
          <>
            <CardHeader className="text-center">
              <CardTitle className="text-3xl">
                Latest Event Statistics
              </CardTitle>
            </CardHeader>
            <div className="flex gap-10">
              <CardContent className="flex flex-col gap-5">
                <div>
                  <h3 className="text-lg font-semibold">Code 0001</h3>
                  <Separator className="mb-2" />
                  <p className="text-neutral-300">{data["0001"]}</p>
                </div>
                <div>
                  <h3 className="text-lg font-semibold">Code 0002</h3>
                  <Separator className="mb-2" />
                  <p className="text-neutral-300">{data["0002"]}</p>
                </div>
              </CardContent>

              <CardContent className="flex flex-col gap-5">
                <div>
                  <h3 className="text-lg font-semibold">Code 0003</h3>
                  <Separator className="mb-2" />
                  <p className="text-neutral-300">{data["0003"]}</p>
                </div>
                <div>
                  <h3 className="text-lg font-semibold">Code 0004</h3>
                  <Separator className="mb-2" />
                  <p className="text-neutral-300">{data["0004"]}</p>
                </div>
              </CardContent>
            </div>

            <CardFooter className="justify-center text-neutral-400">
              <p>Last Updated: {last_updated}</p>
            </CardFooter>
          </>
        )}
      </Card>
    </>
  );
};

export default EventStatsCard;
