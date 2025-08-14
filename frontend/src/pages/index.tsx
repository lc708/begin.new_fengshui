import React from 'react';
import Hero from '../components/Hero';
import NavigationCard from '../components/NavigationCard';

const HomePage: React.FC = () => {
  const navigationItems = [
    {
      title: "八字命理",
      icon: "bagua",
      href: "/bazi"
    },
    {
      title: "风水罗盘",
      icon: "compass", 
      href: "/fengshui"
    },
    {
      title: "日常宜忌",
      icon: "calendar",
      href: "/daily"
    }
  ];

  return (
    <div className="min-h-screen bg-traditional-beige">
      <Hero 
        title="风水命理大师"
        subtitle="传统文化，现代体验"
        background="traditional-chinese"
      />
      
      <div className="py-12">
        <NavigationCard items={navigationItems} />
      </div>

      <footer className="text-center py-8 text-traditional-dark-green">
        <div className="max-w-4xl mx-auto px-6">
          <p className="text-sm opacity-75 mb-4">
            🏮 传承千年智慧，服务现代生活 🏮
          </p>
          <p className="text-xs opacity-60">
            本应用仅供娱乐参考，请理性对待命理文化
          </p>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
