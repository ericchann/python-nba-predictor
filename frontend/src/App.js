import React, { useState } from "react";
import axios from "axios";
import TodayPredictions from "./TodayPredictions";

const NBAPropPredictor = () => {
    const [playerName, setPlayerName] = useState("");
    const [stat, setStat] = useState("");
    const [prediction, setPrediction] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const backendUrl = "http://127.0.0.1:8000";

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        setPrediction(null);

        try {
            const response = await axios.post(`${backendUrl}/predict`, {
                player_name: playerName,
                stat: stat,
            });
            if (response.data.error) {
                setError(response.data.error);
            } else {
                setPrediction(response.data.prediction);
            }
        } catch (err) {
            setError("Failed to fetch prediction. Please try again later.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>NBA Prop Predictor</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Player Name"
                    value={playerName}
                    onChange={(e) => setPlayerName(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Stat (e.g., points)"
                    value={stat}
                    onChange={(e) => setStat(e.target.value)}
                />
                <button type="submit">Predict</button>
            </form>
            {loading && <p>Loading...</p>}
            {error && <p style={{ color: "red" }}>{error}</p>}
            {prediction !== null && <p>Predicted {stat}: {prediction}</p>}
        </div>
    );
};

function App() {
    return (
        <div>
            <NBAPropPredictor />
            <TodayPredictions />
        </div>
    );
}

export default App;
