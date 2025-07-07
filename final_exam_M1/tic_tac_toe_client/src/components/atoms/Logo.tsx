import Image from 'next/image';

const Logo = () => {
  return (
    <Image
      src="/logo.svg"
      width={275}
      height={157}
      alt="logo"
      className="object-cover"
    />
  );
};

export default Logo;
