import React from 'react';
import { Tree } from 'react-d3-tree';

const data = {
  name: "Dashboard",
  children: [
    {
      name: "Reports"
    },
    {
      name: "Settings",
      children: [
        { name: "Profile" },
        { name: "Security" }
      ]
    }
  ]
};

export default function IAView() {
  return (
    <div style={{ width: "100%", height: "100vh" }}>
      <Tree data={data} orientation="vertical" />
    </div>
  );
}
