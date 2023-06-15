import React, { useEffect, useState } from 'react';

function PEBox() {
    // Initialize state variables for the data
    const [data, setData] = useState([]);
    const [sp500PE, setSp500PE] = useState("");

    
    // Function to fetch data from the Flask server
    const fetchData = async () => {
        try {
            const response = await fetch('/data');  // Replace '/data' with the actual route if it's different
            const jsonData = await response.json();

            // Update state variables with the fetched data
            setData(jsonData.data);
            setSp500PE(jsonData.sp500_pe);
        } catch (err) {
            console.error(err.message);
        }
    }

    // Use an effect hook to fetch the data when the component mounts
    useEffect(() => {
        fetchData();
    }, []);

    return (
        <div className="pe-box">
            <h2>S&P 500 P/E Ratio: {sp500PE}</h2>
            {data.map((row, index) => (
                <div key={index} className="pe-row">
                    <p>Symbol: {row[0]}, P/E Ratio: {row[1]}</p>
                </div>
            ))}
        </div>
    );
}

export default PEBox;
