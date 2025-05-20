import { useState } from "react";
import axios from "axios";

function App() {
  const [player, setPlayer] = useState("Julius Randle");
  const [stat, setStat] = useState("points");
  const [prediction, setPrediction] = useState(null);

  const getPrediction = async () => {
    const res = await axios.post("https://python-nba-predictor.onrender.com/", {
      player_name: player,
      stat: stat
    });
    setPrediction(res.data.prediction);
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>NBA Prop Predictor</h1>
      <input value={player} onChange={(e) => setPlayer(e.target.value)} />
      <select value={stat} onChange={(e) => setStat(e.target.value)}>
        <option value="points">Points</option>
        <option value="reb">Rebounds</option>
        <option value="ast">Assists</option>
      </select>
      <button onClick={getPrediction}>Predict</button>
      {prediction !== null && <p>Predicted {stat}: {prediction}</p>}
    </div>
  );
}

export default App;
