import React, { useState, useEffect } from "react";
import axios from "axios";
import PEBox from "./PEBox"; 
//
function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const response = await axios.get("/data");
      setData(response.data);
    };

    fetchData();
  }, []);

  if (!data) return "Loading...";

  return (
    <div>
      <PEBox pe={data.sp500_pe} data={data.data} />
    </div>
  );
}

export default App;
