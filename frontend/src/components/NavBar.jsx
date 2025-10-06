import React from "react";
import { ScrollText, User } from "lucide-react";

const NavBar = () => {
  return (
    <nav className="bg-gray-900 border-b border-gray-700 px-6 py-4 sticky top-0 z-50">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <ScrollText className="text-white w-8 h-8" />
          <h1 className="text-2xl font-bold text-white">
            CDI<span className="text-green-400">Check</span>
          </h1>
        </div>
        <div className="flex items-center space-x-5">
          <div className="text-white">
            <a href="#">Dashboard</a>
          </div>
          <div className="text-white">
            <a href="/upload">Upload</a>
          </div>
          <div className="text-white">
            <a href="#">Settings</a>
          </div>
        </div>
        <div>
          <div className="text-white">
            <User className="text-white w-5 h-5" />
          </div>
        </div>
      </div>
    </nav>
  );
};

export default NavBar;
