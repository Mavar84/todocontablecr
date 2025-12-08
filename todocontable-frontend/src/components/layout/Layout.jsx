import React from "react";
import { useState } from "react";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

export default function Layout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  return (
    <div>
      <Navbar toggleSidebar={toggleSidebar} />

      <Sidebar open={sidebarOpen} toggleSidebar={toggleSidebar} />

      <div style={{ paddingTop: 70, paddingLeft: 20, paddingRight: 20 }}>
        {children}
      </div>
    </div>
  );
}
