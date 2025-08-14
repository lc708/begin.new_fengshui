import React from 'react';
import Link from 'next/link';

interface NavigationItem {
  title: string;
  icon: string;
  href: string;
}

interface NavigationCardProps {
  items: NavigationItem[];
}

const iconMap: Record<string, string> = {
  bagua: '☯',
  compass: '🧭',
  calendar: '📅',
};

const NavigationCard: React.FC<NavigationCardProps> = ({ items }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto p-6">
      {items.map((item, index) => (
        <Link key={index} href={item.href}>
          <div className="traditional-card p-8 text-center hover:shadow-xl transition-shadow cursor-pointer group">
            <div className="text-6xl mb-4 group-hover:scale-110 transition-transform">
              {iconMap[item.icon] || '🔮'}
            </div>
            <h3 className="text-xl font-serif-sc font-semibold text-traditional-red mb-2">
              {item.title}
            </h3>
            <div className="w-16 h-1 bg-traditional-gold mx-auto rounded"></div>
          </div>
        </Link>
      ))}
    </div>
  );
};

export default NavigationCard;
