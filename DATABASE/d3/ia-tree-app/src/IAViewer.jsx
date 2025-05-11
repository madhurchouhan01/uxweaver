// src/IAViewer.jsx
import React from "react";
import Tree from "react-d3-tree";

const iaData = [
  {
    name: "Global Navigation",
    children: [
      {
        name: "Search & Find",
        children: [
          { name: "Books & Media" },
          { name: "Articles" },
          { name: "Journals" },
          { name: "Research Databases" },
          { name: "eBooks" },
          { name: "Film & Video" },
        ],
      },
      {
        name: "Using the Library",
        children: [
          { name: "Borrow, Renew, Request" },
          { name: "Document Delivery / ILL" },
          { name: "Print, Copy, Scan" },
          { name: "Computer Availability" },
        ],
      },
      {
        name: "Research Support",
        children: [
          { name: "Subject Librarians" },
          { name: "Topic Guides" },
          { name: "Citing Sources" },
          { name: "Citation Tools" },
        ],
      },
    ],
  },
];

const containerStyles = {
  width: "100%",
  height: "100vh",
};

const IAViewer = () => {
  return (
    <div style={containerStyles}>
      <Tree
        data={iaData}
        orientation="vertical"
        translate={{ x: 500, y: 100 }}
        collapsible={false}
        styles={{
          nodes: {
            node: {
              circle: { fill: "#004080" },
              name: { fontSize: "14px", fill: "#333" },
            },
            leafNode: {
              circle: { fill: "#ffcc00" },
              name: { fontSize: "12px", fill: "#555" },
            },
          },
        }}
      />
    </div>
  );
};

export default IAViewer;
