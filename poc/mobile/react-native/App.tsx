import React, { useMemo, useState } from "react";
import { SafeAreaView, ScrollView, StatusBar, StyleSheet, Text, TextInput, Pressable, View } from "react-native";
import Ajv2020 from "ajv/dist/2020";
import fixture from "./assets/fixtures/research-demo.json";
import schema from "./assets/fixtures/research-demo.schema.json";

type ScenarioId =
  | "overview"
  | "research-valid"
  | "research-invalid-range"
  | "partial-data"
  | "not-available"
  | "recoverable-error"
  | "evaluation-comparison";

const ajv = new Ajv2020({ allErrors: true });
const validFixture = ajv.validate(schema, fixture);
const scenarioLabels: Record<ScenarioId, string> = {
  overview: "Resumen",
  "research-valid": "Investigación",
  "research-invalid-range": "Rango inválido",
  "partial-data": "Datos parciales",
  "not-available": "No disponible",
  "recoverable-error": "Error recuperable",
  "evaluation-comparison": "Comparar",
};

export default function App() {
  const [scenario, setScenario] = useState<ScenarioId>("overview");
  const [start, setStart] = useState("2025-01-01");
  const [end, setEnd] = useState("2025-01-07");
  const [retried, setRetried] = useState(false);
  const [saved, setSaved] = useState(false);
  const rangeValid = useMemo(() => new Date(start).getTime() <= new Date(end).getTime(), [start, end]);
  const selected = fixture.scenarios.find((item) => item.id === scenario);
  const sections = fixture.researchResult.sections;
  const evaluations = fixture.evaluations;

  const renderDetails = () => {
    switch (scenario) {
      case "overview":
        return <><Text style={styles.heading}>Bitcoin · DEMO</Text><Text>{fixture.researchResult.summary}</Text><Text style={styles.body}>Período: {fixture.researchSelection.period.start} → {fixture.researchSelection.period.end}</Text><Text style={styles.body}>Incertidumbre: {fixture.researchResult.uncertainty.status}</Text></>;
      case "research-valid":
        return <><Text style={styles.heading}>Investigación simulada</Text><Text>{fixture.researchResult.summary}</Text><Text style={styles.body}>Rango aceptado: {fixture.researchSelection.period.start} → {fixture.researchSelection.period.end}</Text></>;
      case "research-invalid-range":
        return <><Text style={styles.heading}>Validación del período</Text><Text>Inicio</Text><TextInput accessibilityLabel="Fecha inicial" value={start} onChangeText={setStart} style={styles.input}/><Text>Fin</Text><TextInput accessibilityLabel="Fecha final" value={end} onChangeText={setEnd} style={styles.input}/><Text style={rangeValid ? styles.ok : styles.error}>{rangeValid ? "Rango válido" : "VALIDATION_ERROR: la fecha inicial debe ser anterior o igual a la final."}</Text></>;
      case "partial-data":
        return <><Text style={styles.heading}>Calidad: PARTIAL</Text><Text>{fixture.dataQuality.coverage.description}</Text>{fixture.dataQuality.coverage.missingIntervals.map((item) => <Text key={item.start} style={styles.body}>Intervalo omitido: {item.start} → {item.end}. {item.reason}</Text>)}{fixture.dataQuality.limitations.map((item) => <Text key={item} style={styles.body}>• {item}</Text>)}</>;
      case "not-available": {
        const section = sections.find((item) => item.id === "technical-structure");
        return <><Text style={styles.heading}>Estructura técnica: {section?.status}</Text><Text>{section?.reason}</Text></>;
      }
      case "recoverable-error":
        return <><Text style={styles.heading}>ERROR · DEMO_RECOVERABLE</Text><Text>{retried ? "Reintento local completado; el fixture sigue en modo SIMULATED." : "Fallo sintético recuperable para probar el estado de error."}</Text><Pressable accessibilityRole="button" onPress={() => setRetried(true)} style={styles.button}><Text style={styles.buttonText}>Reintentar localmente</Text></Pressable></>;
      case "evaluation-comparison":
        return <><Text style={styles.heading}>Comparación sintética</Text>{evaluations.map((item) => <View key={item.id} style={styles.card}><Text style={styles.strong}>{item.id} · {item.status}</Text><Text>{item.createdAt}</Text><Text>{item.summary}</Text><Text>Snapshot: {item.snapshotId}</Text></View>)}</>;
    }
  };

  return (
    <SafeAreaView style={styles.safe}>
      <StatusBar barStyle="dark-content"/>
      <ScrollView contentContainerStyle={styles.container}>
        <Text style={styles.brand}>CPIE · MOBILE POC</Text>
        <View style={styles.disclosure}><Text style={styles.disclosureText}>{fixture.disclosure} · {fixture.environmentStatus}</Text></View>
        {!validFixture && <Text style={styles.error}>Fixture/schema validation failed. UI is blocked.</Text>}
        <Text style={styles.subheading}>Escenarios</Text>
        <View style={styles.nav}>{(Object.keys(scenarioLabels) as ScenarioId[]).map((id) => <Pressable key={id} accessibilityRole="button" accessibilityState={{ selected: scenario === id }} onPress={() => {setScenario(id);setRetried(false);}} style={[styles.navItem, scenario === id && styles.navSelected]}><Text style={[styles.navText, scenario === id && styles.navTextSelected]}>{scenarioLabels[id]}</Text></Pressable>)}</View>
        {validFixture ? renderDetails() : null}
        <View style={styles.card}>
          <Text style={styles.strong}>Estado esperado: {selected?.expectedState}</Text>
          <Text>{selected?.expectedOutcome}</Text>
        </View>
        <Text style={styles.subheading}>Evaluación local</Text>
        <Pressable accessibilityRole="button" onPress={() => setSaved(true)} style={styles.button}><Text style={styles.buttonText}>{saved ? "Marcada en esta sesión" : "Marcar evaluación"}</Text></Pressable>
        {saved && <Text style={styles.warning}>No persistido. El estado se pierde al cerrar la aplicación.</Text>}
        <Text style={styles.footer}>Sin datos reales, API, autenticación, persistencia ni trading.</Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: "#f5f7fa" },
  container: { padding: 18, gap: 14 },
  brand: { fontSize: 12, fontWeight: "800", letterSpacing: 1.5, color: "#53657b" },
  disclosure: { backgroundColor: "#fff0cc", borderRadius: 8, padding: 12 },
  disclosureText: { color: "#694900", fontWeight: "800" },
  subheading: { fontSize: 16, fontWeight: "800", color: "#152238" },
  nav: { flexDirection: "row", flexWrap: "wrap", gap: 8 },
  navItem: { borderWidth: 1, borderColor: "#c8d1dc", borderRadius: 20, paddingVertical: 8, paddingHorizontal: 12, backgroundColor: "#fff" },
  navSelected: { backgroundColor: "#17365d", borderColor: "#17365d" },
  navText: { fontSize: 12, color: "#26384d" },
  navTextSelected: { color: "#fff", fontWeight: "700" },
  heading: { fontSize: 22, fontWeight: "800", color: "#14243a" },
  body: { marginTop: 8, color: "#4b5c70", lineHeight: 20 },
  input: { backgroundColor: "#fff", borderColor: "#c8d1dc", borderWidth: 1, borderRadius: 8, padding: 10, marginVertical: 5 },
  ok: { color: "#176b42", fontWeight: "700" },
  error: { color: "#a52222", fontWeight: "700" },
  card: { backgroundColor: "#fff", borderRadius: 10, padding: 14, gap: 6, borderWidth: 1, borderColor: "#e0e6ed" },
  strong: { fontWeight: "800", color: "#172a43" },
  button: { backgroundColor: "#17365d", borderRadius: 8, padding: 13, alignItems: "center" },
  buttonText: { color: "#fff", fontWeight: "700" },
  warning: { color: "#8a5a00", fontWeight: "700" },
  footer: { color: "#64748b", fontSize: 12, marginTop: 8 },
});
