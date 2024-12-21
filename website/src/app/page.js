"use client";

import db from './firebase';
import { collection, getDocs, getDoc, doc } from 'firebase/firestore';
import { useEffect, useState } from 'react';

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
        for (const espDoc of espDocs.docs) {
          const espData = await getDoc(espDoc.ref);
          master_data[sectorDoc.id] =
          {
            "esp": espData.data().data,
          };
        }

        

        setInfo(master_data);
        console.log(master_data);
      }
    };

    fetchData();

  }, []);


  return (
    <h1>Hello World</h1>
  )
}