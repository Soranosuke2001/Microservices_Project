import { FC } from "react";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "./ui/card";
import { Separator } from "./ui/separator";

interface StatsCardProps {}

const StatsCard: FC<StatsCardProps> = ({}) => {
  return (
    <>
      <Card className="bg-neutral-900 text-white mb-4 p-6">
        <CardHeader className="text-center">
          <CardTitle className="text-3xl">Latest Statistics</CardTitle>
        </CardHeader>

        <div className="flex gap-10">
          <CardContent className="flex flex-col gap-5">
            <div>
              <h3 className="text-lg font-semibold">Gun Stat Event Count</h3>
              <Separator className="mb-2" />
              <p className="text-neutral-300">123</p>
            </div>
            <div>
              <h3 className="text-lg font-semibold">Bullet Shot Count</h3>
              <Separator className="mb-2" />
              <p className="text-neutral-300">123</p>
            </div>
            <div>
              <h3 className="text-lg font-semibold">Head Shot Count</h3>
              <Separator className="mb-2" />
              <p className="text-neutral-300">123</p>
            </div>
          </CardContent>

          <CardContent className="flex flex-col gap-5">
            <div>
              <h3 className="text-lg font-semibold">Purchase History Event Count</h3>
              <Separator className="mb-2" />
              <p className="text-neutral-300">123</p>
            </div>
            <div>
              <h3 className="text-lg font-semibold">Total Revenue</h3>
              <Separator className="mb-2" />
              <p className="text-neutral-300">123</p>
            </div>
          </CardContent>
        </div>

          <CardFooter className="justify-center text-neutral-400">
            <p>Last Updated: "DATE TIME"</p>
          </CardFooter>
      </Card>
    </>
  );
};

export default StatsCard;
