import Grid from '@/components/molecules/Grid';

export default function Home() {
  return (
    <div className="flex justify-center min-h-screen p-8 pb-20 gap-16 sm:p-4">
      <main className="flex justify-around row-start-2 items-center sm:items-start w-full">
        <Grid />
        {/* <div className="bg-box gap-4 flex flex-col py-15 px-10 uppercase text-[24px]">
          <div className="flex justify-between">
            <span>Parties jouées</span>{' '}
            <span className="text-[#1B7953] ms-6">15</span>
          </div>
          <div className="flex justify-between">
            <span>Victoires joueur</span>{' '}
            <span className="text-[#1B7953] ms-6">11</span>
          </div>
          <div className="flex justify-between">
            <span>Victoires IA</span>{' '}
            <span className="text-[#1B7953] ms-6">9</span>
          </div>
          <div className="flex justify-between">
            <span>Matchs Nuls</span>{' '}
            <span className="text-[#1B7953] ms-6">5</span>
          </div>
          <div className="flex justify-between">
            <span>Taux victoires (%)</span>{' '}
            <span className="text-[#1B7953] ms-6">44%</span>
          </div>
        </div> */}
      </main>
    </div>
  );
}
