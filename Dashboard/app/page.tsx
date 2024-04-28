import AnomaliesCard from "@/components/Anomaly/AnomaliesCard";
import AuditCard from "@/components/Audit/AuditCard";
import EventLoggerCard from "@/components/EventLogger/EventLoggerCard";
import StatsCard from "@/components/Processing/StatsCard";
import TitleCard from "@/components/TitleCard";

export default function Home() {
  return (
    <div className="flex flex-col gap-10 min-h-screen justify-center items-center">
      <div className="w-5/12">
        <TitleCard />
      </div>
      <div>
        <AnomaliesCard />
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
    </div>
  );
}
