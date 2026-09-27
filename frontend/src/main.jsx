import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import { Waves, Satellite, BrainCircuit, MapPin, Activity, Database } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import "./styles.css";

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const initial = {
  latitude: 15,
  longitude: 80,
  sst: 28.5,
  sss: 34.5,
  ssh: 0.2,
  current_u: 0.1,
  current_v: -0.05,
  wind_u: 4,
  wind_v: 2
};

function App() {
  const [form, setForm] = useState(initial);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const update = (key, value) => setForm({...form, [key]: Number(value)});

  async function predict(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const r = await fetch(`${API}/predict`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(form)
      });
      if (!r.ok) throw new Error(`API error ${r.status}`);
      setResult(await r.json());
    } catch (err) {
      setError(err.message + ". Start the FastAPI backend first.");
    } finally {
      setLoading(false);
    }
  }

  const chartData = result
    ? result.depths_m.map((d, i) => ({depth: d, temperature: result.temperature_c[i]}))
    : [];

  return (
    <div className="app">
      <header className="hero">
        <div className="brand">
          <div className="logo"><Waves size={26}/></div>
          <div>
            <div className="eyebrow">AI • OCEAN DIGITAL TWIN PoC</div>
            <h1>North Indian Ocean Temperature Reconstruction</h1>
            <p>Satellite surface observations → latent ocean representation → depth-wise temperature profile</p>
          </div>
        </div>
        <div className="region">
          <MapPin size={16}/> 5°N–30°N • 45°E–105°E
        </div>
      </header>

      <section className="stats">
        <div><Satellite/><span><b>7</b><small>Surface Inputs</small></span></div>
        <div><BrainCircuit/><span><b>15</b><small>Depth Levels</small></span></div>
        <div><Database/><span><b>0.25°</b><small>Target Grid</small></span></div>
        <div><Activity/><span><b>Daily</b><small>Temporal Scale</small></span></div>
      </section>

      <main className="grid">
        <section className="card">
          <h2>Surface Observation Inputs</h2>
          <p className="muted">Enter a surface state for a demonstration profile.</p>
          <form onSubmit={predict}>
            <div className="two">
              <label>Latitude<input type="number" step="0.25" min="5" max="30" value={form.latitude} onChange={e=>update("latitude",e.target.value)}/></label>
              <label>Longitude<input type="number" step="0.25" min="45" max="105" value={form.longitude} onChange={e=>update("longitude",e.target.value)}/></label>
            </div>
            <div className="two">
              <label>SST (°C)<input type="number" step="0.1" value={form.sst} onChange={e=>update("sst",e.target.value)}/></label>
              <label>SSS (PSU)<input type="number" step="0.1" value={form.sss} onChange={e=>update("sss",e.target.value)}/></label>
            </div>
            <div className="two">
              <label>SSH / SLA<input type="number" step="0.01" value={form.ssh} onChange={e=>update("ssh",e.target.value)}/></label>
              <label>Current U<input type="number" step="0.01" value={form.current_u} onChange={e=>update("current_u",e.target.value)}/></label>
            </div>
            <div className="two">
              <label>Current V<input type="number" step="0.01" value={form.current_v} onChange={e=>update("current_v",e.target.value)}/></label>
              <label>Wind U<input type="number" step="0.1" value={form.wind_u} onChange={e=>update("wind_u",e.target.value)}/></label>
            </div>
            <label>Wind V<input type="number" step="0.1" value={form.wind_v} onChange={e=>update("wind_v",e.target.value)}/></label>
            <button disabled={loading}>{loading ? "Reconstructing..." : "Reconstruct Temperature Profile"}</button>
          </form>
          {error && <div className="error">{error}</div>}
        </section>

        <section className="card result">
          <div className="result-head">
            <div>
              <h2>Depth-wise Temperature</h2>
              <p className="muted">
                {result ? `${result.mode} • ${result.location.latitude}°N, ${result.location.longitude}°E` : "Run a reconstruction to view the profile"}
              </p>
            </div>
          </div>

          {result ? (
            <>
              <div className="chart">
                <ResponsiveContainer width="100%" height={360}>
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3"/>
                    <XAxis dataKey="depth" label={{value:"Depth (m)", position:"insideBottom", offset:-5}}/>
                    <YAxis label={{value:"Temperature (°C)", angle:-90, position:"insideLeft"}} domain={["auto","auto"]}/>
                    <Tooltip/>
                    <Line type="monotone" dataKey="temperature" strokeWidth={3} dot/>
                  </LineChart>
                </ResponsiveContainer>
              </div>
              <div className="table">
                <div className="tr th"><span>Depth</span><span>Temperature</span></div>
                {result.depths_m.map((d,i)=><div className="tr" key={d}><span>{d} m</span><span>{result.temperature_c[i]} °C</span></div>)}
              </div>
            </>
          ) : (
            <div className="empty">
              <Waves size={54}/>
              <h3>Ready for inference</h3>
              <p>The PoC returns a demonstration profile now. After training, place <code>best.pt</code> in <code>backend/models/</code> and connect gridded inference.</p>
            </div>
          )}
        </section>
      </main>

      <footer>
        <span>PoC • Not an operational ocean forecasting system</span>
        <span>Validation target: independent ARGO observations</span>
      </footer>
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
