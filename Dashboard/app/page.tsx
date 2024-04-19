import AnomaliesCard from "@/components/AnomaliesCard";
import AuditCard from "@/components/AuditCard";
import EventLoggerCard from "@/components/EventLoggerCard";
import StatsCard from "@/components/StatsCard";
import TitleCard from "@/components/TitleCard";

export default function Home() {
  return (
    <div className="flex flex-col gap-10 min-h-screen justify-center items-center">
      <div className="w-5/12">
        <TitleCard />
      </div>
      <div>
        <AuditCard />
      </div>
      <div>
        <StatsCard />
      </div>
      <div>
        <EventLoggerCard />
      </div>
      <div>
        <AnomaliesCard />
      </div>
    </div>
  );
}
