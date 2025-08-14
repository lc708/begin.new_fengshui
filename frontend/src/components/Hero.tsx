import React from 'react';

interface HeroProps {
  title: string;
  subtitle: string;
  background: string;
}

const Hero: React.FC<HeroProps> = ({ title, subtitle, background }) => {
  return (
    <div className="relative h-64 bg-gradient-to-r from-traditional-red to-red-800 flex items-center justify-center text-center">
      <div className="absolute inset-0 bg-black opacity-20"></div>
      <div className="relative z-10 text-white">
        <h1 className="text-4xl font-bold font-serif-sc mb-4">
          {title}
        </h1>
        <p className="text-xl font-sans-sc opacity-90">
          {subtitle}
        </p>
        {/* 装饰性八卦符号 */}
        <div className="mt-6 text-traditional-gold text-6xl">
          ☯
        </div>
      </div>
    </div>
  );
};

export default Hero;
