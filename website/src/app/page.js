"use client";

import db from "./firebase";
import { collection, getDocs, getDoc } from "firebase/firestore";
import { useEffect, useState } from "react";

export default function App() {
  const [info, setInfo] = useState({});

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
          "esp": [],
          "model": []
        };

        for (const espDoc of espDocs.docs) {
          const espData = await getDoc(espDoc.ref);
          data.esp.push(espData.data().occupied);
        }

        const modelDataCollection = collection(sectorDoc.ref, "model");
        const modelDocs = await getDocs(modelDataCollection);

        for (const modelDoc of modelDocs.docs) {
          const modelData = await getDoc(modelDoc.ref);
          data.model.push(modelData.data().model);
        }
        master_data[sectorDoc.id] = data;
      }
      setInfo(master_data);
    };
    setInterval(fetchData, 100);
  }, []);

  const renderDynamicGrid = (data, title) => {
    let totalSeats = 0;
    data.esp.map((filledBoxes, rowIndex) => (
      Array(4)
        .fill(null)
        .map((_, colIndex) => {
          let espSubtract = filledBoxes - (colIndex % 4);
          let modelSubtract = 4 - (data.model[rowIndex]) - (colIndex % 4);

          if ((espSubtract > 0 && modelSubtract > 0) === false) {
            if (espSubtract <= 0 && modelSubtract <= 0) {
              totalSeats++;
            }
          }
        })
      )
    );

    return (
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6 text-gray-700 border-b-2 border-gray-200 pb-2">
          {title}
        </h2>
        <h3 className="text-3xl font-semibold w-full text-center text-blue-600 mb-6">
          Seats Available: <span className="text-green-600">{totalSeats}</span>
        </h3>
        <div className="grid grid-cols-4 gap-4">
          {data.esp.map((filledBoxes, rowIndex) => (
            <div
              className="m-4 grid grid-cols-2 w-60 h-60 border border-gray-300 rounded-2xl p-2"
              key={`row-${rowIndex}`}
            >
              {Array(4)
                .fill(null)
                .map((_, colIndex) => {
                  let espSubtract = filledBoxes - (colIndex % 4);
                  let modelSubtract = 4 - (data.model[rowIndex]) - (colIndex % 4);
                  let boxState = "bg-gray-300";
                  let boxText = "Unknown";

                  if (espSubtract > 0 && modelSubtract > 0) {
                    boxState = "bg-gray-300";
                    boxText = "Filled";
                  } else {
                    if (espSubtract === modelSubtract && espSubtract > 0) {
                      boxState = "bg-gray-300";
                      boxText = "Filled";
                    } else if (espSubtract > modelSubtract && espSubtract > 0) {
                      boxState = "bg-yellow-400";
                      boxText = "Choped";
                    } else if (espSubtract < modelSubtract && modelSubtract > 0) {
                      boxState = "bg-orange-500";
                      boxText = "Occupied Pending";
                    } else if (espSubtract <= 0 && modelSubtract <= 0) {
                      boxState = "bg-green-600";
                      boxText = "Available";
                    }
                  }
                  return (
                    <div
                      key={`row-${rowIndex}-col-${colIndex}`}
                      className={`w-[110px] h-[110px] p-[10px] flex items-center justify-center rounded-2xl text-white font-bold text-lg ${boxState}`}
                    >
                      {boxText}
                    </div>
                  );
                })}
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <h1 className="text-5xl font-bold text-center text-gray-800 mb-10">
        Seats Availability
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
