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
        const data = {
          "esp" : [],
          "model" : []
        };

        for (const espDoc of espDocs.docs) {
          const espData = await getDoc(espDoc.ref);
          data.esp.push(espData.data().occupied);
        }

        const modelDataCollection = collection(sectorDoc.ref, "model");
        const modelDocs = await getDocs(espDataCollection);

        for (const espDoc of espDocs.docs) {
          const espData = await getDoc(espDoc.ref);
          data.model.push(espData.data().occupied);
        }
        master_data[sectorDoc.id] = data;
      }
      console.log(master_data);
      setInfo(master_data);
    };

    fetchData();
  }, []);

  const renderDynamicGrid = (data, title) => {
    if (!data) return null;
    let totalSeats = 0;
    for (let i = 0; i < data.length; i++) {
      totalSeats += parseInt(data[i], 10);
    }

    return (
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6 text-gray-700 border-b-2 border-gray-200 pb-2">
          {title}
        </h2>
        <h3 className="text-3xl font-bold w-full text-center text-blue-600 mb-6">
          Total Seats Available: <span className="text-green-600">{totalSeats}</span>
        </h3>
        <div className="grid grid-cols-4 md:grid-cols-2 gap-4">
          {data.esp.map((filledBoxes, rowIndex) => (
            <div
              className="m-4 grid grid-cols-2 w-60 h-60 border border-gray-300 rounded-2xl p-2"
              key={`row-${rowIndex}`}
            >
              {Array(4)
                .fill(null)
                .map((_, colIndex) => (
                  <div
                    key={`row-${rowIndex}-col-${colIndex}`}
                    className={`w-[110px] h-[110px] p-[10px] flex items-center justify-center rounded-2xl text-white font-bold text-lg ${
                      filledBoxes > colIndex ? "bg-green-500" : "bg-gray-200"
                    }`}
                  >
                    {filledBoxes > colIndex ? "Empty" : "Filled"}
                  </div>
                ))}
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <h1 className="text-4xl font-extrabold text-center text-gray-800 mb-10">
        Dynamic Grid View
      </h1>
      {info &&
        Object.keys(info).map((key) => (
          <div
            key={`grid-${key}`}
            className="p-6 bg-white shadow-lg rounded-lg mb-12"
          >
            {renderDynamicGrid(info[key], `Grid for ${key}`)}
          </div>
        ))}
    </div>
  );
}
