"use client";
import { useMemo, useState } from "react";
import fixture from "../../shared/fixtures/research-demo.json";
import schema from "../../shared/schemas/research-demo.schema.json";
import Ajv from "ajv/dist/2020";

type Tab = "overview" | "research" | "quality" | "availability" | "error" | "comparison";
const validator = new Ajv({ allErrors: true, strict: false });
const validFixture = validator.validate(schema, fixture);
if (!validFixture) throw new Error("Shared demo fixture failed JSON Schema validation: " + JSON.stringify(validator.errors));

const tabs: { id: Tab; label: string }[] = [
  { id: "overview", label: "Resumen" },
  { id: "research", label: "Investigación" },
  { id: "quality", label: "Calidad de datos" },
  { id: "availability", label: "Capacidades" },
  { id: "error", label: "Error recuperable" },
  { id: "comparison", label: "Comparar evaluaciones" }
];

export default function App() {
  const [tab, setTab] = useState<Tab>("overview");
  const [start, setStart] = useState("2025-01-01");
  const [end, setEnd] = useState("2025-01-07");
  const [rangeError, setRangeError] = useState("");
  const [errorVisible, setErrorVisible] = useState(true);
  const [saved, setSaved] = useState(false);
  const selection = fixture.researchSelection;
  const evaluations = fixture.evaluations;

  const formattedPeriod = useMemo(
    () => new Intl.DateTimeFormat("es-ES", { dateStyle: "medium", timeZone: "UTC" }).format(new Date(selection.period.start)),
    []
  );

  function validateRange() {
    if (!start || !end || new Date(end).getTime() < new Date(start).getTime()) {
      setRangeError("La fecha final debe ser igual o posterior a la fecha inicial.");
      return;
    }
    setRangeError("");
    setTab("research");
  }

  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand"><span className="brand-mark">C</span><div><strong>CPIE</strong><small>Research workspace · Web POC</small></div></div>
        <span className="environment">ENTORNO SIMULADO</span>
      </header>
      <div className="disclosure" role="status">⚠ {fixture.disclosure} — no representa datos ni análisis reales del mercado.</div>
      <section className="intro">
        <div><p className="eyebrow">CRYPTO PREDICTIVE INTELLIGENCE ECOSYSTEM</p><h1>Investigación de activos</h1><p className="muted">Prototipo funcional para evaluar navegación, estados y consumo del contrato compartido.</p></div>
        <div className="asset-chip"><span>ACTIVO DEMO</span><strong>₿ BTC</strong><small>Bitcoin · instrumento sintético</small></div>
      </section>
      <nav className="tabs" aria-label="Secciones de la demostración">
        {tabs.map(item => <button key={item.id} className={tab === item.id ? "tab active" : "tab"} onClick={() => setTab(item.id)}>{item.label}</button>)}
      </nav>

      {tab === "overview" && <section className="panel">
        <div className="section-heading"><div><p className="eyebrow">VISTA GENERAL</p><h2>Estado de la investigación</h2></div><span className="status simulated">SIMULATED</span></div>
        <div className="metric-grid"><article className="metric"><span>Activo</span><strong>BTC</strong><small>Identificador de demostración</small></article><article className="metric"><span>Intervalo</span><strong>1 día</strong><small>Fixture sintético</small></article><article className="metric"><span>Calidad</span><strong className="warning-text">PARTIAL</strong><small>Cobertura deliberadamente incompleta</small></article><article className="metric"><span>Incertidumbre</span><strong>NOT QUANTIFIED</strong><small>No se ejecutó calibración</small></article></div>
        <h3>Evaluaciones recientes</h3><div className="evaluation-list">{evaluations.map(e => <article className="evaluation" key={e.id}><div><strong>{e.id}</strong><small>{new Date(e.createdAt).toLocaleString("es-ES", { timeZone: "UTC" })} UTC · {e.snapshotId}</small></div><span className="status simulated">{e.status}</span></article>)}</div>
        <p className="note">Los dos registros son sintéticos. Su diferencia de metadatos no representa una mejora ni un deterioro del mercado.</p>
      </section>}

      {tab === "research" && <section className="panel">
        <div className="section-heading"><div><p className="eyebrow">UC-BTC-RESEARCH-001</p><h2>Parámetros de investigación</h2></div><span className="status simulated">SIMULATED</span></div>
        <div className="form-grid"><label>Activo<input value="BTC · Demo" readOnly /></label><label>Intervalo<select value="1d" disabled><option>1d</option></select></label><label>Fecha inicial<input type="date" value={start} onChange={e => setStart(e.target.value)} /></label><label>Fecha final<input type="date" value={end} onChange={e => setEnd(e.target.value)} /></label></div>
        {rangeError && <p className="field-error" role="alert">{rangeError}</p>}
        <div className="actions"><button className="primary" onClick={validateRange}>Validar y mostrar resultado</button><button className="secondary" onClick={() => {setStart("2025-01-01");setEnd("2025-01-07");setRangeError("");}}>Restablecer fixture</button></div>
        <div className="result-card"><strong>Resultado: {fixture.researchResult.status}</strong><p>{fixture.researchResult.summary}</p><p className="muted">Período de referencia del fixture: {formattedPeriod} — no equivale a una consulta real.</p></div>
      </section>}

      {tab === "quality" && <section className="panel">
        <div className="section-heading"><div><p className="eyebrow">DATA QUALITY</p><h2>Cobertura y limitaciones</h2></div><span className="status partial">PARTIAL</span></div>
        <p>{fixture.dataQuality.coverage.description}</p>
        <h3>Intervalos omitidos</h3>{fixture.dataQuality.coverage.missingIntervals.map((item, i) => <article className="evaluation" key={i}><div><strong>{item.start.slice(0,10)} — {item.end.slice(0,10)}</strong><small>{item.reason}</small></div><span className="status partial">MISSING</span></article>)}
        <h3>Limitaciones declaradas</h3><ul>{fixture.dataQuality.limitations.map(item => <li key={item}>{item}</li>)}</ul>
      </section>}

      {tab === "availability" && <section className="panel">
        <div className="section-heading"><div><p className="eyebrow">CAPABILITY STATUS</p><h2>Secciones disponibles</h2></div><span className="status unavailable">NOT AVAILABLE</span></div>
        {fixture.researchResult.sections.map(section => <article className="capability" key={section.id}><div><strong>{section.title}</strong><p>{section.reason}</p></div><span className="status unavailable">{section.status}</span></article>)}
        <p className="note">La ausencia de evidencia se presenta como NOT_AVAILABLE; nunca se sustituye por cero, vacío o una estimación.</p>
      </section>}

      {tab === "error" && <section className="panel">
        <div className="section-heading"><div><p className="eyebrow">RESILIENCE SCENARIO</p><h2>Error recuperable</h2></div><span className="status error">ERROR</span></div>
        {errorVisible ? <div className="error-card" role="alert"><strong>DEMO_RECOVERABLE</strong><p>Fallo sintético recuperable para probar el estado de error.</p><small>El error no se convierte en ausencia de datos.</small></div> : <div className="success-card">Reintento de demostración completado. No se ha consultado ningún servicio externo.</div>}
        <div className="actions"><button className="primary" onClick={() => setErrorVisible(false)}>Reintentar</button><button className="secondary" onClick={() => setErrorVisible(true)}>Restaurar escenario de error</button></div>
      </section>}

      {tab === "comparison" && <section className="panel">
        <div className="section-heading"><div><p className="eyebrow">LONGITUDINAL EVALUATION</p><h2>Comparación de evaluaciones</h2></div><span className="status simulated">SYNTHETIC</span></div>
        <div className="compare-grid">{evaluations.map(e => <article className="compare-card" key={e.id}><span className="eyebrow">{e.id}</span><h3>{e.snapshotId}</h3><p>{e.summary}</p><dl><dt>Creada (UTC)</dt><dd>{e.createdAt}</dd><dt>Metodología</dt><dd>{e.methodologyVersion}</dd><dt>Estado</dt><dd>{e.status}</dd><dt>Período</dt><dd>{e.periodStart.slice(0,10)} → {e.periodEnd.slice(0,10)}</dd></dl></article>)}</div>
        <p className="note">Comparación de metadatos solamente. No hay métricas de mercado ni evidencia para concluir mejora, deterioro o precisión.</p>
      </section>}

      <footer className="footer"><span>Fixture {fixture.fixtureVersion} · Validación JSON Schema Draft 2020-12</span><button className="save" onClick={() => setSaved(true)}>{saved ? "Guardado local · no persistido" : "Guardar evaluación demo"}</button></footer>
      <p className="footnote">La acción de guardar solo cambia el estado visual de esta sesión. No existe backend ni persistencia.</p>
    </main>
  );
}

