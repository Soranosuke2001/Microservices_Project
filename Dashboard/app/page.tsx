import AuditCard from "@/components/AuditCard";
import GunStatEventCard from "@/components/GunStatEventCard";
import TitleCard from "@/components/TitleCard";

export default function Home() {
  return (
    <main className="flex flex-col gap-10 min-h-screen justify-center items-center">
      <div className="w-5/12">
        <TitleCard />
      </div>
      <div>
        <AuditCard />
      </div>
    </main>
  );
}
