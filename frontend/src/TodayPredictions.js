// Place this in your React frontend, e.g., TodayPredictions.js

import React, { useEffect, useState } from "react";
import axios from "axios";

const backendUrl = "http://127.0.0.1:8000"; // Local backend

const TodayPredictions = () => {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    axios
      .get(`${backendUrl}/today_predictions`)
      .then((res) => {
        setPredictions(res.data.predictions || []);
        setLoading(false);
      })
      .catch((err) => {
        setError("Failed to fetch predictions.");
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading predictions...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <div>
      <h2>Today's NBA Predictions</h2>
      <table border="1" cellPadding="5" style={{ borderCollapse: "collapse", width: "100%" }}>
        <thead>
          <tr>
            <th>Game ID</th>
            <th>Player</th>
            <th>Team</th>
            <th>Opponent</th>
            <th>Predicted Points</th>
            <th>Predicted Rebounds</th>
            <th>Predicted Assists</th>
          </tr>
        </thead>
        <tbody>
          {predictions.map((p, idx) => (
            <tr key={idx}>
              <td>{p.game_id}</td>
              <td>{p.player_name}</td>
              <td>{p.team}</td>
              <td>{p.opponent}</td>
              <td>{p.predicted_points ?? "N/A"}</td>
              <td>{p.predicted_rebounds ?? "N/A"}</td>
              <td>{p.predicted_assists ?? "N/A"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TodayPredictions;