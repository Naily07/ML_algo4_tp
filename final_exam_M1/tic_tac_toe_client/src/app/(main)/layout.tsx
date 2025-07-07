import Nav from '@/components/molecules/Nav';
import React from 'react';

interface RootLayoutProps {
  children: React.ReactNode;
}

const RootLayout = ({ children }: RootLayoutProps) => {
  return (
    <main className="flex flex-col h-screen overflow-hidden min-h-screen p-8 pb-20 gap-4 sm:p-20 sm:pt-8 text-black">
      <Nav />
      {children}
    </main>
  );
};

export default RootLayout;
