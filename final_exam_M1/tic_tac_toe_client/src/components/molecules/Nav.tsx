import Image from 'next/image';
import Logo from '../atoms/Logo';
import Link from 'next/link';

const Nav = () => {
  return (
    <nav className="w-full flex items-center justify-between h-fit">
      <Link href={'/'} className="w-[275px] h-[157px]">
        <Logo />
      </Link>
      <div className="flex-center gap-14 text-[29px]">
        <div className="uppercase flex-center gap-2">
          <Image src="/X-player.svg" width={67} height={67} alt="player X" />{' '}
          Vous
        </div>
        <div className="uppercase text-[56px]">vs</div>
        <div className="uppercase flex-center gap-2">
          <Image src="/O-player.svg" width={67} height={67} alt="player X" /> Ia
        </div>
      </div>
      <div className="flex justify-end align-center w-[275px] gap-[16px]">
        {/* <Image
          src="/bulb.svg"
          width={87}
          height={104}
          alt="bulb icon"
          className="hover:cursor-pointer"
        /> */}
        <Image
          src="/mg-flag.svg"
          width={115}
          height={89}
          alt="MG flag"
          className="hover:cursor-pointer"
        />
      </div>
    </nav>
  );
};

export default Nav;
