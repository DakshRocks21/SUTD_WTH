"use client";

import db from "./firebase";
import { collection, getDocs, getDoc } from "firebase/firestore";
import { useEffect, useState } from "react";

export default function App() {
  const [info, setInfo] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const dataCollection = collection(db, "data");
      const sectorDocs = await getDocs(dataCollection);

      let master_data = {};

      for (const sectorDoc of sectorDocs.docs) {


        if (sectorDoc.id === "esp_mac") {
          continue;
        }

        const espDataCollection = collection(sectorDoc.ref, "esp");
        const espDocs = await getDocs(espDataCollection);
        const data = [];

        for (const espDoc of espDocs.docs) {
          const espData = await getDoc(espDoc.ref);
          data.push(espData.data().occupied);
        }
        master_data[sectorDoc.id] = data;
      }

      setInfo(master_data);
    };

    fetchData();
  }, []);

  const renderDynamicGrid = (data, title) => {
    if (!data) return null;
    var totalSeats = 0;
    for (var i = 0; i < data.length; i++) {
      totalSeats += parseInt(data[i], 10);
    }
    return (
      <div className="mb-8">
        <h2 className="text-xl font-bold mb-4">{title}</h2>
        <h3 className="text-2xl font-bold w-full text-center">Total seats available: {totalSeats}</h3>
        <div className="grid grid-cols-4">
          {data.map((filledBoxes, rowIndex) => (
            <div className="m-10 grid grid-cols-2 w-60 h-60" key={`row-${rowIndex}`}>
              {Array(4)
                .fill(null)
                .map((_, colIndex) => (
                  <div
                    key={`row-${rowIndex}-col-${colIndex}`} // Properly unique key
                    className={`p-4 border border-gray-300 w-[120px] h-[120px] ${
                      filledBoxes > colIndex ? "bg-green-500" : "bg-gray-200"
                    }`}
                  ></div>
                ))}
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Dynamic Grid View</h1>
      {info &&
        Object.keys(info).map((key) => (
          <div key={`grid-${key}`} className="mb-8">
            {renderDynamicGrid(info[key], `Grid for ${key}`)}
          </div>
        ))}
    </div>
  );
}
